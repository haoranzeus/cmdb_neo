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


def get_racks():
    mysql = DbHandler(**mysql_conf)
    sql_str = (
        'SELECT fs_1, fs_2, fs_3, fs_4 '
        'FROM ci_items WHERE ci_id=34 ')
    res = mysql.do_sql(sql_str)
    return res


def rack_insert(driver):
    racks = get_racks()
    clause = (
        'MATCH (i:IDC) WHERE i.name="{idc_name}" '
        'CREATE p=(rack:RACK {{rackcode: "{rackcode}" , floor: "{floor}", '
        'room: "{room}"}})-[:RACK_AT]->(i) '
    )
    for rack in racks:
        rack_dict = {
            'rackcode': rack[0],
            'floor': rack[1],
            'room': rack[2],
            'idc_name': rack[3]
        }
        rack_clause = clause.format(**rack_dict)
        driver.run(rack_clause)


if __name__ == '__main__':
    driver = Neo4jDriver('bolt://localhost:7687', 'neo4j', '123456')
    rack_insert(driver)
