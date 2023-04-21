from Lista import Lista
from bson.objectid import ObjectId
import random
import datetime
import time


class Sensor(Lista):
    def __init__(self, data={}):
        timestamp = time.time()
        fecha_hora = datetime.datetime.fromtimestamp(timestamp)
        clave = str(data.get("clave", "desc"))
        valores = data.get("valores", "0")
        pines = data.get("pines", "4,4")
        jsonFile = clave + ".json"

        super().__init__(jsonFile)
        self.file = jsonFile
        self.clave = clave
        self.tipo, self.dato = self.tipoSensor(self.clave)
        self.valores = valores
        self.hora = fecha_hora.strftime('%H:%M:%S')
        self.fecha = fecha_hora.strftime('%Y-%m-%d')
        self.pines = pines
        self.archivo = jsonFile
        self._id = str(ObjectId())

    def __str__(self):
        return f"{self.clave},{self.tipo},{self.valores},{self.dato},{self.fecha},{self.hora},{self.pines}"

    def tipoSensor(self, clave):
        tipo = "Desconocido"
        dato = "Desconocido"
        if clave.startswith("Ult"):
            tipo = "Ultrasonico"
            dato = "cm"
        elif clave.startswith("Son0"):
            tipo = "Sonido"
            dato = "dB"
        elif clave.startswith("Tem"):
            tipo = "Temperatura"
            dato = "°C"
        elif clave.startswith("Hum"):
            tipo = "Humedad"
            dato = "Hr"
        elif clave.startswith("Bat"):
            tipo = "Bateria"
            dato = "V"
        elif clave.startswith("Pir"):
            tipo = "Movimiento"
            dato = "bool"
        elif clave.startswith("Ifr"):
            tipo = "Infrarrojo"
            dato = "bool"
        elif clave.startswith("Gas"):
            tipo = "Gas"
            dato = "bool"
        return tipo, dato

    def to_dict(self):
        listaDicc = []
        if type(self) == list:
            for item in self:
                if type(item) == dict:
                    listaDicc.append(item)
                else:
                    listaDicc.append(item.to_dict())
            return listaDicc
        elif type(self) == dict:
            listaDicc.append(self.listas)
        else:
            diccionario = {"_id": self._id, "clave": self.clave, "tipo": self.tipo, "valores": self.valores,
                           "dato": self.dato, "fecha": self.fecha, "hora": self.hora, "pines": self.pines,
                           "file": self.file}
            listaDicc.append(diccionario)
            return diccionario

    def from_json(self):
        sensor_json = self.json.leer_de_json()
        sensor_obj = []
        for sen in sensor_json:
            cli = Sensor(clave=sen["clave"], tipo=sen["tipo"], valores=sen["valores"], dato=sen["dato"],
                         fecha=sen["fecha"], hora=sen["hora"], pines=sen["pines"])
            sensor_obj.append(cli)
        return sensor_obj


if __name__ == "__main__":
    valorRandom = random.randint(2, 60)
    data = {
        "clave": "Ult1",
        "tipo": "temperatura",
        "valores": valorRandom,
        "dato": "C",
        "pines": "2,3",
        "dispositivo": "carrito1"
    }
    sensor = Sensor(data)
    file = data["clave"] + ".json"
    print(file)
    Lista(file).agregar(sensor.to_dict())
