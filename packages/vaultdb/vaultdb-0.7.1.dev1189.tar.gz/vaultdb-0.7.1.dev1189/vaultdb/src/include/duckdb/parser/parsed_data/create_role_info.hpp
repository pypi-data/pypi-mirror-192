//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_role_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/map.hpp"
#include "duckdb/parser/parsed_data/create_info.hpp"

namespace duckdb {

struct CreatePrivilegeInfo : public CreateInfo {
	explicit CreatePrivilegeInfo(CatalogType type, string name) : CreateInfo(type, SECURITY_SCHEMA), 
		name(name), privileges(1 << 0), grantOption(false) {
	}

	string name;
	uint64_t privileges;
	bool grantOption;
	vector<string> unauthorized_columns;

public:
	unique_ptr<CreatePrivilegeInfo> CopyPrivilege() const {
		auto result = make_unique<CreatePrivilegeInfo>(type, name);
		CopyProperties(*result);
		result->grantOption = grantOption;
		result->privileges = privileges;
		for (idx_t i=0; i<unauthorized_columns.size(); i++)
			result->unauthorized_columns.push_back(unauthorized_columns[i]);
		return result;
	}

	unique_ptr<CreateInfo> Copy() const override {
		return std::move(CopyPrivilege());
	}

protected:
	void SerializeInternal(Serializer &serializer) const override {
		FieldWriter writer(serializer);
		writer.WriteString(name);
		writer.WriteField<uint64_t>(privileges);
		writer.WriteField<bool>(grantOption);
		writer.WriteList<string>(unauthorized_columns);
		writer.Finalize();
	}
};

struct CreateRoleInfo : public CreateInfo {
	CreateRoleInfo() : CreateInfo(CatalogType::ROLE_ENTRY, SECURITY_SCHEMA), 
		name(string()), login(false), superuser(false) {
	}

	//! role name to create
	string name;
	//! role publickey
	string publickey;
	//! can role login
	bool login;
	//! is role super user
	bool superuser;

	//! privileges (maps used to make sure we can find different privileges by type and name)
	map<CatalogType, map<string, unique_ptr<CreatePrivilegeInfo>>> privileges;

public:
	unique_ptr<CreateRoleInfo> CopyRole() const {
		auto result = make_unique<CreateRoleInfo>();
		CopyProperties(*result);
		result->name = name;
		result->login = login;
		result->superuser = superuser;
		result->schema = schema;
		for (auto &privilegetypes : privileges) {
			auto privilegetype = privilegetypes.first;
			for (auto &privilege : privilegetypes.second) {
				result->privileges[privilegetype][privilege.first]=std::move(privilege.second->CopyPrivilege());
			}
		}
		return result;
	}

	unique_ptr<CreateInfo> Copy() const override {
		return std::move(CopyRole());
	}

protected:
	void SerializeInternal(Serializer &serializer) const override {
		FieldWriter writer(serializer);
		writer.WriteString(name);
		writer.WriteString(publickey);
		writer.WriteField<bool>(login);
		writer.WriteField<bool>(superuser);
		writer.Finalize();
	}
};

} // namespace duckdb
