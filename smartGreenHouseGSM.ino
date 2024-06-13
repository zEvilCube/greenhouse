#include <LiquidCrystal.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>
#define IRRIGATION_TIME 10
#define MAX_BRIGHTNESS_LUX 1000
#define BRIGHTNESS_SETPOINT 700
#define TEMPERATURE_SETPOINT 25
#define MOISTURE_SETPOINT 50
#define MOISTURE_DEVIDER 388.74
#define DELTA 1
#define MAX_BRIGHTNESS_SETPOINT 999
#define MIN_BRIGHTNESS_SETPOINT 299
#define MAX_TEMPERATURE_SETPOINT 45
#define MIN_TEMPERATURE_SETPOINT 15
#define MAX_MOISTURE_SETPOINT 99
#define MIN_MOISTURE_SETPOINT 9
//Размер буфера gsm
#define GSM_BUFFER 64
// сигнальный провод датчика
#define ONE_WIRE_BUS 10
// создаём объект для работы с библиотекой OneWire
OneWire oneWire(ONE_WIRE_BUS);
 
// создадим объект для работы с библиотекой DallasTemperature
DallasTemperature sensor(&oneWire);
float ticksPerSecond = 49910; //1 секунда
LiquidCrystal lcd(9,8,7,6,5,4);

SoftwareSerial GSM(2, 3);
unsigned char gsmBuffer[GSM_BUFFER];
int gsmCount=0; 

String msgFromEsp="";
String msgToEsp="";
//String testMsgToEsp="";//временная переменная
String parsed="";
char charMsg[16];

bool lightFlag = false;
bool lightTestFlag = false;
bool lightOnFlag = false;
bool moistureFlag = false;
bool moistureTestFlag = false;
bool irrigationFlag = false;
bool coolFlag = false;
bool hotFlag = false;
bool tempFlag = false;
bool tempTestFlag = false;
bool loadingFlag = true;
bool doParsing = false;
bool doGsmParsing = false;
bool sendInfoFlag = false;
bool skipSendFlag = true;
bool irgCheckFlag = false;
bool atFlag = false;
bool smsFlag = false;
//bool testFlag = false; //временный удалить
int minute = 0;
int hour = 0;
int second = 0;

int irrigationTime = 0;
int openBracket = 0;
int closeBracket = 0;

//выходы
int irrigation = A5; // левое синее реле включается low
int cooler = A4; // правое синее реле включается low
int heater = A3; // левое красное реле включается high
int light = A2; // правое красное реле ключается high

//входы
int brightness = A1;
int moisture = A0;
int temperature = ONE_WIRE_BUS;

//Показатели датчиков
float temperatureProbe = 0;
float brightnessProbe = 0;
float moistureProbe = 0;

//Уставка
int temperatureSetpoint = TEMPERATURE_SETPOINT;
int brightnessSetpoint = BRIGHTNESS_SETPOINT;
int moistureSetpoint = MOISTURE_SETPOINT;

//GSM Уставка
int temperatureGsmSetpoint = TEMPERATURE_SETPOINT;
int brightnessGsmSetpoint = BRIGHTNESS_SETPOINT;
int moistureGsmSetpoint = MOISTURE_SETPOINT;
String lastGsmPhoneNumber = "phone_number";
String convert(char[],int);

