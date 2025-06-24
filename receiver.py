import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template


class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=10)
            print(msg)
            if msg:
                print("Message received with content: {}".format(msg.body))
                response = Message(to="marcoolivera731@xmpp.jp")
                response.set_metadata("performative", "inform")
                response.body = "send response"

                await self.send(response)
                print("Response sent!")

            else:
                print("Did not receive any message after 10 seconds")

            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        self.add_behaviour(self.RecvBehav())


async def main():
    receiveragent = ReceiverAgent("marcoolivera096@xmpp.jp", "m0a5r0c8o")
    await receiveragent.start(auto_register=True)
    print("Receiver started")

    await  spade.wait_until_finished(receiveragent)
    print("Agent finished")

if __name__ == "__main__":
    spade.run(main())

