#include "duckdb/execution/operator/schema/physical_create_role.hpp"
#include "duckdb/catalog/catalog.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Source
//===--------------------------------------------------------------------===//
class CreateRoleSourceState : public GlobalSourceState {
public:
	CreateRoleSourceState() : finished(false) {
	}

	bool finished;
};

unique_ptr<GlobalSourceState> PhysicalCreateRole::GetGlobalSourceState(ClientContext &context) const {
	return make_unique<CreateRoleSourceState>();
}

void PhysicalCreateRole::GetData(ExecutionContext &context, DataChunk &chunk, GlobalSourceState &gstate,
                                     LocalSourceState &lstate) const {
	auto &state = (CreateRoleSourceState &)gstate;
	if (state.finished) {
		return;
	}
	auto &catalog = Catalog::GetCatalog(context.client, info->catalog);
	catalog.CreateRole(context.client, info.get());
	state.finished = true;
}

} // namespace duckdb
