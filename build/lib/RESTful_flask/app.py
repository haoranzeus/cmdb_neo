import logging
import functools
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

from bll.engine import Engine
from bll.exceptions import InsertParameterError

app = Flask(__name__)
# print(__name__)
api = Api(app)

engine = Engine('bolt://localhost:7687', 'neo4j', '123456')
_log = logging.getLogger(__name__)


def handle_exception(cls):
    def try_orgi_func(func, result, se, *args, **kwargs):
        try:
            res = func(se, *args, **kwargs)
        except InsertParameterError as e:
            result['result']['code'] = e.code
            result['result']['msg'] = e.message
            return result
        else:
            if res is not None:
                result['result'] = res
            result['status'] = 'SUCCESS'
            _log.debug('result = %s', result)
            return result

    if hasattr(cls, 'get'):
        orig_get = cls.get

        def new_get(self, *args, **kwargs):
            result = {'status': 'SUCCESS', "result": {}}
            return try_orgi_func(orig_get, result, self, *args, **kwargs)
        cls.get = new_get

    if hasattr(cls, 'post'):
        orig_post = cls.post

        def new_post(self, *args, **kwargs):
            result = {'status': 'SUCCESS', "result": {}}
            return try_orgi_func(orig_post, result, self, *args, **kwargs)
        cls.post = new_post
    return cls


class Hello(Resource):
    def get(self, name):
        return engine.hello(name)

    def post(self, name):
        print(request.json)
        return "hello world"


@handle_exception
class RaiseTest(Resource):
    def get(self):
        return engine.raise_test()

    def post(self):
        return engine.raise_test()


@handle_exception
class DoMatch(Resource):
    def post(self, node):
        return engine.do_match(node, request.json)


@handle_exception
class AddNodes(Resource):
    def post(self, node):
        return engine.add_nodes(node, request.json)


@handle_exception
class DelNodes(Resource):
    def post(self, node):
        return engine.del_nodes(node, request.json)


api.add_resource(Hello, '/hello/<string:name>/')
api.add_resource(RaiseTest, '/raise_test', '/raise_test/')
api.add_resource(DoMatch, '/neo4j/do_match', '/neo4j/do_match/')
api.add_resource(AddNodes, '/neo4j/<string:node>/nodes_add',
                 '/neo4j/<string:node>/nodes_add/')
api.add_resource(DelNodes, '/neo4j/<string:node>/nodes_del',
                 '/neo4j/<string:node>/nodes_del/')
