from spade import agent

class DummyAgent(agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))

dummy = DummyAgent("frafolco@gtirouter.dsic.upv.es", "4241")
dummy.start()

dummy.stop()