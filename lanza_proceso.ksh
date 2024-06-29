#!/bin/ksh 

. $HOME/env/bin/activate # Activamos el entorno virtual
cd $HOME/ClimaViaSms #Cambiamos de directorio
python3 proyecto_clima.py >> log_ejecuccion.txt #Ejecutamos el script de python
deactivate