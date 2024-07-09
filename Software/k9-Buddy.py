#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get install -y python-smbus
# sudo apt-get install -y i2c-tools
# sudo i2cdetect -y 1
# sudo pip3 install adafruit-circuitpython-servokit
  
#Libraries
import RPi.GPIO as GPIO
import time    
from adafruit_servokit import ServoKit 
import math  
#Constants
nbPCAServo=16
#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]
#Referencia
"""
Mi colocar el valor de la boca cerrada
Ce colocar el valor de la cabeza a la altura media
Cr colocar el valor de la cabeza centrada
"""
servoref =[60 ,80   ,-9  , 90 , 35  ,95  , 47   ,90 , 60  ,80  ,145  , 20 , 15 , 95 , 150, 130]
#PIN      [0  , 1   , 2  , 3  , 4   ,5   , 6    , 7 , 8   , 9  ,10   , 11 , 12  , 13 , 14 , 15 ]
#Nombres  [TD ,FD   , PD , Sc , RD  , HD , ED   , Cr, EI  , HI ,RI   , Mi , PI  , FI , Ce , TI ]
#Objects
pca = ServoKit(channels=16)
#Variables
pitch=0
roll=0
c=[0.0,0.0,0.0,0.0]
d=[0.0,0.0,0.0,0.0]
x=[0.0,0.0,0.0,0.0]
y=[0.0,0.0,0.0,0.0]
z=[0.0,0.0,0.0,0.0]
fo=[0.0,0.0,0.0,0.0]
fn=[0.0,0.0,0.0,0.0]
angle=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#Modificar con las dimensiones del modelo físico
c[0] = c[1] = c[2] = c[3] = 186.81 #mm
fo[0] = fo[1] = fo[2] = fo[3] = 202.63 #mm
a = 95.0 #mm
b = 123.74 #mm
g = 78.50 #mm
# function main 
def main():
    #Setup
    #Para la pca9685
    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])
    time.sleep(0.010)
    x[0]=x[1]=x[2]=x[3]=0
    y[0]=y[1]=y[2]=y[3]=0
    #Para la rasp
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    try:
        #Rutina de baile
        thriller()
        time.sleep(7/6)
        theLazySong()
        time.sleep(19/15)
        whoLetTheDogsOut()
        time.sleep(62/15)
        shaky()
        time.sleep(89/30)
        OppaGangnamStyle()
        time.sleep(0.8)
        ladyGaga()
        time.sleep(1)
        aullar(5)
        time.sleep(1.2)
        risa(0.1)
    except(KeyboardInterrupt):
        print("Programa terminado por el usuario")
        GPIO.cleanup()
#Funcion para mantener la posicion
def holdPosition():
    for i in range(nbPCAServo):
        #print("Send angle {} to Servo {}".format(angle[i],i))
        pca.servo[i].angle = angle[i]
        time.sleep(0.001)
