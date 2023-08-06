//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/parsed_data/create_fortress_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/limits.hpp"
#include "duckdb/common/map.hpp"
#include "duckdb/parser/parsed_data/create_info.hpp"
#include "duckdb/parser/tableref.hpp"
#include "duckdb/parser/parsed_expression.hpp"
#include "duckdb/parser/parsed_data/create_view_info.hpp"

namespace duckdb {

struct CreateFortressInfo : public CreateInfo {
	CreateFortressInfo() : CreateInfo(CatalogType::FORTRESS_ENTRY, SECURITY_SCHEMA), 
		name(string()), locked(false), start_date(string()), end_date(string()), unlocked_for_role(string()) {
	}

	//! fortress name to create
	string name;
	//! fortress lock info
	bool locked;
	string start_date;
	string end_date;
	string unlocked_for_role;
	//! The table to create the fortress on
	unique_ptr<TableRef> table;
	//! where clause
	unique_ptr<ParsedExpression> expression;
	unique_ptr<ParsedExpression> complement_expression;

public:
	unique_ptr<CreateFortressInfo> CopyFortress() const {
		auto result = make_unique<CreateFortressInfo>();
		CopyProperties(*result);
		result->name = name;
		result->schema = schema;
		result->table = table->Copy();
		result->expression = expression->Copy();
		result->expression = complement_expression->Copy();
		return result;
	}

	unique_ptr<CreateInfo> Copy() const override {
		return std::move(CopyFortress());
	}
protected:
	void SerializeInternal(Serializer &serializer) const override {
		FieldWriter writer(serializer);
		writer.WriteString(name);
		writer.WriteString(schema);
		writer.WriteField<bool>(locked);
		writer.WriteString(start_date);
		writer.WriteString(end_date);
		writer.WriteString(unlocked_for_role);
		writer.Finalize();
	}
};

} // namespace duckdb
