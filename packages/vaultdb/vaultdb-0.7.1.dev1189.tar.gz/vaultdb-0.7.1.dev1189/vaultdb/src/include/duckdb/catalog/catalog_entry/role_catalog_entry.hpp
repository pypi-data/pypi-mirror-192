//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/catalog/catalog_entry/sequence_catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/catalog/standard_entry.hpp"
#include "duckdb/common/mutex.hpp"
#include "duckdb/parser/parsed_data/create_role_info.hpp"
#include "duckdb/parser/parsed_data/alter_table_info.hpp"

namespace duckdb {
class Serializer;
class Deserializer;
class BaseTableRef;

//! A role catalog entry
class RoleCatalogEntry : public StandardEntry {
public:
	static constexpr const CatalogType Type = CatalogType::ROLE_ENTRY;
	static constexpr const char *Name = "role";

public:
	//! Create a real RoleCatalogEntry and initialize storage for it
	RoleCatalogEntry(Catalog *catalog, SchemaCatalogEntry *schema, CreateRoleInfo *info);

	//! role information
	unique_ptr<CreateRoleInfo> info;

public:
	unique_ptr<CatalogEntry> AlterEntry(ClientContext &context, AlterInfo *info) override;
	//! Serialize the meta information of the RoleCatalogEntry a serializer
	virtual void Serialize(Serializer &serializer);
	//! Deserializes to a CreateTableInfo
	static unique_ptr<CreateRoleInfo> Deserialize(Deserializer &source);

	string ToSQL() override;
};
} // namespace duckdb
