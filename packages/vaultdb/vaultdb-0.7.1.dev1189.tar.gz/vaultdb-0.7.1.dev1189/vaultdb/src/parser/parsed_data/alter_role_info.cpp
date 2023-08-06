#include "duckdb/parser/parsed_data/alter_role_info.hpp"
#include "duckdb/common/field_writer.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// AlterRoleInfo
//===--------------------------------------------------------------------===//
AlterRoleInfo::AlterRoleInfo(AlterRoleType type, AlterEntryData data)
    : AlterInfo(AlterType::ALTER_ROLE, std::move(data.catalog), std::move(data.schema), std::move(data.name), data.if_exists), 
	  alter_role_type(type) {
}
AlterRoleInfo::~AlterRoleInfo() {
}

CatalogType AlterRoleInfo::GetCatalogType() const {
	return CatalogType::ROLE_ENTRY;
}

void AlterRoleInfo::Serialize(FieldWriter &writer) const {
	writer.WriteField<AlterRoleType>(alter_role_type);
	writer.WriteString(catalog);
	writer.WriteString(schema);
	writer.WriteString(name);
	writer.WriteField(if_exists);
}

unique_ptr<AlterInfo> AlterRoleInfo::Deserialize(FieldReader &reader) {
	auto type = reader.ReadRequired<AlterRoleType>();
	auto catalog = reader.ReadRequired<string>();
	auto schema = reader.ReadRequired<string>();
	auto role = reader.ReadRequired<string>();
	auto if_exists = reader.ReadRequired<bool>();
	AlterEntryData data(catalog, schema, role, if_exists);
	switch (type) {
	case AlterRoleType::SUPERUSER_CHANGE:
	case AlterRoleType::LOGIN_CHANGE:
		return ModifyRoleFlagInfo::Deserialize(reader, type, std::move(data));
	default:
		throw SerializationException("Unknown alter table type for deserialization!");
	}
}

//===--------------------------------------------------------------------===//
// Modify Login flag
//===--------------------------------------------------------------------===//
ModifyRoleFlagInfo::ModifyRoleFlagInfo(AlterRoleType type, AlterEntryData data, bool flag)
    : AlterRoleInfo(type, std::move(data)), flag(std::move(flag)) {
}
ModifyRoleFlagInfo::~ModifyRoleFlagInfo() {
}

unique_ptr<AlterInfo> ModifyRoleFlagInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_exists);
	return make_unique_base<AlterInfo, ModifyRoleFlagInfo>(alter_role_type, std::move(data), flag);
}

void ModifyRoleFlagInfo::SerializeAlterRole(FieldWriter &writer) const {
	writer.WriteField<bool>(flag);
}

unique_ptr<AlterInfo> ModifyRoleFlagInfo::Deserialize(FieldReader &reader, AlterRoleType alter_role_type, AlterEntryData data) {
	auto role_flag = reader.ReadRequired<bool>();
	return make_unique<ModifyRoleFlagInfo>(alter_role_type, std::move(data), role_flag);	
}

//===--------------------------------------------------------------------===//
// Modify Role Privileges
//===--------------------------------------------------------------------===//
ModifyRolePrivilegeInfo::ModifyRolePrivilegeInfo(AlterRoleType type, AlterEntryData data, CatalogType resourcetype, string resourcename, uint64_t privileges, bool modifygrantOption)
    : AlterRoleInfo(type, std::move(data)), resourcetype(std::move(resourcetype)), resourcename(std::move(resourcename)), privileges(privileges), modifygrantOption(std::move(modifygrantOption)) {
}
ModifyRolePrivilegeInfo::~ModifyRolePrivilegeInfo() {
}

unique_ptr<AlterInfo> ModifyRolePrivilegeInfo::Copy() const {
	AlterEntryData data(catalog, schema, name, if_exists);
	return make_unique_base<AlterInfo, ModifyRolePrivilegeInfo>(alter_role_type, std::move(data), resourcetype, resourcename, privileges, modifygrantOption);
}

void ModifyRolePrivilegeInfo::SerializeAlterRole(FieldWriter &writer) const {
	writer.WriteField<CatalogType>(resourcetype);
	writer.WriteString(resourcename);
	writer.WriteField<uint64_t>(privileges);
	writer.WriteField<bool>(modifygrantOption);
}

unique_ptr<AlterInfo> ModifyRolePrivilegeInfo::Deserialize(FieldReader &reader, AlterRoleType alter_role_type, AlterEntryData data) {
	auto role_resourcetype = reader.ReadRequired<CatalogType>();
	auto role_resourcename = reader.ReadRequired<string>();
	auto role_privileges = reader.ReadRequired<uint64_t>();
	auto grantOption_flag = reader.ReadRequired<bool>();
	return make_unique<ModifyRolePrivilegeInfo>(alter_role_type, std::move(data), role_resourcetype, role_resourcename, role_privileges, grantOption_flag);	
}

} // namespace duckdb

