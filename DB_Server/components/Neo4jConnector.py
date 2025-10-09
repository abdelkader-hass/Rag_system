from neo4j import GraphDatabase
from .static_var import NEO4J_URI ,NEO4J_USER ,NEO4J_PASSWORD ,DB


class Neo4jConnector:
    def __init__(self, uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD,db=DB,driver=None):
        self.uri = uri
        self.user = user
        self.password = password
        self.db=db
        self.driver = driver
        if driver :
            self.driver=driver
        else:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password),database=self.db)
                print("Successfully connected to Neo4j.")
            except Exception as e:
                self.driver=None
                print(f"Failed to connect to Neo4j: {e}")


    def close(self):
        if self.driver:
            self.driver.close()
            print("Connection to Neo4j closed.")

