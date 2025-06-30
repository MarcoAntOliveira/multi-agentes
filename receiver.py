import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random
import asyncio
from include.funcoes import grau1  # Função que retorna f(x) = ax + b como lambda


FUNCOES_DISPONIVEIS = [#"A função é 1º grau",
                      #  "A função é 2º grau",
                       "A função é 3º grau",
                       ]


class ReceiverAgent(Agent):
    async def setup(self):
        print("ReceiverAgent iniciado.")

        # Define uma função de 1º grau apenas uma vez
        self.f = grau1()

        # -------------------------------
        # Template para "Qual é a função"
        # -------------------------------
        def match_qual_e_funcao(msg):
            return (
                msg is not None
                and msg.body is not None
                and msg.body.strip().lower() == "qual é a função"
            )

        template_funcao = Template()
        template_funcao.set_metadata("performative", "inform")
        template_funcao.custom_match = match_qual_e_funcao
        self.add_behaviour(self.ResponseFunction(), template_funcao)

        # ------------------------------------
        # Template para mensagens numéricas (x)
        # ------------------------------------
        def match_numero(msg):
            return (
                msg is not None
                and msg.body is not None
                and msg.body.strip().isdigit()
            )

        template_valor = Template()
        template_valor.set_metadata("performative", "inform")
        template_valor.custom_match = match_numero
        self.add_behaviour(self.RecvBehav(), template_valor)

    # ----------------------------
    # Responde "Qual é a função?"
    # ----------------------------
    class ResponseFunction(OneShotBehaviour):
        async def run(self):
            print("Esperando pergunta sobre a função...")
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Mensagem recebida: {msg.body}")
                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "inform")
                response.body = random.choice(FUNCOES_DISPONIVEIS)
                await self.send(response)
                print("Resposta enviada!")
            else:
                print("Nenhuma mensagem recebida para a função.")

    # --------------------------------
    # Responde com o valor de f(x)
    # --------------------------------
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("Esperando mensagem numérica...")
            msg = await self.receive(timeout=10)
            if msg:
                try:
                    conteudo = msg.body
                    x_value = int(conteudo)
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
