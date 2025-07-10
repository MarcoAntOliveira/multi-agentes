import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random
import asyncio
from include.funcoes import grau1, grau2, grau3  # Todas devem retornar lambdas

FUNCOES_DISPONIVEIS = [
    "A função é 1º grau",
    "A função é 2º grau",
    "A função é 3º grau",
]


class ReceiverAgent(Agent):
    async def setup(self):
        print("ReceiverAgent iniciado.")

        self.funcao_escolhida = None
        self.f = None  # Função a ser usada

        # Template: "qual é a função?"
        def match_qual_e_funcao(msg):
            return msg and msg.body and msg.body.strip().lower() == "qual é a função"

        template_funcao = Template()
        template_funcao.set_metadata("performative", "inform")
        template_funcao.custom_match = match_qual_e_funcao
        self.add_behaviour(self.ResponseFunction(), template_funcao)

        # Template: número
        def match_numero(msg):
            return msg and msg.body and msg.body.strip().replace('.', '', 1).isdigit()

        template_valor = Template()
        template_valor.set_metadata("performative", "inform")
        template_valor.custom_match = match_numero
        self.add_behaviour(self.RecvBehav(), template_valor)

    class ResponseFunction(OneShotBehaviour):
        async def run(self):
            print("Esperando pergunta sobre a função...")
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Mensagem recebida: {msg.body}")
                funcao = random.choice(FUNCOES_DISPONIVEIS)
                self.agent.funcao_escolhida = funcao

                # Seleciona a função correspondente
                if funcao == "A função é 1º grau":
                    self.agent.f = grau1()
                elif funcao == "A função é 2º grau":
                    self.agent.f = grau2()
                elif funcao == "A função é 3º grau":
                    self.agent.f = grau3()

                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "inform")
                response.body = funcao
                await self.send(response)
                print(f"Função escolhida: {funcao}")
            else:
                print("Nenhuma mensagem recebida para a função.")

    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("Esperando mensagem numérica...")
            msg = await self.receive(timeout=10)
            if msg:
                try:
                    x_value = float(msg.body.strip())
                    if self.agent.f is None:
                        raise Exception("Função ainda não foi escolhida. Envie 'qual é a função' primeiro.")

                    resultado = self.agent.f(x_value)
                    print(f"f({x_value}) = {resultado}")

                    resposta = Message(to=str(msg.sender))
                    resposta.set_metadata("performative", "inform")
                    resposta.body = f"{resultado}"
                    await self.send(resposta)
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")
            else:
                print("Nenhuma mensagem recebida após 10 segundos.")


# ---------------------
# Inicia o agente SPADE
# ---------------------
async def main():
    receiver = ReceiverAgent("marcoolivera096@xmpp.jp", "m0a5r0c8o")
    await receiver.start()
    print("Agente iniciado.")

    try:
        while receiver.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await receiver.stop()
        print("Agente finalizado.")


if __name__ == "__main__":
    spade.run(main())
