#!/usr/bin/env python3
from neo4j.v1 import GraphDatabase


class Neo4jTool:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def run(self, clause):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                result = tx.run(clause)
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()


class Neo4jStrTool:
    @staticmethod
    def node_str(label, properties=None, name=''):
        """
        get a node string, like '(name:label {property1:"v1", property2:"v2"})'
        paras:
            name - node name
            label - node label
            properties - a dict of properties
        """
        if properties is None:
            properties_str = ''
        else:
            properties_list = []
            for k, v in properties.items():
                if isinstance(v, str):
                    v = '"' + v + '"'
                property_str = '{p}:{v}'.format(p=k, v=v)
                properties_list.append(property_str)
            properties_str = ' {' + ', '.join(properties_list) + '}'
        node_str = '({name}:{label}{properties_str})'.format(
                name=name, label=label, properties_str=properties_str)
        return node_str

    @staticmethod
    def relationship_str(relationship, name=None, direction='right'):
        """
        get a relationship string, like '-[name:relationship]->'
        paras:
            direction - must be left or right
        """
        if name is None:
            inter = '[:{relationship}]'.format(relationship=relationship)
        else:
            inter = '[{name}:{relationship}]'.format(
                    name=name, relationship=relationship)

        if direction == 'right':
            rel_str = '-{inter}->'.format(inter=inter)
        elif direction == 'left':
            rel_str = '<-{inter}-'.format(inter=inter)
        else:
            raise UserWarning('direction must be right or left')

        return rel_str
