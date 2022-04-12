import time
import webbrowser
import json
from unittest import case
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class Sender(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="frafolco_r@gtirouter.dsic.upv.es")
            msg.set_metadata("performative", "inform")
            msg.body = input(
                "Introduzca la palabra clave para buscar una noticia: ")

            await self.send(msg)
            print("News requested!")

            print("Waiting for response...")
            msg = await self.receive(timeout=120)
            if msg:
                instance = json.loads(msg.body)
                option = input("Response recieved, open article? [Y/n] ")
                if option.lower() == "y" or option == "":
                    webbrowser.open(instance["instance"]["url"], new=2)

            else:
                print("Response timeout")
            await self.agent.stop()

    async def setup(self):
        self.b = self.InformBehav()
        self.add_behaviour(self.b)


if __name__ == "__main__":
    senderagent = Sender("frafolco@gtirouter.dsic.upv.es", "4241")
    res = senderagent.start()
    time.sleep(2)
    res.result()

    while senderagent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            break
