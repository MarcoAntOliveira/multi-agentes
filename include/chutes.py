def encontrar_raiz_reta(X,  Y):
    if X[0]== X[1]:
        raise ValueError("x1 e x2 não podem ser iguais (reta vertical).")

    # Coeficiente angular
    x_zero = (Y[1] - Y[0]) / (X[1] - X[0])
    # Intercepto


    return x_zero
def resolver_sistema_linear_3x3(A, B):
    # Eliminação de Gauss para 3x3
    for i in range(3):
        # Pivô
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Pivô zero. Troca de linha necessária.")
        for j in range(i+1, 3):
            mult = A[j][i] / pivot
            for k in range(3):
                A[j][k] -= mult * A[i][k]
            B[j] -= mult * B[i]

    # Substituição reversa
    x = [0] * 3
    for i in reversed(range(3)):
        s = B[i]
        for j in range(i+1, 3):
            s -= A[i][j] * x[j]
        x[i] = s / A[i][i]
    return x

def encontrar_zeros_grau1(x, y):
    a = (y[1] - y[0]) / (x[1] - x[0])
    b = y[0] - a * x[0]
    if a == 0:
        return []  # sem raiz
    return [-b / a]

def encontrar_zeros_grau2(x, y):
    A = []
    B = []
    for xi, yi in zip(x, y):
        A.append([xi**2, xi, 1])
        B.append(yi)
    a, b, c = resolver_sistema_linear_3x3(A, B)
    delta = b**2 - 4*a*c
    if delta < 0:
        return []
    elif delta == 0:
        return [-b / (2*a)]
    else:
        sqrt_d = delta**0.5
        return [(-b + sqrt_d)/(2*a), (-b - sqrt_d)/(2*a)]

def resolver_sistema_4x4(A, b):
    # Eliminação de Gauss com pivoteamento parcial
    n = 4
    for i in range(n):
        # Pivoteamento
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            raise ValueError("Sistema singular (pivô zero).")
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminação
        for j in range(i + 1, n):
            f = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= f * A[i][k]
            b[j] -= f * b[i]

    # Substituição regressiva
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x  # Coeficientes: a, b, c, d

def derivada_polinomio(a, b, c):
    return lambda x: 3 * a * x**2 + 2 * b * x + c

def polinomio(a, b, c, d):
    return lambda x: a * x**3 + b * x**2 + c * x + d

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-10:
            break  # Derivada muito pequena, evita divisão por zero
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    return x

def encontrar_zeros_grau3(x_vals, y_vals):
    if len(x_vals) != 4 or len(y_vals) != 4:
        raise ValueError("São necessários exatamente 4 pontos.")

    if len(set(x_vals)) < 4:
        raise ValueError("Todos os valores de x devem ser distintos.")

    # Monta sistema linear: [x³ x² x 1] * [a,b,c,d] = y
    A = [[x**3, x**2, x, 1] for x in x_vals]
    b = list(y_vals)

    # Resolve sistema para achar coeficientes
    a, b_, c, d = resolver_sistema_4x4(A, b)

    # Define f(x) e f'(x)
    f = polinomio(a, b_, c, d)
    df = derivada_polinomio(a, b_, c)

    # Tenta encontrar até 3 raízes com chutes diferentes
    chutes = [-10, 0, 10]
    zeros = []
    for x0 in chutes:
        raiz = newton_raphson(f, df, x0)
        # Evita raízes repetidas (considerando tolerância)
        if all(abs(raiz - r) > 1e-4 for r in zeros):
            zeros.append(raiz)

    return zeros
def encontrar_zeros(x, y):
    if len(x) != len(y):
        raise ValueError("Listas de x e y devem ter o mesmo tamanho.")

    grau = len(x) - 1
    if grau == 1:
        return encontrar_zeros_grau1(x, y)
    elif grau == 2:
        return encontrar_zeros_grau2(x, y)
    elif grau == 3:
        return encontrar_zeros_grau3(x, y)
    else:
        raise ValueError("Somente polinômios de grau 1 a 3 são suportados.")
