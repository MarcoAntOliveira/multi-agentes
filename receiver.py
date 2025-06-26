import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("Esperando mensagem...")
            msg = await self.receive(timeout=10)  # Espera por 10s
            if msg:
                print(f"Mensagem recebida: {msg.body}")

                if msg.body == "Qual é a função":
                    response = Message(to="marcoolivera731@xmpp.jp")
                    response.set_metadata("performative", "inform")
                    response.body = "A função é 1grau"
                    await self.send(response)
                    print("Resposta enviada!")

                elif msg.body == "1,2":
                    numeros = [int(n.strip()) for n in msg.body.split(",")]
                    print(f"Números recebidos: {numeros}")

                else:
                    print("Mensagem não reconhecida.")
            else:
                print("Nenhuma mensagem recebida após 10 segundos.")

    async def setup(self):
        print("ReceiverAgent iniciado.")
        self.add_behaviour(self.RecvBehav())


async def main():
    receiveragent = ReceiverAgent("marcoolivera096@xmpp.jp", "m0a5r0c8o")
    await receiveragent.start(auto_register=True)
    print("Agente iniciado.")
    await receiveragent.web.start(hostname="127.0.0.1", port="10000")  # Interface web opcional


if __name__ == "__main__":
    spade.run(main())
