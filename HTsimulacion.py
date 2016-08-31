#Universidad del Valle de Guatemala, Algoritmos y Estructuras de Datos, Seccion 20
#Hoja de Trabajo 5
#German Garcia 15008, Luis Najera 15581


import simpy
import random

#---------------------------------------------------------#
#Variables del programa

semillaRam = 10  #Valor de la Semilla para el random
Procesos = 200   #Cantidad de Procesos a Efectuar   

#Variables para llevar el control de los tiempos
Tiempo1 = 0
Tiempo2 = []

random.seed(semillaRam)     #Creacion de random usando el valor de la variable semillaRam como semilla
env = simpy.Environment()   #Creacion del environment para el programa
valorCPU = simpy.Resource(env,capacity=2)   #Variable para asignacion del valor del cpu usandola como tipo Resource
memoria = simpy.Container(env,init=100,capacity=100)    #Valor de la memoria, utilizando un Container para su manejo, init valor inicial, capacity capacidad maxima
tEsperaCola = simpy.Resource(env,capacity=3)    #Variable para el tiempo de espera de la cola usandola como tipo Resorce

#---------------------------------------------------------#


# Operaciones requeridas por el programa y obtencion de tiempos
     
def Proceso (env,NumProceso,numero,memoria,memoriaRequerida,nInst,cantInst):

    global Tiempo1, Tiempo2 #variables globales para los tiempos

    
    #Primer Tiempo de la etapa
    # Obtencion del primer tiempo medido e impresion del numero de proceso y memoria que requiere el proceso
    
    yield env.timeout(NumProceso) 
    print('Tiempo: %f - Proceso %s - requiere %d de la RAM' % (env.now,numero,memoriaRequerida))
    tiempoMedido = env.now


    #New asignacion de mRam RAM
    # Impresion del tiempo transcurrido, el numero de proceso y validacion de la memoria asignada al proceso
    yield memoria.get(memoriaRequerida)
    print('Tiempo: %f - Proceso %s - Ram Asignada al Proceso %d' % (env.now,numero,memoriaRequerida))


    # Siguiente etapa
    
    numIns = 0  # Variable para el control de instrucciones
    
    #Etapa Ready y Running
    # Ciclo que se realiza mientras la variable numIns sea menor a nInst, que es el numero de Instrucciones random asignada al proceso

    while numIns < nInst:
        with valorCPU.request() as req:
            yield req
            if (nInst-numIns)>=cantInst: 
                instruccionaProcesar = cantInst 

            else:
                instruccionaProcesar=(nInst-numIns)

    #Impresion del tiempo usado, el numero del proceso y validacion para ver que paso a la etapa ready                
            print('Tiempo necesario: %f - Proceso %s - pasa a etapa ready %d ' % (env.now,numero,instruccionaProcesar))
            yield env.timeout(instruccionaProcesar/cantInst)
            numIns += instruccionaProcesar      #Incremento de la variable numIns

    
    #Etapa Final Ramdom para el Waiting o Ready
            
            variableCola = random.randint(1,2) #Se realiza un random para ver si el proceso para a ready o waiting
            if variableCola == 1 and instruccionaProcesar < cantInst:
                with tEsperaCola.request() as reqE:
                    yield reqE
                yield env.timeout(1)
        

    yield memoria.put(memoriaRequerida)

    # Impresion para verificar el proceso llego a terminated, el numero de proceso y la cantidad de ram que utilizo
    print('Terminated %f - Proceso %s - Cantidad de RAM utilizada: %d ' % (env.now, numero, memoriaRequerida))
    Tiempo1 = Tiempo1+(env.now-tiempoMedido)
    Tiempo2.append(env.now-tiempoMedido)
    print ('')		  

   

# Creacion de for para generacion random de los valores del numero de procesos, memoria para los procesos y el numero de instrucciones asignadas

for i in range(Procesos):
    
    NumProceso = random.expovariate(1.0)       #Generacion de numero de Procesos
    nInst = random.randint(1, 10)              #Generacion de de instrucciones del proceso
    memoriaRequerida = random.randint(1,10)    #mRam para procesos    
    
    env.process(Proceso(env,NumProceso,str (i),memoria, memoriaRequerida,nInst,3.0))
   	
env.run ()

#Impresion del numero de procesos realizados

print ("Numero de Procesos %d" %(Procesos))

#Calculo del tiempo promedio
promedio = (Tiempo1/Procesos)

#Impresion del valor del tiempo promedio
print ("Tiempo Promedio %f" %(promedio))

#Calculo e impresion de la desviacion estandar
tiempo=0
for k in Tiempo2:
    tiempo=tiempo+((k-promedio))**2
    DesviacionEstandar = (tiempo/(Procesos-1))**0.5
print("La desviacion Estandar es: %f" %(DesviacionEstandar))
