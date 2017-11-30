#!/usr/bin/env python3
from driver import Neo4jDriver
from mysqlhandle import DbHandler


mysql_conf = {
    'host': 'localhost',
    'port': 3306,
    'table': 'cmdb',
    'user': 'root',
    'password': '123456'
}


def get_custom_servers():
    mysql = DbHandler(**mysql_conf)
    sql_str = (
        'SELECT name, brand, model_number, sn, status, form_factor, '
        'multi_thread, drivers_detail, console_ip, control_type, '
        'affliated_area, os, ipmi_user, ipmi_pwd, kvm_ip, kvm_pwd, position, '
        'raid_cache_s, machine_area, processors, cores, logical_processor, '
        'memory, storage, rackcode, dc_name '
        'FROM custom_server'
    )
    res = mysql.do_sql(sql_str)
    return res


def server_insert(driver):
    servers = get_custom_servers()
    clause = (
        'MATCH (rack:RACK {{rackcode: "{rackcode}"}})-[:RACK_AT]->'
        '(idc:IDC {{name:"{dc_name}"}}) '
        'CREATE p=(server:SERVER {{name:"{name}", brand:"{brand}", '
        'model_number:"{model_number}", sn:"{sn}", status:"{status}", '
        'form_factor:"{form_factor}", multi_thread:"{multi_thread}", '
        'drivers_detail:"{drivers_detail}", console_ip:"{console_ip}", '
        'control_type:"{control_type}", affliated_area:"{affliated_area}", '
        'os:"{os}", ipmi_user:"{ipmi_user}", ipmi_pwd:"{ipmi_pwd}", '
        'kvm_ip:"{kvm_ip}", kvm_pwd:"{kvm_pwd}", position:"{position}", '
        'raid_cache_s:"{raid_cache_s}", machine_area:"{machine_area}", '
        'processors: {processors}, cores: {cores}, '
        'logical_processor: {logical_processor}, memory: {memory}, '
        'storage: {storage} '
        '}})-[:SERVER_AT]->(rack) '
    )
    for server in servers:
        key_list = [
            'name', 'brand', 'model_number', 'sn', 'status', 'form_factor',
            'multi_thread', 'drivers_detail', 'console_ip', 'control_type',
            'affliated_area', 'os', 'ipmi_user', 'ipmi_pwd', 'kvm_ip',
            'kvm_pwd', 'position', 'raid_cache_s', 'machine_area',
            'processors', 'cores', 'logical_processor', 'memory', 'storage',
            'rackcode', 'dc_name']
        server = list(server)
        for i in range(0, len(server)):
            if server[i] is None:
                server[i] = "null"
        server_dict = dict(zip(key_list, server))
        server_clause = clause.format(**server_dict)
        driver.run(server_clause)


if __name__ == '__main__':
    driver = Neo4jDriver('bolt://localhost:7687', 'neo4j', '123456')
    server_insert(driver)
    driver.close()
