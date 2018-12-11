from engine import Engine


engine = Engine('bolt://localhost:7687', 'neo4j', '123456')


class Test_DoCypher:
    def test_match(self):
        res = engine._do_cypher('MATCH (idc:IDC) RETURN idc')
        print(res.data())


class TestAddIdc:
    def teardown(self):
        pass

    def test_add_idc(self):
        condition_dict = {
            'name': '红山机房2',
            'address': '地址测试'
        }
        self.engine.add_idc(condition_dict)


class TestDoMatch:
    def test_do_match(self):
        cy_str = 'MATCH (idc:IDC)<-[:RACK_AT]-(rack:RACK) RETURN idc, rack'
        condition_dict = {
            'cypher_str': cy_str
        }
        res = engine.do_match(condition_dict)
        print(res)


class TestAddNode:
    def setup(self):
        condition_list = [
            {
                'name': '石桥机房2',
                'address': '用于测试update'
            }
        ]
        engine.add_nodes('IDC', condition_list)

    def teardown(self):
        condition_dict = {
                'property_name': 'name',
                'values': ['红山机房2', '红山机房3', '石桥机房2']
        }
        engine.del_nodes('IDC', condition_dict)

    def test_add_idc(self):
        condition_list = [
            {
                'name': '红山机房2',
                'address': '地址测试2'
            },
            {
                'name': '红山机房3',
                'address': '地址测试3'
            }]
        engine.add_nodes('IDC', condition_list)

    def test_update_idc(self):
        condition_list = [
            {
                'match_kv': {
                    'name': '石桥机房2'
                },
                'set_kv': {
                    'address': '更改后的地址'
                }
            }
        ]
        engine.update_nodes('IDC', condition_list)
