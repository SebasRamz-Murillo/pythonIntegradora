from Sensor import Sensor
from UltimaLectura import ultimaLectura
from Lista import Lista
import random
from datetime import datetime, timedelta
from Api import Api
import time
class Sensores:
    def __init__(self):
        self.sensores = Sensor()
        self.historico = ultimaLectura()
        self.api=Api()
       
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
            print(dataApi)
            if not self.api.post_data(newSensor.to_dict()):
                self.historico.agregar(newSensor.to_dict())
            horaPrincipal= Lista(file).mostrar()[0]["hora"]
            horaTurno= Lista(file).mostrar()[len(Lista(file).mostrar())-1]["hora"]
            if (datetime.strptime(horaTurno, "%H:%M:%S")-timedelta(minutes=5)>=datetime.strptime(horaPrincipal, "%H:%M:%S")) or len(Lista(file).mostrar()) > 200 :
                Lista(file).borrarInfo()



    def checkarHistorico(self):
        dataHistorial=self.historico.to_dict()
        return dataHistorial
    

    

if __name__ == "__main__":

    for j in range(800):
        # asi debe quedar el json que se reciba o al menos tener esos datos desde el arduino, menos dispositivo
        claves = ["Ult0","Ult1","Son0","Tem0","Hum0","Bat0","Bat1","Ifr0","Ifr1","Pir0","Pir1","Gas0"]
        clavesBooleanos = ["Ifr0","Ifr1","Pir0","Pir1","Gas0"]
        for clave in claves:
            if clave in clavesBooleanos:
                valor = random.choice([0, 1])
            else:
                valor = random.randint(2, 60)

            data = {
                "clave": clave,
                "valores": str(valor),
                "pines": "2,3",
                "dispositivo": "carrito1"
            }
            sens=Sensores()
            nuevo=sens.guardarDatos(data,True,True)

        time.sleep(10)
    print("Se acabo el envio de datoooooooos")