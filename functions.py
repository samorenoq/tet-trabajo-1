import json
import random
import math
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


def split_file(file_name: str, num_chunks: int = 3) -> None:
    # Abrir el archivo
    with open(file_name, 'rb') as file:
        file_content = file.read()  # Leer archivo

    size_of_chunk = len(file_content) // num_chunks  # División entera
    current_chunk = 0  # Apuntador a la parte actual del archivo
    chunks = {}  # Crear mapa de las partes para conservar el orden
    # Poner todas las partes del archivo en una lista (excepto la última)
    for i in range(num_chunks-1):
        # Apuntador al último byte que se toma para esta parte del archivo
        end_of_chunk = size_of_chunk + current_chunk
        # Tomar una parte del archivo
        chunks[i] = file_content[current_chunk:end_of_chunk]
        current_chunk += size_of_chunk  # Mover el apuntador al inicio de la siguiente parte
    # Agregar la última parte del archivo (que puede no tener el mismo tamaño que las demás)
    chunks[num_chunks-1] = file_content[current_chunk:]
    # Escribir cada parte en un archivo distinto
    for index, chunk in chunks.items():
        # Nombre del archivo para cada parte
        filename = f'{file_name}_{index}.part'
        with open(filename, 'wb') as f:
            f.write(chunk)
    return None

# Función para asignar aleatoriamente el servidor al que irá cada parte y un factor de replicación


def assign_server(num_chunks: int, num_servers: int, replication_factor: int) -> dict:
    server_assignment = {}
    # El proceso de asignación se repite tantas veces como el factor de replicación
    for _ in range(replication_factor):
        # Crear un orden aleatorio para la asignación de servidores.
        # Si el número de partes es mayor que el de servidores, se repiten servidores
        # Si el número de servidores es mayor que el de partes, hay servidores que pueden no recibir una parte
        random_sample = random.sample(
            range(num_servers), min(num_servers, num_chunks))
        # Repetir el orden aleatorio hasta que sea tan grande como el número de partes
        # Si hay más servidores que partes, no repetir
        repeated_sample = random_sample * \
            max(math.ceil(num_chunks/num_servers), 1)
        # Convertir en iterador para no recorrerlo por índice
        repeated_sample_iter = iter(repeated_sample)
        # Asignar un servidor a cada parte
        for chunk in range(num_chunks):
            # Si ya hay al menos un servidor asignado a la parte
            if chunk in server_assignment:
                # Revisar que no se esté asignando una parte dos veces al mismo servidor
                assigned_server = next(repeated_sample_iter)
                # En caso de que ya esté asignado el servidor a esa parte, se escogerá un servidor que no lo esté
                if assigned_server in server_assignment[chunk]:
                    already_assigned = set(server_assignment[chunk])
                    list_of_servers = set(range(num_servers))
                    # Diferencia de conjuntos para conocer los servidores disponibles
                    available_servers = list(
                        list_of_servers - already_assigned)
                    # Tomar cualquier servidor aleatoriamente de los disponibles
                    assigned_server = random.choice(available_servers)
                server_assignment[chunk].append(assigned_server)
            else:
                server_assignment[chunk] = [next(repeated_sample_iter)]

    return server_assignment


# Función para tomar las partes de un archivo y juntarlas
def join_file(chunks: dict, file_name: str) -> None:
    file_content = b''

    ordered_chunks = OrderedDict(sorted(chunks.items()))  # Ordenar las partes
    for _, chunk in ordered_chunks.items():
        file_content += chunk

    # Escribir la información completa a un archivo
    with open(file_name, 'wb') as f:
        f.write(file_content)

    return None
