import os
from owlready2 import *

ontology_path = os.getcwd() + "/pizza.owl"

onto = get_ontology(ontology_path)
onto.load()

# for entity in onto.classes():
#     print(entity)

for entity in onto.search(subclass_of=onto.VegetalTopping):
    print(entity)

for entity in onto.search(type=onto.PizzaConNombre):
    print(entity)

# for entity in onto.search(hasCountryOfOrigin=onto.Italy):
#     print(entity)

with onto:
    class Drug(Thing):
        pass
    print(Drug.iri)

    class DrugAssociation(Drug):
        pass
    print(DrugAssociation.ancestors())