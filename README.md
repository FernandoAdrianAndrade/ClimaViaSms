Crontab task set like follows:
0 12-17/1 * * * . $HOME/ClimaViaSms/lanza_proceso.ksh

Tener en cuenta que el repositorio de este codigo se encuentra en la carpeta por default de ubuntu "$HOME", igualmente las claves para acceder a las API's requeridas son personales y no se encuentran subidas al repositorio actual.
Se encuentran alojadas dentro de un archivo py seteado como sigue:

claves_api.py:

WEATHER_API_KEY = 'zzzzzZZXXcXXXXZzzz'
PHONE_NUMBER ='+1 788 888 888'
TWILIO_ACCOUNT_SID = 'AC8ccccacsac9sad78dcsa9'
TWILIO_AUTH_TOKEN = 'abcd123456789abcd123765'