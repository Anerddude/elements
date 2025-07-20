#Imports
import os
from google import genai

#API KEY and model setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


class Element:
    """ This will hold all of the needed info about the elements and will create new elements as they get dicovered"""
    data = dict()
    def __init__(self, name):
        self.name = name
    def __add__(self, other):
        elements_names = self.name + " " + other.name
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents=f"in a single word, give me the result of merging these 2 things together : {elements_names}"
        )
        result_element = Element(response.text)
        if result_element.name not in [i.name in Element.data.keys()]:
            Element.data[self].append(result_element)
            Element.data[other].append(result_element)
            Element.data[result_element] = []
        return result_element

#Basic Elements:
stone = Element("stone")
fire = Element("fire")
water = Element("fire")
air = Element("air")

Element.data[stone] = []
Element.data[air] = []
Element.data[fire] = []
Element.data[water] = []

l = [stone, fire, water, air]
for i in l:
    for j in l:
        var = i + j

print([i.name for i in Element.data.keys()])