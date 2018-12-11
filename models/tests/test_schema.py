from nose.tools import assert_equal

from models import schema


class TestIdcSchema:
    def test_idc_schema(self):
        condition_dict = {
            'name': '红山机房2',
            'address': '地址测试'
        }
        data, errors = schema.IdcSchema().load(condition_dict)
        assert_equal(condition_dict, data)
        assert_equal({}, errors)
        condition_dict = {
            'address': '地址测试'
        }
        data, errors = schema.IdcSchema().load(condition_dict)
        assert_equal(condition_dict, data)
        assert_equal({'name': ['Missing data for required field.']}, errors)
