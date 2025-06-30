import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import asyncio
from include.chutes import encontrar_raiz_reta, encontrar_zeros_grau2, encontrar_zeros_grau3
# Listas globais para armazenar pares (x, y)
x_vals = []
y_vals = []

class SenderAgent(Agent):
    class PerguntaFuncao(OneShotBehaviour):
        async def run(self):
            print("Perguntando: Qual é a função?")
            msg = Message(to="marcoolivera096@xmpp.jp")
            msg.set_metadata("performative", "inform")
            msg.body = "Qual é a função"
            await self.send(msg)
            print("Mensagem enviada!")

    class ConversaComReceiver(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.funcao_confirmada = False
            self.x_enviados = [-1, 0, 1, 2, 3]  # Pode aumentar aqui para mais pontos
            self.index = 0

        async def run(self):
            reply = await self.receive(timeout=10)
            if reply:
                print(f"Recebido: {reply.body}")

                if not self.funcao_confirmada and "função" in reply.body.lower():
                  print(f"Função confirmada: {reply.body}")
                  self.funcao_confirmada = True
                  self.tipo_funcao = reply.body  # Guarda a descrição da função, se quiser usar depois
                  await self.envia_proximo_x()


                elif reply.body.replace('.', '', 1).isdigit() or reply.body.startswith("-"):
                    y_valor = float(reply.body)
                    x_valor = self.x_enviados[self.index - 1]  # -1 pois index já foi incrementado
                    x_vals.append(x_valor)
                    y_vals.append(y_valor)
                    print(f"Armazenado: f({x_valor}) = {y_valor}")

                    if self.index < len(self.x_enviados):
                        await self.envia_proximo_x()
                    else:
                        print("Todos os valores enviados e recebidos.")
                        print(f"x: {x_vals}")
                        print(f"y: {y_vals}")
                        if self.tipo_funcao == "A função é 1º grau":
                          zero_funcao = encontrar_raiz_reta(x_vals, y_vals)
                        elif self.tipo_funcao == "A função é 2º grau":
                          zero_funcao = encontrar_zeros_grau2(x_vals, y_vals)
                        elif self.tipo_funcao == "A função é 3º grau":
                          zero_funcao = encontrar_zeros_grau3(x_vals, y_vals)

                        print(f"O zero da função é dada por {zero_funcao}")
                        await self.agent.stop()
                else:
                    print("Resposta não reconhecida:", reply.body)
            else:
                print("Nenhuma mensagem recebida.")

        async def envia_proximo_x(self):
            if self.index < len(self.x_enviados):
                x_valor = self.x_enviados[self.index]
                msg = Message(to="marcoolivera096@xmpp.jp")
                msg.set_metadata("performative", "inform")
                msg.body = str(x_valor)
                await self.send(msg)
                print(f"Enviado x = {x_valor}")
                self.index += 1

    async def setup(self):
        print("SenderAgent iniciado")
        self.add_behaviour(self.PerguntaFuncao())
        self.add_behaviour(self.ConversaComReceiver())


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
