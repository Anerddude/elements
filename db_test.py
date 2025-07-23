from neo4j import GraphDatabase
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "bahboha12")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()