#Funcion donde se implementa cinematica inversa
def IK():
    A=[0.0,0.0,0.0,0.0]
    B=[0.0,0.0,0.0,0.0]
    C=[0.0,0.0,0.0,0.0]
    D=[0.0,0.0,0.0,0.0]
    E=[0.0,0.0,0.0,0.0]
    s=[0.0,0.0,0.0,0.0]
    thetaX=[0.0,0.0,0.0,0.0]
    thetaY=[0.0,0.0,0.0,0.0]
    
    for n in range(4):
        if pitch>=0:
            if n==1 or n==3:
                thetaX[n] = math.atan2(x[n]+ 155*(1 - math.cos((pitch * math.pi) / 180)) , c[n])
                d[n] = ((c[n] - z[n]) + 155 * math.sin((pitch*math.pi)/180)) / math.cos(thetaX[n])
                fo[n] = math.sqrt(pow(g,2)+pow(c[n],2))
                fn[n] = math.sqrt(pow(g,2)+pow(d[n],2))
                thetaY[n] = math.atan2(math.sin((90+math.atan2(g, c[n])*y[n])/fn[n]),(pow(fo[n],2)+pow(fn[n],2)-pow(y[n],2))/(2*fo[n]*fn[n]))
            if n==0 or n==2:
                thetaX[n] = math.atan2(x[n]- 155*(1 - math.cos((pitch*math.pi)/180)) , c[n])
                d[n] = ((c[n] - z[n]) - 155 * math.sin((pitch*math.pi)/180)) / math.cos(thetaX[n])
                fo[n] = math.sqrt(pow(g,2)+pow(c[n],2))
                fn[n] = math.sqrt(pow(g,2)+pow(d[n],2))
                thetaY[n] = math.atan2(math.sin((90+math.atan2(g, c[n])*y[n])/fn[n]),(pow(fo[n],2)+pow(fn[n],2)-pow(y[n],2))/(2*fo[n]*fn[n]))
        else:
            if n == 0 or n == 2:
                s[n] = x[n] + 155*(1 - math.cos((pitch*math.pi)/180))
                thetaX[n] = math.atan2(s[n], c[n])
                d[n] = ((c[n] - z[n]) - 155 * math.sin((pitch*math.pi)/180)) / math.cos(thetaX[n])
                fo[n] = math.sqrt(pow(g,2)+pow(c[n],2))
                fn[n] = math.sqrt(pow(g,2)+pow(d[n],2))
                thetaY[n] = math.atan2(math.sin((90+math.atan2(g, c[n])*y[n])/fn[n]),(pow(fo[n],2)+pow(fn[n],2)-pow(y[n],2))/(2*fo[n]*fn[n]))
            if n == 1 or n == 3:
                s[n] = x[n] - 155*(1 - math.cos((pitch*math.pi)/180))
                thetaX[n] = math.atan2(s[n], c[n])
                d[n] = ((c[n] - z[n]) + 155 * math.sin((pitch*math.pi)/180)) / math.cos(thetaX[n])
                fo[n] = math.sqrt(pow(g,2)+pow(c[n],2))
                fn[n] = math.sqrt(pow(g,2)+pow(d[n],2))
                thetaY[n] = math.atan2(math.sin((90+math.atan2(g, c[n])*y[n])/fn[n]),(pow(fo[n],2)+pow(fn[n],2)-pow(y[n],2))/(2*fo[n]*fn[n]))
    for n in range(4):
        A[n] = math.acos((pow(b, 2) + pow(d[n], 2) - pow(a, 2)) / (2 * b * d[n]))
        B[n] = math.acos((pow(a, 2) + pow(d[n], 2) - pow(b, 2)) / (2 * a * d[n]))
        C[n] = math.acos((pow(a, 2) + pow(b, 2) - pow(d[n], 2)) / (2 * a * b))
        D[n] = 90 - ((C[n] * 180) / math.pi)
        E[n] = math.acos((pow(g,2) + pow(fn[n],2) - pow(d[n],2))/(2 * g * fn[n]))
    for i in range(16):
        if i == 0:
            if C[0] >= math.pi / 2:
                angle[i] = servoref[i] + abs(D[0])
            else:
                angle[i] = servoref[i] - abs(D[0])
        elif i == 1:
            angle[i] = servoref[i] - ((B[0] * 180) / math.pi) + ((thetaX[0] * 180) / math.pi)
        elif i == 2:
            angle[i] = servoref[i] + ((E[0] * 180) / math.pi) + ((thetaY[0] * 180) / math.pi)
        elif i == 4:
            if C[1] >= math.pi / 2:
                angle[i] = servoref[i] + abs(D[1])
            else:
                angle[i] = servoref[i] - abs(D[1])
        elif i == 5:
            angle[i] = servoref[i] - ((B[1] * 180) / math.pi) + ((thetaX[1] * 180) / math.pi)
        elif i == 6:
            angle[i] = servoref[i] + ((E[1] * 180) / math.pi) - ((thetaY[1] * 180) / math.pi)
        elif i == 8:
            angle[i] = servoref[i] + ((E[3] * 180) / math.pi) - ((thetaY[3] * 180) / math.pi)
        elif i == 9:
            angle[i] = servoref[i] + ((B[3] * 180) / math.pi) - ((thetaX[3] * 180) / math.pi)
        elif i == 10:
            if C[3] >= math.pi / 2:
                angle[i] = servoref[i] - abs(D[3])
            else:
                angle[i] = servoref[i] + abs(D[3])
        elif i == 12:
            angle[i] = servoref[i] + ((E[2] * 180) / math.pi) + ((thetaY[2] * 180) / math.pi)
        elif i == 13:
            angle[i] = servoref[i] + ((B[2] * 180) / math.pi) - ((thetaX[2] * 180) / math.pi)
        elif i == 15:
            if C[2] >= math.pi / 2:
                angle[i] = servoref[i] - abs(D[2])
            else:
                angle[i] = servoref[i] + abs(D[2])
        else:
            angle[i] = servoref[i]
