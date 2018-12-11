#!/usr/bin/env python3


class IDC:
    def __init__(
            self, name, address, province, city, district, floor, contact,
            telephone, stars, status):
        """
        paras:
            name - 机房名
            address - 机房地址
            provice - 省
            city - 市
            district - 区
            floor - 楼层
            contact - 联系人
            telephone - 联系电话
            stars - 星级
            status - 状态
        """
        self.name = name
        self.address = address
        self.province = province
        self.city = city
        self.district = district
        self.floor = floor
        self.contact = contact
        self.telephone = telephone
        self.stars = stars
        self.status = status
