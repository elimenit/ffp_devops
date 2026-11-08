# Requirements
Los paquetes utilizados para ejecutar la aplicacion es:
- ***pydantic***: Validacion de tipos.
- ***pydantic[email]***: Validacion del correo electronico.
- ***fastapi***: Aplicacion del servidor.
- ***typing***: Tipos de datos faltantes.
- ***sqlmodel***: ORM para la base de datos.
- ***requests***: Para testear (No es necesario)
- ***pytest***: Para testear unitarimente la aplicacion.
- ***uvicorn***: El servidor donde corre nuestra aplicacion.
- ***sqlalchemy[asyncio]***: maneja la asinronia de la R/W en la Base de Datos.
- ***asyncpg***: asincronia.
- ***httpx2***: Testing de integracion con testclient.

```bash
pydantic
fastapi
typing
sqlmodel
requests
pytest
uvicorn
pydantic[email]
load_dotenv
sqlalchemy[asyncio]
asyncpg
```