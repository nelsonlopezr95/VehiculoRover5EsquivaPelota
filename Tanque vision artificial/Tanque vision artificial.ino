// Motor derecha
#define MotorDerechaB 4 	// Definimos constante para el motor derecho en el ping 3
#define MotorDerechaA 5		// Definimos constante para el motor derecho en el ping 4

// Motor izquierda
#define MotorIzquierdaA 6	// Definimos constante para el motor izquierdo en el ping 5
#define MotorIzquierdaB  7	// Definimos constante para el motor izquierdo en el ping 6
#include<SoftwareSerial.h>

SoftwareSerial mySerial(13,12); // Pin 2 RX, Pin 3 TX
int ENA = 3; 			// Velocidad motor A
int ENB = 11; 			// Velocidad motor B

//Pin Servo
const int servoPin = 2; 	// Pin para la señal del servomotor

//Angulo Inicial
const int angulo = 90;		// Angulo inicial del servimotor
int velocidadGiro = 190;	// Velociada para el giro cuando encuentre un angulo agudo
int velocidad = 80;		// Velocidad normal 

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(9600);
  //configuracion de los pines de salida
   pinMode(ENA, OUTPUT);	// Motor A
   pinMode(ENB, OUTPUT);	// Motor B
  //MOTOR DERECHO
  pinMode(MotorDerechaA, OUTPUT);   // Definimos el motor derecho como salidas
  pinMode(MotorDerechaB, OUTPUT);
  //MOTOR IZQUIERDO
  pinMode(MotorIzquierdaA , OUTPUT);// Definimos el motor izquierdo como salidas
  pinMode(MotorIzquierdaB , OUTPUT);
  mySerial.begin(9600);
}
char dato;
void loop() {
    
  if(mySerial.available()){        // Lee el bluetooth y almacena en estado
   dato=mySerial.read();
  }
  if(dato=='w')			   // Avanzar
  {
   Avanzar();
  }
  if(dato=='d')			   // Voltear derecha
  {
    derecha(); 
  }
   if(dato=='a')	           // Voltear izquierda
  {
    Izquierda();
  }
  if(dato=='q')			   // Parar
  {
    parar();
  }

}
void Avanzar()
{
 
  //MOTOR DERECHO
  digitalWrite(MotorDerechaB, HIGH);
  digitalWrite(MotorDerechaA, LOW);
  analogWrite(ENA, velocidad); //Velo7cidad del motor A 0
  //MOTOR IZQUEIDO
  digitalWrite(MotorIzquierdaA , LOW);
  digitalWrite(MotorIzquierdaB, HIGH);
  analogWrite(ENB, velocidad); //Velo7cidad del motor A 0
  Serial.println("Avanzando");
  
}
// MODULO PARA RETROCEDER TANQUE
void Retroceder()
{
   //MOTOR DERECHO 
  digitalWrite(MotorDerechaA, HIGH);
  digitalWrite(MotorDerechaB, LOW);
  analogWrite(ENA, 0); //Velo7cidad del motor A 0
  //MOTOR IZQUEIDO
  digitalWrite(MotorIzquierdaA , HIGH);
  digitalWrite(MotorIzquierdaB, LOW);
  analogWrite(ENB, 0); //Velo7cidad del motor A 0
  Serial.println("Parar");

}
// MODULO PARA GIRAR IZQUIERDA  TANQUE
void Izquierda()
{
  // MOTOR DERECHO
  digitalWrite(MotorDerechaA, HIGH);
  digitalWrite(MotorDerechaB, LOW);
   analogWrite(ENA, velocidadGiro);
  // MOTOR IZQUEIDO
  digitalWrite(MotorIzquierdaB, HIGH);
  digitalWrite(MotorIzquierdaA , LOW);
  analogWrite(ENB, velocidadGiro);
 

}
// MODULO PARA GIRAR DERECHA  TANQUE
void derecha()
{
  // MOTOR DERECHO
  digitalWrite(MotorDerechaB, HIGH);
  digitalWrite(MotorDerechaA, LOW);
  analogWrite(ENA, velocidadGiro);
  //MOTOR IZQUEIDO
  digitalWrite(MotorIzquierdaA , HIGH);
  digitalWrite(MotorIzquierdaB, LOW);
  analogWrite(ENB, velocidadGiro);

 

}
// MODULO PARA PARAR EL  TANQUE
void parar()
{
  digitalWrite(MotorDerechaA, LOW);
  digitalWrite(MotorDerechaB, LOW);
  analogWrite(ENA, 0);
  //MOTOR IZQUEIDO
  digitalWrite(MotorIzquierdaA , LOW);
  digitalWrite(MotorIzquierdaB, LOW);
  analogWrite(ENB, 0);
  Serial.println("Parar");

}
