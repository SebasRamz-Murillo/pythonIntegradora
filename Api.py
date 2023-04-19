import requests


class Api:
    def __init__(self):
        self.ruta = "https://securebot.ninja"
        self.timeout = 5
        self.check = self.ruta + "/check"  # uso de ruta para que la api verifique que el dispositivo esta conectado
        self.internet = "https://www.google.com"  # checar si hay conexion a internet
        self.post = self.ruta + "/sensor"  # posteo de datos de sensores
        #self.get = self.ruta + "/status"  # ruta para obtener la activacion del joystick(prueba)

    def check_internet(self):
        timeout = 5
        try:
            request = requests.get(self.internet, timeout=timeout)
            request.raise_for_status()
            print("Internet connection is active")
            return True
        except requests.HTTPError as e:
            print("Checking internet connection failed, status code {0}".format(e.response.status_code))
        except requests.RequestException as e:
            print("Checking internet connection failed, errowsar: {0}".format(e))
        return False

    def check_api(self):
        timeout = 5
        try:
            request = requests.get(self.online, timeout=timeout)
            request.raise_for_status()
            print("Api connection is active")
            return True
        except requests.HTTPError as e:
            print("Checking api connection failed, status code {0}".format(e.response.status_code))
        except requests.RequestException as e:
            print("Checking api connection failed, error: {0}".format(e))
        return False

    def start_connection(self):
        response = requests.post(self.start)
        if response.status_code == 200:
            # La solicitud se ha enviado correctamente
            print(response.text)
        else:
            # Ha ocurrido un error al enviar la solicitud
            print(f'No empezo la conexion, Error: {response.status_code}')

    def stay_alive(self):
        response = requests.post(self.check)
        if response.status_code == 200:
            # La solicitud se ha enviado correctamente
            print(response.text)
        else:
            # Ha ocurrido un error al enviar la solicitud
            print(f'Error: {response.status_code}')

    def post_data(self, data):
        response = requests.post(self.post, data=data)
        if response.status_code == 200:
            # La solicitud se ha enviado correctamente
            print(response.text)
            return True
        else:
            # Ha ocurrido un error al enviar la solicitud
            print(f'No se subieron datos, Error: {response.status_code}')
            return False

    def get_status(self, data):
        # este es de bromis, o sea prueba xd
        timeout = 5
        try:
            request = requests.get(self.get, timeout=timeout)
            request.raise_for_status()
            print("Api connection is active")
            return True
        except requests.HTTPError as e:
            print("Checking api connection failed, status code {0}".format(e.response.status_code))
        except requests.RequestException as e:
            print("Checking api connection failed, error: {0}".format(e))
        return False


if __name__ == "__main__":
    # Ejemplo de uso
    if Api().check_internet():
        if Api().check_api():
            print("paso todo")
