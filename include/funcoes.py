import random

# 1º grau: f(x) = ax + b
def grau1():
    a = random.randint(-100, 100)
    while a == 0:  # Garante que seja realmente de 1º grau
        a = random.randint(-100, 100)
    b = random.randint(-100,100)
    return lambda x: a * x + b

# 2º grau: f(x) = ax² + bx + c
def grau2():
    a = random.randint(-100, 100)
    while a == 0:  # Garante que seja realmente de 2º grau
        a = random.randint(-100, 100)
    b = random.randint(-100,100)
    c = random.randint(-100,100)
    return lambda x: a * x**2 + b * x + c

# 3º grau: f(x) = ax³ + bx² + cx + d
def grau3(a, b, c, d):
    a = random.randint(-100, 100)
    while a == 0:  # Garante que seja realmente de 2º grau
        a = random.randint(-100, 100)
    b = random.randint(-100,100)
    c = random.randint(-100,100)
    d =   random.randint(-100,100)
    return lambda x: a * x**3 + b * x**2 + c * x + d

# Exponencial: f(x) = a * e^(b*x)

def exponencial(x, termos=20):
    resultado = 1.0  # primeiro termo da série é 1
    termo = 1.0      # termo atual
    for n in range(1, termos):
        termo *= x / n  # termo_n = termo_(n-1) * x / n
        resultado += termo
    return resultado


# Logarítmica: f(x) = a * log_b(x) + c
def log_natural(x, termos=20):
    if x <= 0:
        return float('nan')  # log indefinido para x <= 0
    y = (x - 1) / (x + 1)
    resultado = 0
    for n in range(termos):
        termo = (1 / (2 * n + 1)) * (y ** (2 * n + 1))
        resultado += termo
    return 2 * resultado

def logaritmica(a, base, termos = 20):
    ln_x =log_natural(a, termos)
    ln_base =log_natural(base, termos)
    return ln_x / ln_base

def pi_nilakantha(termos=100000):
    pi_aprox = 3.0
    for n in range(1, termos):
        termo = 4 / (2*n * (2*n + 1) * (2*n + 2))
        if n % 2 == 0:
            pi_aprox -= termo
        else:
            pi_aprox += termo
    return pi_aprox
pi =  pi_nilakantha(termos=100000)

# Seno
def sin(x, termos=10):
    x = x % (2 * pi)  # normaliza o valor para melhor precisão
    resultado = 0
    for n in range(termos):
        termo = ((-1)**n) * (x**(2*n + 1)) / math.factorial(2*n + 1)
        resultado += termo
    return resultado

# Cosseno
def cos(x, termos=10):
    x = x % (2 * pi)
    resultado = 0
    for n in range(termos):
        termo = ((-1)**n) * (x**(2*n)) / math.factorial(2*n)
        resultado += termo
    return resultado

# Tangente (usando seno e cosseno)
def tan_aproximado(x, termos=10):
    cos = cos_aproximado(x, termos)
    if abs(cos) < 1e-10:
        return float('inf')  # aproximação de assíntota
    return sin_aproximado(x, termos) / cos
