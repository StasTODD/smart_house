import socketserver
from datetime import datetime
import time
from os.path import isfile
from typing import List, Dict, Union, Any

from lib.help_functions import syslog_message_parser, query_set_connection_status
from db import create_db, basic_data_filling


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        # socket = self.request[1]

        syslog_server = self.client_address[0]
        syslog_message = syslog_message_parser(data)
        db_updater(syslog_server, syslog_message)


def db_updater(syslog_server: str, syslog_message: Dict[str, str]):
    """
    Change data in DB smart_house_db.db.

    :param syslog_server: '10.201.0.1'
    :param syslog_message: {'client_ip': '10.201.0.10', 'cleint_mac': '52:12:54:35:25:21', 'client_status': '1'}
    :return:
    """
    database_name = "db/smart_house_db.db"
    if isfile(database_name):
        conn = create_db.create_connection(database_name)
    else:
        create_db.main(database_name)
        basic_data_filling.main(database_name)
        conn = create_db.create_connection(database_name)

    client_ip = syslog_message.get("client_ip")
    cleint_mac = syslog_message.get("cleint_mac")
    client_status = syslog_message.get("client_status")

    # Set dhcp-server status - active:
    query_set_connection_status(conn, syslog_server, 1)
    # Set connected device status - active:
    query_set_connection_status(conn, client_ip, int(client_status))

    conn.close()


def main():
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
