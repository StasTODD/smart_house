import sqlite3
from sqlite3 import Error
from typing import List, Dict, Union, Any


def create_connection(db_file: str) -> Union[type(sqlite3.connect), None]:
    """
    Create a database connection to the SQLite database specified by db_file

    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return


def create_table(conn: type(sqlite3.connect), create_table_sql: str):
    """
    Create a table from the create_table_sql statement

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    """

    try:
        c = conn.cursor()
        c.executescript(create_table_sql)
    except Error as e:
        print(e)


def main():
    database_name = "smart_house_db.db"
    sql_project = """
    PRAGMA foreign_keys = OFF;
    CREATE TABLE "City"(
    --   Table must contains the list of cities name
      "id_city" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "city" VARCHAR(255) NOT NULL
    );
    CREATE TABLE "AuthAttribute"(
      "id_auth_attributes" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "login" VARCHAR(255),
      "password" VARCHAR(255)
    );
    CREATE TABLE "ConnectType"(
      "id_connect_type" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "connect_type" VARCHAR(45) NOT NULL
    );
    CREATE TABLE "RefAuth"(
      "id_ref_auth" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "AuthAttribute_id_auth_attributes" INTEGER NOT NULL,
      "ConnectType_id_connect_type" INTEGER NOT NULL,
      CONSTRAINT "fk_Ref_auth_AuthAttribute1"
        FOREIGN KEY("AuthAttribute_id_auth_attributes")
        REFERENCES "AuthAttribute"("id_auth_attributes"),
      CONSTRAINT "fk_Ref_auth_ConnectType1"
        FOREIGN KEY("ConnectType_id_connect_type")
        REFERENCES "ConnectType"("id_connect_type")
    );
    CREATE INDEX "RefAuth.fk_Ref_auth_AuthAttribute1_idx" ON "RefAuth" ("AuthAttribute_id_auth_attributes");
    CREATE INDEX "RefAuth.fk_Ref_auth_ConnectType1_idx" ON "RefAuth" ("ConnectType_id_connect_type");
    CREATE TABLE "RefDeviceLocationPlace"(
      "id_ref_device_location_place" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "Device_id_device" INTEGER NOT NULL,
      "LocationPlace_id_location_place" INTEGER NOT NULL
    );
    CREATE TABLE "OwnerStatus"(
      "id_owner_status" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "LocationPlace_id_location_place" INTEGER NOT NULL,
      "at_home" INTEGER DEFAULT 0
    );
    CREATE TABLE "Place"(
    --   Table must contains the list of places
      "id_place" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "place" VARCHAR(255) NOT NULL
    );
    CREATE TABLE "Address"(
    --   Table must contains the list of addresses
      "id_address" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "address" VARCHAR(255) NOT NULL
    );
    CREATE TABLE "DeviceType"(
      "id_device_type" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "device_type" VARCHAR(100) NOT NULL
    );
    CREATE TABLE "RefDeviceAuth"(
      "id_ref_device_auth" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "Device_id_device" INTEGER NOT NULL,
      "RefAuth_id_ref_auth" INTEGER NOT NULL
    );
    CREATE TABLE "LocationPlace"(
      "id_location_place" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "City_id_city" INTEGER NOT NULL,
      "Address_id_address" INTEGER NOT NULL,
      "Place_id_place" INTEGER,
      CONSTRAINT "fk_Location_City"
        FOREIGN KEY("City_id_city")
        REFERENCES "City"("id_city"),
      CONSTRAINT "fk_Location_Address1"
        FOREIGN KEY("Address_id_address")
        REFERENCES "Address"("id_address")
    );
    CREATE INDEX "LocationPlace.fk_Location_City_idx" ON "LocationPlace" ("City_id_city");
    CREATE INDEX "LocationPlace.fk_Location_Address1_idx" ON "LocationPlace" ("Address_id_address");
    CREATE TABLE "Device"(
      "id_device" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "DeviceType_id_device_type" INTEGER NOT NULL,
      "LocationPlace_id_location_place" INTEGER,
      "vendor_name" VARCHAR(100),
      "vendor_model" VARCHAR(100),
      "mac_address" VARCHAR(12),
      "ip_address4" INTEGER,
      "ip_address6" BINARY(16),
      CONSTRAINT "fk_Device_DeviceType1"
        FOREIGN KEY("DeviceType_id_device_type")
        REFERENCES "DeviceType"("id_device_type")
    );
    CREATE INDEX "Device.fk_Device_DeviceType1_idx" ON "Device" ("DeviceType_id_device_type");
    CREATE TABLE "DeviceConnectionStatus"(
      "id_device_connection_status" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      "Device_id_device" INTEGER NOT NULL,
      "LocationPlace_id_location_place" INTEGER,
      "online" INTEGER DEFAULT 0,
      CONSTRAINT "fk_DeviceConnectionStatus_Device1"
        FOREIGN KEY("Device_id_device")
        REFERENCES "Device"("id_device")
    );
    CREATE INDEX "DeviceConnectionStatus.fk_DeviceConnectionStatus_Device1_idx" ON "DeviceConnectionStatus" ("Device_id_device");
    """
    conn = create_connection(database_name)
    if conn is not None:
        create_table(conn, sql_project)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
    conn.close()


if __name__ == '__main__':
    main()
