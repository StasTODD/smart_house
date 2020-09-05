import sqlite3
from typing import List, Dict, Union, Any

from create_db import create_connection

# TODO: add typing to all objects


def create_query_message(queries):
    for query_name, query_info in queries.items():
        query_message = query_info[0]
        query_data = query_info[1]
        if isinstance(query_data, str):
            query_message = query_message.format(query_data)
            yield query_message
        elif isinstance(query_data, list):
            for one_query_data in query_data:
                yield query_message.format(one_query_data)


def query_injection(conn, query_message):
    cur = conn.cursor()
    cur.execute(query_message)
    return cur.lastrowid


def main():
    database_name = "smart_house_db.db"

    # TODO: add more info to table
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
                          [6, "Nokia", "6.1 Plus", "521254352521", inet_aton("10.201.0.10")]]],
        "query_ref_device_auth": ["""INSERT INTO RefDeviceAuth (Device_id_device, RefAuth_id_ref_auth) 
                                                                                                VALUES ({}, {});""",
                                  [[1, 1]]],
        "query_ref_device_location_place": ["""INSERT INTO RefDeviceLocationPlace (Device_id_device, 
                                                                                   LocationPlace_id_location_place) 
                                                                                                VALUES ({}, {});""",
                                            [[1, 1], [2, 1], [3, 1], [1, 2], [2, 3]]],
        "query_device_connection_status": ["""INSERT INTO DeviceConnectionStatus (Device_id_device, 
                                                                                  LocationPlace_id_location_place) 
                                                                                                VALUES ({}, {});""",
                                           [[1, 1]]]
    }

    conn = create_connection(database_name)
    if conn is not None:
        for query_message in create_query_message(queries):
            query_injection(conn, query_message)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
    conn.close()


if __name__ == '__main__':
    main()
