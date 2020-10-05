# -*- coding: utf-8 -*-
from scipy import signal
import numpy as np

class bessel:
    
    # Iniciação dos parâmetros
    def __init__(self, tipo, Wp1, Ap, Ws1, As, Wp2 = 0, Ws2 = 0):
        self.tipo = tipo
        self.Ap = Ap
        self.As = As
        self.N = 0
        if tipo == "PB" or tipo == "PA":
            self.Wp = Wp1
            self.Ws = Ws1
        if tipo == "PF" or tipo == "RF":
            self.Wp1 = Wp1
            self.Wp2 = Wp2
            self.Ws1 = Ws1
            self.Ws2 = Ws2
            self.Bp = Wp2 - Wp1
            self.Bs = Ws2 - Ws1
    
    
    # Método principal, que chama todos os outros
    def principal(self):
        for N in range(1, 51):
            self.N = N
            
            den = bessel.den(self)
            
            H = signal.TransferFunction(1, den)
            w, y, phase = H.bode(w = np.arange(0, 10, step = 0.001))
            
            Wpl = bessel.Wpl(self, w, y)
            
            Kp = self.Wp/Wpl
            
            H = bessel.TransfFreq(self, H.num, H.den, Kp)
            w, y, phase = H.bode(w = np.arange(0, 25000, step = 1))
            
            Ks = bessel.Wsl(self, w, y)
            
            if self.tipo == "PB":
                if (self.Wp >= Kp) and (self.Ws >= Ks):
                    break
            elif self.tipo == "PA":
                if (self.Wp >= Kp) and (self.Ws <= Ks):
                    break
            
            if N == 50:
                print("\nNão foi possível achar um filtro\n")
                
        return H, w, y, Kp, Ks, self.N
    
    
    # Define e retorna o denominador da FT
    def den(self):
        ak = list()
        ak.append(1)
        for k in range(0, self.N):
            ak.append(2*(self.N-k)*ak[k] / ((2*self.N-k)*(k+1)))
        den = ak[::-1]
        return den
    
    
    # Encontra o ponto em w correspondente ao Ap
    def Wpl(self, w, y):
        for i in y:
            if i < self.Ap or i == y[-1]:
                indice, = np.where(np.isclose(y, i))
                self.indice = indice
                aux = w[indice-1]
                break
        return aux
    
    
    def Wsl(self, w, y):
        if self.tipo == "PB":
            for i in y:
                if i < self.As or i == y[-1]:
                    indice, = np.where(np.isclose(y, i))
                    self.indice = indice
                    aux = w[indice-1]
                    break
            return aux
        elif self.tipo == "PA":
            for i in y:
                if i > self.As or i == y[-1]:
                    indice, = np.where(np.isclose(y, i))
                    self.indice = indice
                    aux = w[indice-1]
                    break
            return aux
    
    
    def TransfFreq(self, zeros, polos, Kp):
        if self.tipo == "PB":
            num, den = signal.lp2lp(zeros, polos, Kp)
        elif self.tipo == "PA":
            num, den = signal.lp2hp(zeros, polos, Kp)
        elif self.tipo == "PF":
            num, den = signal.lp2bp(zeros, polos, Kp, self.Bp)
        elif self.tipo == "RF":
            num, den = signal.lp2bs(zeros, polos, Kp, self.Bp)
        H = signal.TransferFunction(num, den)
        return H
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    