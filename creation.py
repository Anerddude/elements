#Imports
from ollama import chat
from ollama import ChatResponse

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
                You are a creative entities combiner. 
                Generate a name for the combination of the entities included in this prompt. 
                Your response should only include the generated name.
                Elements : {elements_names}.
                new element :

                """
            }])
        combined_element = Element((response.message.content))
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
var_14 = water + water
var_5 = stone + water
var_6 = fire + water

print(Element.data)