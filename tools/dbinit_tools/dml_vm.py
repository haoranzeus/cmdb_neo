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


key_list = [
    'name', 'os', 'inner_ip', 'pwd', 'use', 'contact', 'status', 'remarks',
    'wk_no', 'server_type', 'cores', 'ram', 'hdd', 'assigned_date', 'end_date',
    'server_name', 'server_ip_addr']


def get_custom_vms():
    mysql = DbHandler(**mysql_conf)
    select_list = ['`'+item+'`' for item in key_list]
    sql_select_fields = ', '.join(select_list)
    sql_str = 'SELECT {} FROM custom_vm'.format(sql_select_fields)
    res = mysql.do_sql(sql_str)
    return res


def vm_insert(driver):
    vms = get_custom_vms()
    clause = (
        'MATCH (server:SERVER {{name: "{server_name}", '
        'kvm_ip:"{server_ip_addr}"}}) '
        'CREATE p=(vm:VM {{name:"{name}", os:"{os}", inner_ip:"{inner_ip}", '
        'pwd:"{pwd}", use:"{use}", contact:"{contact}", status:"{status}", '
        'remarks:"{remarks}", wk_no:"{wk_no}", server_type:"{server_type}", '
        'cores:{cores}, ram:{ram}, hdd:{hdd}, '
        'assigned_date:"{assigned_date}", end_date:"{end_date}" '
        '}})-[:VM_AT]->(server) '
    )
    for vm in vms:
        vm = list(vm)
        for i in range(0, len(vm)):
            if vm[i] is None:
                vm[i] = 'null'

        vm_dict = dict(zip(key_list, vm))
        vm_clause = clause.format(**vm_dict)
        # print(vm_clause)
        driver.run(vm_clause)


if __name__ == '__main__':
    driver = Neo4jDriver('bolt://localhost:7687', 'neo4j', '123456')
    vm_insert(driver)
    driver.close()
