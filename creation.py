#Imports
from ollama import chat
from ollama import ChatResponse
import networkx as nx
import matplotlib.pyplot as plt
from neo4j import GraphDatabase

def draw_parent_child_graph(parent_child_dict, output_file="parent_child_graph.png"):
    """This function will be used to visualize the parent-child relationship between the 
    elements that are created"""
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add edges to the graph
    for child, parents in parent_child_dict.items():
        for parent_tuple in parents:
            for parent in parent_tuple:
                G.add_edge(parent, child)
    
    # Draw the graph
    plt.figure(figsize=(10, 8))  # Set figure size
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", 
            font_size=10, font_weight="bold", arrowsize=10)
    
    plt.title("Parent-Child Relationship Graph")
    
    # Save to file instead of showing
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory


def clean_name(raw: str) -> str:
    """This will clean the names of the new elements"""
    # Extract first alphanumeric word
    import re
    match = re.search(r'\b([a-zA-Z]+)\b', raw)
    return match.group(1) if match else "ERROR"

class Element:
    """ This will hold all of the needed info about the elements and will create new elements as they get dicovered"""
    data = dict()
    def __init__(self, name):
        self.name = name
    def __add__(self, other):
        elements_names = self.name + " and " + other.name
        response : ChatResponse = chat(model='phi3:3.8b', messages=[
            {
                'role': 'user',
                'content': f"""
You are a naming wizard who combines elements into single, perfect names.
COMBINE THESE INTO ONE CLEVER NAME: {elements_names}.

STRICT RULES:
- OUTPUT MUST BE **EXACTLY ONE WORD** (ONLY IN RARE CASES TWO WORDS IF TECHNICALLY UNAVOIDABLE)
- NO SENTENCES, NO PUNCTUATION, NO QUOTES, NO EXPLANATIONS
- NO PREFIXES/SUFFIXES LIKE "Name:" or "Combination:"
- IF YOU CAN'T FOLLOW THE RULES, OUTPUT ONLY 'ERROR'

BAD EXAMPLES (NEVER DO THIS):
- "The combined name is 'leafstone'" → WRONG (has sentence)
- "aquaflare" → WRONG (two words)
- > name: firewater < → WRONG (has punctuation/formatting)

GOOD EXAMPLES:
- fire + water → steam
- stone + air → sandstone
- light + dark → twilight

NOW COMBINE: {elements_names} → """
            }],)
        combined_element = Element((clean_name(response.message.content)))
        if combined_element.name in Element.data.keys():
            Element.data[combined_element.name].append((self.name, other.name))
        else: 
            Element.data[combined_element.name] = [(self.name, other.name)]
        return combined_element


#Basic Elements:
stone = Element("stone")
fire = Element("fire")
water = Element("water")
air = Element("air")

var_1 = water + fire
var_2 = stone + fire
var_3 = fire + air
var_4 = water + water
var_5 = stone + water
var_6 = fire + water

var_1_1 = var_1 + var_4
var_1_2 = var_2 + var_5
var_1_3 = var_6 + var_3
var_1_4 = var_1 + var_2


print(Element.data)
draw_parent_child_graph(Element.data)

def save_to_neo4j(parent_child_dict, uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def create_relationship(tx, parent, child):
        tx.run("MERGE (p:Person {name: $parent}) "
               "MERGE (c:Person {name: $child}) "
               "MERGE (p)-[:PARENT_OF]->(c)",
               parent=parent, child=child)
    
    with driver.session() as session:
        for child, parents in parent_child_dict.items():
            for parent_tuple in parents:
                for parent in parent_tuple:
                    session.execute_write(create_relationship, parent, child)
    
    driver.close()

save_to_neo4j(Element.data, "neo4j://localhost:7687", "neo4j", "bahboha12")