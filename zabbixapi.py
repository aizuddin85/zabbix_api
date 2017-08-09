#!/usr/bin/python
"""
Author: Muhammad Aizuddin Zali <aizuddin.zali@gmail.com>
Date: 8th Aug 2017
A high level python wrapper to do single or bulk addition into Zabbix using pyzabbix module.
Original Zabbix API Documentation: https://www.zabbix.com/documentation/3.0/manual/api
"""
import sys
import os
import logging
import urllib3

"""
Now try to import pyzabbix library. The main library to talks to Zabbix jsonrpc.
"""
try:
    from pyzabbix import ZabbixAPI, ZabbixAPIException
except:
    print("Please install pyzabbix library from https://github.com/lukecyca/pyzabbix.git!")
    raise ImportError
"""
Globally suppress noisy urllib3 warning due to self-signed HTTPS on Zabbix server.
"""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
"""
If DEBUG environment set, make the script verbosely write the stdout.
"""
try:
    if os.environ['ZABBIX_DEBUG']:
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(logging.DEBUG)
        log = logging.getLogger('pyzabbix')
        log.addHandler(stream)
        log.setLevel(logging.DEBUG)
except:
    pass


class ZabApi:
    def __init__(self, username, userpass, zabbix_host):
        """
        Instantiation of the connection and login attempt.
        """
        print("Attempting to connect to {0}...".format(zabbix_host))
        try:
            global zapi
            zapi = ZabbixAPI(zabbix_host)
            zapi.session.verify = False
            zapi.login(username, userpass)
        except ZabbixAPIException as err:
            print("Unable to connect!")
            raise err

    def get_host_id(self, host_name):
        """
        :param host_name:
        :return:  host id in zabbix
        """
        try:
            host_info = zapi.host.get(filter={'host': host_name})
            host_id = host_info[0]['hostid']
            return host_id
        except ZabbixAPIException as err:
            raise err

    def get_template_id(self, template_name):
        """
        :param template_name:
        :return: template id in zabbix
        """
        try:
            template_info = zapi.template.get(filter={'host': template_name})
            template_id = template_info[0]['templateid']
            return template_id
        except ZabbixAPIException as err:
            raise err

    def get_hostgroup_id(self, group_name):
        """
        :param group_name:
        :return: group id in zabbix
        """
        try:
            group_info = zapi.hostgroup.get(filter={'name': group_name})
            group_id = group_info[0]['groupid']
            return group_id
        except ZabbixAPIException as err:
            raise err

    def create_host(self, host_name, interface_json_list, group_json_list, template_json_list, host_ip):
        """
        :param host_name:
        :param interface_json_list:
        :param group_json_list:
        :param template_json_list:
        :param host_ip:
        :return: created object
        """
        if not isinstance(template_json_list, list):
            raise TypeError
        elif not isinstance(group_json_list, list):
            raise TypeError
        elif not isinstance(interface_json_list, list):
            raise TypeError
        try:
            item = zapi.host.create({'host': host_name,
                                     'interfaces': interface_json_list,
                                     'groups': group_json_list,
                                     'templates': template_json_list})
                return item
        except ZabbixAPIException as err:
            """
            Continue with error.
            """
            print err
            pass
