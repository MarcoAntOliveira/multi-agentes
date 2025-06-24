import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="marcoolivera096@xmpp.jp")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
                msg = Message(to="marcoolivera096@xmpp.jp")     # Instantiate the message
                msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                msg.body = "send hi"                    # Set the message content

                await self.send(msg)
                print("Message sent!")

            else:
                print("Did not received any message after 10 seconds")


            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)


async def main():


  senderagent = SenderAgent("marcoolivera731@xmpp.jp", "m0a5r0c8o")
  await senderagent.start(auto_register=True)
  print("Sender started")

  await spade.wait_until_finished(senderagent)
  print("Agents finished")


if __name__ == "__main__":
    spade.run(main())

