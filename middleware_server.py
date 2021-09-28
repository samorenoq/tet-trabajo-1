from flask import Flask, request, redirect, send_file, render_template
from werkzeug.utils import secure_filename
import os
import json
from functions import *

app = Flask('__name__', template_folder='templates')

TEMP_FOLDER = 'temp_files'
app.config['UPLOAD_FOLDER'] = TEMP_FOLDER

# Cargar el diccionario con los pares (key, value)
key_value_index = read_index('index.json')

# Ruta para la interfaz inicial
@app.route('/')
def upload_form():
    return render_template('index.html', files = list_files(key_value_index))

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
                write_index(key_value_index, 'index.json')
                # Guardar el achivo temporalmente en el servidor
                file.save(os.path.join(TEMP_FOLDER, server_file_name))

        return redirect('/')

# Ruta para descarga de archivos
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path = os.path.join(TEMP_FOLDER, filename)
    return send_file(path, as_attachment=True, attachment_filename='')


# Correr el servidor
if __name__ == '__main__':
    app.run(host='localhost')