String convert(char* buffer,int lenght){
  String result;
  String stringToParse;
  int counter;
  for(int i=0;i<lenght;i++){
      switch (buffer[i]){
        case 'O':
          if(i+1<lenght){
            if(buffer[i+1]=='K'){
              result.concat("1");//флаг что связь с модемом есть и мы можем принимать и отправлять сообщения, до этого  мы ничего не парсим и не отправляем
              atFlag = true;
            }
          }
          break;
        case 'i':
        case 'I':
          if(i+1<lenght){
              if((buffer[i+1]=='N') || (buffer[i+1]=='n')){
                result.concat("2");//флаг отправки смс
                smsFlag = true;
              }
            }
          break;
        case 'b':
        case 'B':
          if(i+1<lenght){
            if(buffer[i+1]==':' ){
              counter =i+2;
              while(counter != lenght ){
                if(buffer[counter]!=';'){
                  stringToParse.concat(buffer[counter]);
                }
                counter++;
              }
              brightnessGsmSetpoint = stringToParse.toInt();
              result.concat("B:");
              result.concat("stringToParse");
              result.concat("l");
              //парсим овещенность и concat-им отпрарсенную строку в  виде B:800l
              counter=0;
              stringToParse = "";  
            }
          }
          break;
        case 'm':
        case 'M':
          if(i+1<lenght){
            if(buffer[i+1]==':' ){
              
              counter =i+2;
              while(counter != lenght ){
                if(buffer[counter]!=';'){
                  stringToParse.concat(buffer[counter]);
                }
                counter++;
              }
              moistureGsmSetpoint = stringToParse.toInt();
              result.concat("M:");//парсим влажность и concat-им отпрарсенную строку в  виде M:80% 
              result.concat("stringToParse");
              result.concat("%");
              counter=0;
              stringToParse = ""; 
            }
          }
          break;
        case 't':
        case 'T':
          if(i!=0){
            if(buffer[i-1]!='M'){
              if(i+1<lenght){
                if(buffer[i+1]==':' ){
                  result.concat("T");
                  counter =i+2;
                  while(counter != lenght ){
                    if(buffer[counter]!=';'){
                      stringToParse.concat(buffer[counter]);
                    }
                    counter++;
                  }
                  temperatureGsmSetpoint = stringToParse.toInt();
                  result.concat("T:");//парсим температуру и concat-им отпрарсенную строку в  виде T:25C
                  result.concat("stringToParse");
                  result.concat("C");
                  counter=0;
                  stringToParse = ""; 
                }
              }
            }
          }
          break;
        case '+':
          if(i+1<lenght){
            if(buffer[i+1]=='7' ){
              result.concat("+7");
              lastGsmPhoneNumber.concat("+7");
              for(int j =i+2;j<i+12;j++){
                lastGsmPhoneNumber.concat(buffer[j]);
              }
              //парсим номер телефона и запихиваем в отдельную строку
            }
          }
          break;
      }
      //result.concat(buffer[i]);
  }
  return result;
}

void setup() {
  // put your setup code here, to run once:

  //выходы
  pinMode(irrigation, OUTPUT);
  pinMode(cooler, OUTPUT);
  pinMode(heater,OUTPUT);
  pinMode(light, OUTPUT);
  //входы
  pinMode(brightness, INPUT);
  pinMode(moisture, INPUT);
  pinMode(temperature,INPUT);
  digitalWrite(irrigation,HIGH);
  digitalWrite(cooler,HIGH);
  lcd.begin(16, 2);
  // начинаем работу с датчиком
  sensor.begin();
  // устанавливаем разрешение датчика от 9 до 12 бит
  sensor.setResolution(12);
  noInterrupts();                       // отключаем все прерывания
  
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = ticksPerSecond;                        // preload timer
  TCCR1B |= (1 << CS10)|(1 << CS12);    // 1024 prescaler (коэффициент деления предделителя)
  TIMSK1 |= (1 << TOIE1);               // enable timer overflow interrupt ISR (разрешаем вызов процедуры обработки прерывания переполнения счетчика)
  interrupts();                         // разрешаем все прерывания
  //Установливаем связь Wi-Fi
  Serial.begin(9600);
  //Связь с GPRS модемом
  GSM.begin(9600);
}

