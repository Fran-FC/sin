import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.template import Template

class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=20)
            if msg:
                print("Message received {}".format(msg.body))
            else:
                print("No message after 20 seconds")
            await self.agent.stop()
        
    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

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