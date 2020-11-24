import numpy as np
import matplotlib.pyplot as plt
import random



NUMBER_OF_STEPS_EQUILIBRATING = 0    #Step number for equlibrating
NUMBER_OF_STEPS_SAMPLING = 1000      #Step number for sampling

RANDOM_WALK = [1,2,3,4]


def validar_data(mensaje_usuario, tipo_=None, min_=None, max_=None, lista_=None, dimension_tablero_=None):
  if min_ is not None and max_ is not None and max_ < min_:
    raise ValueError("Backend Error: Wrong parameter values\n")
  while True:
    usr_input = input(mensaje_usuario)
    if tipo_ is not None:
      try:
        data = tipo_(usr_input)
      except ValueError:
        print("Tipo de dato erróneo.\n")
        continue
    if lista_ is not None:
      letra = usr_input[FILA]
      try:
        idx = lista_.index(letra)
      except ValueError:
        print("Valor fuera de rango. Por favor, ingresarlo nuevamente.\n")
        continue
      numero = int(usr_input[1:])
      if numero < 1 or numero > dimension_tablero_:
        print("Valor fuera de rango. Por favor, ingresarlo nuevamente.\n")
        continue
    if max_ is not None and min_ is not None and (data < min_ or data > max_):
      print("Valor fuera de rango. Por favor, ingresar un número del {0} al {1}".format(min_, max_))
    else:
      return data

n = validar_data("\n Ingrese un tamaño de matriz! \n",int)

TABLERO =  np.random.choice([1, 0], size=(n, n), p=[0.3, 0.7])

#    Function_1: Random Direction
def random_direction(x,y,a):
  if a==1:
    x = x+1
    if x >=n:
      x=x-1
  elif a==2:
    x = x-1
    if x<=0:
      x=x+1
  elif a==3:
    y = y+1
    if y >=n:
      y=y-1
  elif a==4:
    y = y-1
    if y <=0:
      y=y+1
  return x,y



#    Function_2: Monte Carlo Step
def MCStep(M):
  x        =  np.random.choice(range(0,np.shape(M)[1]))
  y        =  np.random.choice(range(0,np.shape(M)[1]))
  M_i      =  np.copy(M)
  a = random.choice(RANDOM_WALK)
  p,q = random_direction(x,y,a)
  if M_i[x,y]==1 and M_i[p,q] == 0:
    M_i[p,q] = 1
    M_i[x,y] = 0
    M = np.copy(M_i)
  return M
#    Function_3: Value of dx or dy
def signo(d):
    if d < 0:
        return -1
    elif d > 0:
        return 1
    else:
        return 0

# Function_4: Compute
def computar_R2(x_ubicaciones,y_ubicaciones,x_ubicaciones0,y_ubicaciones0):
  R2=0
  for i in range(len(x_ubicaciones)):
    dx = x_ubicaciones[i] - x_ubicaciones0[i]
    dy = y_ubicaciones[i] - y_ubicaciones0[i] 
    if abs(dx)>n/2:
      dx = dx - signo(dx)*n
    if abs(dy)>n/2:
      dy = dy - signo(dy)*n  
    R2 = R2 +dx*dx+dy*dy
  return R2/PARTICULAS

def ubicaciones(M):
  x_ubicacion = []
  y_ubicacion = [] 
  for i in range(len(M)):
    for j in range(len(M)):
      if M[i,j] == 1:
        x_ubicacion.append(i)
        y_ubicacion.append(j)
  return x_ubicacion,y_ubicacion


TABLERO_INICIAL = np.copy(TABLERO)
x_ubicacion0,y_ubicacion0 = ubicaciones(TABLERO_INICIAL)
TABLERO_FINAL = np.copy(TABLERO)
PARTICULAS = np.sum(TABLERO_INICIAL)

print(np.sum(TABLERO_INICIAL))
t=0
tiempo = []
R2_etc =[]
for N_steps in range(0,NUMBER_OF_STEPS_SAMPLING):
  if N_steps > NUMBER_OF_STEPS_EQUILIBRATING:
    TABLERO_FINAL = np.copy(MCStep(TABLERO_FINAL))
    x_ubicacion,y_ubicacion = ubicaciones(TABLERO_FINAL)
    t+=1
    R2bar = computar_R2(x_ubicacion,y_ubicacion,x_ubicacion0,y_ubicacion0)
    R2_etc.append(R2bar) 
    tiempo.append(t)



print(np.sum(TABLERO_FINAL))

plt.plot(tiempo,R2_etc)
plt.xlim(0,400)      
plt.ylim(0,50) 
plt.xlabel(r'tiempo')
plt.ylabel("R2")


plt.show()
