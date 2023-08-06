//===----------------------------------------------------------------------===//
//                         VaultDB
//
// duckdb_python/pyresult.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb_python/pybind_wrapper.hpp"
#include "duckdb.hpp"
#include "arrow_array_stream.hpp"
#include "duckdb/main/external_dependencies.hpp"
#include "duckdb_python/pandas_type.hpp"
#include "duckdb_python/registered_py_object.hpp"
#include "duckdb_python/pyresult.hpp"

namespace duckdb {

struct VaultDBPyConnection;

class PythonDependencies : public ExternalDependency {
public:
	explicit PythonDependencies(py::function map_function)
	    : ExternalDependency(ExternalDependenciesType::PYTHON_DEPENDENCY), map_function(std::move(map_function)) {};
	explicit PythonDependencies(unique_ptr<RegisteredObject> py_object)
	    : ExternalDependency(ExternalDependenciesType::PYTHON_DEPENDENCY) {
		py_object_list.push_back(std::move(py_object));
	};
	explicit PythonDependencies(unique_ptr<RegisteredObject> py_object_original,
	                            unique_ptr<RegisteredObject> py_object_copy)
	    : ExternalDependency(ExternalDependenciesType::PYTHON_DEPENDENCY) {
		py_object_list.push_back(std::move(py_object_original));
		py_object_list.push_back(std::move(py_object_copy));
	};
	py::function map_function;
	vector<unique_ptr<RegisteredObject>> py_object_list;
};

struct VaultDBPyRelation {
public:
	explicit VaultDBPyRelation(shared_ptr<Relation> rel);
	explicit VaultDBPyRelation(unique_ptr<VaultDBPyResult> result);

	shared_ptr<Relation> rel;

public:
	static void Initialize(py::handle &m);

	py::list Description();

	void Close();

