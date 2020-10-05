# -*- coding: utf-8 -*-

from funcoes import *
import numpy as np
import matplotlib.pyplot as plt

# Boas Vindas
print("\nBem Vindo(a)!\n")
print("--------------------------------------------------------------------")
print("Tipos de Filtros Bessel:")
print("(PB) - Passa-Baixa\n(PA) - Passa-Alta")
print("(PF) - Passa-Faixa\n(RF) - Rejeita-Faixa")
print("--------------------------------------------------------------------")

# Pega o tipo de filtro e os pontos de projeto
tipo = "PA"
Wp = 26000 / (2*np.pi)
Ws = 4000 / (2*np.pi)
Ap = 20*np.log10(0.9)
As = 20*np.log10(0.1)

# Inicializa um Objeto da Classe Butterworth
if tipo == "PB" or tipo == "PA":
    filtro = bessel(tipo, Wp, Ap, Ws, As)
elif tipo == "PF" or tipo == "RF":
    filtro = bessel(tipo, Wp1, Ws1, Ap, As, Wp2, Ws2)

H, w, y, Kp, Ks, N = filtro.principal()

    
plt.figure(1)
plt.grid(True)
plt.xlim(0, 10000)
plt.ylim(-30, 0)
plt.scatter(Wp, Ap)
plt.scatter(Ws, As)
plt.plot(w, y)











