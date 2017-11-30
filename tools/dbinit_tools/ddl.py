#!/usr/bin/env python3
from driver import Neo4jDriver


def idc(driver):
    clause = 'CREATE CONSTRAINT ON (idc:IDC) ASSERT idc.name IS UNIQUE'
    driver.run(clause)


def rack(driver):
    # clause = (
    #     'CREATE CONSTRAINT ON (rack:RACK) '
    #     'ASSERT rack.idcname_rackcode IS UNIQUE'
    # )
    # driver.run(clause)
    pass
    # 不要加限制了，通过与机房的链接以及本身的机柜号过滤


def vm(driver):
    clause = 'CREATE CONSTRAINT ON (vm:VM) ASSERT vm.name IS UNIQUE'
    driver.run(clause)


if __name__ == '__main__':
    driver = Neo4jDriver('bolt://localhost:7687', 'neo4j', '123456')
    idc(driver)
    rack(driver)
    vm(driver)
    driver.close()
