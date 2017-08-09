# zabbix_api
Zabbix high level API script.

## Example:  
```
import zabbixapi
from pyzabbix import ZabbixAPIException

host_name = "zabbix_client"
host_ip = "192.168.0.100"
group_name = "Linux servers"
template_name = "Template OS Linux"

zabapi = zabbixapi.ZabApi('zabbixuser', 'zabbixpass', 'https://zabbix.example.com')

group_id = zabapi.get_hostgroup_id(group_name)
template_id = zabapi.get_template_id(template_name)
template_json = [{'templateid': template_id}]
group_json = [{'groupid': group_id}]
interface_json = [{'type': 1, 'main': 1, 'useip': 1, 'port': '10050', 'dns': host_name, 'ip': host_ip}]

try:
    zabapi.create_host(host_name, interface_json, group_json, template_json, host_ip)
except ZabbixAPIException as err:
    raise err
```
