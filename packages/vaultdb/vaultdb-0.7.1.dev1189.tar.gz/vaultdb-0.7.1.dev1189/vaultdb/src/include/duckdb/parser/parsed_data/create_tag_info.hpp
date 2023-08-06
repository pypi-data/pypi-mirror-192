//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_tag_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/map.hpp"
#include "duckdb/parser/parsed_data/create_info.hpp"

namespace duckdb {

struct CreateTagInfo : public CreateInfo {
	CreateTagInfo() : CreateInfo(CatalogType::TAG_ENTRY, SECURITY_SCHEMA), 
		name(string()), comment(string()) {
	}

	//! tag name to create
	string name;
	//! tag comment to create
	string comment;
	//! tag function expression
	unique_ptr<ParsedExpression> function;

public:
	unique_ptr<CreateTagInfo> CopyTag() const {
		auto result = make_unique<CreateTagInfo>();
		CopyProperties(*result);
		result->name = name;
		result->comment = comment;
		result->function = function->Copy();
		result->schema = schema;
		return result;
	}

	unique_ptr<CreateInfo> Copy() const override {
		return std::move(CopyTag());
	}
protected:
	void SerializeInternal(Serializer &serializer) const override {
		FieldWriter writer(serializer);
		writer.WriteString(name);
		writer.WriteString(comment);
		writer.Finalize();
	}
};

} // namespace duckdb
