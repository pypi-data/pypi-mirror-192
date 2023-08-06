#include "duckdb/catalog/catalog_entry/tag_catalog_entry.hpp"

#include "duckdb/catalog/catalog_entry/schema_catalog_entry.hpp"
#include "duckdb/catalog/dependency_manager.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/common/field_writer.hpp"

#include <algorithm>
#include <sstream>

namespace duckdb {

TagCatalogEntry::TagCatalogEntry(Catalog *catalog, SchemaCatalogEntry *schema, CreateTagInfo *info)
    : StandardEntry(CatalogType::TAG_ENTRY, schema, catalog, info->name), 
	comment(std::move(info->comment)), function(std::move(info->function)) {
}

unique_ptr<CatalogEntry> TagCatalogEntry::AlterEntry(ClientContext &context, AlterInfo *alterinfo) {
	throw InternalException("Tag Alter is not supported yet! Please drop and recreate");
}

void TagCatalogEntry::Serialize(Serializer &serializer) {
	FieldWriter writer(serializer);
	writer.WriteString(schema->name);
	writer.WriteString(name);
	writer.WriteString(comment);
	writer.WriteSerializable(*function);
	writer.Finalize();
}

unique_ptr<CreateTagInfo> TagCatalogEntry::Deserialize(Deserializer &source) {
	auto info = make_unique<CreateTagInfo>();

	FieldReader reader(source);
	info->schema = reader.ReadRequired<string>();
	info->name = reader.ReadRequired<string>();
	info->comment = reader.ReadRequired<string>();
	info->function = reader.ReadRequiredSerializable<ParsedExpression>();
	reader.Finalize();
	return info;
}

string TagCatalogEntry::ToSQL() {
	std::stringstream ss;
	ss << "CREATE TAG ";
	ss << name;
	ss << " AS '";
	ss << comment;
	ss << "';";
	return ss.str();
}

} // namespace duckdb
