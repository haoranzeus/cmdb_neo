from marshmallow import Schema, fields


class IdcSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str()
    province = fields.Str()
    city = fields.Str()
    district = fields.Str()
    floor = fields.Str()
    contact = fields.Str()
    telephone = fields.Str()
    stars = fields.Integer()
    status = fields.Str()


SCHEMA_DICT = {
    'IDC': IdcSchema,       # 机房
}
