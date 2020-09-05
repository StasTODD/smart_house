from typing import List, Dict, Union, Any
from pathlib import Path
import hashlib
import ipaddress
import sqlite3


def create_dir(dir_path: str):
    """
    Create dir
    :param dir_path: 'images/background_template'
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def hash_str(string: str, hash_type: str = "sha1") -> str:
    """
    Create from string - hash string. Return a hash string.
    """
    if hash_type == "sha1":
        hash_object = hashlib.sha1(string.encode())
        return hash_object.hexdigest()


def inet_aton(address: str) -> int:
    """
    Convert IP-address to the int value
    :param address: '192.168.0.1'
    :return: 3232235521
    """
    return int(ipaddress.IPv4Address(address))


def inet_ntoa(number: int) -> str:
    """
    Convert int value to the IP-address
    :param number: 3232235521
    :return: '192.168.0.1'
    """
    return str(ipaddress.IPv4Address(number))


def query_injection(conn: type(sqlite3.connect), query_message: str, fetch: bool = False) -> Union[None, str]:
    cur = conn.cursor()
    cur.execute(query_message)
    if fetch:
        return cur.fetchall()


__all__ = ["create_dir",
           "hash_str",
           "inet_aton",
           "inet_ntoa"]
