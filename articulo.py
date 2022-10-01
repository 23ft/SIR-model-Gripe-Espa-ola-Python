"""
   Felipe Deaza - 23ft
   Modelo SIR en python!

   2022
"""

from sympy import *
from scipy.integrate import odeint
import numpy as np
#from sympy.plotting import plot
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def _grafica_resistentes():
   plt.plot(time, solution[0][:,2], lw = 1.5, color = 'purple')
   plt.plot(time, solutionWithVaccine[0][:,2], lw = 1.5, color = 'brown')
   plt.title('$Resistentes$ $R_{(t)}$')
   plt.xlabel('$t_{(weeks)}$')
   plt.ylabel('$R_{(t)}$')
   plt.legend(labels=["$not$ $vaccine$", "$vaccine$"])
   plt.grid(True)
   plt.savefig('resistentes.pdf')
   plt.show()

def _grafica_infectados():
   plt.plot(time, solution[0][:,1], lw = 1.5, color = 'red')
   plt.plot(time, solutionWithVaccine[0][:,1], lw = 1.5, color = 'orange')
   plt.xlabel('$t_{(weeks)}$')
   plt.ylabel('$I_{(t)}$')
   plt.title('$Infectados$ $I_{(t)}$')
   plt.legend(labels=["$not$ $vaccine$", "$vaccine$"])
   plt.grid(True)
   plt.savefig("infectados.pdf")
   plt.show()

def _grafica_sucep():
   plt.plot(time, solution[0][:,0], lw = 1.5, color = 'green')
   plt.plot(time, solutionWithVaccine[0][:,0], lw = 1.5, color = 'blue')
   plt.subplots_adjust(left=0.19)
   plt.title('$Suceptibles$ $S_{(t)}$')
   plt.xlabel('$t_{(weeks)}$')
   plt.ylabel('$S_{(t)}$')
   plt.legend(labels=["$not$ $vaccine$", "$vaccine$"])
   plt.grid(True)
   plt.savefig('suceptilbles.pdf')
   plt.show()

def graficacion():
   """ Graficacion """

   figure, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10,5), constrained_layout=True)
   figure.suptitle('Modelo SIR -  Python')
   #figure.supylabel('s')

   ax1.plot(time, solution[0][:,0], lw = 1.5, color = 'green')
   ax1.plot(time, solutionWithVaccine[0][:,0], lw = 1.5, color = 'blue')
   ax1.set_title('$Suceptibles$ $S_{(t)}$')
   ax1.set_xlabel('$t_{(weeks)}$')
   ax1.set_ylabel('$S_{(t)}$')
   ax1.legend(labels=["$not$ $vaccine$", "$vaccine$"])
   ax1.grid(True)

   ax2.plot(time, solution[0][:,1], lw = 1.5, color = 'red')
   ax2.plot(time, solutionWithVaccine[0][:,1], lw = 1.5, color = 'orange')
   ax2.set_xlabel('$t_{(weeks)}$')
   ax2.set_ylabel('$I_{(t)}$')
   ax2.set_title('$Infectados$ $I_{(t)}$')
   ax2.legend(labels=["$not$ $vaccine$", "$vaccine$"])
   ax2.grid(True)

   ax3.plot(time, solution[0][:,2], lw = 1.5, color = 'purple')
   ax3.plot(time, solutionWithVaccine[0][:,2], lw = 1.5, color = 'brown')
   ax3.set_title('$Resistentes$ $R_{(t)}$')
   ax3.set_xlabel('$t_{(weeks)}$')
   ax3.set_ylabel('$R_{(t)}$')
   ax3.legend(labels=["$not$ $vaccine$", "$vaccine$"])
   ax3.grid(True)

   #figure.tight_layout()
   plt.savefig('grafica.png')
   plt.show()

def Vacunados(N,v,e):
    """ Aplicando la formula V = (Nve)/9 --> para el calculo numero individuos vacunados cada semana """
    return ((N*v*e)/9) 

def modelWithVaccine(t, x, B, Y, N,v,e):
    
   S = x[0] # suceptibles
   I = x[1] # infectados
   R = x[2] # resistentes
   
   """ Funcion a trozo Vacunados """
   V = Vacunados(N,v,e) if ((t>9) and (t <= 18)) else 0 # Individuos vacunados
   
   """ Sistema ecuaciones ordenado """
   dS = -(B*I*S) - V
   dI = (B*I*S) - (Y*I)
   dR = (Y*I) + V
   
   return [dS, dI, dR]

def modelWithoutVaccine(t, x, B, Y):
    
   S = x[0] # suceptibles
   I = x[1] # infectados
   R = x[2] # resistentes
   
   """ Sistema ecuaciones ordenado """
   dS = -(B*I*S)
   dI = (B*I*S) - (Y*I)
   dR = (Y*I)
   
   return [dS, dI, dR]

""" Initial Values """
S0 = 99986  # suceptibles en semana 0
I0 = 14     # infectados en semana 0
R0 = 0      # resistentes en semana 0
    
""" Constants """
B = 3.61e-5  # tasa de contagio
Y = 3.47     # coeficiente retiro natural
N = S0+I0+R0 # numero individuos
v = 0.20     # indice cobertura vacunal
e = 0.67     # indice eficacia vacuna

time = np.linspace(0,51,52) # del 0 al 10, 2501 datos.
print(time)
y0 = [S0, I0, R0]

solution = odeint(modelWithoutVaccine, y0, time, full_output=True, tfirst=True, args=(B, Y))
solutionWithVaccine = odeint(modelWithVaccine, y0, time, full_output=True, tfirst=True, args=(B, Y, N,v,e))

graficacion()