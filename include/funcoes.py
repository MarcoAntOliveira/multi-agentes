# 1º grau: f(x) = ax + b
def grau1(a, b):
    return lambda x: a * x + b

# 2º grau: f(x) = ax² + bx + c
def grau2(a, b, c):
    return lambda x: a * x**2 + b * x + c

# 3º grau: f(x) = ax³ + bx² + cx + d
def grau3(a, b, c, d):
    return lambda x: a * x**3 + b * x**2 + c * x + d

# Exponencial: f(x) = a * e^(b*x)
import math
def exponencial(a, b):
    return lambda x: a * math.exp(b * x)

# Logarítmica: f(x) = a * log_b(x) + c
def logaritmica(a, base, c):
    return lambda x: a * math.log(x, base) + c if x > 0 else float('nan')
