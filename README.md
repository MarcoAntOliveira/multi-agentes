SPADE é uma plataforma para o desenvolvimento de sistemas multiagentes (SMA) na linguagem Python e cuja mensagens trocadas são baseadas no protocolo de mensagens instantâneas XMPP.

A nova versão do SPADE foi implementada para Python 3 e representa uma significativa melhoria com relação a sua versão para Python 2.7. Embora a essência de funcionamento seja a mesma, a plataforma foi reformulada e está mais fácil de codificar, além de permitir o uso com qualquer servidor XMPP (antes precisa utilizar o servidor um servidor específico).

O trabalho aqui apresentado foi solicitado para uma turma da disciplina de Sistemas Inteligentes. A ideia desse projeto foi desenvolver 2 tipos de agentes:

    Gerador: agente responsável por gerar uma função e retornar o valor calculado para a função a partir de um número x recebido.
        Exemplo de funções:
            1grau: a.x + b
            2grau: a.x2 – b
            3grau: -0.2(x+a)(x-b)(x-c)

    Resolvedor: agente responsável por acertar o número para obter o zero da função.

O diagrama abaixo ilustra a interação e suas performativas. Observe que não foi seguido o padrão FIPA dos protocolos.

![Diagrama de comunicação](http://www.galirows.com.br/meublog/wp-content/uploads/2019/12/SMAfuncao.png)

O agente Gerador é realmente simples, precisando de 2 comportamentos cíclicos: (1) um para responder a solicitação do tipo da função; e (2) outro para calcular e retornar o resultado da função para um valor informado. Quando a agente Gerador é criado, ele sorteará um dos 3 tipos de função e gerará uma função apropriada para aquele tipo (uma vez que a função é gerada ela não mudará até a próxima vez que o agente for executado).

Um agente Gerador pode responder para vários agentes “Resolvedor”. Todos os resolvedores tentarão acertar o zero da função e sendo assim, o Gerador não deverá parar quando um resultado zero for encontrado.

Para simplificar o problema, a função sempre terá um número inteiro como solução e o número estará no intervalo entre -1000 e 1000. Isso quer dizer que, no pior dos casos, um agente que envia valores inteiros dentro desse intervalo, eventualmente irá acertar um valor que retorna o zero da função. O valorCalculado retornado pelo Gerador será apenas a parte inteira do cálculo da função, ou seja, não será retornado o valor exato.

Uma vez que se sabe o tipo da função, é possível elaborar soluções para encontrar o zero da função mais facilmente. Por exemplo, para encontrar o zero para a equação do primeiro grau, é possível obter uma solução que resolve em 3 tentativas.

Uma sugestão é criar um agente resolvedor para cada tipo de função e instanciar o agente específico assim que souber qual o tipo de função.

Na segunda parte (SMA com SPADE – parte da solução do agente “Gerador”) eu trago o script do Gerador e uma breve explicação sobre o funcionamento.
