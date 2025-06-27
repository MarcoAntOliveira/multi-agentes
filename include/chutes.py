def encontrar_raiz_reta(X,  Y):
    if X[0]== X[1]:
        raise ValueError("x1 e x2 não podem ser iguais (reta vertical).")

    # Coeficiente angular
    x_zero = (Y[1] - Y[0]) / (X[1] - X[0])
    # Intercepto


    return x_zero
