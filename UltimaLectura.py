from Lista import Lista
from bson.objectid import ObjectId


class ultimaLectura(Lista):
    def __init__(self, data={}):
        clave = str(data.get("clave", ""))
        tipo = data.get("tipo", "")
        valores = data.get("valores", "")
        dato = data.get("dato", "")
        pines = data.get("pines", "")
        hora = data.get("hora", "")
        fecha = data.get("fecha", "")
        jsonFile = data.get("file", "")
        super().__init__("historico.json")
        self.file = jsonFile
        self.clave = clave
        self.tipo = tipo
        self.valores = valores
        self.dato = dato
        self.hora = hora
        self.fecha = fecha
        self.pines = pines
        self.archivo = jsonFile
        self._id = str(ObjectId())

    def __str__(self):
        return f"{self.clave},{self.tipo},{self.valores},{self.dato},{self.fecha},{self.hora},{self.pines}"

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
