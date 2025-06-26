import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class SenderAgent(Agent):
    class InformBehav(CyclicBehaviour):
        async def run(self):
            print("InformBehav running")

            # Envia primeira mensagem
            msg = Message(to="marcoolivera096@xmpp.jp")
            msg.set_metadata("performative", "inform")
            msg.body = "Qual é a função"
            await self.send(msg)
            print("Mensagem 'Qual é a função' enviada!")

            # Espera pela resposta
            reply = await self.receive(timeout=10)
            if reply:
                print(f"Resposta recebida: {reply.body}")
                if reply.body == "A função é 1grau":
                    msg2 = Message(to="marcoolivera096@xmpp.jp")
                    msg2.set_metadata("performative", "inform")
                    msg2.body = "1,2"
                    await self.send(msg2)
                    print("Mensagem '1,2' enviada!")
                else:
                    print("Resposta não esperada.")
            else:
                print("Nenhuma resposta recebida após 10 segundos.")

            await self.sleep(5)  # Espera antes de tentar de novo

    async def setup(self):
        print("SenderAgent iniciado")
        self.add_behaviour(self.InformBehav())


async def main():
    senderagent = SenderAgent("marcoolivera731@xmpp.jp", "m0a5r0c8o")
    await senderagent.start(auto_register=True)
    print("Sender iniciado")
    await senderagent.web.start(hostname="127.0.0.1", port="10001")


if __name__ == "__main__":
    spade.run(main())
