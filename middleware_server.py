from flask import Flask, request, redirect, send_file, render_template, flash, after_this_request
from werkzeug.utils import secure_filename
import os
import json
from functions import *
from constants import *

app = Flask('__name__', template_folder='templates')

app.config['UPLOAD_FOLDER'] = TEMP_UPLOADS_FOLDER

# Cargar el diccionario con los pares (key, value)
file_index = read_index(FILE_INDEX_FILE_NAME)
# Cargar el diccionario con las direcciones de los servidores
server_index = read_index(SERVER_INDEX_FILE_NAME)

# Lista de archivos disponibles
files = list_files(file_index)

# Ruta para la interfaz inicial


@app.route('/')
def upload_form():
    return render_template('index.html', **globals())

# Ruta para carga de archivos


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Revisar que la petición sí contenga un archivo
        if 'file' not in request.files:
            print('Error: no se escogió ningún archivo')
            return redirect(request.url)
        file = request.files['file']  # Archivo que se está subiendo
        filename = file.filename  # Nombre del archivo
        # Revisar que el nombre del archivo no sea vacío
        if filename == '':
            print('Error: el nombre del archivo no puede ser vacío')
            return redirect(request.url)
        else:
            # Verificar que el archivo no exista
            if filename in file_index:
                print('Error: el nombre del archivo ya existe')
                return redirect('/')
            else:
                # Crear un nombre de archivo compatible con el servidor
                server_file_name = secure_filename(filename)
                # Guardar un registro del archivo en el index de key, value
                file_index[filename] = {'serverFileName': server_file_name}
                # Guardar el achivo temporalmente en el servidor
                file.save(os.path.join(TEMP_UPLOADS_FOLDER, server_file_name))
                # Separar el archivo en distintas partes
                chunks = split_file(os.path.join(TEMP_UPLOADS_FOLDER, server_file_name),
                                    NUM_PARTS)
                # Agregar los nombres de las partes al índice, en el key del archivo
                file_index[filename]['serverAssignment'] = assign_server(NUM_PARTS,
                                                                         len(server_index),
                                                                         REPLICATION_FACTOR)
                # Actualizar el índice y la lista de archivos
                update_index()

                # Enviar las partes a los servidores correspondientes
                send_parts_to_servers(file_index[filename],
                                      chunks,
                                      server_index)

                # Eliminar el archivo de los archivos temporales
                os.remove(os.path.join(TEMP_UPLOADS_FOLDER, server_file_name))

        return redirect('/')

# Ruta para descarga de archivos


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    destination_path = request_parts_from_servers(
        filename, file_index, server_index)

    # Borrar el archivo después de enviárselo al usuario
    @after_this_request
    def delete_temp_file(response):
        try:
            os.remove(destination_path)
        except:
            pass
        return response
    return send_file(destination_path, as_attachment=True, attachment_filename='')


# Ruta para eliminar un archivo


@app.route('/delete', methods=['DELETE'])
def delete_file():
    # Obtener el cuerpo de la petición
    body = json.loads(request.data)
    filename = body['fileName']
    # Eliminar todas las partes y sus réplicas de los servidores
    request_parts_from_servers(filename, file_index, server_index, True)
    # Verificar si el archivo sí existe
    if filename in file_index:
        # Quitar el archivo del índice
        del file_index[filename]
        update_index()
    else:
        print('Error: el archivo no existe')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# Función para actualizar el índice y la lista ante cambios


def update_index() -> None:
    global file_index, files
    write_index(file_index, FILE_INDEX_FILE_NAME)
    file_index = read_index(FILE_INDEX_FILE_NAME)
    files = list_files(file_index)

    return None


# Correr el servidor
if __name__ == '__main__':
    app.run(host=HOST)
