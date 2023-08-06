#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/view_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/table_function_catalog_entry.hpp"
#include "duckdb/common/string_util.hpp"
#include "duckdb/function/table/table_scan.hpp"
#include "duckdb/main/authorizer.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/config.hpp"
#include "duckdb/parser/constraints/unique_constraint.hpp"
#include "duckdb/parser/query_node/select_node.hpp"
#include "duckdb/parser/statement/select_statement.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"
#include "duckdb/parser/tableref/subqueryref.hpp"
#include "duckdb/parser/tableref/table_function_ref.hpp"
#include "duckdb/planner/binder.hpp"
#include "duckdb/planner/operator/logical_get.hpp"
#include "duckdb/planner/tableref/bound_basetableref.hpp"
#include "duckdb/planner/tableref/bound_cteref.hpp"
#include "duckdb/planner/operator/logical_get.hpp"
#include "duckdb/parser/statement/select_statement.hpp"
#include "duckdb/common/string_util.hpp"
#include "duckdb/parser/tableref/table_function_ref.hpp"
#include "duckdb/main/config.hpp"
#include "duckdb/planner/tableref/bound_dummytableref.hpp"
#include "duckdb/planner/tableref/bound_subqueryref.hpp"

namespace duckdb {

static void BindRemoteDataTableFunction(ClientContext &context, LogicalGet &get, TableCatalogEntry *table) {
	auto &config = DBConfig::GetConfig(context);
	string schema = table->schema->name;
	if (schema.empty())
		schema = DEFAULT_SCHEMA;
	// TODO: get pattern based on partition key
	string file_path = config.options.data_inheritance_path + "/" + schema + "_" + table->name + "*.parquet"; 
	vector<Value> parameters;
	parameters.push_back(file_path);

	vector<LogicalType> return_types;
	vector<string> return_names;
	for (auto &col : table->GetColumns().Logical()) {
		return_types.push_back(col.Type());
		return_names.push_back(col.Name());
	}

	// fetch the function from the catalog
	QueryErrorContext error_context(nullptr, 0);
	auto function = (TableFunctionCatalogEntry *)Catalog::GetEntry(context, CatalogType::TABLE_FUNCTION_ENTRY, 
						INVALID_CATALOG, INVALID_SCHEMA, "parquet_scan", false, error_context);

	get.parquet_function = function->functions.GetFunctionByOffset(0);

	named_parameter_map_t named_parameters;
	named_parameters["union_by_name"] = Value::BOOLEAN(true);
	vector<LogicalType> input_table_types;	
	vector<string> input_table_names; 
	vector<string> column_name_alias;
	TableFunctionBindInput bind_input(parameters, named_parameters, input_table_types, input_table_names,
										get.parquet_function.function_info.get());
											
	auto bind_data = get.parquet_function.bind(context, bind_input, return_types, return_names);
	get.parquet_bind_data = std::move(bind_data);	
}

unique_ptr<BoundTableRef> Binder::Bind(BaseTableRef &ref) {
	QueryErrorContext error_context(root_statement, ref.query_location);
	// CTEs and views are also referred to using BaseTableRefs, hence need to distinguish here
	// check if the table name refers to a CTE
	auto cte = FindCTE(ref.table_name, ref.table_name == alias);
	if (cte) {
		// Check if there is a CTE binding in the BindContext
		auto ctebinding = bind_context.GetCTEBinding(ref.table_name);
		if (!ctebinding) {
			if (CTEIsAlreadyBound(cte)) {
				throw BinderException("Circular reference to CTE \"%s\", use WITH RECURSIVE to use recursive CTEs",
				                      ref.table_name);
			}
			// Move CTE to subquery and bind recursively
			SubqueryRef subquery(unique_ptr_cast<SQLStatement, SelectStatement>(cte->query->Copy()));
			subquery.alias = ref.alias.empty() ? ref.table_name : ref.alias;
			subquery.column_name_alias = cte->aliases;
			for (idx_t i = 0; i < ref.column_name_alias.size(); i++) {
				if (i < subquery.column_name_alias.size()) {
					subquery.column_name_alias[i] = ref.column_name_alias[i];
				} else {
					subquery.column_name_alias.push_back(ref.column_name_alias[i]);
				}
			}
			return Bind(subquery, cte);
		} else {
			// There is a CTE binding in the BindContext.
			// This can only be the case if there is a recursive CTE present.
			auto index = GenerateTableIndex();
			auto result = make_unique<BoundCTERef>(index, ctebinding->index);
			auto b = ctebinding;
			auto alias = ref.alias.empty() ? ref.table_name : ref.alias;
			auto names = BindContext::AliasColumnNames(alias, b->names, ref.column_name_alias);

			bind_context.AddGenericBinding(index, alias, names, b->types);
			// Update references to CTE
			auto cteref = bind_context.cte_references[ref.table_name];
			(*cteref)++;

			result->types = b->types;
			result->bound_columns = std::move(names);
			return std::move(result);
		}
	}
	// not a CTE
	// extract a table or view from the catalog
	BindSchemaOrCatalog(ref.catalog_name, ref.schema_name);
	auto table_or_view = Catalog::GetEntry(context, CatalogType::TABLE_ENTRY, ref.catalog_name, ref.schema_name,
	                                       ref.table_name, true, error_context);
	if (!table_or_view) {
		string table_name = ref.catalog_name;
		if (!ref.schema_name.empty()) {
			table_name += (!table_name.empty() ? "." : "") + ref.schema_name;
		}
		table_name += (!table_name.empty() ? "." : "") + ref.table_name;
		// table could not be found: try to bind a replacement scan
		auto &config = DBConfig::GetConfig(context);
		if (context.config.use_replacement_scans) {
			for (auto &scan : config.replacement_scans) {
				auto replacement_function = scan.function(context, table_name, scan.data.get());
				if (replacement_function) {
					replacement_function->alias = ref.alias.empty() ? ref.table_name : ref.alias;
					if (replacement_function->type == TableReferenceType::TABLE_FUNCTION) {
						auto &table_function = (TableFunctionRef &)*replacement_function;
						table_function.column_name_alias = ref.column_name_alias;
						;
					} else if (replacement_function->type == TableReferenceType::SUBQUERY) {
						auto &subquery = (SubqueryRef &)*replacement_function;
						subquery.column_name_alias = ref.column_name_alias;
					} else {
						throw InternalException("Replacement scan should return either a table function or a subquery");
					}
					return Bind(*replacement_function);
				}
			}
		}

		// we still didn't find the table
		if (GetBindingMode() == BindingMode::EXTRACT_NAMES) {
			// if we are in EXTRACT_NAMES, we create a dummy table ref
			AddTableName(table_name);
			AddSchemaName(ref.schema_name);

			// add a bind context entry
			auto table_index = GenerateTableIndex();
			auto alias = ref.alias.empty() ? table_name : ref.alias;
			vector<LogicalType> types {LogicalType::INTEGER};
			vector<string> names {"__dummy_col" + to_string(table_index)};
			bind_context.AddGenericBinding(table_index, alias, names, types);
			return make_unique_base<BoundTableRef, BoundEmptyTableRef>(table_index);
		}
		// could not find an alternative: bind again to get the error
		table_or_view = Catalog::GetEntry(context, CatalogType::TABLE_ENTRY, ref.catalog_name, ref.schema_name,
		                                  ref.table_name, false, error_context);
	}
	switch (table_or_view->type) {
	case CatalogType::TABLE_ENTRY: {
		// Authorize role
		if (root_statement)
			context.authorizer->Authorize_table(ref.schema_name, ref.table_name, root_statement->type);
		// base table: create the BoundBaseTableRef node
		auto table_index = GenerateTableIndex();
		auto table = (TableCatalogEntry *)table_or_view;

		unique_ptr<FunctionData> bind_data;
		auto scan_function = table->GetScanFunction(context, bind_data);
		auto alias = ref.alias.empty() ? ref.table_name : ref.alias;
		// TODO: bundle the type and name vector in a struct (e.g PackedColumnMetadata)
		vector<LogicalType> table_types;
		vector<string> table_names;
		vector<TableColumnType> table_categories;

		vector<LogicalType> return_types;
		vector<string> return_names;
		for (auto &col : table->GetColumns().Logical()) {
			table_types.push_back(col.Type());
			table_names.push_back(col.Name());
			return_types.push_back(col.Type());
			return_names.push_back(col.Name());
		}
		table_names = BindContext::AliasColumnNames(alias, table_names, ref.column_name_alias);

		auto logical_get = make_unique<LogicalGet>(table_index, scan_function, std::move(bind_data), 
						std::move(return_types), std::move(return_names));

		if (context.IsMergeEnabled()) {
			for (auto column_index:table->GetPrimaryKeyColumnIndex()){
				logical_get->merge_column_indexes.push_back(column_index);
			}
			BindRemoteDataTableFunction(context, *logical_get, table);			
		}
		bind_context.AddBaseTable(table_index, alias, table_names, table_types, 
								logical_get->column_ids, logical_get->GetTable());
		return make_unique_base<BoundTableRef, BoundBaseTableRef>(table, std::move(logical_get));
	}
	case CatalogType::VIEW_ENTRY: {
		// the node is a view: get the query that the view represents
		auto view_catalog_entry = (ViewCatalogEntry *)table_or_view;
		// Authorize role
		if (root_statement)
			context.authorizer->Authorize_view(view_catalog_entry->schema->name, view_catalog_entry->name,
			                                   root_statement->type);
		// We need to use a new binder for the view that doesn't reference any CTEs
		// defined for this binder so there are no collisions between the CTEs defined
		// for the view and for the current query
		bool inherit_ctes = false;
		auto view_binder = Binder::CreateBinder(context, this, inherit_ctes);
		view_binder->can_contain_nulls = true;
		SubqueryRef subquery(unique_ptr_cast<SQLStatement, SelectStatement>(view_catalog_entry->query->Copy()));
		subquery.alias = ref.alias.empty() ? ref.table_name : ref.alias;
		subquery.column_name_alias =
		    BindContext::AliasColumnNames(subquery.alias, view_catalog_entry->aliases, ref.column_name_alias);
		// bind the child subquery
		view_binder->AddBoundView(view_catalog_entry);
		auto bound_child = view_binder->Bind(subquery);
		if (!view_binder->correlated_columns.empty()) {
			throw BinderException("Contents of view were altered - view bound correlated columns");
		}

		D_ASSERT(bound_child->type == TableReferenceType::SUBQUERY);
		// verify that the types and names match up with the expected types and names
		auto &bound_subquery = (BoundSubqueryRef &)*bound_child;
		if (bound_subquery.subquery->types != view_catalog_entry->types) {
			throw BinderException("Contents of view were altered: types don't match!");
		}
		bind_context.AddView(bound_subquery.subquery->GetRootIndex(), subquery.alias, subquery,
		                     *bound_subquery.subquery, view_catalog_entry);
		return bound_child;
	}
	default:
		throw InternalException("Catalog entry type");
	}
}
} // namespace duckdb
