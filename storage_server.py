# Importar librerías para crear un servidor HTTP
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
#Importar librería para leer argumentos de consola
import sys

# Clase para gestionar peticiones
class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, ip_addr, port, storage_folder):
        self.ip_addr = ip_addr
        self.port = port

    def do_POST(self):
        content_length = int(self.headers('Content-Length'))
        body = self.rfile.read(content_length)
        print(body)
    
    def do_DELETE(self):
        pass

# Función para crear una nueva instancia de servidor
def start_server(ip_addr: str, port: int, storage_folder: str) -> None:
    # Crear servidor que escuche peticiones
    with ThreadingHTTPServer((ip_addr, port), RequestHandler) as httpd:
        print(f'Starting server on {ip_addr}:{port}')
        httpd.serve_forever()

def main(*args):
    args = args[0]
    start_server(args[0], int(args[1]), args[2])

if __name__ == "__main__":
    main(sys.argv[1:])
