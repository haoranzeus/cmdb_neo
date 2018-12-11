from bll import result_schema
from bll import engine_schema

from models import model
from models import schema
from utils.neo4jtool import Neo4jStrTool
from utils.neo4jtool import Neo4jTool
from bll.exceptions import QueryParameterError
from bll.exceptions import InsertParameterError
from bll.exceptions import UpdateParameterError
from bll.exceptions import DeleteParameterError


class Engine:
    def __init__(self, neo_uri, neo_user, neo_password):
        self.neo_uri = neo_uri
        self.neo_user = neo_user
        self.neo_password = neo_password

    def _do_cypher(self, cypher_str):
        """
        执行一条cypher语句，返回结果
        """
        with Neo4jTool(self.neo_uri, self.neo_user, self.neo_password) as neo:
            result = neo.run(cypher_str)
        return result

    def _check_node(self, schema, condition_dict, exception):
        """
        检测一个condition_dict参数合法性
        paras:
            schema - 用于检测参数合法性的schema
            condition_dict - 参数字典
            exception - 要raise的异常
        """
        data, errors = schema().load(condition_dict)
        if errors != {}:
            raise exception(str(errors))
        else:
            return data

    def hello(self, name='stranger'):
        return 'hello {}'.format(name)

    def raise_test(self):
        raise InsertParameterError('exception test')

    def add_idc(self, condition_dict):
        """
        添加一个idc
        """
        data, errors = schema.IdcSchema().load(condition_dict)
        if errors != {}:
            raise InsertParameterError(str(errors))
        cy_node_str = Neo4jStrTool.node_str(label='IDC')
        cy_str = 'CREATE ' + cy_node_str
        self._do_cypher(cy_str)
        return result_schema.result_model(
                code=result_schema.CODE_SUCCESS_GET, msg='插入成功')

    def _traverse_match_data(self, data):
        """
        遍历一个match的结果，以行的列表形式返回
        """
        data_line = []
        for item in data:
            dict_line = {}
            for item_k, item_v in item.items():
                item_dict = dict(item_v)
                item_dict = {
                        '{}.{}'.format(item_k, k): v
                        for k, v in item_dict.items()}
                dict_line = dict(dict_line, **item_dict)
            data_line.append(dict_line)
        return data_line

    def do_match(self, condition_dict):
        """
        执行一条MATCH查询
        condition_dict = {
            'cypher_str': 'MATCH xxxx'
        }
        """
        cy_str_tmp = condition_dict['cypher_str']
        cy_str_tmp = cy_str_tmp.lstrip('MATCH').lstrip('match')
        cy_str = 'MATCH ' + cy_str_tmp
        res = self._do_cypher(cy_str)
        res_data = res.data()
        res_line = self._traverse_match_data(res_data)
        return result_schema.result_model(
                code=result_schema.CODE_SUCCESS_GET, msg='获取成功', data=res_line)

    def add_nodes(self, label, condition_list):
        if label not in schema.SCHEMA_DICT.keys():
            raise InsertParameterError('{} not a valid node'.format(label))

        node_str_list = []
        for condition_dict in condition_list:
            condition_dict = self._check_node(
                    schema.SCHEMA_DICT[label], condition_dict,
                    InsertParameterError)
            cy_node_str = Neo4jStrTool.node_str(
                    label=label, properties=condition_dict)
            node_str_list.append(cy_node_str)

        cy_str = 'CREATE ' + ', '.join(node_str_list)
        self._do_cypher(cy_str)
        return result_schema.result_model(
                code=result_schema.CODE_SUCCESS_ADD, msg='插入成功')

    def del_nodes(self, label, condition_dict):
        """
        删除node
        condition_dict = {
            'property_name': 'name',
            'values': ['v1', 'v2']
        }
        """
        if label not in schema.SCHEMA_DICT.keys():
            raise DeleteParameterError('{} not a valid node'.format(label))
        data, errors = engine_schema.DelNodeSchema().load(condition_dict)
        if errors != {}:
            raise DeleteParameterError(str(errors))
        property_name = condition_dict['property_name']
        values = condition_dict['values']
        cy_str = (
            'MATCH (node:{label}) WHERE node.{property_name} in '
            '{values} DELETE node '
        ).format(label=label, property_name=property_name, values=str(values))
        self._do_cypher(cy_str)

        return result_schema.result_model(
                code=result_schema.CODE_SUCCESS_DELETE, msg='删除成功')

    def update_nodes(self, label, condition_list):
        """
        修改nodes
        condition_list = [
            {
                'match_kv': {
                    'mk1': 'mv1',
                    'mk2': 'mv2'
                },
                'set_kv': {
                    'sk1': 'sv1',
                    'sk2': 'sv2
                }
            },
            ...
        ]
        """
        if label not in schema.SCHEMA_DICT.keys():
            raise UpdateParameterError('{} not a valid node'.format(label))

        for condition_dict in condition_list:
            # 参数形式检测
            data = self._check_node(
                    engine_schema.UpdateNodeSchema, condition_dict,
                    UpdateParameterError)
            self._check_node(
                    schema.SCHEMA_DICT[label], data['match_kv'],
                    UpdateParameterError)
            # 执行更新
            cy_node_str = Neo4jStrTool.node_str(
                    label='IDC', properties=data['match_kv'], name='n')
            cy_set_one_str_list = []
            for k, v in data['set_kv'].items():
                if isinstance(v, str):
                    v = '"' + v + '"'
                cy_set_one_str = (
                    'n.{k} = {v}'
                ).format(k=k, v=v)
                cy_set_one_str_list.append(cy_set_one_str)
            cy_set_str = ', '.join(cy_set_one_str_list)
            cy_str = 'MATCH {node} SET {set_str}'.format(
                    node=cy_node_str, set_str=cy_set_str)
            self._do_cypher(cy_str)

        return result_schema.result_model(
                code=result_schema.CODE_SUCCESS_UPDATE, msg='更新成功')
