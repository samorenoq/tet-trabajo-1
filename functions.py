import json
from collections import OrderedDict

# Función para leer el índice (key, value)
def read_index(path: str) -> dict:
    with open(path) as f:
        index = json.load(f)
    
    return index

# Función para actualizar el índice (key, value)
def write_index(index: dict, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(index, f)

    return None

# Función para retornar la lista de archivos disponibles
def list_files(index: dict) -> list:
    return sorted(list(index))

# Función para separar un archivo en un número específico de pedazos
def split_file( file_name: str, num_chunks: int = 3) -> dict:
    # Abrir el archivo
    with open(file_name, 'rb') as file:
        file_content = file.read() # Leer archivo
    
    size_of_chunk = len(file_content) // num_chunks # División entera
    current_chunk = 0 # Apuntador a la parte actual del archivo
    chunks = {} # Crear mapa de las partes para conservar el orden
    # Poner todas las partes del archivo en una lista (excepto la última)
    for i in range(num_chunks-1):
        end_of_chunk = size_of_chunk + current_chunk # Apuntador al último byte que se toma para esta parte del archivo
        chunks[i] = file_content[current_chunk:end_of_chunk] # Tomar una parte del archivo
        current_chunk += size_of_chunk # Mover el apuntador al inicio de la siguiente parte
    #Agregar la última parte del archivo (que puede no tener el mismo tamaño que las demás)
    chunks[num_chunks-1] = file_content[current_chunk:]
    return chunks

# Función para tomar las partes de un archivo y juntarlas
def join_file(chunks: dict, file_name: str) -> None:
    file_content = b''
    
    ordered_chunks = OrderedDict(sorted(chunks.items())) # Ordenar las partes
    for _, chunk in ordered_chunks.items():
        file_content += chunk
    
    # Escribir la información completa a un archivo
    with open(file_name, 'wb') as f:
        f.write(file_content)
        
    return None