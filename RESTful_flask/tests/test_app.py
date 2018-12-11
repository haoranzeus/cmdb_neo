import json
from flask import request
from nose.tools import assert_equal

from RESTful_flask.app import app


class TestHello:
    def setup(self):
        app.testing = True
        self.app = app.test_client()

    def test_get(self):
        with app.test_request_context(
                'hello/zhr/', method='POST', content_type='application/json',
                data=json.dumps({'a': 1})):
            assert_equal({'a': 1}, request.json)
            assert_equal('/hello/zhr/', request.path)
            assert_equal('application/json', request.content_type)
        res = self.app.get('/hello/zhr/')
        assert_equal(json.loads(res.data.decode()), 'hello zhr')
        assert_equal(res.content_type, 'application/json')


class TestRaiseTest:
    def setup(self):
        app.testing = True
        self.app = app.test_client()

    def test_get(self):
        result = {
                "status": "SUCCESS",
                "result": {
                    "msg": "exception test",
                    "code": "230202"
                    }
                }
        res = self.app.get('/raise_test/')
        assert_equal(json.loads(res.data.decode()), result)
        assert_equal(res.content_type, 'application/json')


class TestDoMatch:
    def setup(self):
        app.testing = True
        self.app = app.test_client()

    def test_do_match(self):
        cypher_str = 'MATCH (idc:IDC)<-[:RACK_AT]-(rack:RACK) RETURN idc, rack'
        condition_dict = {
            'cypher_str': cypher_str
        }
        res = self.app.post(
                '/neo4j/do_match/', data=json.dumps(condition_dict),
                content_type='application/json')
        print(res)


class TestAddNode:
    def setup(self):
        app.testing = True
        self.app = app.test_client()

    def teardown(self):
        del_dict = {
            'property_name': 'name',
            'values': ['红山机房2', '红山机房3']
        }
        res = self.app.post(
                '/neo4j/IDC/nodes_del/', data=json.dumps(del_dict),
                content_type='application/json')

    def test_add(self):
        nodes_list = [
            {
                'name': '红山机房2',
                'address': '地址测试'
            },
            {
                'name': '红山机房3',
                'address': '另一个地址测试'
            }
        ]
        res = self.app.post(
                '/neo4j/IDC/nodes_add', data=json.dumps(nodes_list),
                content_type='application/json')
        assert_equal(res.status, '200 OK')
