import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import asyncio

x = []
y = []

class SenderAgent(Agent):

    class AskFunctionBehaviour(OneShotBehaviour):
        async def run(self):
            print("Perguntando: Qual é a função?")
            msg = Message(to="marcoolivera096@xmpp.jp")
            msg.set_metadata("performative", "inform")
            msg.body = "Qual é a função"
            await self.send(msg)
            print("Mensagem enviada!")

    class HandleRespostaFuncao(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.funcao_recebida = False
            self.x_atual = 1

        async def run(self):
            reply = await self.receive(timeout=10)
            if reply:
                conteudo = reply.body.strip()
                print(f"Resposta recebida: {conteudo}")

                if not self.funcao_recebida:
                    if conteudo == "A função é 1º grau":
                        self.funcao_recebida = True
                        print("Função identificada. Enviando valor de x...")
                        x.append(self.x_atual)

                        msg = Message(to="marcoolivera096@xmpp.jp")
                        msg.set_metadata("performative", "inform")
                        msg.body = str(self.x_atual)
                        await self.send(msg)
                        print(f"Enviado x = {self.x_atual}")
                    else:
                        print("Resposta inesperada antes de definir a função.")
                else:
                    # Após receber o valor de y
                    try:
                        valor_y = float(conteudo)
                        y.append(valor_y)
                        print(f"Valor de f({self.x_atual}) = {valor_y} armazenado")
                    except ValueError:
                        print(f"Resposta não numérica inesperada: {conteudo}")
            else:
                print("Nenhuma resposta recebida.")

    async def setup(self):
        print("SenderAgent iniciado")
        self.add_behaviour(self.AskFunctionBehaviour())
        self.add_behaviour(self.HandleRespostaFuncao())


async def main():
    senderagent = SenderAgent("marcoolivera731@xmpp.jp", "m0a5r0c8o")
    await senderagent.start()
    print("Sender iniciado")

    try:
        while senderagent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await senderagent.stop()
        print("Sender finalizado")


if __name__ == "__main__":
    spade.run(main())
