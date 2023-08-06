#include "duckdb/execution/operator/schema/physical_create_tag.hpp"
#include "duckdb/catalog/catalog.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
class CreateTagSourceState : public GlobalSourceState {
public:
	CreateTagSourceState() : finished(false) {
	}

	bool finished;
};

unique_ptr<GlobalSourceState> PhysicalCreateTag::GetGlobalSourceState(ClientContext &context) const {
	return make_unique<CreateTagSourceState>();
}

void PhysicalCreateTag::GetData(ExecutionContext &context, DataChunk &chunk, GlobalSourceState &gstate,
                                     LocalSourceState &lstate) const {
	auto &state = (CreateTagSourceState &)gstate;
	if (state.finished) {
		return;
	}
	auto &catalog = Catalog::GetCatalog(context.client, info->catalog);
	catalog.CreateTag(context.client, info.get());
	state.finished = true;
}

} // namespace duckdb
