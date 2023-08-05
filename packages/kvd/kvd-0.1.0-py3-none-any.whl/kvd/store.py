from typing import Dict
from urllib.request import urlretrieve
from io import TextIOWrapper
import os
import logging

from modelos import Object


logging.basicConfig(level=logging.INFO)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "raw.txt")


class KVStore(Object):
    """An immutable KV store"""

    hash_table: Dict[str, int]
    raw_file: TextIOWrapper

    def __init__(self, data_uri: str) -> None:
        """Create a KV store

        Args:
            data_uri (str): URI of immutable data to fetch
        """
        try:
            os.remove(DATA_PATH)
        except OSError:
            pass
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        urlretrieve(data_uri, DATA_PATH)
        self._build_table()

    def _build_table(self) -> None:
        tbl = {}

        f = open(DATA_PATH, "r", encoding="UTF-8")
        line = f.readline()
        uid = line.split(" ")[0]
        tbl[uid] = 0
        while line:
            offset = f.tell()
            line = f.readline()
            uid = line.split(" ")[0]
            tbl[uid] = offset
        f.seek(0)

        self.raw_file = f
        self.hash_table = tbl

    def get(self, uid: str) -> str:
        """Get a key

        Args:
            uid (str): UID to get

        Returns:
            str: Value
        """
        try:
            offset = self.hash_table[uid]
        except Exception:
            raise ValueError(f"key {uid} not found")

        self.raw_file.seek(offset)
        val_parts = self.raw_file.readline().split(" ")
        if len(val_parts) <= 1:
            raise ValueError(f"line at offset {offset} was malformed: '{val_parts}'")
        val = " ".join(val_parts[1:])
        return val
