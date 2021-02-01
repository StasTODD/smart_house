import sys
import sqlite3
from typing import Dict, Union, Iterator
from os.path import isfile

sys.path.insert(0, "..")
from db import create_db
from lib.help_functions import hash_str, inet_aton, query_injection


def create_query_message(queries: Dict[str, list]) -> Iterator[str]:
    """
    Function for work with 'queries' variable. Returning the iterator with SQL query data from dictionary data structure
    """
    for query_name, query_info in queries.items():
        query_message = query_info[0]
        query_data = query_info[1]
        if isinstance(query_data, str):
            query_message = query_message.format(query_data)
            yield query_message
        elif isinstance(query_data, list):
            if query_message.count("{}") == 1:
                for one_query_data in query_data:
                    yield query_message.format(one_query_data)
            elif query_message.count("{}") > 1:
                for one_query_data_group in query_data:
                    yield query_message.format(*one_query_data_group)


def main(database_name: str):
    if isfile(database_name):
        conn = create_db.create_connection(database_name)
    else:
        create_db.main(database_name)
        conn = create_db.create_connection(database_name)

    queries = {
        "query_city": ["""INSERT INTO City (city) VALUES ("{}");""", "Kyiv"],
        "query_address": ["""INSERT INTO Address (address) VALUES ("{}");""", "Khreshchatyk 1"],
        "query_place": ["""INSERT INTO Place (place) VALUES ("{}");""", ["hallway",
                                                                         "main room",
                                                                         "children's room",
                                                                         "bedroom",
                                                                         "kitchen",
                                                                         "attic",
                                                                         "garage",
                                                                         "backyard",
                                                                         "basement"]
                        ],
        "query_location_place": ["""INSERT INTO LocationPlace (City_id_city, Address_id_address, Place_id_place) 
                                                                                            VALUES ({}, {}, {});""",
                                 [[1, 1, "NULL"], [1, 1, 1], [1, 1, 2]]],

        "query_connect_type": ["""INSERT INTO ConnectType (connect_type) VALUES ("{}");""", ["ssh", "telnet"]],
        "query_auth_attribute": ["""INSERT INTO AuthAttribute (login, password) VALUES ("{}", "{}");""",
                                 [["login", hash_str("password")]]],
        "query_ref_auth": ["""INSERT INTO RefAuth (AuthAttribute_id_auth_attributes, ConnectType_id_connect_type) 
                                                                                                VALUES ({}, {});""",
                           [[1, 1]]],
        "query_device_type": ["""INSERT INTO DeviceType (device_type) VALUES ("{}");""",
                              ["router", "switch", "wi-fi ap", "pc", "notebook", "smartphone", "raspberrypi"]],
        "query_device": ["""INSERT INTO Device (DeviceType_id_device_type, 
                                                vendor_name,
                                                vendor_model,
                                                mac_address,
                                                ip_address4) 
                                                    VALUES ({}, "{}", "{}", "{}", {});""",
                         [[1, "MikroTik", "hAP lite", "cc2de08b6f41", inet_aton("10.201.0.1")],
                          [4, "MainPC", "MSI Z370", "309c2388b878", inet_aton("10.201.0.13")],
                          [6, "Google", "Pixel 4a", "58242951f51d", inet_aton("10.201.0.26")],
                          [6, "Xiaomi", "Redmi Note 8", "28167fe8f393", inet_aton("10.201.0.12")],
                          [5, "Notebook MSI (wlan)", "GP62 6QF-1295XPL-BB7670H8G1T0SX", "b88198ef5295", inet_aton("10.201.0.11")]]],
        "query_ref_device_auth": ["""INSERT INTO RefDeviceAuth (Device_id_device, RefAuth_id_ref_auth) 
                                                                                                VALUES ({}, {});""",
                                  [[1, 1]]],
        "query_ref_device_location_place": ["""INSERT INTO RefDeviceLocationPlace (Device_id_device, 
                                                                                   LocationPlace_id_location_place) 
                                                                                                VALUES ({}, {});""",
                                            [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [1, 2], [2, 3]]],
        "query_device_connection_status": ["""INSERT INTO DeviceConnectionStatus (Device_id_device, 
                                                                                  LocationPlace_id_location_place) 
                                                                                                VALUES ({}, {});""",
                                           [[1, 1]]],
        "query_owner_status": ["""INSERT INTO OwnerStatus (LocationPlace_id_location_place) VALUES ({});""", [1]]
    }

    if conn is not None:
        for query_message in create_query_message(queries):
            # print("query_message:", query_message)
            query_injection(conn, query_message)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
    conn.close()


if __name__ == '__main__':
    database_name = "smart_house_db.db"
    main(database_name)
