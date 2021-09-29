from flask import Flask, request, redirect, send_file, render_template, flash
from werkzeug.utils import secure_filename
import os
import json
from functions import *
from constants import *

app = Flask('__name__', template_folder='templates')

app.config['UPLOAD_FOLDER'] = TEMP_FOLDER

# Cargar el diccionario con los pares (key, value)
key_value_index = read_index(INDEX_FILE_NAME)

# Lista de archivos disponibles
files = list_files(key_value_index)

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
            if filename in key_value_index:
                print('Error: el nombre del archivo ya existe')
                return redirect('/')
            else:
                # Crear un nombre de archivo compatible con el servidor
                server_file_name = secure_filename(filename)
                # Guardar un registro del archivo en el index de key, value
                key_value_index[filename] = {'serverName': server_file_name}
                # Actualizar el índice y la lista de archivos
                update_index()
                # Guardar el achivo temporalmente en el servidor
                file.save(os.path.join(TEMP_FOLDER, server_file_name))
        return redirect('/')

# Ruta para descarga de archivos
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path = os.path.join(TEMP_FOLDER, filename)
    return send_file(path, as_attachment=True, attachment_filename='')

import json

# Ruta para eliminar un archivo
@app.route('/delete', methods=['DELETE'])
def delete_file():
    # Obtener el cuerpo de la petición
    body = json.loads(request.data)
    filename = body['fileName']
    server_file_name = secure_filename(filename)
    # Verificar si el archivo sí existe
    if filename in key_value_index:
        path = os.path.join(TEMP_FOLDER, server_file_name)
        os.remove(path)
        # TODO: borrar el archivo los servidores, no sólo del índice
        # Quitar el archivo del índice
        del key_value_index[filename]
        update_index()
    else:
        print('Error: el archivo no existe')

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# Función para actualizar el índice y la lista ante cambios
def update_index() -> None:
    global key_value_index, files
    write_index(key_value_index, INDEX_FILE_NAME)
    key_value_index = read_index(INDEX_FILE_NAME)
    files = list_files(key_value_index)

    return None


# Correr el servidor
if __name__ == '__main__':
    app.run(host=HOST)
