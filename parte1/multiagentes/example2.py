from multiprocessing import dummy
import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade import quit_spade

class DummyAgent(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour...")
            self.counter = 0

        async def run(self): 
            print("Counter: {}".format(self.counter))
            self.counter += 1
            if self.counter >= 3:
                self.kill(exit_code=10)
                return
            await asyncio.sleep(1)
    async def setup(self):
        print("Agent starting...")
        b = self.MyBehav()
        self.add_behaviour(b)

if __name__ == "__main__":
    dummy = DummyAgent("frafolco@gtirouter.dsic.upv.es", "4241")
    res = dummy.start()

    res.result()

    print("Wait until user interrupts with control+c")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    dummy.stop()
    quit_spade()


    class CreateBehav(OneShotBehaviour):
        async def run(self):
            agent2 = Agent 