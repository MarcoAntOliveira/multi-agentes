import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import random
import asyncio
from include.funcoes import grau1, grau3  # grau2 opcional

FUNCOES_DISPONIVEIS = {
    "A função é do 1º grau: f(x) = ax + b": grau1,
    "A função é 3º grau: f(x) = ax^3 + bx^2 + cx + d": grau3,
}


class ReceiverAgent(Agent):
    async def setup(self):
        print("ReceiverAgent iniciado.")
        self.f = None
        self.add_behaviour(self.UnifiedReceiverBehaviour())

    class UnifiedReceiverBehaviour(CyclicBehaviour):
        async def run(self):
            print("Aguardando mensagem...")
            msg = await self.receive(timeout=10)
            if msg:
                conteudo = msg.body.strip().lower()
                resposta = Message(to=str(msg.sender))
                resposta.set_metadata("performative", "inform")

                if conteudo == "qual é a função":
                    funcao_escolhida = random.choice(list(FUNCOES_DISPONIVEIS.keys()))
                    self.agent.f = FUNCOES_DISPONIVEIS[funcao_escolhida]()  # chama grau1(), grau3(), etc.
                    resposta.body = funcao_escolhida
                else:
                    try:
                        if self.agent.f is None:
                            raise Exception("Função ainda não definida. Envie 'qual é a função' primeiro.")

                        x = float(conteudo)
                        y = self.agent.f(x)
                        resposta.body = f"f({x}) = {y}"
                    except ValueError:
                        resposta.body = "Mensagem inválida. Envie um número ou 'qual é a função'."
                    except Exception as e:
                        resposta.body = f"Erro: {e}"

                await self.send(resposta)
                print(f"Resposta enviada: {resposta.body}")
            else:
                print("Nenhuma mensagem recebida após 10 segundos.")
