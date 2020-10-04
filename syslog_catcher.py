#!/home/stastodd/projects/smart_house/venv/bin/python3.8

"""
This program is a complex methods for to trace owner status in smart house or other following place.
How does it work? For example, some short steps from program algorithm:
1) Started custom port (5555) listening.
2) Prepared home Mikrotik Wi-Fi router is send on this custom port (using router syslog server program)
dhcp-lease information about client activity.
3) syslog_server will catch and pars this information.
4) DB has manually prepared data with owner information in query line (see db/base_data_filling.py)
5) dhcp-lease info is inject to DB
6) DB write/update triggers works and write 'at_home' field in 'OwnerStatus' table. Some place or object owner
was marked self-status. Able to use this field in other projects.
"""

import socketserver
from os.path import isfile
from typing import List, Dict, Union, Any

from lib.help_functions import syslog_message_parser, query_set_connection_status, query_mac_all_devices
import lib.device_network_status as syslog_server_request
from db import create_db, basic_data_filling


database_name = "db/smart_house_db.db"


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        # socket = self.request[1]
        syslog_server = self.client_address[0]
        syslog_message = syslog_message_parser(data)
        db_updater(syslog_message, syslog_server=syslog_server)


def db_updater(syslog_message: Dict[str, Union[str, int]], syslog_server: Union[str, None] = None):
    """
    Change data in DB smart_house_db.db.

    :param syslog_server: None|'10.201.0.1'
    :param syslog_message: {'client_ip': '10.201.0.10', 'cleint_mac': '52:12:54:35:25:21', 'client_status': '1'}
    """
    conn = create_db.create_connection(database_name)
    client_ip = syslog_message.get("client_ip")
    cleint_mac = syslog_message.get("cleint_mac")
    client_status = syslog_message.get("client_status")

    if syslog_server:
        # Set dhcp-server status - active:
        query_set_connection_status(conn, syslog_server, 1)
    # Set connected device status - active:
    query_set_connection_status(conn, client_ip, int(client_status))

    conn.close()


def check_db_status():
    """
    Before start syslog_catcher program will check some parameters of DB smart_house:
    - DB presence check. If file is missing, will create it and fill basic information.
    - Connecting to the Mikrotik router and get dhcp-lease status.
    - Injecting reformatted data from Mikrotik router to DB.
    """
    # DB presence check. If file is missing, will create it:
    if not isfile(database_name):
        create_db.main(database_name)
        basic_data_filling.main(database_name)
    # Connecting to the Mikrotik router and get dhcp-lease status:
    syslog_server_data = syslog_server_request.main()
    if not syslog_server_data:
        print("Additional DB update is skipping. Mikrotik API is unreachable")
        return
    conn = create_db.create_connection(database_name)
    db_data = query_mac_all_devices(conn)
    # From List[Tuple[str]] to List[str] conversion:
    db_data = [''.join(list(one_mac)) for one_mac in db_data]
    # List rebuilding with including filter. If MAC-address from Mikrotik match with MAC-address from DB:
    syslog_server_data = [one_dict for one_dict in syslog_server_data if one_dict.get("client_mac").lower().replace(":", "") in db_data]

    for one_data in syslog_server_data:
        db_updater(one_data)
    print("Additional DB data update is completed successfully")


def main():
    check_db_status()
    HOST, PORT = "0.0.0.0", 5555
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")


if __name__ == "__main__":
    main()
