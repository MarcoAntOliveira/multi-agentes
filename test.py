
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import random as rnd
import re

a_time = 100


def extrair_numero(texto):
    padrao = r'[+-]?\d+'
    numeros = re.findall(padrao, texto)
    return numeros[0]


##agente gerador da funcao
class Gerador_funcao(Agent):

    #atributos da funcao
    grau = 0
    a = 0
    b = 0
    c = 0
    #cliente
    cliente = 0

    def f(self,x,grau):

        if grau == 1: return       self.a*(x + self.b)
        elif grau == 2: return    (self.a+x)*(self.b+x)
        else: return              (self.a+x)*(self.b+x)*(self.c+x)



    class Aguardar_solicitacao(CyclicBehaviour):
        async def run(self):

            try:
                msg = await self.receive(timeout=a_time)
                self.agent.cliente = str(msg.sender)
                print("[GERADOR]")
                print("solicitacao de " + self.agent.cliente + " recebida \n")

            except:
               pass

    class Gerar_funcao(OneShotBehaviour):
        async def run(self):
            self.agent.grau = rnd.randint(1,3)
            self.agent.a = rnd.randint(-100, 100)
            self.agent.b = rnd.randint(-100, 100)
            self.agent.c = rnd.randint(-100, 100)
            self.agent.d = rnd.randint(-100, 100)

            msg = Message(to=self.agent.cliente)
            msg.set_metadata("performative", "inform")
            msg.body = "O grau da funcao e: " + str(self.agent.grau)

            await self.send(msg)
            print("[GERADOR]")
            print("Grau da funcao enviado\n")

    class Receber_x(CyclicBehaviour):
        async def run(self):

            try:
                msg = await self.receive(timeout=a_time)
                print("[GERADOR]")
                print(msg.body + "\n")
                x = extrair_numero(msg.body)
                y = self.agent.f(x,self.agent.grau)
                send_msg = Message(to=self.agent.cliente)
                send_msg.set_metadata("performative", "subscribe")
                send_msg.body = str(y)

                await self.send(send_msg)
                print("[GERADOR]")
                print("Valor de f(" + str(x) + ") enviado \n")
            except:
                pass


    async def setup(self):
        print("[GERADOR]")
        print("gerador iniciou \n")


        template_solicitar = Template()
        template_solicitar.set_metadata("performative", "request")
        self.add_behaviour(self.Aguardar_solicitacao(), template_solicitar)

        template_receber_x = Template()
        template_receber_x.set_metadata("performative", "inform")
        self.add_behaviour(self.Receber_x(),template_receber_x)



## agente que solicita e encontra o zero da funcao
class Resolvedor_funcao(Agent):
    gerador = "gyrozeppeli8471@xmpp.jp"
    grau = 0
    valores_testados = []

    def Encontrar_zero(self):
        x = rnd.randint(-100,100)
        for numero in self.valores_testados:
            while(x == numero): x = rnd.randint(-100,100)

        self.valores_testados += [x]
        return x

    class Solicitar_funcao(OneShotBehaviour):
        async def run(self):
            msg = Message(to=self.agent.gerador)
            msg.set_metadata("performative", "request")
            msg.body = "Me de um polinomio de grau ate 3"

            await self.send(msg)
            print("[RESOLVEDOR]")
            print("pedido enviado \n")

    class Receber_grau(CyclicBehaviour):
        async def run(self):


            try:
                msg = await self.receive(timeout=a_time)
                print("[RESOLVEDOR]")
                print("Grau recebido = " + msg.body[-1] + "\n")
                grau = int(msg.body[-1])
                self.agent.add_behaviour(self.agent.Enviar_x())
            except:
                pass

    class Enviar_x(OneShotBehaviour):
        async def run(self):
            x = self.agent.Encontrar_zero()

            msg = Message(to=self.agent.gerador)
            msg.set_metadata("performative", "inform")
            msg.body = "o zero da funcao e: " + str(x)

            await self.send(msg)
            print("[RESOLVEDOR]")
            print("zero de funcao enviado com valor de x = " + str(x))

    class Receber_y(CyclicBehaviour):
        async def run(self):


            try:
                msg = await self.receive(timeout=a_time)
                print("[RESOLVEDOR]")
                print("valor calculado = " + msg.body + "\n")
                y = int(msg.body)
                if y != 0:
                    print("[RESOLVEDOR]")
                    print("zero de funcao nao encontrado")
                    print("realizando nova tentativa \n")
                    self.agent.add_behaviour(self.agent.Enviar_x())
                else:
                    print("[RESOLVEDOR]")
                    print("zero de funcao encontrado f(" + str(self.agent.valores_testados[-1]) + ") = " + msg.body)
                    print("Encerrando agente \n")
                    ##await self.stop()
            except:
                pass



    async def setup(self):

        print("[RESOLVEDOR]")
        print("resolvedor iniciou \n")

        self.add_behaviour(self.Solicitar_funcao())

        template_grau = Template()
        template_grau.set_metadata("performative", "inform")
        self.add_behaviour(self.Receber_grau(),template_grau)

        template_recebe_y = Template()
        template_recebe_y.set_metadata("performative", "subscribe")
        self.add_behaviour(self.Receber_y(),template_recebe_y)

async def main():


    gerador = Gerador_funcao("gyrozeppeli8471@xmpp.jp", "ufsc4040")
    await gerador.start()
    ##print("resolvedor iniciado \n")


    resolvedor = Resolvedor_funcao("diegobrando8471@xmpp.jp", "ufsc4040")
    await resolvedor.start()
    ##print("gerador iniciado \n")
    print("[MAIN]")
    print("ambos agentes iniciaram \n")

if __name__ == "__main__":
    spade.run(main())