"""Funciones de movimiento"""
#Función para que el robot avance hacia adelante
def forward():
    for x[0] in range(0, 41, 2):
        x[3] = x[0]
        z[0] = math.sqrt(400 - pow((x[0] - 20),2))
        z[3] = math.sqrt(400 - pow((x[3] - 20),2))
        
        x[1]=x[2]=-x[0]

        IK()
        holdPosition()

    for x[0] in range(40, -1, -2):
        x[3] = x[0]
        
        x[1]=x[2]=-x[0]
        z[1] = math.sqrt(400 - pow((x[1] + 20),2))
        z[2] = math.sqrt(400 - pow((x[2] + 20),2))
        
        IK()
        holdPosition()
#Función para que el robot se mueva hacia atras
def backward():
    #Paso A
    for x[0] in range(0,-41,-2):
        z[0]=math.sqrt(pow(20,2)-pow((x[0]+20),2))

        x[1]=-x[0]
        x[2]=-x[0]

        x[3]=x[0]
        z[3]=math.sqrt(pow(20,2)-pow((x[3]+20),2))

        IK()
        holdPosition()
    #Paso B
    for x[0] in range(-40,1,2):

        x[1]=-x[0]
        z[1]=math.sqrt(pow(20,2)-pow((x[1]-20),2))

        x[2]=-x[0]
        z[2]=math.sqrt(pow(20,2)-pow((x[2]-20),2))

        x[3]=x[0]

        IK()
        holdPosition()
#Función para que el robot se mueva hacia la derecha
def right():
    for y[0] in range(0 , 41, 4):
        y[3] = y[0]
        z[0] = math.sqrt(400 - pow((y[0] - 20), 2))
        z[3] = math.sqrt(400 - pow((y[3] - 20), 2))

        y[1]=y[2]=-y[0]
        
        IK()
        holdPosition()
    for y[0] in range(40, -1, -4):
        y[3] = y[0]
        
        y[1]=y[2]=-y[0]
        
        z[1]= math.sqrt(400-pow((y[1]+20),2))
        z[2]= math.sqrt(400-pow((y[2]+20),2))
        
        IK()
        holdPosition()    
#Función para que el robot se mueva hacia la izquierda
def left():
    #Paso A
    for y[0] in range(0,-41,-2):
        z[0]=math.sqrt(pow(20,2)-pow((y[0]+20),2))

        y[1]=-y[0]
        
        y[2]=-y[0]

        y[3]=y[0]
        z[3]=math.sqrt(pow(20,2)-pow((y[3]+20),2))

        IK()
        holdPosition()
    #Paso B
    for y[0] in range(-40,1,2):

        y[1]=-y[0]
        z[1]=math.sqrt(pow(20,2)-pow((y[1]-20),2))

        y[2]=-y[0]
        z[2]=math.sqrt(pow(20,2)-pow((y[2]-20),2))

        y[3]=y[0]

        IK()
        holdPosition()
#Funcion para girar a la izquierda
def yaw_left():
    #Paso A
    for y[0] in range(0,61,1):
        z[0]=math.sqrt(pow(30,2)-pow((y[0]-30),2))

        y[1]=y[0]
        
        y[2]=-y[0]

        y[3]=-y[0]
        z[3]=math.sqrt(pow(30,2)-pow((y[3]+30),2))

        IK()
        holdPosition()
    #Paso B
    for y[0] in range(60,-1,-1):

        y[1]=y[0]
        z[1]=math.sqrt(pow(30,2)-pow((y[1]-30),2))

        y[2]=-y[0]
        z[2]=math.sqrt(pow(30,2)-pow((y[2]+30),2))

        y[3]=-y[0]

        IK()
        holdPosition()
#Funcion para girar a la derecha
def yaw_right():
    #Paso A
    for y[0] in range(0,61,1):

        y[1]=y[0]
        z[1]=math.sqrt(pow(30,2)-pow((y[1]-30),2))
        
        y[2]=-y[0]
        z[2]=math.sqrt(pow(30,2)-pow((y[2]+30),2))

        y[3]=-y[0]

        IK()
        holdPosition()
    #Paso B
    for y[0] in range(60,-1,-1):
        z[0]=math.sqrt(pow(30,2)-pow((y[0]-30),2))

        y[1]=y[0]

        y[2]=-y[0]

        y[3]=-y[0]
        z[3]=math.sqrt(pow(30,2)-pow((y[3]+30),2))

        IK()
        holdPosition()
