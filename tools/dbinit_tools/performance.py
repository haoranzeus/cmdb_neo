#!/usr/bin/env python3
from datetime import datetime

from driver import Neo4jDriver
from mysqlhandle import DbHandler


def get_all_vm_server_rack_idc(driver):
    begin = datetime.now()
    clause = (
        'MATCH (vm:VM)-[v:VM_AT]->(server:SERVER)-[s:SERVER_AT]->'
        '(rack:RACK)-[r:RACK_AT]->(idc:IDC) RETURN vm, server, rack, idc')
    res = driver.run(clause)
    r = open('/home/zhr/tmp/test1.json', 'w')
    r.write(str(res.data()))
    r.close()
    end = datetime.now()
    return end - begin


if __name__ == '__main__':
    driver = Neo4jDriver('bolt://localhost:7687', 'neo4j', '123456')
    time1 = get_all_vm_server_rack_idc(driver)
    print("get all vm, server, rack, idc: ", time1)
    driver.close()
