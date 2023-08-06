#include "duckdb/execution/operator/persistent/physical_delete.hpp"

#include "duckdb/execution/expression_executor.hpp"
#include "duckdb/storage/data_table.hpp"
#include "duckdb/transaction/transaction.hpp"
#include "duckdb/transaction/duck_transaction.hpp"
#include "duckdb/common/types/column_data_collection.hpp"

#include "duckdb/common/atomic.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Sink
//===--------------------------------------------------------------------===//
class DeleteGlobalState : public GlobalSinkState {
public:
	explicit DeleteGlobalState(ClientContext &context, const vector<LogicalType> &return_types)
	    : deleted_count(0), return_collection(context, return_types) {
	}

	mutex delete_lock;
	mutex append_index_lock;
	idx_t deleted_count;
	ColumnDataCollection return_collection;
};

class DeleteLocalState : public LocalSinkState {
public:
	DeleteLocalState(Allocator &allocator, const vector<LogicalType> &table_types) {
		delete_chunk.Initialize(allocator, table_types);
	}
	DataChunk delete_chunk;
};

SinkResultType PhysicalDelete::Sink(ExecutionContext &context, GlobalSinkState &state, LocalSinkState &lstate,
                                    DataChunk &input) const {
	auto &gstate = (DeleteGlobalState &)state;
	auto &ustate = (DeleteLocalState &)lstate;

	// get rows and
	auto &transaction = DuckTransaction::Get(context.client, table.db);
	DataChunk delete_local_data;
	delete_local_data.Initialize(Allocator::DefaultAllocator(), input.GetTypes());
	DataChunk remote_data;
	remote_data.Initialize(Allocator::DefaultAllocator(), input.GetTypes());

	SelectionVector sel(STANDARD_VECTOR_SIZE);
	SelectionVector remote_data_sel(STANDARD_VECTOR_SIZE);
	if (is_remote_data_delete && table.info->tombstone){
		idx_t deleted_row_count = 0;
		idx_t remote_row_count = 0;
		auto &row_ids = input.data[row_id_index];
		auto row_id_data = FlatVector::GetData<row_t>(row_ids);
		for (idx_t i = 0; i < input.size(); i++) {
			auto row_id = row_id_data[i];
			if (row_id==REMOTE_ROW_ID)
				remote_data_sel.set_index(remote_row_count++, i);
			else
				sel.set_index(deleted_row_count++, i);
		}
		delete_local_data.Slice(input, sel, deleted_row_count);
		remote_data.Slice(input, remote_data_sel, remote_row_count);
	} else {
		delete_local_data.SetCardinality(input);
		for (idx_t i = 0; i < input.ColumnCount(); i++)
			delete_local_data.data[i].Reference(input.data[i]);
	}

	if (delete_local_data.size()>0){
		auto &row_identifiers = delete_local_data.data[row_id_index];

		vector<column_t> column_ids;
		for (idx_t i = 0; i < table.column_definitions.size(); i++) {
			column_ids.emplace_back(i);
		};
		auto cfs = ColumnFetchState();

		lock_guard<mutex> delete_guard(gstate.delete_lock);
		if (return_chunk) {
			row_identifiers.Flatten(input.size());
			table.Fetch(transaction, ustate.delete_chunk, column_ids, row_identifiers, input.size(), cfs);
			gstate.return_collection.Append(ustate.delete_chunk);
		}
		gstate.deleted_count += table.Delete(tableref, context.client, row_identifiers, input.size());
	}	
	
	if (remote_data.size()>0){
		vector<LogicalType> types;
		types.push_back(LogicalType::HASH);
		DataChunk mock_chunk;
		mock_chunk.Initialize(Allocator::DefaultAllocator(), types);
		mock_chunk.SetCardinality(remote_data);
		
		auto partitionKey_index = row_id_index;				
		for (idx_t row_idx = 0; row_idx < remote_data.size(); row_idx++) {
			hash_t primaryKey_hashvalue;
			bool combinehash = false;
			for (auto col_idx:merge_key_column_ids) {
				auto value = remote_data.GetValue(col_idx, row_idx);				
				if (combinehash) {
					auto hash_val = value.Hash();
					primaryKey_hashvalue = (primaryKey_hashvalue * UINT64_C(0xbf58476d1ce4e5b9)) ^ hash_val;
				} else{
					primaryKey_hashvalue = value.Hash();
					combinehash = true;
				}
				if (partitionKey_index == row_id_index && tableref.partition_key_columns.size()>0)
					partitionKey_index = col_idx;
			}
			mock_chunk.SetValue(0, row_idx, Value::HASH(primaryKey_hashvalue));
		}
		auto &row_identifiers = remote_data.data[partitionKey_index];
		lock_guard<mutex> append_index_guard(gstate.append_index_lock);
		if (table.info->tombstone){
			table.info->tombstone->VerifyAppend(mock_chunk);
			table.info->tombstone->Append(mock_chunk, row_identifiers);
		}
		gstate.deleted_count += mock_chunk.size();
	}

	return SinkResultType::NEED_MORE_INPUT;
}

unique_ptr<GlobalSinkState> PhysicalDelete::GetGlobalSinkState(ClientContext &context) const {
	return make_unique<DeleteGlobalState>(context, GetTypes());
}

unique_ptr<LocalSinkState> PhysicalDelete::GetLocalSinkState(ExecutionContext &context) const {
	return make_unique<DeleteLocalState>(Allocator::Get(context.client), table.GetTypes());
}

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
class DeleteSourceState : public GlobalSourceState {
public:
	explicit DeleteSourceState(const PhysicalDelete &op) : finished(false) {
		if (op.return_chunk) {
			D_ASSERT(op.sink_state);
			auto &g = (DeleteGlobalState &)*op.sink_state;
			g.return_collection.InitializeScan(scan_state);
		}
	}

	ColumnDataScanState scan_state;
	bool finished;
};

unique_ptr<GlobalSourceState> PhysicalDelete::GetGlobalSourceState(ClientContext &context) const {
	return make_unique<DeleteSourceState>(*this);
}

void PhysicalDelete::GetData(ExecutionContext &context, DataChunk &chunk, GlobalSourceState &gstate,
                             LocalSourceState &lstate) const {
	auto &state = (DeleteSourceState &)gstate;
	auto &g = (DeleteGlobalState &)*sink_state;
	if (state.finished) {
		return;
	}

	if (!return_chunk) {
		chunk.SetCardinality(1);
		chunk.SetValue(0, 0, Value::BIGINT(g.deleted_count));
		state.finished = true;
		return;
	}

	g.return_collection.Scan(state.scan_state, chunk);
}

} // namespace duckdb
