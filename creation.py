#Imports
import os
import requests
import re
import networkx as nx
import matplotlib.pyplot as plt
from neo4j import GraphDatabase

class Element:
    """ This will hold all of the needed info about the elements and will create new elements as they get dicovered"""
    data = dict()
    def __init__(self, name):
        self.name = name
    def __add__(self, other):
        elements_names = self.name + " " + other.name
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:3.8b",
                "prompt": f"""
                            You are a creative entities combiner. 
                            Generate a name for the combination of the entities included in this prompt. 
                            Your response should only include the generated name.
                            Elements : {elements_names}.
                            new element : 
                        """,
                "stream": False
            }
        )
        if response.status_code == 200:
            try:
                response_text = response.json()["response"].strip()
                match = re.search(r"(\w+)", response_text)
                if not match:
                    result = response_text.split()[0] if response_text else "unknown"
                else:
                    result = match.group(1)
                result_element = Element(result)
                if result_element.name.lower() not in [i.lower() for i in Element.data.keys()]:
                    Element.data[self.name].append(result_element.name)
                    Element.data[other.name].append(result_element.name)
                    Element.data[result_element.name] = []
                    return result_element
            except (KeyError, AttributeError) as e:
                print(f"Error processing response: {e}")
                print(f"Response was: {response.text}")
                return Element("unknown")

#Basic Elements:
stone = Element("stone")
fire = Element("fire")
water = Element("water")
air = Element("air")

Element.data["stone"] = []
Element.data["air"] = []
Element.data["fire"] = []
Element.data["water"] = []

var_1 = water + fire
var_2 = stone + fire
var_3 = fire + air
var_14 = water + water
var_5 = stone + water
var_6 = fire + water

print(Element.data)