	static unique_ptr<VaultDBPyRelation> FromDf(const DataFrame &df, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> Values(py::object values = py::list(),
	                                           shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromQuery(const string &query, const string &alias,
	                                              shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> RunQuery(const string &query, const string &alias,
	                                             shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromParquet(const string &file_glob, bool binary_as_string,
	                                                bool file_row_number, bool filename, bool hive_partitioning,
	                                                bool union_by_name, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromParquets(const vector<string> &file_globs, bool binary_as_string,
	                                                 bool file_row_number, bool filename, bool hive_partitioning,
	                                                 bool union_by_name, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromSubstrait(py::bytes &proto, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> GetSubstrait(const string &query,
	                                                 shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> GetSubstraitJSON(const string &query,
	                                                     shared_ptr<VaultDBPyConnection> conn = nullptr);
	static unique_ptr<VaultDBPyRelation> FromSubstraitJSON(const string &json,
	                                                      shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromParquetDefault(const string &filename,
	                                                       shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromArrow(py::object &arrow_object,
	                                              shared_ptr<VaultDBPyConnection> conn = nullptr);

	unique_ptr<VaultDBPyRelation> Project(const string &expr);

	static unique_ptr<VaultDBPyRelation> ProjectDf(const DataFrame &df, const string &expr,
	                                              shared_ptr<VaultDBPyConnection> conn = nullptr);

	py::str GetAlias();

	unique_ptr<VaultDBPyRelation> SetAlias(const string &expr);

	static unique_ptr<VaultDBPyRelation> AliasDF(const DataFrame &df, const string &expr,
	                                            shared_ptr<VaultDBPyConnection> conn = nullptr);

	unique_ptr<VaultDBPyRelation> Filter(const string &expr);

	static unique_ptr<VaultDBPyRelation> FilterDf(const DataFrame &df, const string &expr,
	                                             shared_ptr<VaultDBPyConnection> conn = nullptr);

	unique_ptr<VaultDBPyRelation> Limit(int64_t n, int64_t offset = 0);

	static unique_ptr<VaultDBPyRelation> LimitDF(const DataFrame &df, int64_t n,
	                                            shared_ptr<VaultDBPyConnection> conn = nullptr);

	unique_ptr<VaultDBPyRelation> Order(const string &expr);

	static unique_ptr<VaultDBPyRelation> OrderDf(const DataFrame &df, const string &expr,
	                                            shared_ptr<VaultDBPyConnection> conn = nullptr);

	unique_ptr<VaultDBPyRelation> Aggregate(const string &expr, const string &groups = "");

	unique_ptr<VaultDBPyRelation> GenericAggregator(const string &function_name, const string &aggregated_columns,
	                                               const string &groups = "", const string &function_parameter = "",
	                                               const string &projected_columns = "");

	unique_ptr<VaultDBPyRelation> Sum(const string &sum_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Count(const string &count_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Median(const string &median_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Quantile(const string &q, const string &quantile_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Min(const string &min_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Max(const string &max_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Mean(const string &mean_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Var(const string &var_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> STD(const string &std_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> ValueCounts(const string &std_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> MAD(const string &aggr_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Mode(const string &aggr_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Abs(const string &aggr_columns);
	unique_ptr<VaultDBPyRelation> Prod(const string &aggr_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Skew(const string &aggr_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Kurt(const string &aggr_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> SEM(const string &aggr_columns, const string &groups = "");

	unique_ptr<VaultDBPyRelation> Describe();

	duckdb::pyarrow::RecordBatchReader FetchRecordBatchReader(idx_t chunk_size);

	idx_t Length();

	py::tuple Shape();

	unique_ptr<VaultDBPyRelation> Unique(const string &aggr_columns);

	unique_ptr<VaultDBPyRelation> GenericWindowFunction(const string &function_name, const string &aggr_columns);
	unique_ptr<VaultDBPyRelation> CumSum(const string &aggr_columns);
	unique_ptr<VaultDBPyRelation> CumProd(const string &aggr_columns);
	unique_ptr<VaultDBPyRelation> CumMax(const string &aggr_columns);
	unique_ptr<VaultDBPyRelation> CumMin(const string &aggr_columns);

	static unique_ptr<VaultDBPyRelation> AggregateDF(const DataFrame &df, const string &expr, const string &groups = "",
	                                                shared_ptr<VaultDBPyConnection> conn = nullptr);

	unique_ptr<VaultDBPyRelation> Distinct();

	static unique_ptr<VaultDBPyRelation> DistinctDF(const DataFrame &df, shared_ptr<VaultDBPyConnection> conn = nullptr);

	DataFrame FetchDF(bool date_as_object);

	py::object FetchOne();

	py::object FetchAll();

	py::object FetchMany(idx_t size);

	py::dict FetchNumpy();

	py::dict FetchNumpyInternal(bool stream = false, idx_t vectors_per_chunk = 1);

	DataFrame FetchDFChunk(idx_t vectors_per_chunk, bool date_as_object);

	duckdb::pyarrow::Table ToArrowTable(idx_t batch_size);

	duckdb::pyarrow::RecordBatchReader ToRecordBatch(idx_t batch_size);

	unique_ptr<VaultDBPyRelation> Union(VaultDBPyRelation *other);

	unique_ptr<VaultDBPyRelation> Except(VaultDBPyRelation *other);

	unique_ptr<VaultDBPyRelation> Intersect(VaultDBPyRelation *other);

	unique_ptr<VaultDBPyRelation> Map(py::function fun);

	unique_ptr<VaultDBPyRelation> Join(VaultDBPyRelation *other, const string &condition, const string &type);

	void ToParquet(const string &filename, const py::object &compression = py::none());

	void ToCSV(const string &filename, const py::object &sep = py::none(), const py::object &na_rep = py::none(),
	           const py::object &header = py::none(), const py::object &quotechar = py::none(),
	           const py::object &escapechar = py::none(), const py::object &date_format = py::none(),
	           const py::object &timestamp_format = py::none(), const py::object &quoting = py::none(),
	           const py::object &encoding = py::none(), const py::object &compression = py::none());

	static void WriteCsvDF(const DataFrame &df, const string &file, shared_ptr<VaultDBPyConnection> conn = nullptr);

	// should this return a rel with the new view?
	unique_ptr<VaultDBPyRelation> CreateView(const string &view_name, bool replace = true);

	unique_ptr<VaultDBPyRelation> Query(const string &view_name, const string &sql_query);

	// Update the internal result of the relation
	VaultDBPyRelation &Execute();

	static unique_ptr<VaultDBPyRelation> QueryDF(const DataFrame &df, const string &view_name, const string &sql_query,
	                                            shared_ptr<VaultDBPyConnection> conn = nullptr);

	void InsertInto(const string &table);

	void Insert(const py::object &params = py::list());

	void Create(const string &table);

	py::str Type();
	py::list Columns();
	py::list ColumnTypes();

	string Print();

	string Explain();

	static bool IsRelation(const py::object &object);

private:
	string GenerateExpressionList(const string &function_name, const string &aggregated_columns,
	                              const string &groups = "", const string &function_parameter = "",
	                              const string &projected_columns = "", const string &window_function = "");
	string GenerateExpressionList(const string &function_name, const vector<string> &aggregated_columns,
	                              const string &groups = "", const string &function_parameter = "",
	                              const string &projected_columns = "", const string &window_function = "");
	void AssertResult() const;
	void AssertResultOpen() const;
	void ExecuteOrThrow();
	unique_ptr<QueryResult> ExecuteInternal();

private:
	unique_ptr<VaultDBPyResult> result;
	std::string rendered_result;
};

} // namespace duckdb
