from Sensor import Sensor
from UltimaLectura import ultimaLectura
from Lista import Lista
import random
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from Api import Api
import time
class Sensores:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.sensores = Sensor()
        self.historico = ultimaLectura()
        self.api=Api()
        self.puerto = '/dev/ttyUSB0'
        self.baudios = 9600
        self.ledInternet=5
        self.ledApi=20
        self.ledPost=13
        GPIO.setup(self.ledInternet, GPIO.OUT)
    

        self.ledOff(self.ledInternet)
   
        

    # def lecturaSerial(self):
    #     ser = serial.Serial(self.puerto, self.baudios, timeout=1)
    #     ser.reset_input_buffer()
    #     while True:
    #         if ser.in_waiting > 0:
    #             line = ser.readline().decode('utf-8').rstrip()
    #             return line
    
    def guardarDatos(self, data, redStatus, apiStatus):
        newSensor = Sensor(data)
        if not redStatus or not apiStatus:
            self.historico.agregar(newSensor.to_dict())
            print("guardando en historico")
        else:
            historial=self.historico.mostrar()
            if len(historial) > 0:
                x=0
                for sens in historial:
                    file = sens["clave"] + ".json"
                    Lista(file).agregar(sens)
                    self.historico.eliminar(x)
                    x+=1
            file = data["clave"] + ".json"
            Lista(file).agregar(newSensor.to_dict())
            #aqui va la insercion a mongo desde la api
            sensor= newSensor.to_dict()
            dataApi={
                "clave":sensor["clave"],
                "tipo":sensor["tipo"],
                "valores":sensor["valores"],
                "dato":sensor["dato"],
                "fecha":sensor["fecha"],
                "hora":sensor["hora"],
                "pines":sensor["pines"],
                "file":sensor["file"]
            }
            dataFalsa={
                "clave":"prueba",
                "tipo":"prueba_5",
                "valores":50,
                "dato":"prueba",
                "fecha":"prueba",
                "hora":"prueba",
                "pines":"prueba",
                "file":"prueba"
            }
            print(dataApi)
            if not self.api.post_data(dataFalsa):
                self.historico.agregar(newSensor.to_dict())
            #aaaaaaaaaaaaaaaaaa
            horaPrincipal= Lista(file).mostrar()[0]["hora"]
            horaTurno= Lista(file).mostrar()[len(Lista(file).mostrar())-1]["hora"]
            if datetime.strptime(horaTurno, "%H:%M:%S")-timedelta(minutes=5)>=datetime.strptime(horaPrincipal, "%H:%M:%S"):
                Lista(file).borrarInfo()

    def ledOn(self,led):
        print("Sucedio algooooooooo aaaaaaaaaaaa")
        GPIO.output(led, GPIO.HIGH)
    def ledOff(self,led):
        print("SE APAGOOOOO aaaaaaaaaaaa")
        GPIO.output(led, GPIO.LOW)



    def checkarHistorico(self):
        dataHistorial=self.historico.to_dict()
        return dataHistorial
    

    

if __name__ == "__main__":

    #for i in range(5):
        valorRandom=random.randint(2, 60)
        #asi debe quedar el json que se reciba o al menos tener esos datos desde el arduino, menos dispositivo
        data = {
            "clave": "Ult2",
            "tipo": "temperatura",
            "valores": valorRandom,
            "dato": "C",
            "pines": "2,3",
            "dispositivo": "carrito1"
        }

        sens=Sensores()
        inter=sens.api.check_internet()
        ap=False
        if inter:
            sens.ledOn(sens.ledInternet)
            ap=sens.api.check_api()
        nuevo=sens.guardarDatos(data,inter,ap)




