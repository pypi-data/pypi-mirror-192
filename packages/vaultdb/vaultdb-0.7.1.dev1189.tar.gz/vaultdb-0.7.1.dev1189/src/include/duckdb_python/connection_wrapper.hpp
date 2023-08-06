#pragma once

#include "duckdb_python/pyconnection.hpp"
#include "duckdb_python/pyrelation.hpp"

namespace duckdb {

class PyConnectionWrapper {
public:
	PyConnectionWrapper() = delete;

public:
	static shared_ptr<VaultDBPyConnection> ExecuteMany(const string &query, py::object params = py::list(),
	                                                  shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> Execute(const string &query, py::object params = py::list(),
	                                              bool many = false, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> Append(const string &name, DataFrame value,
	                                             shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> RegisterPythonObject(const string &name, py::object python_object,
	                                                           shared_ptr<VaultDBPyConnection> conn = nullptr);

	static void InstallExtension(const string &extension, bool force_install = false,
	                             shared_ptr<VaultDBPyConnection> conn = nullptr);

	static void LoadExtension(const string &extension, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromQuery(const string &query, const string &alias = "query_relation",
	                                              shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> RunQuery(const string &query, const string &alias = "query_relation",
	                                             shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> Table(const string &tname, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> Values(py::object params = py::none(),
	                                           shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> View(const string &vname, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> TableFunction(const string &fname, py::object params = py::list(),
	                                                  shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromDF(const DataFrame &value, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromParquet(const string &file_glob, bool binary_as_string,
	                                                bool file_row_number, bool filename, bool hive_partitioning,
	                                                bool union_by_name, const py::object &compression = py::none(),
	                                                shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromParquets(const vector<string> &file_globs, bool binary_as_string,
	                                                 bool file_row_number, bool filename, bool hive_partitioning,
	                                                 bool union_by_name, const py::object &compression = py::none(),
	                                                 shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromArrow(py::object &arrow_object,
	                                              shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> FromSubstrait(py::bytes &proto, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> GetSubstrait(const string &query,
	                                                 shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation> GetSubstraitJSON(const string &query,
	                                                     shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unordered_set<string> GetTableNames(const string &query, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> UnregisterPythonObject(const string &name,
	                                                             shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> Begin(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> Commit(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> Rollback(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static void Close(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static shared_ptr<VaultDBPyConnection> Cursor(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static py::object GetDescription(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static py::object FetchOne(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static py::list FetchMany(idx_t size, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static unique_ptr<VaultDBPyRelation>
	ReadCSV(const string &name, shared_ptr<VaultDBPyConnection> conn, const py::object &header = py::none(),
	        const py::object &compression = py::none(), const py::object &sep = py::none(),
	        const py::object &delimiter = py::none(), const py::object &dtype = py::none(),
	        const py::object &na_values = py::none(), const py::object &skiprows = py::none(),
	        const py::object &quotechar = py::none(), const py::object &escapechar = py::none(),
	        const py::object &encoding = py::none(), const py::object &parallel = py::none(),
	        const py::object &date_format = py::none(), const py::object &timestamp_format = py::none(),
	        const py::object &sample_size = py::none(), const py::object &all_varchar = py::none(),
	        const py::object &normalize_names = py::none(), const py::object &filename = py::none());

	static py::list FetchAll(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static py::dict FetchNumpy(shared_ptr<VaultDBPyConnection> conn = nullptr);

	static DataFrame FetchDF(bool date_as_object, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static DataFrame FetchDFChunk(const idx_t vectors_per_chunk = 1, bool date_as_object = false,
	                              shared_ptr<VaultDBPyConnection> conn = nullptr);

	static duckdb::pyarrow::Table FetchArrow(idx_t chunk_size, shared_ptr<VaultDBPyConnection> conn = nullptr);

	static duckdb::pyarrow::RecordBatchReader FetchRecordBatchReader(const idx_t chunk_size,
	                                                                 shared_ptr<VaultDBPyConnection> conn = nullptr);

	static void RegisterFilesystem(AbstractFileSystem file_system, shared_ptr<VaultDBPyConnection> conn);
	static void UnregisterFilesystem(const py::str &name, shared_ptr<VaultDBPyConnection> conn);
	static py::list ListFilesystems(shared_ptr<VaultDBPyConnection> conn);
};
} // namespace duckdb
