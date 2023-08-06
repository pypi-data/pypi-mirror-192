#include "duckdb_python/connection_wrapper.hpp"
#include "duckdb/common/constants.hpp"

namespace duckdb {

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::ExecuteMany(const string &query, py::object params,
                                                                shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->ExecuteMany(query, params);
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::Execute(const string &query, py::object params, bool many,
                                                            shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Execute(query, params, many);
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::Append(const string &name, DataFrame value,
                                                           shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Append(name, value);
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::RegisterPythonObject(const string &name, py::object python_object,
                                                                         shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->RegisterPythonObject(name, python_object);
}

void PyConnectionWrapper::InstallExtension(const string &extension, bool force_install,
                                           shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	conn->InstallExtension(extension, force_install);
}

void PyConnectionWrapper::LoadExtension(const string &extension, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	conn->LoadExtension(extension);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::FromQuery(const string &query, const string &alias,
                                                            shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromQuery(query, alias);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::RunQuery(const string &query, const string &alias,
                                                           shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->RunQuery(query, alias);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::Table(const string &tname, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Table(tname);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::Values(py::object params, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Values(params);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::View(const string &vname, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->View(vname);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::TableFunction(const string &fname, py::object params,
                                                                shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->TableFunction(fname, params);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::FromDF(const DataFrame &value, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromDF(value);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::FromParquet(const string &file_glob, bool binary_as_string,
                                                              bool file_row_number, bool filename,
                                                              bool hive_partitioning, bool union_by_name,
                                                              const py::object &compression,
                                                              shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromParquet(file_glob, binary_as_string, file_row_number, filename, hive_partitioning, union_by_name,
	                         compression);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::FromParquets(const vector<string> &file_globs, bool binary_as_string,
                                                               bool file_row_number, bool filename,
                                                               bool hive_partitioning, bool union_by_name,
                                                               const py::object &compression,
                                                               shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromParquets(file_globs, binary_as_string, file_row_number, filename, hive_partitioning, union_by_name,
	                          compression);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::FromArrow(py::object &arrow_object,
                                                            shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromArrow(arrow_object);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::FromSubstrait(py::bytes &proto, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FromSubstrait(proto);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::GetSubstrait(const string &query,
                                                               shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->GetSubstrait(query);
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::GetSubstraitJSON(const string &query,
                                                                   shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->GetSubstraitJSON(query);
}

unordered_set<string> PyConnectionWrapper::GetTableNames(const string &query, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->GetTableNames(query);
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::UnregisterPythonObject(const string &name,
                                                                           shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->UnregisterPythonObject(name);
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::Begin(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Begin();
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::Commit(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Commit();
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::Rollback(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Rollback();
}

void PyConnectionWrapper::Close(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	conn->Close();
}

shared_ptr<VaultDBPyConnection> PyConnectionWrapper::Cursor(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->Cursor();
}

py::object PyConnectionWrapper::GetDescription(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->GetDescription();
}

py::object PyConnectionWrapper::FetchOne(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchOne();
}

unique_ptr<VaultDBPyRelation> PyConnectionWrapper::ReadCSV(
    const string &name, shared_ptr<VaultDBPyConnection> conn, const py::object &header, const py::object &compression,
    const py::object &sep, const py::object &delimiter, const py::object &dtype, const py::object &na_values,
    const py::object &skiprows, const py::object &quotechar, const py::object &escapechar, const py::object &encoding,
    const py::object &parallel, const py::object &date_format, const py::object &timestamp_format,
    const py::object &sample_size, const py::object &all_varchar, const py::object &normalize_names,
    const py::object &filename) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->ReadCSV(name, header, compression, sep, delimiter, dtype, na_values, skiprows, quotechar, escapechar,
	                     encoding, parallel, date_format, timestamp_format, sample_size, all_varchar, normalize_names,
	                     filename);
}

py::list PyConnectionWrapper::FetchMany(idx_t size, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchMany(size);
}

py::list PyConnectionWrapper::FetchAll(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchAll();
}

py::dict PyConnectionWrapper::FetchNumpy(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchNumpy();
}

DataFrame PyConnectionWrapper::FetchDF(bool date_as_object, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchDF(date_as_object);
}

DataFrame PyConnectionWrapper::FetchDFChunk(const idx_t vectors_per_chunk, bool date_as_object,
                                            shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchDFChunk(vectors_per_chunk, date_as_object);
}

duckdb::pyarrow::Table PyConnectionWrapper::FetchArrow(idx_t chunk_size, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchArrow(chunk_size);
}

duckdb::pyarrow::RecordBatchReader PyConnectionWrapper::FetchRecordBatchReader(const idx_t chunk_size,
                                                                               shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->FetchRecordBatchReader(chunk_size);
}

void PyConnectionWrapper::RegisterFilesystem(AbstractFileSystem file_system, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->RegisterFilesystem(std::move(file_system));
}
void PyConnectionWrapper::UnregisterFilesystem(const py::str &name, shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->UnregisterFilesystem(name);
}
py::list PyConnectionWrapper::ListFilesystems(shared_ptr<VaultDBPyConnection> conn) {
	if (!conn) {
		conn = VaultDBPyConnection::DefaultConnection();
	}
	return conn->ListFilesystems();
}

} // namespace duckdb
