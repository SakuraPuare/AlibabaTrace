from fastapi import APIRouter
from sqlalchemy import func

from database.model import *

router = APIRouter(prefix="/database", tags=["database"], responses={404: {"description": "Not found"}}, )

tables = {
    'batch_instance': BatchInstance,
    'batch_task': BatchTask,
    'call_graph': CallGraph,
    'container': Container,
    'container_meta': ContainerMeta,
    'container_usage': ContainerUsage,
    'core': Core,
    'host_meta': HostMeta,
    'machine_meta': MachineMeta,
    'machine_usage': MachineUsage,
    'ms_metric': MSMetrics,
    'ms_resource': MSResource,
    'node': Node,
    'uncore': UnCore,
}


@router.get("/list")
async def get_dataset_list():
    return list(tables.keys())


@router.get("/{dataset}")
async def get_dataset_data(dataset: str, page: int = 1, random: bool = False):
    if dataset not in tables:
        return {"message": "Dataset not found"}
    table = tables[dataset]

    if random:
        data = await table.all().limit(1000).order_by(func.rand()).offset((page - 1) * 1000)
    else:
        data = await table.all().limit(1000).offset((page - 1) * 1000)
    return data
