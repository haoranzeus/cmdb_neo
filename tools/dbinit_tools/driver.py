from neo4j.v1 import GraphDatabase


class Neo4jDriver:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def run(self, clause):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                result = tx.run(clause)
        return result
