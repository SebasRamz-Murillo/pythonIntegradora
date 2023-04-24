from Sensor import Sensor
from UltimaLectura import ultimaLectura
from Lista import Lista
import random
from gpiozero import LED
from datetime import datetime, timedelta
from Api import Api
import time
import serial
import json


class Sensores:
    def __init__(self):
        self.sensores = Sensor()
        self.historico = ultimaLectura()
        self.api = Api()
        self.puerto = '/dev/ttyACM0'  # hay doc conocidas "ttyACM0", "ttyUSB0", ACMO siendo el joystick y USB0 el sensor
        self.baudios = 9600
        # self.ledInternet = LED(17)
        # self.ledApi = LED(20)
        # self.ledPost = LED(13)
        # self.ledWInternet = LED(21)
        # print("Configurando canal: ", self.ledInternet)
        # GPIO.setup(self.ledInternet, GPIO.OUT)

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
            historial = self.historico.mostrar()
            if len(historial) > 0:
                x = 0
                for sens in historial:
                    file = sens["clave"] + ".json"
                    Lista(file).agregar(sens)
                    self.historico.eliminar(x)
                    x += 1
            file = data["clave"] + ".json"
            Lista(file).agregar(newSensor.to_dict())
            # aqui va la insercion a mongo desde la api
            sensor = newSensor.to_dict()
            dataApi = {
                "clave": sensor["clave"],
                "tipo": sensor["tipo"],
                "valores": sensor["valores"],
                "dato": sensor["dato"],
                "fecha": sensor["fecha"],
                "hora": sensor["hora"],
                "pines": sensor["pines"],
                "file": sensor["file"]
            }
            print(dataApi)
            if not self.api.post_data(newSensor.to_dict()):
                self.historico.agregar(newSensor.to_dict())
            horaPrincipal = Lista(file).mostrar()[0]["hora"]
            horaTurno = Lista(file).mostrar()[len(Lista(file).mostrar()) - 1]["hora"]
            if (datetime.strptime(horaTurno, "%H:%M:%S") - timedelta(minutes=5) >= datetime.strptime(horaPrincipal,
                                                                                                     "%H:%M:%S")) or len(
                    Lista(file).mostrar()) > 200:
                Lista(file).borrarInfo()

    def ledOn(self, led):
        print("Sucedio algooooooooo aaaaaaaaaaaa")
        # GPIO.output(led, GPIO.HIGH)
        led.on()

    def ledOff(self, led):
        print("SE APAGOOOOO aaaaaaaaaaaa")
        # GPIO.output(led, GPIO.LOW)
        led.off()

    def checkarHistorico(self):
        dataHistorial = self.historico.to_dict()
        return dataHistorial


if __name__ == "__main__":
    while True:
        valorRandom = random.randint(2, 60)
        sens = Sensores()
        Communication = serial.Serial(sens.puerto, sens.baudios)
        data = Communication.readline().decode().strip()
        print(data)
        # inter = sens.api.check_internet()
        # ap = True
        # if inter:
        #     try:
        #         sensor = json.loads(data)
        #         clave = sensor['clave']
        #         valor = sensor['valores']
        #         pines = "2,3"
        #         dispositivo = "carrito1"
        #         data = {
        #             "clave": clave,
        #             "valores": str(valor),
        #             "pines": pines,
        #             "dispositivo": dispositivo
        #         }
        #         print(data)
        #         nuevo = sens.guardarDatos(data, True, ap)
                #
                # if "clave" in sensor and sensor.get("dato") is not None:
                #     sensor['valores'] = sensor.pop('dato')
                #     sensor['pines'] = "5,3"
                #     sensor['dispositivo'] = 'carrito1'
                #     newSensor = Sensor(sensor)
                #     nuevo = sens.guardarDatos(newSensor.to_dict(), inter, ap)
                #     if nuevo:
                #         sens.ledOn(sens.ledPost)
                #         time.sleep(5)
                #         sens.ledOff(sens.ledPost)
                #         time.sleep(5)
                #     else:
                #         sens.ledOn(sens.ledWInternet)
                #         time.sleep(10)

                # Imprimir la lista de diccionarios con el nuevo parámetro "valores"
            except json.decoder.JSONDecodeError as e:
                print("Error al cargar la cadena JSON:", e)
        else:
            time.sleep(10)



    # for j in range(200):
    #     # asi debe quedar el json que se reciba o al menos tener esos datos desde el arduino, menos dispositivo
    #     claves = ["Ult1", "Ult2", "Pir0", "Pir1", "Bat1", "Bat2"]
    #     for k in range(len(claves)):
    #         valorRandom = random.randint(2, 60)
    #         data = {
    #             "clave": claves[k],
    #             "tipo": "temperatura",
    #             "valores": valorRandom,
    #             "dato": "C",
    #             "pines": "2,3",
    #             "dispositivo": "carrito1"
    #         }
    #         sens=Sensores()
    #         inter=sens.api.check_internet()
    #         ap=False
    #         sens.ledOn(sens.ledInternet)
    #         ap=sens.api.check_api()
    #         nuevo=sens.guardarDatos(data,True,ap)




