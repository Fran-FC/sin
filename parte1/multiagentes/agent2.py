from re import A
import time, os
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from owlready2 import *
import feedparser

class Onto:
    def __init__(self, onto_url):
        self.onto_url_ = onto_url
        self.onto_ = get_ontology(self.onto_url_)
        self.onto_.load()
    
    def list_classes(self):
        for onto_class in self.onto_.classes():
            print(onto_class)

class NewsScrapper:
    def __init__(self, url):
        self.news_feed_ = feedparser.parse(url)

    def __manhattan_distance(self, p1, p2):
        distance = 0
        for x1, x2 in zip(p1, p2):
            difference = ord(x2) - ord(x1)
            absolute_difference = abs(difference)
            distance += absolute_difference

        return distance
        
    def list_keys(self):
        print(self.news_feed_.entries[0].keys())

    def list_titles(self):
        for entry in self.news_feed_.entries:
            print(entry.title)

    def search_from_titles(self, substr_title):
        for entry in self.news_feed_.entries:
            if substr_title in entry.title:
                self.entry_ = entry
                print("match, distance: {}".format(self.__manhattan_distance(substr_title, entry.title)))
                break
    
    def get_title(self):
        return self.entry_.title


class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        def __init__(self):
            super().__init__()
            self.ontology_url_= "rnews_1.0_draft3_rdfxml.owl"
            
        async def run(self):
            msg = await self.receive(timeout=120)
            if msg:
                print("Message received: {}".format(msg.body))

                self.processNews(msg.body)

                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body="Respuesta"

                await self.send(msg)
            else:
                print("No message after 120 seconds")
            await self.agent.stop()
        
        def processNews(self, new_text):
            onto = Onto(self.ontology_url_)
            onto.list_classes()

        
    async def setup(self):
        self.b = self.RecvBehav()
        self.add_behaviour(self.b)

if __name__ == "__main__":
    receiveragent = ReceiverAgent("frafolco_r@gtirouter.dsic.upv.es", "4241")
    res = receiveragent.start()
    time.sleep(2)
    res.result()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break