ISR(TIMER1_OVF_vect)                    // процедура обработки прерывания переполнения счетчика
{
  second++;
  if(second==60)
  {
    second = 0;
    minute++;
  }
  if(minute == 60)
  {
    minute = 0;
    hour++;
  }
  if(hour == 24)
  {
    hour == 0;    
  }
  TCNT1 = ticksPerSecond;
  if(!irrigationFlag && minute==1 && second==0)
  {
    irrigationFlag = true;
  }
  if(!moistureFlag && second == 0)
  {
    moistureFlag = true;
    tempFlag = false;
    moistureTestFlag = true;
  }
  if(!lightFlag && second == 20)
  {
    lightFlag = true;
    lightTestFlag = true; 
    loadingFlag = false;
    moistureFlag = false;
  }
  if(!tempFlag && second == 40)
  {
    tempFlag = true;
    tempTestFlag = true;
    lightFlag = false;
  }
  if(!sendInfoFlag && second == 50 ){
    if(!skipSendFlag){
      sendInfoFlag = true;
    }
    else{
      skipSendFlag=false;
    }
  }
}
void loop() {
  // put your main code here, to run repeatedly:
  lcd.print(hour);
  lcd.print(":");
  lcd.print(minute);
  lcd.print(":");
  lcd.print(second);

 
  if(doParsing)
  {
    openBracket = msgFromEsp.indexOf("humidity");
    if(openBracket!=-1){

      closeBracket = msgFromEsp.indexOf("light");
      parsed = msgFromEsp.substring(openBracket+10,closeBracket-2);
      moistureSetpoint = parsed.toInt();
      if(moistureSetpoint>MAX_MOISTURE_SETPOINT){
        moistureSetpoint = MAX_MOISTURE_SETPOINT;
      }
      if(moistureSetpoint<MIN_MOISTURE_SETPOINT){
        moistureSetpoint = MIN_MOISTURE_SETPOINT;
      }
      openBracket = msgFromEsp.indexOf("light");
      closeBracket = msgFromEsp.indexOf("temperature");
      parsed = msgFromEsp.substring(openBracket+7,closeBracket-2);
      brightnessSetpoint = parsed.toInt();
      if(brightnessSetpoint>MAX_BRIGHTNESS_SETPOINT){
        brightnessSetpoint = MAX_BRIGHTNESS_SETPOINT;
      }
      if(brightnessSetpoint<MIN_BRIGHTNESS_SETPOINT){
        brightnessSetpoint = MIN_BRIGHTNESS_SETPOINT;
      }
      openBracket = msgFromEsp.indexOf("temperature");
      parsed = msgFromEsp.substring(openBracket+13);
      temperatureSetpoint = parsed.toInt();
      if(temperatureSetpoint>MAX_TEMPERATURE_SETPOINT){
        temperatureSetpoint = MAX_TEMPERATURE_SETPOINT;
      }
      if(temperatureSetpoint<MIN_TEMPERATURE_SETPOINT){
        temperatureSetpoint = MIN_TEMPERATURE_SETPOINT;
      }
      sprintf(charMsg,"Data: %d %d %d", moistureSetpoint,brightnessSetpoint,temperatureSetpoint);
      //msgFromEsp =parsed;
    }
    else{
       msgFromEsp.toCharArray(charMsg,17);
    }
    doParsing = false;
  }

  if(loadingFlag)
  {
    lcd.setCursor(0,1);
    if (msgFromEsp.length()>0){
      lcd.print(charMsg);
    }
    else{
      lcd.print("Loading...");
    }
  }
  
  if(moistureFlag)
  {
    if(moistureTestFlag)
    {
      moistureTestFlag = false;
      moistureProbe = analogRead(moisture);
      moistureProbe = 1023 - moistureProbe;
      if(moistureProbe > MOISTURE_DEVIDER)
      {
        moistureProbe = MOISTURE_DEVIDER;
      }
      moistureProbe = (moistureProbe/MOISTURE_DEVIDER)*100;
    }
    lcd.setCursor(0,1);
    lcd.print("Moisture %: ");
    lcd.print((int)moistureProbe);
    if(irrigationFlag)
    {
      irrigationFlag = false;
      //Проверка влажности
      //OLD if(moistureProbe < MOISTURE_SETPOINT )
      if(moistureProbe < moistureSetpoint )
      {
        //Если требуется полив
        digitalWrite(irrigation, LOW);
        irrigationTime = IRRIGATION_TIME;
        irgCheckFlag = true;
      }
      
      //Если не требуется полив  
    }
    lcd.setCursor(10,0);
    if(irrigationTime>0)
    {
      lcd.print("i:on");
      irrigationTime--;
    }
    else
    {
     lcd.print("i:off");
     irrigationFlag = false;
     digitalWrite(irrigation, HIGH);
    }
  }

  if(lightFlag)
  {
    if(second==23){
      GSM.print("AT\r");
    }
    

    if(lightTestFlag)
    {
      lightTestFlag = false;
      
      // Измеряем  освещенность
      brightnessProbe = analogRead(brightness);
      brightnessProbe = (brightnessProbe/1023)*MAX_BRIGHTNESS_LUX;
      //Проверка освещенности
      //OLD if(brightnessProbe < BRIGHTNESS_SETPOINT)
      if(brightnessProbe < brightnessSetpoint)
      {
        // Необходимо освещение
        digitalWrite(light, HIGH);
        lightOnFlag = true;
      }
      else
      {
        digitalWrite(light, LOW);
        lightOnFlag = false;
      }
    }
    lcd.setCursor(0,1);
    
    lcd.print("Brightness: ");
    lcd.print((int)brightnessProbe);
    
    lcd.setCursor(10,0);
    if(lightOnFlag)
    {
      lcd.print("l:on");
    }
    else
    {
      lcd.print("l:off");
    }
  }

  if(tempFlag)
  {
    if(tempTestFlag)
    {
      tempTestFlag = false;
      coolFlag = false;
      hotFlag  = false;
      sensor.requestTemperatures();
      temperatureProbe = sensor.getTempCByIndex(0);
      // 3 состояния 
      // 1 "cooler: on" "heating: off"
      /* OLD if(temperatureProbe > TEMPERATURE_SETPOINT + DELTA)
      {
        coolFlag = true;        
      }
      if(temperatureProbe < TEMPERATURE_SETPOINT - DELTA)
      {
        hotFlag = true;
      }*/
      if(temperatureProbe > temperatureSetpoint + DELTA)
      {
        coolFlag = true;        
      }
      if(temperatureProbe < temperatureSetpoint - DELTA)
      {
        hotFlag = true;
      }
      
    }
    lcd.setCursor(0,1);
    lcd.print("Temp C: ");
    lcd.print(temperatureProbe);
    lcd.setCursor(10,0);
    if(coolFlag)
    {
      lcd.print("c:on");
      digitalWrite(heater, LOW);
      digitalWrite(cooler, LOW);
    }
    else if(hotFlag)
    {
      lcd.print("h:on");
      digitalWrite(heater, HIGH);
      digitalWrite(cooler, HIGH);
    }
    else
    {
      lcd.print("ch:off");    
      digitalWrite(cooler, HIGH); 
      digitalWrite(heater, LOW); 
    }
  }
  /*if(testFlag){
    lcd.setCursor(0,0);
    lcd.print(testMsgToEsp);
    testFlag = false;
  }*/
  if(doGsmParsing && atFlag){
    lcd.setCursor(0,0);
    lcd.print(convert(gsmBuffer,gsmCount));
    doGsmParsing = false;
  }
  delay(1000);
  //Работа с wi-fi модулем esp
  while (Serial.available()) {
      msgFromEsp = Serial.readString();
      doParsing = true;
  }
  if(sendInfoFlag){ 
    msgToEsp ="";
    //testMsgToEsp="";
    msgToEsp.concat("tmp:");
    msgToEsp.concat((int)temperatureProbe);
    msgToEsp.concat("clr:");
    msgToEsp.concat((int)coolFlag);
    msgToEsp.concat("htr:");
    msgToEsp.concat((int)hotFlag);
    msgToEsp.concat("brt:");
    msgToEsp.concat((int)brightnessProbe);
    msgToEsp.concat("lmp:");
    msgToEsp.concat((int)lightOnFlag);
    msgToEsp.concat("mst:");
    msgToEsp.concat((int)moistureProbe);
    msgToEsp.concat("irg:");
    msgToEsp.concat((int)irgCheckFlag);
    irgCheckFlag = false;
    msgToEsp.concat("end:");
    Serial.print(msgToEsp);
    /*
    testMsgToEsp.concat((int)temperatureProbe);
    testMsgToEsp.concat((int)coolFlag);
    testMsgToEsp.concat((int)hotFlag);
    testMsgToEsp.concat((int)brightnessProbe);
    testMsgToEsp.concat((int)lightOnFlag);
    testMsgToEsp.concat((int)moistureProbe);
    testFlag = true;*/
    sendInfoFlag=false;
  }
  //Работа с GSM модулем
  if (GSM.available()){         // if date is comming from softwareserial port ==> data is comming from gprs shield
    gsmCount = 0;
    while(GSM.available()){          // reading data into char array 
      gsmBuffer[gsmCount++]=GSM.read();     // writing data into array
      if(gsmCount == GSM_BUFFER)break;
    }
    doGsmParsing = true;
  }
  lcd.clear();
}