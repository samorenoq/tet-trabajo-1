# tet-trabajo-1

- Restricciones:
    * El desarrollador no debe definir un factor de replicación que sea superior al número de servidores, porque, de lo contrario, se repetirán archivos idénticos en el mismo servidor, haciendo uso ineficiente del almacenamiento.

Notas:
    * Se asegura que no se repite la misma parte de un archivo dos veces en el mismo servidor. El código está programado para que esto no pase, siempre y cuando el desarrollador cumpla la restricción de que el factor de replicación no puede ser superior al número de servidores.