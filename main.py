from include.funcoes import grau1  # ou do arquivo onde você salvou a função

def main():
    # Gerar função aleatória do 1º grau
    f = grau1()
    X = []
    Y = []
    # Chutar alguns valores de x
    for x in range(1, 3):  # de -5 a 5
        X.append(x)
        y = f(x)
        Y.append(y)
        print(f"f({x}) = {y}")


    zero =( X[1] - X[0])/(Y[1] - Y[0])
    return zero


if __name__ == "__main__":
    zero = main()
    print(f"o zero da função é {zero}")
