import math
import random
import sys
import requests
import time
import json
import numpy
import Clases
import Metaheuristico
from datetime import datetime, date
from io import StringIO

s = StringIO()
#sys.stdout = s

def main ():
    """Main function to run the optimization experiments."""
    start = time.time()
    # Check for a command-line argument to run a batch experiment
    if((sys.argv[1]) == "x"): 
        sys.stdout = sys.__stdout__
        archivo = "ArrivalLima190504.txt"
        a=corrida (archivo)
        # ... (runs for other dates)
        archivo = "ArrivalLima190505.txt"
        b=corrida (archivo)
        archivo = "ArrivalLima190506.txt"
        c=corrida (archivo)
        archivo = "ArrivalLima190507.txt"
        d=corrida (archivo)
        archivo = "ArrivalLima190508.txt"
        e=corrida (archivo)
        archivo = "ArrivalLima190509.txt"
        f=corrida (archivo)
        archivo = "ArrivalLima190520.txt"
        g=corrida (archivo)
        archivo = "ArrivalLima190521.txt"
        h=corrida (archivo)
        
        # Print summary of results
        print("-------------------------")
        print("Experimentación Final: ")
        print("4 de mayo: "+ str(round(a,2)))
        print("5 de mayo: "+ str(round(b,2)))
        print("6 de mayo: "+ str(round(c,2)))
        print("7 de mayo: "+ str(round(d,2)))
        print("8 de mayo: "+ str(round(e,2)))
        print("9 de mayo: "+ str(round(f,2)))
        print("20 de mayo: "+ str(round(g,2)))
        print("21 de mayo: "+ str(round(h,2)))
        print ("Promedio: "+str(round((a+b+c+d+e+f+g+h)/8,2)))
        print("-------------------------")
        
    else:
        # Run for a single file specified in the command line
        corrida (sys.argv[1])
        sys.stdout = sys.__stdout__
        print(s.getvalue())
    end = time. time()
    print("Tiempo de ejecución: " + str((end-start)))

def corrida(archivo):
    """Runs a single optimization instance for a given flight data file.
    
    Args:
        archivo (str): The path to the input text file with flight data.

    Returns:
        float: The final energy (cost) of the best solution found.
    """
    with open(archivo) as json_file:  
        data = json.loads(json_file.read().replace("\'", "\""))

    # Filter out flights that have already landed or were cancelled
    data_filtered = list(filter(lambda x : x['status'] != 'landed' and x['status'] != 'cancelled', data))
    data_canceled = list (filter(lambda x: x['status'] == 'cancelled',data))
    listaVuelos = []
    tamanos = ["Pequeño", "Mediano", "Grande"]
    Clases.Vuelo.nVuelo =0
    i = 0
    for flight in data_filtered:
        # --- Data Parsing and Object Creation ---
        i +=1
        vuelo = Clases.Vuelo()
        # Randomly assign a size to the aircraft for simulation purposes
        vuelo.setTamano(tamanos[round(random.random()*2)])
        jsonDestino = flight ['arrival']
        anho = int(jsonDestino['scheduledTime'][0:4])
        mes = int(jsonDestino['scheduledTime'][5:7])
        dia = int(jsonDestino['scheduledTime'][8:10])
        hora = int(jsonDestino['scheduledTime'][11:13])
        minuto = int(jsonDestino['scheduledTime'][14:16])
        segundo = int(jsonDestino['scheduledTime'][17:19])
        vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                   hour=hora, minute=minuto, second=segundo))
        vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                   hour=hora, minute=minuto, second=segundo))
        vuelo.setEstado(flight['status'])
        if (vuelo.estado=="active"):
            try:
                anho = int(jsonDestino['scheduledTime'][0:4])
                mes = int(jsonDestino['scheduledTime'][5:7])
                dia = int(jsonDestino['scheduledTime'][8:10])
                hora = int(jsonDestino['scheduledTime'][11:13])
                minuto = int(jsonDestino['scheduledTime'][14:16])
                segundo = int(jsonDestino['scheduledTime'][17:19])
                vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                           hour=hora, minute=minuto, second=segundo))
                vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                           hour=hora, minute=minuto, second=segundo))
            except:
                pass
            
        jsonVuelo = flight['flight']
        vuelo.addNumeroVuelo(jsonVuelo['number'])
        vuelo.addIata(jsonVuelo['iataNumber'])
        try:
            vuelo.addIcao(jsonVuelo['icaoNumber'])
        except:
            vuelo.addIata(jsonVuelo['iataNumber'])
        if(vuelo.icao == "None"):
            vuelo.addNumeroVuelo(jsonVuelo['number'])

        jsonAerolinea = flight['airline']
        aerolinea =Clases.TAerolinea()
        aerolinea.addIata(jsonAerolinea['iataCode'])
        try:
            aerolinea.addIcao(jsonAerolinea['icaoCode'])
        except:
            pass
        aerolinea.addNombre(jsonAerolinea['name'])

        avion = Clases.Avion()
        avion.addTAerolinea(aerolinea)
        vuelo.setAvion(avion)

        vuelo.asignarIDVuelo()
        listaVuelos.append(vuelo)

    # --- Initialize Airport Resources (Gates and Zones) ---
    nPuertas = 20
    nZonas = 52
    
    listaZonas = []
    listaPuertas = []
    # Create Puerta (Gate) objects with random sizes
    for i in range(1,nPuertas+1):
        area2 = Clases.Puerta("Puerta",tamanos[round(random.random()*2)],i, random.random()*499+1,random.random()*499+1,10)
        listaPuertas.append(area2)
        
    for i in range(1,nZonas +1):
        area = Clases.Zona("Zona", tamanos[round(random.random()*2)], i, random.random()*499+1, random.random()*499+1)
        listaZonas.append(area)

    # --- Run the Simulated Annealing + Tabu Search Algorithm ---
    ann = Metaheuristico.Annealer(listaVuelos,listaPuertas,listaZonas)
    x,y = ann.anneal()

    # --- Print the final results in a JSON-like format ---
    print ("{ [", end="")
    for i in x[0]:
        i.imprimirLista()
        print (", ",end="")
    cont =0
    for i in x[1]:
        if(cont ==0):
            cont =1
        else:
            print(", ",end="")
        i.imprimirLista() 
    print (" ] }, {", end="")
    print (json.dumps(data_canceled),end="")

    print ("} ",end="")
    
    return y

if __name__ == '__main__':
    main()