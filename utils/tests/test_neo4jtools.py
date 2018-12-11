from nose.tools import assert_equal

from utils.neo4jtool import Neo4jTool
from utils.neo4jtool import Neo4jStrTool


URI = 'bolt://localhost:7687'
USER = 'neo4j'
PASSWORD = '123456'


class TestNeo4jTool:
    def test_run(self):
        with Neo4jTool(URI, USER, PASSWORD) as neo:
            result = neo.run('MATCH (idc:IDC) RETURN idc')
        print(result)


class TestNeo4jStrTool:
    def test_node_str(self):
        name = 'one_name'
        label = 'ONE_LABEL'
        properties = {
            'p1': 'v1',
            'p2': 100
        }
        res = Neo4jStrTool.node_str(
                name=name, label=label, properties=properties)
        print(res)
        res = Neo4jStrTool.node_str(label=label, properties=properties)
        print(res)
        res = Neo4jStrTool.node_str(label=label)
        print(res)

    def test_relationship_str(self):
        res1 = Neo4jStrTool.relationship_str(
                relationship='RELATION_SHIP', name='r', direction='left')
        assert_equal('<-[r:RELATION_SHIP]-', res1)
