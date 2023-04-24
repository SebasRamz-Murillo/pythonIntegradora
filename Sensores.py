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
        self.puerto = serial.Serial('/dev/ttyACM0', 9600)

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
    sens = Sensores()
    while True:
        data = sens.puerto.readline().decode('utf-8').rstrip()
        print(data)
        time.sleep(1)
        inter = sens.api.check_internet()
        ap = True
        try:
            sensor = json.loads(data)
            clave = sensor['clave']
            valor = sensor['valores']
            pines = "2,3"
            dispositivo = "carrito1"
            data = {
                "clave": clave,
                "valores": str(valor),
                "pines": pines,
                "dispositivo": dispositivo
            }
            print(data)
            if inter:
                inta=True
            else:
                inta=False
            nuevo = sens.guardarDatos(data, inta, ap)
        except json.decoder.JSONDecodeError as e:
            print("Error al cargar la cadena JSON:", e)

            # else:
            #     time.sleep(10)







