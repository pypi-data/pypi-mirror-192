#include "duckdb/parser/parsed_data/create_fortress_info.hpp"
#include "duckdb/parser/statement/alter_statement.hpp"
#include "duckdb/parser/parsed_data/alter_fortress_info.hpp"
#include "duckdb/parser/statement/create_statement.hpp"
#include "duckdb/parser/statement/drop_statement.hpp"
#include "duckdb/parser/transformer.hpp"
#include "duckdb/parser/expression/list.hpp"
#include "duckdb/catalog/catalog.hpp"
#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"

namespace duckdb {

unique_ptr<ParsedExpression> Transformer::ComplementWhereClause(ParsedExpression &expr) {	
	switch (expr.expression_class) {
	case ExpressionClass::BETWEEN: {
		auto &cast_expr = (BetweenExpression &)expr;
		auto left = make_unique<ComparisonExpression>(ExpressionType::COMPARE_GREATERTHAN, 
				ComplementWhereClause(*cast_expr.input), 
				ComplementWhereClause(*cast_expr.upper));
		auto right = make_unique<ComparisonExpression>(ExpressionType::COMPARE_LESSTHAN, 
				ComplementWhereClause(*cast_expr.input), 
				ComplementWhereClause(*cast_expr.lower));
		auto result = make_unique<ConjunctionExpression>(ExpressionType::CONJUNCTION_AND, std::move(left), std::move(right));
		return std::move(result);
	}
	case ExpressionClass::COMPARISON: {
		auto &comp_expr = (ComparisonExpression &)expr;
		ExpressionType flipped_type = ExpressionType::INVALID;
		switch (comp_expr.type) {
		case ExpressionType::COMPARE_NOTEQUAL:
			flipped_type = ExpressionType::COMPARE_EQUAL;
			break;
		case ExpressionType::COMPARE_EQUAL:
			flipped_type = ExpressionType::COMPARE_NOTEQUAL;
			break;
		case ExpressionType::COMPARE_LESSTHAN:
			flipped_type = ExpressionType::COMPARE_GREATERTHAN;
			break;
		case ExpressionType::COMPARE_GREATERTHAN:
			flipped_type = ExpressionType::COMPARE_LESSTHAN;
			break;
		case ExpressionType::COMPARE_LESSTHANOREQUALTO:
			flipped_type = ExpressionType::COMPARE_GREATERTHANOREQUALTO;
			break;
		case ExpressionType::COMPARE_GREATERTHANOREQUALTO:
			flipped_type = ExpressionType::COMPARE_LESSTHANOREQUALTO;
			break;
		default:
			throw InternalException("Unsupported comparison type in flip");
		}		
		auto result = make_unique<ComparisonExpression>(flipped_type,
				ComplementWhereClause(*comp_expr.left), 
				ComplementWhereClause(*comp_expr.right));
		return std::move(result);
	}
	case ExpressionClass::CONJUNCTION: {
		auto &conj_expr = (ConjunctionExpression &)expr;
		unique_ptr<ConjunctionExpression> result;
		if (conj_expr.type==ExpressionType::CONJUNCTION_OR)
			result = make_unique<ConjunctionExpression>(ExpressionType::CONJUNCTION_AND);
		else if (conj_expr.type==ExpressionType::CONJUNCTION_AND)
			result = make_unique<ConjunctionExpression>(ExpressionType::CONJUNCTION_OR);
		else
			throw NotImplementedException("Unimplemented fortress conjuction type expression class");

		for (auto &child : conj_expr.children) {
			result->AddExpression(ComplementWhereClause(*child));
		}
		return std::move(result);
	}
	case ExpressionClass::OPERATOR: {
		auto &op_expr = (OperatorExpression &)expr;
		ExpressionType flipped_type = ExpressionType::INVALID;
		switch (expr.type) {
		case ExpressionType::COMPARE_NOTEQUAL:
			flipped_type = ExpressionType::COMPARE_EQUAL;
			break;
		case ExpressionType::COMPARE_EQUAL:
			flipped_type = ExpressionType::COMPARE_NOTEQUAL;
			break;
		case ExpressionType::COMPARE_LESSTHAN:
			flipped_type = ExpressionType::COMPARE_GREATERTHAN;
			break;
		case ExpressionType::COMPARE_GREATERTHAN:
			flipped_type = ExpressionType::COMPARE_LESSTHAN;
			break;
		case ExpressionType::COMPARE_LESSTHANOREQUALTO:
			flipped_type = ExpressionType::COMPARE_GREATERTHANOREQUALTO;
			break;
		case ExpressionType::COMPARE_GREATERTHANOREQUALTO:
			flipped_type = ExpressionType::COMPARE_LESSTHANOREQUALTO;
			break;
		default:
			throw InternalException("Unsupported comparison type in flip");
		}

		auto result = make_unique<OperatorExpression>(flipped_type);
		for (auto &child : op_expr.children) {
			result->children.push_back(ComplementWhereClause(*child));
		}
		return std::move(result);
	}
	case ExpressionClass::COLUMN_REF:
	case ExpressionClass::CONSTANT:
	case ExpressionClass::DEFAULT:
	case ExpressionClass::COLLATE:
	case ExpressionClass::CAST:
		return expr.Copy();
	default:
		throw NotImplementedException("Unimplemented fortress expression class");
	}
}

unique_ptr<CreateStatement> Transformer::TransformCreateFortress(duckdb_libpgquery::PGNode *node) {
	auto stmt = reinterpret_cast<duckdb_libpgquery::PGCreateFortressStmt *>(node);
	D_ASSERT(stmt);
	(void)stmt;

	if (context)
		context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_CREATE);

