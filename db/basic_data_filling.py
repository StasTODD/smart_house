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
