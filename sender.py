import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
import time
import asyncio
x = []
y = []
class SenderAgent(Agent):
    class askFunction(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")

            # Envia primeira mensagem
            msg = Message(to="marcoolivera096@xmpp.jp")
            msg.set_metadata("performative", "inform")
            msg.body = "Qual é a função"
            await self.send(msg)
            print("Mensagem 'Qual é a função' enviada!")
    class InformBehav(CyclicBehaviour):
        async def run(self):

            # Espera pela resposta
            reply = await self.receive(timeout=10)
            if reply:
                print(f"Resposta recebida: {reply.body}")
                if reply.body == "A função é 1º grau":
                    msg2 = Message(to="marcoolivera096@xmpp.jp")
                    msg2.set_metadata("performative", "inform")
                    msg2.body = "1"
                    x.append(msg2.body)
                    await self.send(msg2)
                    print("Mensagem ' enviada!")
                elif reply.body.isdigit():
                  print("é um número")
                else:
                    print("Resposta não esperada.")
            else:
                print("Nenhuma resposta recebida após 10 segundos.")



    async def setup(self):
        print("SenderAgent iniciado")
        self.add_behaviour(self.askFunction()) 
        self.add_behaviour(self.InformBehav())


async def main():
    senderagent = SenderAgent("marcoolivera731@xmpp.jp", "m0a5r0c8o")
    await senderagent.start()
    print("Sender iniciado")


    while senderagent.is_alive():
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            await senderagent.stop()
            break


if __name__ == "__main__":
    spade.run(main())
