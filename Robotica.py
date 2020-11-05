# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:56:16 2020

------------------------------------------------------------------------------
| UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO
| FACULTAD DE INGENIERÍA ELÉCTRICA, ELECTRÓNICA, INFORMÁTICA Y MECÁNICA 
| ESCUELA PROFESIONAL DE INGENIERÍA INFORMÁTICA Y DE SISTEMAS
|-----------------------------------------------------------------------------
| ASIGNATURA : ROBÓTICA Y PROCESAMIENTO DE SEÑAL
| DOCENTE : 
            Ing. PILLCO QUISPE, Jose Mauro
| TEMA : PROYECTO FINAL
|           VEHÍCULO ROVER 5 ESQUIVANDO RUTA ENTRE PELOTAS
| ALUMNOS :
|           134547 CATUNTA CHUCHULLO, Jose Luis 
|           124207 LETONA ASTO,Wiliams 
|           120283 LÓPEZ RAMOS, Nelson 
|           103172 PALOMINO POVEA, Angel 
|           124210 POLO DOLMOS, Jorge 
|           111651 QUISPE SOTO, William
| SEMESTRE : 2020-I
|-----------------------------------------------------------------------------
  ARCHIVO  : Robotica.py
"""
# librerias importadas necesarias
import cv2
import numpy as np
import math
import serial
import time

# modulo para filtrar contornos muy pequeños que sean detectatos y que no queremos mostrar tambien sirve para mostrar la pocision
#detectado
ser = serial.Serial('COM19',9600) #Comunicacion con el puerto COM16, debes cambiarlo por el tuyo.

# Modulo que dibuja el objeto y halla la distncia

def burbuja(A,B):# Metodo burbuja para ordenar las distancias y cordenadas y obtenidad
    for i in range(1,len(A)):
        for j in range(0,len(A)-i):
            if(A[j+1] < A[j]):
                aux=A[j];
                aux1=B[j];
                A[j]=A[j+1];
                B[j]=B[j+1];
                A[j+1]=aux;
                B[j+1]=aux1;
    return(A,B)

def distanciaPuntos(p0, p1): # Distancia entre dos puntos
  return ((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)**(0.5)

def dibujar(mask,color,w,f, Distancias, Coordenadas): # metodod para dibular los contornos cada circulo encontrado
  # Hallamos los contornos en la imagen
  font = cv2.FONT_HERSHEY_SIMPLEX
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for c in contornos:           # Recorremos cada uno de los contornos hallados
    area = cv2.contourArea(c)   # Hallamos el area del objeto
    if area > 3000:
      r=math.sqrt(area/math.pi) # Hallamos el radio a parir del area del objeto
      p=r*2                     # Hallamos el diametro   
      distancia = (w*f)/p       # Calculamos la distancia del objeto a la camara
      
      Distancias.append(distancia)    # Guardamos la distancia
      Punto = []                      # Arreglo para guardar punto
      
      M = cv2.moments(c)        # Obtener las coordenadas del objeto
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])    # Coordenadas de X
      y = int(M['m01']/M['m00'])    # Coordenadas de Y

      Punto.append(x)           # Guardamos x
      Punto.append(y)           # Guardamos y
      
      Coordenadas.append(Punto) # Devolvemos las coordenadas de los puntos
      
      # Escribimos el mensaje donde escribimos la distancia y dibujamos el contorno
      nuevoContorno = cv2.convexHull(c)
      mensaje = str(round(distancia,1))+" cm"
      cv2.putText(frame,mensaje,(x,y),font,0.75,(0,0,255),2,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
     
      
def AnalizarImagen(frame): ## metodod para analizar la iamagen y enviar distancias obtenidas para poder analizarlas
  # Rangos de los colores de objetos a detectar
  azulBajo = np.array([100,100,20],np.uint8)
  azulAlto = np.array([125,255,255],np.uint8)
  Distancias = []
  Coordenadas = []
  
  distancia = 0
  w = 6.5 # Ancho aparente 
  f = 1150 #Distancia focal
  # Transformar la imagen de BGR a HSV
  frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
  maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
  dibujar(maskAzul,(255,0,0),w,f,Distancias, Coordenadas)
  A,B = burbuja(Distancias,Coordenadas)  # A Distancias , B = Coordenadas
  DistanciaReal = 0
  DistanciaPuntos = 0
  
  if(len(Distancias)>1):
    DistanciaPuntos = distanciaPuntos(B[0],B[1])
    DistanciaReal = (((A[0] + A[1])/2)*DistanciaPuntos)/f
    DistanciaPelota=A[0]
  if(len(Distancias)==1):
    DistanciaPelota=A[0]
  if(len(Distancias)==0):
    DistanciaPelota=0
 
  # Pinhole 
  #print(DistanciaPuntos)   # Distancia entre dos pelotas pixeles
  print("Distancia entre Pelotas =",DistanciaReal,'cm')
  
  # Distancia entre dos pelosta en centimetros
  #print(len(Distancias),"frezzer puto")
  
  return (len(Distancias),DistanciaReal,DistanciaPelota)
cap=cv2.VideoCapture("http://192.168.0.102:8080/video")
i=0
#bucle de ejecucion continua
while(True):
    
    tiempolimite = time.time() + 1   # Ejecutamos el bucle de video por 1 segundos
    #cap=cv2.VideoCapture("http://192.168.1.12:8080/video")
    success,image = cap.read()
    count = 0;
    while True:    
        success,image = cap.read()
        if (count%10 == 0):
            cv2.imwrite("frame%d.jpg" % count, image)
        count += 1
        if  time.time() > tiempolimite:
            break
    frame = cv2.imread('frame10.jpg') #imagen a analizar
    cantidadPelotas,distReal,DistanciaPelota=AnalizarImagen(frame)
    print(cantidadPelotas)
    cv2.imshow('frame',frame)
    if(cantidadPelotas>1):# numero de pelotas es  ayor a dos 
       
        if((distReal>33 and DistanciaPelota>29)or distReal==0):#si la distancia entre pelotas es mayor ala del carrito avanzara
            print(cantidadPelotas," Hay dos pelotascon una Distancia de >33 entre ellas")
            print("Distancia alas Pelotas",DistanciaPelota)
            ser.write('w'.encode('ascii'))
            time.sleep(1)
            print("Avanzar")
            ser.write('q'.encode('ascii'))
            time.sleep(3)
            print("Parar") 
        else:
            if(distReal<33 and DistanciaPelota<29):#si la distancia entre pelotas es menor  ala del carrito gira derecha
                print(cantidadPelotas,"Hay dos pelotascon una Distancia de <33 entre ellas")
                print("Distancia alas Pelotas",DistanciaPelota)
                ser.write('d'.encode('ascii'))
                time.sleep(1)
                ser.write('q'.encode('ascii'))
                time.sleep(3)
                print("Girar Derecha")
            if(distReal<33 and DistanciaPelota>29):#si la distancia entre pelotas es menor  ala del carrito pero la distancia ala pelota es >29 que siga avanzando
                print(cantidadPelotas," Hay dos pelotascon una Distancia de <33 entre ellas")
                print("Distancia alas Pelotas",DistanciaPelota)
                ser.write('w'.encode('ascii'))
                time.sleep(1)
                print("Avanzar")
                ser.write('q'.encode('ascii'))
                time.sleep(3)
                print("Parar")
    else:
        #si solo se encuentra una pelota gira para la derecha
        if(cantidadPelotas==1):       
            print(cantidadPelotas,"Hay solo Una pelota")
            ser.write('d'.encode('ascii'))
            time.sleep(1)
            ser.write('q'.encode('ascii'))
            time.sleep(3)
            print("Girar Derecha")
        #si no se encontro ninguna pelota avanzar hacia adelnate
        if(cantidadPelotas==0):
            print(cantidadPelotas,"no hay Ninguna Pelota")
            ser.write('w'.encode('ascii'))
            time.sleep(1)
            ser.write('q'.encode('ascii'))
            time.sleep(3)
            print("Avanze")
    if cv2.waitKey(1) and 0xFF == ord('s'):
        break

#Finalmente cerramos todas las ventanas que se hubieran podido abrirse
cv2.destroyAllWindows()
    
        
    
        
        
        
    
    

 
    
    




