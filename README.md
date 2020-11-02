<h1 align="center">Smart house database</h1>

Private, little database for smart house. General idea is work with events log and scheduling events. Project including syslog catcher who got, parse and write information to DB tables.

## Functional:

✔️SQLite database that describe a places (location, devices, auth data and references of objects params).

✔️Syslog server for events catching.

✔️SQLite table `OwnerStatus` with place owner status.

### How works owner detecting?

This program is a complex methods for to trace owner status in smart house or other following place.
For example, some short steps from program algorithm:

1. Started syslog custom port (5555) listening.
2. Prepared home Mikrotik Wi-Fi router is send on this custom port (using router syslog server program)
dhcp-lease information about client activity.
3. `syslog_server.py` is catching and parsing this information.
4. DB is manually prepared data with owner information in query line (see `db/base_data_filling.py`) 
5. DB write/update triggers works and write `at_home` field in `OwnerStatus` table. Some place or object owner was marked self-status.

#### Mikrotik cooking:

```
/ip dhcp-server
add address-pool=default-dhcp disabled=no interface=bridge lease-script=myLeaseScript lease-time=3m name=defconf
/system logging action
add name=remotetopythonsyslog remote=10.201.0.10 remote-port=5555 syslog-severity=warning target=remote
/ip dhcp-server lease
# static dhcp-raws
/system script
add dont-require-permissions=no name=myLeaseScript owner=stastodd policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="# Show dhcp-lease items status:\
    \n#/ip dhcp-server lease \
    \n#:foreach i in=[find] do={:put ([get \$i address].\",\".[get \$i mac-address].\",\".[get \$i status])}\
    \n\
    \n# Send to log short dhcp lease status:\
    \n:log info (\"\$leaseActIP|\$leaseActMAC|\$leaseBound\")\
    \n\
    \n# Send to log short dhcp lease status with 'else' construction\
    \n#:if (\$leaseBound = \"1\") do={:log info (\"bound|\$leaseActIP|\$leaseActMAC\")} else={:log info (\"unbound|\$leaseActIP|\$leaseActMAC\")}"
/system logging
add action=remotetopythonsyslog topics=script
``` 

### Syslog catcher algorithm:

![](structure_of_part_scheme_of_smart_house.png?style=centerme "syslog_server.py algorithm")

### Graphic schema of DB:

![](db/smart_house_db_model_v1.png?style=centerme "Graphic schema of DB")