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


def syslog_message_parser(message: str) -> Dict[str, str]:
    """
    :param message: 'script,info 10.201.0.10|52:12:54:35:25:21|1'
    :return: {
        "client_ip": "10.201.0.10",
        "cleint_mac": "52:12:54:35:25:21",
        "client_status": message[2],
    }
    """
    message = message.split()[1].split("|")
    return {
        "client_ip": message[0],
        "cleint_mac": message[1].lower(),
        "client_status": message[2],
    }


def query_set_connection_status(conn: type(sqlite3.connect), client_address: str, client_status: int):
    query = f"""
        INSERT OR replace INTO DeviceConnectionStatus (id_device_connection_status,
                                                       Device_id_device,
                                                       LocationPlace_id_location_place,
                                                       online)
        VALUES (
                (SELECT id_device_connection_status FROM Device
                    LEFT JOIN DeviceConnectionStatus
                    ON DeviceConnectionStatus.Device_id_device = Device.id_device
                    WHERE Device.ip_address4 = {inet_aton(client_address)}),
                (SELECT id_device FROM Device WHERE Device.ip_address4 = {inet_aton(client_address)}),
                (SELECT id_location_place FROM LocationPlace WHERE LocationPlace.id_location_place IN
	                (SELECT LocationPlace_id_location_place FROM RefDeviceLocationPlace WHERE Device_id_device = 
		                (SELECT id_device FROM Device WHERE ip_address4 = {inet_aton(client_address)}))
	                AND	LocationPlace.Place_id_place IS NULL),
                {client_status}
               );"""

    if conn is not None:
        query_injection(conn, query)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")


__all__ = ["create_dir",
           "hash_str",
           "inet_aton",
           "inet_ntoa",
           "syslog_message_parser",
           "query_set_connection_status"]
