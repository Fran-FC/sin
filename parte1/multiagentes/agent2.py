import time, os
from owlready2 import *
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        def __init__(self):
            super().__init__()
            self.ontology_= "rnews_1.0_draft3_rdfxml.owl"
            
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=120)
            if msg:
                print("Message received: {}".format(msg.body))

                self.processNews(msg.body)

                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body="Respuesta"

                await self.send(msg)
                print("Responded!")
            else:
                print("No message after 20 seconds")
            await self.agent.stop()
        
        def processNews(self, new_text):
            onto = get_ontology(self.ontology_)
            onto.load()
            for i in onto.classes():
                print(i)

        
    async def setup(self):
        print("Agent 2 started")
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