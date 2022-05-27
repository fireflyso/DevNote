import prefect
from prefect import task, Flow, Parameter
from prefect.executors import LocalDaskExecutor
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run
import time


def get_info_by_id(server_id):
    # 数据库查询
    return server_id


@task
def run_server(server_id):
    logger = prefect.context.get("logger")
    logger.info(f"Hello, {server_id}!")
    server_info = get_info_by_id(server_id)

    return server_info


with Flow("parent-flow") as flow:
    run_server(1)
    server_list = Parameter("node", default=[2, 3])
    run_server.map(server_list)
    run_server(4)

flow.executor = LocalDaskExecutor()
# Register the flow under the "tutorial" project
# flow.register(project_name="liuxulu")
flow.run()
