#include "duckdb/execution/operator/schema/physical_create_fortress.hpp"
#include "duckdb/catalog/catalog.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
class CreateFortressSourceState : public GlobalSourceState {
public:
	CreateFortressSourceState() : finished(false) {
	}

	bool finished;
};

unique_ptr<GlobalSourceState> PhysicalCreateFortress::GetGlobalSourceState(ClientContext &context) const {
	return make_unique<CreateFortressSourceState>();
}

void PhysicalCreateFortress::GetData(ExecutionContext &context, DataChunk &chunk, GlobalSourceState &gstate,
                                     LocalSourceState &lstate) const {
	auto &state = (CreateFortressSourceState &)gstate;
	if (state.finished) {
		return;
	}
	auto &catalog = Catalog::GetCatalog(context.client, info->catalog);
	catalog.CreateFortress(context.client, info.get());
	state.finished = true;
}

} // namespace duckdb
