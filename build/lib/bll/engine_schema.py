# coding=utf-8
"""
synopsis: 用于验证engine.py中的方法的参数
author: zhanghaoran@cmhi.chinamobil.com
"""
from marshmallow import Schema, fields


class DelNodeSchema(Schema):
    """
    Schema of del_nodes
    """
    property_name = fields.Str(required=True)
    values = fields.List(fields.Field, srequired=True)  # 由于list中可能是不同的类型，就不检测了


class UpdateNodeSchema(Schema):
    """
    Schema of update_nodes
    """
    match_kv = fields.Dict(required=True)
    set_kv = fields.Dict(required=True)
