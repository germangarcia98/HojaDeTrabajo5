#Universidad del Valle de Guatemala, Algoritmos y Estructuras de Datos, Seccion 20
#Hoja de Trabajo 5
#German Garcia 15008, Luis Najera 15581


import simpy
import random
             
def proceso (env,nProcesos,numero,cMemoria,mProcesos,nInst,cantInst):

    global tiempo1,tiempo2 

    
    #Primer Tiempo del Proceso
    yield env.timeout(nProcesos)
    print('Tiempo %f - Proceso %s requiere %d de la RAM' % (env.now,numero,mProcesos))
    tiempoMedido = env.now


    #New asignacion de memoria RAM
    yield cMemoria.get(mProcesos)
    print('Tiempo2 %f Proceso - %s Memoria Asignada al Proceso %d' % (env.now,numero,mProcesos))


    numIns = 0
    #Etapa Ready y Running
    while numIns < nInst:
        with vCpu.request() as req:
            yield req
            if (nInst-numIns)>=cantInst: ###########
                instrucProcesar = cantInst ########

            else:
                instrucProcesar=(nInst-numIns)

    #Impresion del tiempo usado
            print('Tiempo3 %f Proceso - %s pasa a etapa ready %d ' % (env.now,numero,instrucProcesar))


            yield env.timeout(instrucProcesar/cantInst)
            numIns += instrucProcesar

    
    #Etapa Final Ramdom para el Waiting o Ready

            variableCola = random.randint(1,2)
            if variableCola == 1 and instrucProcesar < cantInst:
                with tEsperaCola() as req2:
                    yield req2
                yield env.timeout(1)
        

        yield cMemoria.put(mProcesos)
        print('Terminated %f - %s, Se Requirio de la RAM %d ' % (env.now, numero, mProcesos))

        tiempo1 = tiempo1+(env.now-tiempoMedido)
        tiempo2.append(env.now-tiempoMedido)
          

    



intervaloP = 10  #Invervalos de Instrucciones
cantRam = 10        #Semilla para ramdom ram
mRam = 100          #Ram Disponible

tiempo1= 0.0
tiempo2=[]
                      
env = simpy.Environment()
vCpu = simpy.Resource(env, capacity=2)
cMemoria = simpy.Container(env, init=100, capacity=100)
tEsperaCola=simpy.Resource(env, capacity=1)
nProsCPU=3
random.seed(cantRam) #Generador random para asignacion de memoria
interval=2           #Variable para generar numeros al azar, para simulacion de llegada de procesos
cantInst = 3.0 #sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

#Se realizan los procesos

for i in range(intervaloP):
    nProcesos = random.expovariate(1.0/interval)       #Generacion de numero de Procesos
    nInst = random.randint(1,13)        #Generacion de de instrucciones del proceso
    mProcesos = random.randint(1,10)   #Memoria para procesos
    env.process(proceso(env,nProcesos,str (i),cMemoria, mProcesos,nInst,cantInst))
   	
env.run()

print ("Numero de Procesos %f" %(intervaloP))
print ("Numero de Procesos Soportados %f" %(cantInst))
promedio = (tiempo1/intervaloP)
print ("Timpo Promedio %f" %(promedio))
tiempoPre=0
for k in tiempo2:
    tiempoPre=tiempoPre+((k-promedio))**2
    DesviacionEstandar = (tiempoPre/(intervaloP-1))**0.5
print("La desviacion Estandar es: %f" %(DesviacionEstandar))