"""Funciones de pasos de baile"""
#Funcion que pasa de posicion agachado a parado lentamente
def levantar(angulo, tiempo):
    servoref[14]=servoref[14]-40
    c[0]-=40
    c[1]-=50
    c[2]-=15
    c[3]-=45
    IK()
    holdPosition()
    time.sleep(5)
    print("Que suene la musica maestro")
    while c[0]!=186.81 or c[1]!=186.81 or c[2]!=186.81 or c[3]!=186.81:
        if c[0]!=186.81:
            c[0]+=angulo
        if c[1]!=186.81:
            c[1]+=angulo
        if c[2]!=186.81:
            c[2]+=angulo
        if c[3]!=186.81:
            c[3]+=angulo
        IK()
        holdPosition()
        time.sleep(tiempo)
    pca.servo[7].angle = servoref[7]-45
    time.sleep(0.5)
    pca.servo[7].angle = servoref[7]+45
    time.sleep(0.5)
    pca.servo[7].angle = servoref[7]
    time.sleep(0.6)
    servoref[14]=servoref[14]+40
    IK()
    holdPosition()
#Funcion para realizar un pisoton con la pierna delantera derecha
def pisotonDer():
    for y[1] in range(0,-91,-10):
        z[1]=math.sqrt(pow(45,2)-pow((y[1]+45),2)) 
        IK()
        holdPosition()
    for y[1] in range(-90,1,10):
        IK()
        holdPosition()
#Funcion para realizar un pisoton con la pierna delantera izquierda
def pisotonIz():
    for y[3] in range(0,-91,-10):
        z[3]=math.sqrt(pow(45,2)-pow((y[3]+45),2))
        IK()
        holdPosition()
    for y[3] in range(-90,1,10):
        IK()
        holdPosition()
#funcion para inclinar el robot hacia la derecha
def roll_der(tiempo):
    c[0]-=40
    c[1]-=40
    IK()
    holdPosition()
    time.sleep(tiempo)
    c[0]+=40
    c[1]+=40
    IK()
    holdPosition()
#funcion para inclinar el robot hacia la izquierda
def roll_iz(tiempo):
    c[2]-=40
    c[3]-=40
    IK()
    holdPosition()
    time.sleep(tiempo)
    c[2]+=40
    c[3]+=40
    IK()
    holdPosition()
#Funcion para alternar el pitch
def pitchAlterna():
    global pitch
    #se inclina hacia atras
    while pitch<5:
        pitch += 1
        IK()
        holdPosition()
        time.sleep(0.05)
    #se inclina hacia adelante
    while pitch>-5:
        pitch-=1
        IK()
        holdPosition()
        time.sleep(0.05)
    #regresa a su posicion inicial
    while pitch<=-1:
        pitch+=1
        IK()
        holdPosition()
        time.sleep(0.05)
    print("{}" .format(pitch))
#Funcion que simula la acción de morder
def morder(tiempo):
    pca.servo[11].angle = servoref[11]+6 #Boca abierta
    time.sleep(tiempo)
    pca.servo[11].angle = servoref[11] #Boca cerrada
#Funcion que mueve la cabeza a la izquierda 
def cabezaIz(angulo,tiempo):
    #Cr [7]  izquierda(180) medio(90) derecha(0)
    pca.servo[7].angle = servoref[7]+angulo
    time.sleep(tiempo)
    pca.servo[7].angle = servoref[7]
#Funcion que mueve la cabeza a la derecha 
def cabezaDer(angulo,tiempo):
    #Cr [7]  izquierda(180) medio(90) derecha(0)
    pca.servo[7].angle = servoref[7]-angulo
    time.sleep(tiempo)
    pca.servo[7].angle = servoref[7]
#Funcion que mueve la cola hacia la derecha
def cola_der(tiempo):
    #Sc [3] izquierda(70) medio(90) derecha(110)
    pca.servo[3].angle = 110
    time.sleep(tiempo)
    pca.servo[3].angle = 90
