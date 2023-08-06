#include "duckdb_python/pyrelation.hpp"
#include "duckdb_python/pyconnection.hpp"
#include "duckdb_python/pyresult.hpp"
#include "duckdb/parser/qualified_name.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb_python/vector_conversion.hpp"
#include "duckdb_python/pandas_type.hpp"
#include "duckdb/main/relation/query_relation.hpp"
#include "duckdb/parser/parser.hpp"
#include "duckdb/main/relation/view_relation.hpp"
#include "duckdb/function/pragma/pragma_functions.hpp"
#include "duckdb/parser/statement/pragma_statement.hpp"
#include "duckdb/common/box_renderer.hpp"

namespace duckdb {

VaultDBPyRelation::VaultDBPyRelation(shared_ptr<Relation> rel) : rel(std::move(rel)) {
}

VaultDBPyRelation::VaultDBPyRelation(unique_ptr<VaultDBPyResult> result) : rel(nullptr), result(std::move(result)) {
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FromDf(const DataFrame &df, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Values(py::object values, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Values(std::move(values));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FromQuery(const string &query, const string &alias,
                                                         shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromQuery(query, alias);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::RunQuery(const string &query, const string &alias,
                                                        shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->RunQuery(query, alias);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FromParquet(const string &file_glob, bool binary_as_string,
                                                           bool file_row_number, bool filename, bool hive_partitioning,
                                                           bool union_by_name, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromParquet(file_glob, binary_as_string, file_row_number, filename, hive_partitioning, union_by_name);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FromParquets(const vector<string> &file_globs, bool binary_as_string,
                                                            bool file_row_number, bool filename, bool hive_partitioning,
                                                            bool union_by_name, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromParquets(file_globs, binary_as_string, file_row_number, filename, hive_partitioning,
	                          union_by_name);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::GetSubstrait(const string &query, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->GetSubstrait(query);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::GetSubstraitJSON(const string &query,
                                                                shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->GetSubstraitJSON(query);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FromSubstraitJSON(const string &json,
                                                                 shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromSubstraitJSON(json);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FromSubstrait(py::bytes &proto, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromSubstrait(proto);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FromArrow(py::object &arrow_object,
                                                         shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromArrow(arrow_object);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Project(const string &expr) {
	auto projected_relation = make_unique<VaultDBPyRelation>(rel->Project(expr));
	projected_relation->rel->extra_dependencies = this->rel->extra_dependencies;
	return projected_relation;
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::ProjectDf(const DataFrame &df, const string &expr,
                                                         shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->Project(expr);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::SetAlias(const string &expr) {
	return make_unique<VaultDBPyRelation>(rel->Alias(expr));
}

py::str VaultDBPyRelation::GetAlias() {
	return py::str(string(rel->GetAlias()));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::AliasDF(const DataFrame &df, const string &expr,
                                                       shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->SetAlias(expr);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Filter(const string &expr) {
	return make_unique<VaultDBPyRelation>(rel->Filter(expr));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::FilterDf(const DataFrame &df, const string &expr,
                                                        shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->Filter(expr);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Limit(int64_t n, int64_t offset) {
	return make_unique<VaultDBPyRelation>(rel->Limit(n, offset));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::LimitDF(const DataFrame &df, int64_t n,
                                                       shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->Limit(n);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Order(const string &expr) {
	return make_unique<VaultDBPyRelation>(rel->Order(expr));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::OrderDf(const DataFrame &df, const string &expr,
                                                       shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->Order(expr);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Aggregate(const string &expr, const string &groups) {
	if (!groups.empty()) {
		return make_unique<VaultDBPyRelation>(rel->Aggregate(expr, groups));
	}
	return make_unique<VaultDBPyRelation>(rel->Aggregate(expr));
}

void VaultDBPyRelation::AssertResult() const {
	if (!result) {
		throw InvalidInputException("No open result set");
	}
}

void VaultDBPyRelation::AssertResultOpen() const {
	if (result && result->IsClosed()) {
		throw InvalidInputException("No open result set");
	}
}

py::list VaultDBPyRelation::Description() {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	return result->Description();
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Describe() {
	auto &columns = rel->Columns();
	vector<string> column_list;
	column_list.reserve(columns.size());
	for (auto &column_rel : columns) {
		column_list.push_back(column_rel.Name());
	}
	auto expr = GenerateExpressionList("stats", column_list);
	return make_unique<VaultDBPyRelation>(rel->Project(expr)->Limit(1));
}

string VaultDBPyRelation::GenerateExpressionList(const string &function_name, const string &aggregated_columns,
                                                const string &groups, const string &function_parameter,
                                                const string &projected_columns, const string &window_function) {
	auto input = StringUtil::Split(aggregated_columns, ',');
	return GenerateExpressionList(function_name, input, groups, function_parameter, projected_columns, window_function);
}

string VaultDBPyRelation::GenerateExpressionList(const string &function_name, const vector<string> &input,
                                                const string &groups, const string &function_parameter,
                                                const string &projected_columns, const string &window_function) {
	string expr;
	if (!projected_columns.empty()) {
		expr = projected_columns + ", ";
	}
	for (idx_t i = 0; i < input.size(); i++) {
		if (function_parameter.empty()) {
			expr += function_name + "(" + input[i] + ") " + window_function;
		} else {
			expr += function_name + "(" + input[i] + "," + function_parameter + ")" + window_function;
		}

		if (i < input.size() - 1) {
			expr += ",";
		}
	}
	return expr;
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::GenericAggregator(const string &function_name,
                                                                 const string &aggregated_columns, const string &groups,
                                                                 const string &function_parameter,
                                                                 const string &projected_columns) {

	//! Construct Aggregation Expression
	auto expr =
	    GenerateExpressionList(function_name, aggregated_columns, groups, function_parameter, projected_columns);
	return Aggregate(expr, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Sum(const string &sum_columns, const string &groups) {
	return GenericAggregator("sum", sum_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Count(const string &count_columns, const string &groups) {
	return GenericAggregator("count", count_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Median(const string &median_columns, const string &groups) {
	return GenericAggregator("median", median_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Quantile(const string &q, const string &quantile_columns,
                                                        const string &groups) {
	return GenericAggregator("quantile", quantile_columns, groups, q);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Min(const string &min_columns, const string &groups) {
	return GenericAggregator("min", min_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Max(const string &max_columns, const string &groups) {
	return GenericAggregator("max", max_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Mean(const string &mean_columns, const string &groups) {
	return GenericAggregator("avg", mean_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Var(const string &var_columns, const string &groups) {
	return GenericAggregator("var_pop", var_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::STD(const string &std_columns, const string &groups) {
	return GenericAggregator("stddev_pop", std_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::ValueCounts(const string &count_column, const string &groups) {
	if (count_column.find(',') != string::npos) {
		throw InvalidInputException("Only one column is accepted in Value_Counts method");
	}
	return GenericAggregator("count", count_column, groups, "", count_column);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::MAD(const string &aggr_columns, const string &groups) {
	return GenericAggregator("mad", aggr_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Mode(const string &aggr_columns, const string &groups) {
	return GenericAggregator("mode", aggr_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Abs(const string &columns) {
	auto expr = GenerateExpressionList("abs", columns);
	return Project(expr);
}
unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Prod(const string &aggr_columns, const string &groups) {
	return GenericAggregator("product", aggr_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Skew(const string &aggr_columns, const string &groups) {
	return GenericAggregator("skewness", aggr_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Kurt(const string &aggr_columns, const string &groups) {
	return GenericAggregator("kurtosis", aggr_columns, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::SEM(const string &aggr_columns, const string &groups) {
	return GenericAggregator("sem", aggr_columns, groups);
}

idx_t VaultDBPyRelation::Length() {
	auto aggregate_rel = GenericAggregator("count", "*");
	aggregate_rel->Execute();
	D_ASSERT(aggregate_rel->result && aggregate_rel->result->result);
	auto tmp_res = std::move(aggregate_rel->result);
	return tmp_res->result->Fetch()->GetValue(0, 0).GetValue<idx_t>();
}

py::tuple VaultDBPyRelation::Shape() {
	auto length = Length();
	return py::make_tuple(length, rel->Columns().size());
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Unique(const string &std_columns) {
	return make_unique<VaultDBPyRelation>(rel->Project(std_columns)->Distinct());
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::GenericWindowFunction(const string &function_name,
                                                                     const string &aggr_columns) {
	auto expr = GenerateExpressionList(function_name, aggr_columns, "", "", "",
	                                   "over (rows between unbounded preceding and current row) ");
	return make_unique<VaultDBPyRelation>(rel->Project(expr));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::CumSum(const string &aggr_columns) {
	return GenericWindowFunction("sum", aggr_columns);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::CumProd(const string &aggr_columns) {
	return GenericWindowFunction("product", aggr_columns);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::CumMax(const string &aggr_columns) {
	return GenericWindowFunction("max", aggr_columns);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::CumMin(const string &aggr_columns) {
	return GenericWindowFunction("min", aggr_columns);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::AggregateDF(const DataFrame &df, const string &expr,
                                                           const string &groups, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->Aggregate(expr, groups);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Distinct() {
	return make_unique<VaultDBPyRelation>(rel->Distinct());
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::DistinctDF(const DataFrame &df, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->Distinct();
}
duckdb::pyarrow::RecordBatchReader VaultDBPyRelation::FetchRecordBatchReader(idx_t chunk_size) {
	AssertResult();
	return result->FetchRecordBatchReader(chunk_size);
}

static unique_ptr<QueryResult> PyExecuteRelation(const shared_ptr<Relation> &rel) {
	auto context = rel->context.GetContext();
	py::gil_scoped_release release;
	auto pending_query = context->PendingQuery(rel, false);
	return VaultDBPyConnection::CompletePendingQuery(*pending_query);
}

unique_ptr<QueryResult> VaultDBPyRelation::ExecuteInternal() {
	return PyExecuteRelation(rel);
}

void VaultDBPyRelation::ExecuteOrThrow() {
	auto tmp_result = make_unique<VaultDBPyResult>();
	tmp_result->result = ExecuteInternal();
	if (tmp_result->result->HasError()) {
		tmp_result->result->ThrowError();
	}
	result = std::move(tmp_result);
}

DataFrame VaultDBPyRelation::FetchDF(bool date_as_object) {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	auto df = result->FetchDF(date_as_object);
	result = nullptr;
	return df;
}

py::object VaultDBPyRelation::FetchOne() {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	return result->Fetchone();
}

py::object VaultDBPyRelation::FetchMany(idx_t size) {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	return result->Fetchmany(size);
}

py::object VaultDBPyRelation::FetchAll() {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	auto res = result->Fetchall();
	result = nullptr;
	return std::move(res);
}

py::dict VaultDBPyRelation::FetchNumpy() {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	auto res = result->FetchNumpy();
	result = nullptr;
	return res;
}

py::dict VaultDBPyRelation::FetchNumpyInternal(bool stream, idx_t vectors_per_chunk) {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	auto res = result->FetchNumpyInternal(stream, vectors_per_chunk);
	result = nullptr;
	return res;
}

//! Should this also keep track of when the result is empty and set result->result_closed accordingly?
DataFrame VaultDBPyRelation::FetchDFChunk(idx_t vectors_per_chunk, bool date_as_object) {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	return result->FetchDFChunk(vectors_per_chunk, date_as_object);
}

duckdb::pyarrow::Table VaultDBPyRelation::ToArrowTable(idx_t batch_size) {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	auto res = result->FetchArrowTable(batch_size);
	result = nullptr;
	return res;
}

duckdb::pyarrow::RecordBatchReader VaultDBPyRelation::ToRecordBatch(idx_t batch_size) {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	return result->FetchRecordBatchReader(batch_size);
}

void VaultDBPyRelation::Close() {
	if (!result) {
		ExecuteOrThrow();
	}
	AssertResultOpen();
	result->Close();
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Union(VaultDBPyRelation *other) {
	return make_unique<VaultDBPyRelation>(rel->Union(other->rel));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Except(VaultDBPyRelation *other) {
	return make_unique<VaultDBPyRelation>(rel->Except(other->rel));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Intersect(VaultDBPyRelation *other) {
	return make_unique<VaultDBPyRelation>(rel->Intersect(other->rel));
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Join(VaultDBPyRelation *other, const string &condition,
                                                    const string &type) {
	JoinType dtype;
	string type_string = StringUtil::Lower(type);
	StringUtil::Trim(type_string);
	if (type_string == "inner") {
		dtype = JoinType::INNER;
	} else if (type_string == "left") {
		dtype = JoinType::LEFT;
	} else {
		throw InvalidInputException("Unsupported join type %s try 'inner' or 'left'", type_string);
	}
	return make_unique<VaultDBPyRelation>(rel->Join(other->rel, condition, dtype));
}

void VaultDBPyRelation::ToParquet(const string &filename, const py::object &compression) {
	case_insensitive_map_t<vector<Value>> options;

	if (!py::none().is(compression)) {
		if (!py::isinstance<py::str>(compression)) {
			throw InvalidInputException("to_csv only accepts 'compression' as a string");
		}
		options["compression"] = {Value(py::str(compression))};
	}

	auto write_parquet = rel->WriteParquetRel(filename, std::move(options));
	PyExecuteRelation(write_parquet);
}

void VaultDBPyRelation::ToCSV(const string &filename, const py::object &sep, const py::object &na_rep,
                             const py::object &header, const py::object &quotechar, const py::object &escapechar,
                             const py::object &date_format, const py::object &timestamp_format,
                             const py::object &quoting, const py::object &encoding, const py::object &compression) {
	case_insensitive_map_t<vector<Value>> options;

	if (!py::none().is(sep)) {
		if (!py::isinstance<py::str>(sep)) {
			throw InvalidInputException("to_csv only accepts 'sep' as a string");
		}
		options["delimiter"] = {Value(py::str(sep))};
	}

	if (!py::none().is(na_rep)) {
		if (!py::isinstance<py::str>(na_rep)) {
			throw InvalidInputException("to_csv only accepts 'na_rep' as a string");
		}
		options["null"] = {Value(py::str(na_rep))};
	}

	if (!py::none().is(header)) {
		if (!py::isinstance<py::bool_>(header)) {
			throw InvalidInputException("to_csv only accepts 'header' as a boolean");
		}
		options["header"] = {Value::BOOLEAN(py::bool_(header))};
	}

	if (!py::none().is(quotechar)) {
		if (!py::isinstance<py::str>(quotechar)) {
			throw InvalidInputException("to_csv only accepts 'quotechar' as a string");
		}
		options["quote"] = {Value(py::str(quotechar))};
	}

	if (!py::none().is(escapechar)) {
		if (!py::isinstance<py::str>(escapechar)) {
			throw InvalidInputException("to_csv only accepts 'escapechar' as a string");
		}
		options["escape"] = {Value(py::str(escapechar))};
	}

	if (!py::none().is(date_format)) {
		if (!py::isinstance<py::str>(date_format)) {
			throw InvalidInputException("to_csv only accepts 'date_format' as a string");
		}
		options["dateformat"] = {Value(py::str(date_format))};
	}

	if (!py::none().is(timestamp_format)) {
		if (!py::isinstance<py::str>(timestamp_format)) {
			throw InvalidInputException("to_csv only accepts 'timestamp_format' as a string");
		}
		options["timestampformat"] = {Value(py::str(timestamp_format))};
	}

	if (!py::none().is(quoting)) {
		// TODO: add list of strings as valid option
		if (py::isinstance<py::str>(quoting)) {
			string quoting_option = StringUtil::Lower(py::str(quoting));
			if (quoting_option != "force" && quoting_option != "all") {
				throw InvalidInputException(
				    "to_csv 'quoting' supported options are ALL or FORCE (both set FORCE_QUOTE=True)");
			}
		} else if (py::isinstance<py::int_>(quoting)) {
			int64_t quoting_value = py::int_(quoting);
			// csv.QUOTE_ALL expands to 1
			static constexpr int64_t QUOTE_ALL = 1;
			if (quoting_value != QUOTE_ALL) {
				throw InvalidInputException("Only csv.QUOTE_ALL is a supported option for 'quoting' currently");
			}
		} else {
			throw InvalidInputException(
			    "to_csv only accepts 'quoting' as a string or a constant from the 'csv' package");
		}
		options["force_quote"] = {Value("*")};
	}

	if (!py::none().is(encoding)) {
		if (!py::isinstance<py::str>(encoding)) {
			throw InvalidInputException("to_csv only accepts 'encoding' as a string");
		}
		string encoding_option = StringUtil::Lower(py::str(encoding));
		if (encoding_option != "utf-8" && encoding_option != "utf8") {
			throw InvalidInputException("The only supported encoding option is 'UTF8");
		}
	}

	if (!py::none().is(compression)) {
		if (!py::isinstance<py::str>(compression)) {
			throw InvalidInputException("to_csv only accepts 'compression' as a string");
		}
		options["compression"] = {Value(py::str(compression))};
	}

	auto write_csv = rel->WriteCSVRel(filename, std::move(options));
	PyExecuteRelation(write_csv);
}

void VaultDBPyRelation::WriteCsvDF(const DataFrame &df, const string &file, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->ToCSV(file);
}

// should this return a rel with the new view?
unique_ptr<VaultDBPyRelation> VaultDBPyRelation::CreateView(const string &view_name, bool replace) {
	rel->CreateView(view_name, replace);
	// We need to pass ownership of any Python Object Dependencies to the connection
	auto all_dependencies = rel->GetAllDependencies();
	rel->context.GetContext()->external_dependencies[view_name] = std::move(all_dependencies);
	return make_unique<VaultDBPyRelation>(rel);
}

static bool IsDescribeStatement(SQLStatement &statement) {
	if (statement.type != StatementType::PRAGMA_STATEMENT) {
		return false;
	}
	auto &pragma_statement = (PragmaStatement &)statement;
	if (pragma_statement.info->name != "show") {
		return false;
	}
	return true;
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Query(const string &view_name, const string &sql_query) {
	auto view_relation = CreateView(view_name);
	auto all_dependencies = rel->GetAllDependencies();
	rel->context.GetContext()->external_dependencies[view_name] = std::move(all_dependencies);

	Parser parser(rel->context.GetContext()->GetParserOptions());
	parser.ParseQuery(sql_query);
	if (parser.statements.size() != 1) {
		throw InvalidInputException("'VaultDBPyRelation.query' only accepts a single statement");
	}
	auto &statement = *parser.statements[0];
	if (statement.type == StatementType::SELECT_STATEMENT) {
		auto select_statement = unique_ptr_cast<SQLStatement, SelectStatement>(std::move(parser.statements[0]));
		auto query_relation =
		    make_shared<QueryRelation>(rel->context.GetContext(), std::move(select_statement), "query_relation");
		return make_unique<VaultDBPyRelation>(std::move(query_relation));
	} else if (IsDescribeStatement(statement)) {
		FunctionParameters parameters;
		parameters.values.emplace_back(view_name);
		auto query = PragmaShow(*rel->context.GetContext(), parameters);
		return Query(view_name, query);
	}
	{
		py::gil_scoped_release release;
		auto query_result = rel->context.GetContext()->Query(std::move(parser.statements[0]), false);
		// Execute it anyways, for creation/altering statements
		// We only care that it succeeds, we can't store the result
		D_ASSERT(query_result);
		if (query_result->HasError()) {
			query_result->ThrowError();
		}
	}
	return nullptr;
}

VaultDBPyRelation &VaultDBPyRelation::Execute() {
	if (!rel) {
		throw InvalidInputException("This relation was created from a result");
	}
	ExecuteOrThrow();
	return *this;
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::QueryDF(const DataFrame &df, const string &view_name,
                                                       const string &sql_query, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(df)->Query(view_name, sql_query);
}

void VaultDBPyRelation::InsertInto(const string &table) {
	auto parsed_info = QualifiedName::Parse(table);
	auto insert = rel->InsertRel(parsed_info.schema, parsed_info.name);
	PyExecuteRelation(insert);
}

static bool IsAcceptedInsertRelationType(const Relation &relation) {
	return relation.type == RelationType::TABLE_RELATION;
}

void VaultDBPyRelation::Insert(const py::object &params) {
	if (!IsAcceptedInsertRelationType(*this->rel)) {
		throw InvalidInputException("'VaultDBPyRelation.insert' can only be used on a table relation");
	}
	vector<vector<Value>> values {VaultDBPyConnection::TransformPythonParamList(params)};

	py::gil_scoped_release release;
	rel->Insert(values);
}

void VaultDBPyRelation::Create(const string &table) {
	auto parsed_info = QualifiedName::Parse(table);
	auto create = rel->CreateRel(parsed_info.schema, parsed_info.name);
	PyExecuteRelation(create);
}

unique_ptr<VaultDBPyRelation> VaultDBPyRelation::Map(py::function fun) {
	vector<Value> params;
	params.emplace_back(Value::POINTER((uintptr_t)fun.ptr()));
	auto relation = make_unique<VaultDBPyRelation>(rel->TableFunction("python_map_function", params));
	relation->rel->extra_dependencies = make_unique<PythonDependencies>(fun);
	return relation;
}

string VaultDBPyRelation::Print() {
	if (rendered_result.empty()) {
		idx_t limit_rows = 10000;
		BoxRenderer renderer;
		auto limit = Limit(limit_rows, 0);
		auto res = limit->ExecuteInternal();

		auto context = rel->context.GetContext();
		BoxRendererConfig config;
		config.limit = limit_rows;
		rendered_result = res->ToBox(*context, config);
	}
	return rendered_result;
}

string VaultDBPyRelation::Explain() {
	return rel->ToString(0);
}

// TODO: RelationType to a python enum
py::str VaultDBPyRelation::Type() {
	return py::str(RelationTypeToString(rel->type));
}

py::list VaultDBPyRelation::Columns() {
	py::list res;
	for (auto &col : rel->Columns()) {
		res.append(col.Name());
	}
	return res;
}

py::list VaultDBPyRelation::ColumnTypes() {
	py::list res;
	for (auto &col : rel->Columns()) {
		res.append(col.Type().ToString());
	}
	return res;
}

bool VaultDBPyRelation::IsRelation(const py::object &object) {
	return py::isinstance<VaultDBPyRelation>(object);
}

} // namespace duckdb