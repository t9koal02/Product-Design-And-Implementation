int sensor = 2;              // Liiketunnistimen output pin
int state = LOW;             
int val = 0;                 

int motionDetection(void);

void setup() {   
  pinMode(sensor, INPUT);    
  Serial.begin(9600);        
  }

void loop(){
  motionDetection();
}

int motionDetection(void) {
  val = digitalRead(sensor); // Luetaan liiketunnistimen arvo
  if (val == HIGH) {          
    Serial.println("1");   // Kun tila on HIGH (liikettä havaittu) tulostetaan sarjaportille 1
    delay(500);   // Puolen sekunnin viive, koska tunnistimen ei tarvitse olla tätä nopeampi
    if (state == LOW) {   // Kun liike lakkaa tulostetaan vielä yksi ykkönen
      Serial.println("1"); 
    }
  }
  else {
      Serial.println("0"); // Kun tila on LOW (ei liikettä) tulostetaan 0 
      delay(500);
  }
}
