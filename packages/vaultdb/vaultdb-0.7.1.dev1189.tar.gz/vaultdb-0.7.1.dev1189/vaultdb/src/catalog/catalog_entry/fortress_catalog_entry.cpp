#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/catalog_entry/fortress_catalog_entry.hpp"
#include "duckdb/catalog/dependency_manager.hpp"
#include "duckdb/common/types/date.hpp"
#include "duckdb/common/types/timestamp.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/common/field_writer.hpp"
#include "duckdb/planner/binder.hpp"
#include "duckdb/parser/parsed_data/alter_fortress_info.hpp"
#include "duckdb/parser/parsed_data/create_view_info.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"
 
#include <algorithm>
#include <sstream>

namespace duckdb {

FortressCatalogEntry::FortressCatalogEntry(Catalog *catalog, SchemaCatalogEntry *schema, CreateFortressInfo *info)
    : StandardEntry(CatalogType::FORTRESS_ENTRY, schema, catalog, info->name), 
		locked(std::move(info->locked)), start_date(std::move(info->start_date)), end_date(std::move(info->end_date)), 
		unlocked_for_role(std::move(info->unlocked_for_role)), table(std::move(info->table)), 
		expression(std::move(info->expression)), complement_expression(std::move(info->complement_expression)) {
}

unique_ptr<CatalogEntry> FortressCatalogEntry::AlterEntry(ClientContext &context, AlterInfo *alterinfo) {
	if (alterinfo->type != AlterType::ALTER_FORTRESS) {
		throw CatalogException("Can only modify fortress with ALTER FORTRESS statement");
	}
	auto fortress_info = (AlterFortressInfo *)alterinfo;
	auto info = make_unique<CreateFortressInfo>();
	info->name = fortress_info->name;
	info->table = std::move(table);
	info->expression = std::move(expression);
	info->complement_expression = std::move(complement_expression);
	info->unlocked_for_role = unlocked_for_role;
	info->locked = locked;
	info->start_date = start_date;
	info->end_date = end_date;

	switch (fortress_info->alter_fortress_type) {
	case AlterFortressType::FORTRESS_CHANGE: {
		auto modify_info = (ModifyFortressInfo *)fortress_info;
		info->table = modify_info->table->Copy();
		info->expression = modify_info->expression->Copy();
		info->complement_expression = modify_info->complement_expression->Copy();
		return make_unique<FortressCatalogEntry>(catalog, schema, info.get());
	}
	case AlterFortressType::LOCK_CHANGE: {
		auto locked_info = (LockFortressInfo *)fortress_info;
		info->locked = true;
		info->start_date = locked_info->start_date;
		info->end_date = locked_info->end_date;
		if (!unlocked_for_role.empty())
			info->unlocked_for_role = unlocked_for_role;
		return make_unique<FortressCatalogEntry>(catalog, schema, info.get());
	}
	case AlterFortressType::UNLOCK_CHANGE: {
		auto unlock_info = (UnlockFortressInfo *)fortress_info;
		if (!unlock_info->for_role.empty())
			info->unlocked_for_role = unlock_info->for_role;
		else {
			info->locked = false;
			info->unlocked_for_role = std::move(string());
			info->start_date = std::move(string());
			info->end_date = std::move(string());
		}
		return make_unique<FortressCatalogEntry>(catalog, schema, info.get());
	}
	default:
		throw InternalException("Unrecognized alter table type!");
	}
}

void FortressCatalogEntry::Serialize(Serializer &serializer) {
	FieldWriter writer(serializer);
	writer.WriteString(schema->name);
	writer.WriteString(name);
	writer.WriteSerializable(*table);
	writer.WriteSerializable(*expression);
	writer.WriteSerializable(*complement_expression);
	writer.WriteField<bool>(locked);
	if (locked){
		writer.WriteString(start_date);
		writer.WriteString(end_date);
	}
	writer.Finalize();
}

unique_ptr<CreateFortressInfo> FortressCatalogEntry::Deserialize(Deserializer &source) {
	auto info = make_unique<CreateFortressInfo>();

	FieldReader reader(source);
	info->schema = reader.ReadRequired<string>();
	info->name = reader.ReadRequired<string>();
	info->table = reader.ReadRequiredSerializable<TableRef>();
	info->expression = reader.ReadRequiredSerializable<ParsedExpression>();
	info->complement_expression = reader.ReadRequiredSerializable<ParsedExpression>();
	info->locked = reader.ReadRequired<bool>();
	if (info->locked){
		info->start_date = reader.ReadRequired<string>();
		info->end_date = reader.ReadRequired<string>();
	}
	reader.Finalize();
	return info;
}

string FortressCatalogEntry::ToSQL() {
	auto basetable = unique_ptr_cast<TableRef, BaseTableRef>(table->Copy());
	std::stringstream ss;
	ss << "CREATE FORTRESS ";
	ss << name;
	ss << " ON ";
	if (!basetable->schema_name.empty()){
		ss << name;	ss << basetable->schema_name;
		ss << ".";
	}
	ss << basetable->table_name;
	ss << " ";
	ss << expression->ToString();
	ss << ";";
	return ss.str();
}

bool FortressCatalogEntry::isLocked() {
	if (!locked)
		return false;
	if (!start_date.empty() && !end_date.empty()){
		auto begin  = Date::FromString(start_date);
		auto end  = Date::FromString(end_date);
		auto currentdate = Timestamp::GetDate(Timestamp::GetCurrentTimestamp());
		if (currentdate< begin || currentdate>=end)
			return false;
	}
	return true;
}

void FortressCatalogEntry::AddFortressToTableEntry(CatalogTransaction transaction) {
	auto basetable = unique_ptr_cast<TableRef, BaseTableRef>(table->Copy());
	auto table_entry = 
			Catalog::GetEntry<TableCatalogEntry>(transaction.GetContext(), INVALID_CATALOG, basetable->schema_name, basetable->table_name, true);
	if (!table_entry)
		return;
	table_entry->fortress.insert(name);
}

} // namespace duckdb
