#include "duckdb/parser/parsed_data/alter_fortress_info.hpp"
#include "duckdb/common/field_writer.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// AlterFortressInfo
//===--------------------------------------------------------------------===//
AlterFortressInfo::AlterFortressInfo(AlterFortressType type, AlterEntryData data)
    : AlterInfo(AlterType::ALTER_FORTRESS, std::move(data.catalog), std::move(data.schema), std::move(data.name), data.if_exists), alter_fortress_type(type) {
}
AlterFortressInfo::~AlterFortressInfo() {
}

CatalogType AlterFortressInfo::GetCatalogType() const {
	return CatalogType::FORTRESS_ENTRY;
}

void AlterFortressInfo::Serialize(FieldWriter &writer) const {
	writer.WriteField<AlterFortressType>(alter_fortress_type);
	writer.WriteString(catalog);
	writer.WriteString(schema);
	writer.WriteString(name);
	writer.WriteField(if_exists);
	SerializeAlterRole(writer);
}

unique_ptr<AlterInfo> AlterFortressInfo::Deserialize(FieldReader &reader) {
	auto type = reader.ReadRequired<AlterFortressType>();
	AlterEntryData data;
	data.catalog = reader.ReadRequired<string>();
	data.schema = reader.ReadRequired<string>();
	data.name = reader.ReadRequired<string>();
	data.if_exists = reader.ReadRequired<bool>();
	switch (type) {
	case AlterFortressType::FORTRESS_CHANGE:
		return ModifyFortressInfo::Deserialize(reader, std::move(data));
	case AlterFortressType::LOCK_CHANGE:
		return LockFortressInfo::Deserialize(reader, std::move(data));
	case AlterFortressType::UNLOCK_CHANGE:
		return UnlockFortressInfo::Deserialize(reader, std::move(data));
	default:
		throw SerializationException("Unknown alter table type for deserialization!");
	}
}

//===--------------------------------------------------------------------===//
// Modify Fortress
//===--------------------------------------------------------------------===//
ModifyFortressInfo::ModifyFortressInfo(AlterEntryData data)
    : AlterFortressInfo(AlterFortressType::FORTRESS_CHANGE, std::move(data)) {
}
ModifyFortressInfo::~ModifyFortressInfo() {
}

unique_ptr<AlterInfo> ModifyFortressInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_exists);
	auto result = make_unique<ModifyFortressInfo>(std::move(data));
	result->table = table->Copy();
	result->expression = expression->Copy();
	result->complement_expression = complement_expression->Copy();
	return result;
}

void ModifyFortressInfo::SerializeAlterRole(FieldWriter &writer) const {
	writer.WriteSerializable(*table);
	writer.WriteSerializable(*expression);
	writer.WriteSerializable(*complement_expression);
}

unique_ptr<AlterInfo> ModifyFortressInfo::Deserialize(FieldReader &reader, AlterEntryData data) {
	auto table = reader.ReadRequiredSerializable<TableRef>();
	auto expression = reader.ReadRequiredSerializable<ParsedExpression>();
	auto complement_expression = reader.ReadRequiredSerializable<ParsedExpression>();
	auto result = make_unique<ModifyFortressInfo>(std::move(data));
	result->table = std::move(table);
	result->expression = std::move(expression);
	result->complement_expression = std::move(complement_expression);
	return result;
}

//===--------------------------------------------------------------------===//
// Lock Fortress
//===--------------------------------------------------------------------===//
LockFortressInfo::LockFortressInfo(AlterEntryData data, string start_date, string end_date)
    : AlterFortressInfo(AlterFortressType::LOCK_CHANGE, std::move(data)), start_date(std::move(start_date)), end_date(std::move(end_date)) {
}
LockFortressInfo::~LockFortressInfo() {
}

unique_ptr<AlterInfo> LockFortressInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_exists);
	return make_unique_base<AlterInfo, LockFortressInfo>(std::move(data), start_date, end_date);
}

void LockFortressInfo::SerializeAlterRole(FieldWriter &writer) const {
	writer.WriteString(start_date);
	writer.WriteString(end_date);
}

unique_ptr<AlterInfo> LockFortressInfo::Deserialize(FieldReader &reader, AlterEntryData data) {
	auto start_date = reader.ReadRequired<string>();
	auto end_date = reader.ReadRequired<string>();
	return make_unique<LockFortressInfo>(std::move(data), start_date, end_date);	
}

//===--------------------------------------------------------------------===//
// Unlock Fortress
//===--------------------------------------------------------------------===//
UnlockFortressInfo::UnlockFortressInfo(AlterEntryData data)
    : AlterFortressInfo(AlterFortressType::UNLOCK_CHANGE, std::move(data)), for_role(string()) {
}
UnlockFortressInfo::~UnlockFortressInfo() {
}

unique_ptr<AlterInfo> UnlockFortressInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_exists);
	auto result = make_unique<UnlockFortressInfo>(std::move(data));
	result->for_role = for_role;
	return result;
}

void UnlockFortressInfo::SerializeAlterRole(FieldWriter &writer) const {
	writer.WriteString(for_role);
}

unique_ptr<AlterInfo> UnlockFortressInfo::Deserialize(FieldReader &reader, AlterEntryData data) {
	return make_unique<UnlockFortressInfo>(std::move(data));	
}

} // namespace duckdb