#Funcion que mueve la cola hacia la izquierda
def cola_iz(tiempo):
    #Sc [3] izquierda(70) medio(90) derecha(110)
    pca.servo[3].angle = 70
    time.sleep(tiempo)
    pca.servo[3].angle = 90
#Funcion para que el robot haga una flexion
def flexion(tiempo):
    #Baja el torso
    c[0] -=30
    c[1] -=30
    c[2] -=30
    c[3] -=30
    IK()
    holdPosition()
    time.sleep(tiempo)
    #Sube el torso
    c[0] +=30
    c[1] +=30
    c[2] +=30
    c[3] +=30
    IK()
    holdPosition()
#Funcion para que el robot aulle
def aullar(tiempo):
    #Se bajan las patas traseras
    c[0]-=25
    c[2]-=25
    #Se suben la delanteras
    c[1]+=5
    c[3]+=5
    IK()
    holdPosition()
    morder(tiempo)
    #Se levantan las patas traseras
    c[0]+=25
    c[2]+=25
    #Se bajan las delanteras
    c[1]-=5
    c[3]-=5
    IK()
    holdPosition()
#Funcion que simula una risa malvada
def risa(tiempo):
    #Cervical [14]
    ceArriba = servoref[14]
    ceAbajo = servoref[14]-60
    #Craneo [7]
    crMedio = servoref[7]
    crDerecho = servoref[7]-80
    while(ceArriba != ceAbajo or crMedio != crDerecho):
        if(ceArriba != ceAbajo):
            ceArriba = ceArriba - 2
            pca.servo[14].angle = ceArriba
        if crMedio != crDerecho:
            crMedio = crMedio - 4
            pca.servo[7].angle = crMedio
        morder(0.1)
        time.sleep(tiempo)
#Funcion para mover los hombros
def hombros(paso, tiempo):
    #Primero
    c[1]+=paso
    c[3]-=paso
    IK()
    holdPosition()
    time.sleep(tiempo)
    #Segundo
    c[1]-=2*paso
    c[3]+=2*paso
    IK()
    holdPosition()
    time.sleep(tiempo)
    #Tercero
    c[1]+=paso
    c[3]-=paso
    IK()
    holdPosition()
#Funcion para sacudir las extremidades inferiores
def terremoto(paso, tiempo):
    #Primero
    c[0]+=paso
    c[2]-=paso
    IK()
    holdPosition()
    time.sleep(tiempo)
    #Segundo
    c[0]-=2*paso
    c[2]+=2*paso
    IK()
    holdPosition()
    time.sleep(tiempo)
    #Tercero
    c[0]+=paso
    c[2]-=paso
    IK()
    holdPosition()
#funcion para cabecear
def cabecear(angulo, tiempo):
    #cervical [14] 130 alto, 110 medio y 40 bajo
    pca.servo[14].angle = servoref[14] - angulo
    time.sleep(tiempo)
    pca.servo[14].angle = servoref[14]
    time.sleep(tiempo)
#Funcion que combina cervical con craneo
def ceCr():
    #Parte 1
    pca.servo[14].angle = servoref[14]+3 #sube
    pca.servo[7].angle = servoref[7]+10 #izquierda
    time.sleep(0.2)
    pca.servo[14].angle = servoref[14]+6 #sube
    pca.servo[7].angle = servoref[7] #medio
    time.sleep(0.2)
    pca.servo[14].angle = servoref[14]+9 #sube
    pca.servo[7].angle = servoref[7]+10 #izquierda
    time.sleep(0.4)
    #Parte 2
    pca.servo[14].angle = servoref[14]+12 #sube
    pca.servo[7].angle = servoref[7]-10 #derecha
    time.sleep(0.2)
    pca.servo[14].angle = servoref[14]+15 #sube
    pca.servo[7].angle = servoref[7] #medio
    time.sleep(0.2)
    pca.servo[14].angle = servoref[14]+18 #sube
    pca.servo[7].angle = servoref[7]-10 #derecha
    time.sleep(0.2)
#Funcion para que el robot haga una reverencia
def reverencia():
    print("reverencia")
