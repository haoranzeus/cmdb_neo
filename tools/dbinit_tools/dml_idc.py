#!/usr/bin/env python3
import neo4j
from driver import Neo4jDriver


def idc_insert(driver):
    """
    插入两个机房
    """
    clause = (
        'CREATE (hs:IDC {{name: "{name}", address: "{address}", '
        'status: "{status}", telephone: "{telephone}", contact: "{contact}", '
        'floor: "{floor}", province: "{province}", city: "{city}", '
        'district: "{region}", stars: {stars}}}) '
    )
    hs_dict = {
        'name': '红山机房',
        'address': '红山大道与团结路交叉口团结路1号萧山电信机房',
        'status': '正常',
        'telephone': '13456875273',
        'contact': '卓弘亮',
        'floor': '1,2',
        'province': '浙江省',
        'city': '杭州市',
        'district': '萧山区',
        'stars': 5
    }
    sq_dict = {
        'name': '石桥机房',
        'address': '石桥枢纽楼浙江移动IDC机房（华西路330号）',
        'status': '正常',
        'telephone': '13777861607',
        'contact': '包淑丽',
        'floor': '5',
        'province': '浙江省',
        'city': '杭州市',
        'district': '下城区',
        'stars': 5
    }
    cd_dict = {
        'name': '成都机房',
        'address': '石桥枢纽楼浙江移动IDC机房（华西路330号）',
        'status': '正常',
        'telephone': '18867105013',
        'contact': '谯宇',
        'floor': '3,2',
        'province': '四川省',
        'city': '成都市',
        'district': '金牛区',
        'stars': 5
    }
    hs_clause = clause.format(**hs_dict)
    try:
        driver.run(hs_clause)
    except neo4j.exceptions.ConstraintError:
        pass
    sq_clause = clause.format(**sq_dict)
    try:
        driver.run(sq_clause)
    except neo4j.exceptions.ConstraintError:
        pass
    cd_clause = clause.format(**cd_dict)
    try:
        driver.run(cd_clause)
    except neo4j.exceptions.ConstraintError:
        pass


if __name__ == '__main__':
    driver = Neo4jDriver('bolt://localhost:7687', 'neo4j', '123456')
    idc_insert(driver)
