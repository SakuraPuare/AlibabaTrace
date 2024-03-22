import pathlib

from fastapi import APIRouter, Query

from config import *
from utils import md5

list_cache = {}
tree_cache = {}

router = APIRouter(
    prefix="/table",
    tags=["table"],
)


def update_list_cache() -> None:
    global list_cache
    table_folder = pathlib.Path(TABLE_FOLDER)
    if not table_folder.exists():
        return
    for i in table_folder.iterdir():
        if i.is_dir():
            for j in i.iterdir():
                name = str(j)
                list_cache[md5(name)] = name


def update_tree_cache() -> None:
    global tree_cache
    table_folder = pathlib.Path(TABLE_FOLDER)
    if not table_folder.exists():
        return
    for i in table_folder.iterdir():
        if i.is_dir():
            files = i.iterdir()
            tree_cache[md5(i.name)] = {
                "name": i.name,
                "files": {
                    md5(str(j)): j.name for j in files if j.is_file()
                }
            }


@router.get("/")
async def base_table():
    return {"message": "Table Home"}


@router.get("/list")
async def table_lists():
    global list_cache
    update_list_cache()
    return {"code": 200, "data": list_cache, "count": len(list_cache)}


@router.get("/tree")
async def table_tree():
    global tree_cache
    update_tree_cache()
    return {"code": 200, "data": tree_cache, "count": len(tree_cache)}


@router.get("/{table_hash}")
async def table_list(*, table_hash: str, page: int = Query(0)):
    global list_cache
    if table_hash not in list_cache:
        update_list_cache()
    if table_hash not in list_cache:
        return {"code": 404, "message": "Table not found"}
    table = list_cache[table_hash]
    data = []
    with open(table, "r") as f:
        for i in range(page * 50):
            f.readline()
        for i in range(50):
            line = f.readline()
            if not line:
                break
            data.append(line.strip())
    return {"code": 200, "data": '\n'.join(data)}