#Funcion para variar el roll suavemente
def rollVaria(paso,tiempo):
    #se inclina a la derecha
    for i in range(paso):
        c[0]-=1
        c[1]-=1
        c[2]+=1
        c[3]+=1
        IK()
        holdPosition()
        time.sleep(tiempo)
    #se inclina a la izquierda
    for i in range(paso*2):
        c[0]+=1
        c[1]+=1
        c[2]-=1
        c[3]-=1
        IK()
        holdPosition()
        time.sleep(tiempo)
    #regresa a su posicion inicial
    for i in range(paso):
        c[0]-=1
        c[1]-=1
        c[2]+=1
        c[3]+=1
        IK()
        holdPosition()
        time.sleep(tiempo)
"""Canciones"""
def thriller():
    #Parte 1
    levantar(1,0.162)
    time.sleep(26/15) #ajustar
    #Parte 2
    forward()
    time.sleep(0.25)
    cabezaIz(20,0.1)
    time.sleep(0.05)
    backward()
    time.sleep(0.25)
    cabezaDer(20,0.1)
    time.sleep(0.05)
    forward()
    time.sleep(0.25)
    cabezaIz(20,0.1)
    time.sleep(0.05)
    backward()
    time.sleep(0.25)
    cabezaDer(20,0.1)
    time.sleep(0.5)    
    #Parte 3
    roll_iz(1.25)
    time.sleep(0.25)
    cabezaIz(20,0.1) 
    time.sleep(0.35)
    roll_der(1.25)
    time.sleep(0.25)
    cabezaDer(20,0.1)
    time.sleep(2.2)
    #Parte 4
    pisotonIz()
    time.sleep(0.4)
    pisotonDer()
    time.sleep(0.5)
    'Subir cervical y bajar lentamente'
    for num in range(24,-1,-2):
        pca.servo[14].angle = servoref[14]+num
        time.sleep(0.1)
def theLazySong():
    #Posicion neutral
    pca.servo[14].angle = servoref[14]
    pca.servo[7].angle = servoref[7]
    #Parte 1
    for i in range(6):
        cabecear(5,0.3)
    time.sleep(0.3)
    ceCr()
    pca.servo[7].angle = servoref[7]
    #Parte 2
    for i in range(6):
        cabecear(5,0.3)
    time.sleep(0.35)
    ceCr()
    time.sleep(0.4)
    #Posicion neutral
    pca.servo[14].angle = servoref[14]
    pca.servo[7].angle = servoref[7]
def whoLetTheDogsOut():
    for i in range(3):
        time.sleep(2)
        morder(0.1)
        time.sleep(0.4)
        morder(0.1)
        time.sleep(0.35)
        morder(0.1)
        time.sleep(0.25)
        morder(0.1)
        time.sleep(0.20)
        morder(0.1)        
def shaky():
    #Parte 1
    time.sleep(0.7)
    for i in range(3):
        terremoto(3,0.05)
    time.sleep(0.7)
    for i in range(3):
        terremoto(3,0.05)
    time.sleep(0.7)
    for i in range(3):
        terremoto(3,0.05)
    cola_iz(0.5)
    cola_der(0.5)
    #Parte 2
    time.sleep(1.2)
    for i in range(3):
        terremoto(3,0.05)
    time.sleep(0.7)
    for i in range(3):
        terremoto(3,0.05)
    time.sleep(0.7)
    for i in range(3):
        terremoto(3,0.05)
    cola_iz(0.5)
    cola_der(0.5)
def OppaGangnamStyle():
    #Parte 1
    rollVaria(5,0.02)
    rollVaria(5,0.02)
    time.sleep(13/15)
    pisotonIz()
    pisotonDer()
    pisotonIz()
    pisotonIz()
    #Parte 2
    time.sleep(0.63)
    rollVaria(5,0.02)
    rollVaria(5,0.02)
    time.sleep(19/15)
    pisotonDer()
    pisotonIz()
    pisotonDer()
    pisotonDer()
def ladyGaga():
    #Parte 1
    servoref[14]=servoref[14]+20
    hombros(5,0.5)
    time.sleep(0.5)
    servoref[14]=servoref[14]-20
    hombros(5,0.5)
    time.sleep(0.6)
    hombros(5,0.5)
    time.sleep(0.7)
    pitchAlterna()
    time.sleep(0.5)    
    #Parte 2
    servoref[14]=servoref[14]+20
    hombros(5,0.5)
    time.sleep(0.5)
    servoref[14]=servoref[14]-20
    hombros(5,0.5)
    time.sleep(0.6)
    pitchAlterna()
    pitchAlterna()
#Llamado a la funcion principal
main()