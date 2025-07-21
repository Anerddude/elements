#Database
G = nx.Graph(Element.data)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
def save_to_neo4j(tx):
    tx.run("MATCH (n) DETACH DELETE n")
    for node in G.nodes():
        tx.run("MERGE (n:Node {name: $name})", name=node)
    for (u, v) in G.edges():
        tx.run("""
            MATCH (a:Node {name: $u})
            MATCH (b:Node {name: $v})
            MERGE (a)-[:CONNECTED_TO]->(b)
        """, u=u, v=v)

with driver.session() as session:
    session.write_transaction(save_to_neo4j)

driver.close()
print("Graph saved to Neo4j!")


nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', font_weight='bold')
plt.savefig("graph.png")