	auto result = make_unique<CreateStatement>();
	auto info = make_unique<CreateFortressInfo>();
	info->name = stmt->fortress->relname;
	auto tableref = make_unique<BaseTableRef>();
	tableref->table_name = stmt->tablename->relname;
	if (stmt->tablename->schemaname) {
		tableref->schema_name = stmt->tablename->schemaname;
	}
	else{
		tableref->schema_name = DEFAULT_SCHEMA;
	}
	info->table = std::move(tableref);	
	info->expression = TransformExpression(stmt->whereClause);
	info->complement_expression = ComplementWhereClause(*info->expression);
	result->info = std::move(info);
	return result;
}

unique_ptr<AlterStatement> Transformer::TransformAlterFortress(duckdb_libpgquery::PGNode *node) {
	auto stmt = reinterpret_cast<duckdb_libpgquery::PGAlterFortressStmt *>(node);
	D_ASSERT(stmt);
	(void)stmt;
	context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_ALTER);

	auto result = make_unique<AlterStatement>();
	auto tableref = make_unique<BaseTableRef>();
	tableref->table_name = stmt->tablename->relname;
	if (stmt->tablename->schemaname) {
		tableref->schema_name = stmt->tablename->schemaname;
	}
	else{
		tableref->schema_name = DEFAULT_SCHEMA;
	}
	AlterEntryData data(INVALID_CATALOG, SECURITY_SCHEMA, stmt->fortress->relname, true);
	auto info = make_unique<ModifyFortressInfo>(std::move(data));
	info->table = std::move(tableref);	
	info->expression = TransformExpression(stmt->whereClause);
	info->complement_expression = ComplementWhereClause(*info->expression);
	result->info = std::move(info);
	return result;
}

unique_ptr<AlterStatement> Transformer::TransformLockFortress(duckdb_libpgquery::PGNode *node) {
	context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_ALTER);
	auto stmt = reinterpret_cast<duckdb_libpgquery::PGLockFortressStmt *>(node);
	D_ASSERT(stmt);
	(void)stmt;
	auto result = make_unique<AlterStatement>();
	AlterEntryData data(INVALID_CATALOG, SECURITY_SCHEMA, stmt->fortress->relname, true);
	auto start_date = (duckdb_libpgquery::PGValue *)stmt->start_date;
	auto end_date = (duckdb_libpgquery::PGValue *)stmt->end_date;
	result->info = make_unique<LockFortressInfo>(std::move(data), start_date->val.str, end_date->val.str);
	return result;
}

unique_ptr<AlterStatement> Transformer::TransformUnlockFortress(duckdb_libpgquery::PGNode *node) {
	context->authorizer->Authorize_schema(SECURITY_SCHEMA, duckdb_libpgquery::PG_PRIVILEGE_ALTER);
	auto stmt = reinterpret_cast<duckdb_libpgquery::PGUnLockFortressStmt *>(node);
	D_ASSERT(stmt);
	(void)stmt;
	auto result = make_unique<AlterStatement>();
	AlterEntryData data(INVALID_CATALOG, SECURITY_SCHEMA, stmt->fortress->relname, true);
	auto info = make_unique<UnlockFortressInfo>(std::move(data));
	if (stmt->role)
		info->for_role = stmt->role->relname;
	result->info = std::move(info);
	return result;
}
} // namespace duckdb
