# Importar librerías para crear un servidor HTTP
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
#Importar librería para leer argumentos de consola
import sys
from constants import ENCODING
from functions import write_bytes_to_file
import json
import os

# Fábrica para gestores de peticiones
def createHandler(storage_folder: str) -> BaseHTTPRequestHandler:
# Clase para gestionar peticiones
    class RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.storage_folder = storage_folder
            super(RequestHandler, self).__init__(*args, **kwargs)
        def do_POST(self):
            # Si la petición fue para subir archivo
            if 'serverFileName' in self.headers.keys():
                content_length = int(self.headers['Content-Length'])
                data = self.rfile.read(content_length)
                # Extraer el nombre del archivo
                filename = self.headers['serverFileName']
                # Extraer el id de la parte del archivo a la que los datos corresponden
                part_id = self.headers['partId']
                # Nombre del fragmento de archivo
                file_part_name = f'{filename}_{part_id}.part'
                # Ruta en la que se guardará la parte del archivo
                file_path = os.path.join(self.storage_folder, file_part_name)
                write_bytes_to_file(data, file_path)
                # Enviar respuesta
                self.send_response(200)
                # Importante para decirle al cliente que terminó la petición
                self.end_headers()
            #Si la petición fue para bajar archivo
            else:
                pass
        
        def do_DELETE(self):
            pass
    
    return RequestHandler

# Función para crear una nueva instancia de servidor
def start_server(ip_addr: str, port: int, storage_folder: str) -> None:
    handler = createHandler(storage_folder)
    # Crear servidor que escuche peticiones
    with ThreadingHTTPServer((ip_addr, port), handler) as httpd:
        print(f'Starting server on {ip_addr}:{port}')
        httpd.serve_forever()

def main(*args):
    args = args[0]
    start_server(args[0], int(args[1]), args[2])

if __name__ == "__main__":
    main(sys.argv[1:])
