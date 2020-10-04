from librouteros import connect, exceptions
from typing import List, Dict, Union
from os import path


def dhcp_server_lease_parser(command_result: List[Dict[str, str]]) -> List[Dict[str, Union[str, int]]]:
    """
    Parse '/ip/dhcp-server/lease/print' command response to structure convenient for DB.

    :param command_result: [{'.id': '*49',
                              'address': '10.201.0.10',
                              'address-lists': '',
                              'blocked': False,
                              'client-id': '1:52:12:54:35:25:21',
                              'comment': 'StasTODD Nokia 6.1 plus wifi',
                              'dhcp-option': '',
                              'disabled': False,
                              'dynamic': False,
                              'last-seen': '5h6m1s',
                              'mac-address': '52:12:54:35:25:21',
                              'radius': False,
                              'server': 'defconf',
                              'status': 'waiting'},
                              {...}]
    :return: [{'client_ip': '10.201.0.10',
              'client_mac': '52:12:54:35:25:21',
              'client_status': 0},
              ...]
    """
    result = []
    for one_res in command_result:
        one_res_data = {}
        client_status = one_res.get("status")
        # https://wiki.mikrotik.com/wiki/Manual:IP/DHCP_Server#General
        if client_status in ["waiting", "testing", "authorizing", "busy", "offered"]:
            one_res_data["client_status"] = 0
        else:
            one_res_data["client_status"] = 1
        one_res_data["client_ip"] = one_res.get("address")
        one_res_data["client_mac"] = one_res.get("mac-address")
        result.append(one_res_data)

    return result


def main():
    mikrotik_command = "/ip/dhcp-server/lease/print"

    # TODO: add Mikrotik auth data from other source:
    username = "username"
    password = "password"
    host = "127.0.0.1"

    try:
        api = connect(username=username, password=password, host=host)
    except OSError as er:
        print(f"Wrong connection to Mikrotik {host} host:", er)
        print(f"Auth data set in file: {path.dirname(path.abspath(__file__))}")
        return
    except exceptions.TrapError as er:
        print(f"Wrong connection to Mikrotik {host} host:", er)
        print(f"Auth data set in file: {path.dirname(path.abspath(__file__))}")
        return
    dhcp_lease_data = [one_res for one_res in api(cmd=mikrotik_command)]

    return dhcp_server_lease_parser(dhcp_lease_data)


if __name__ == '__main__':
    main()
