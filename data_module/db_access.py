import pickle, shelve, json
from typing import Dict, Iterable
from config import db_path


def dump_to_shelve(obj: Dict, path: str) -> None:
    with shelve.open(path, flag="c") as db:
        [db.setdefault(k, obj[k]) for k in obj]


def load_from_pickle(path: str) -> Iterable:
    with open(path, "rb") as db:
        return pickle.load(db)


def dump_to_pickle(obj: Dict, path: str) -> None:
    with open(path, "wb") as db:
        pickle.dump(obj, db)


def load_from_json(path: str) -> Iterable:
    with open(path, "r") as f:
        return json.load(f)


def dump_to_json(obj: Dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def get_node(id: str, node_dict: Dict):
    if id in node_dict:
        return node_dict[id]
    with (open(f"{db_path}/shared_node_dict.db", "rb") as f):
        shared_node_dict = pickle.load(f)
        assert id in shared_node_dict, f"{id = } cannot be found!"
        return shared_node_dict[id]
