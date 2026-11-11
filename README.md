
# FFP_DevOps
Plantilla de servicios FastApi y PostgreSQL base de juguete para ser usada de ejemplo DevOps.

## Testing es Documentacion y la Documentacion es Testing

## Base de Datos 
Usamos PostgreSQL con la activacion de la extension **pg_trgm** y un indice **GIN** para tokenizar las busquedas difusas.

- ***Activar la extension en PostgreSQL***:
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

La implementacion de la Busqueda de la Barra Principal:
    1) Priorizacion estricta por indice: PostgreSQL aplica primero 
    los filtros numericos/exactos (como price o category) para reducir la tabla a una fraccion pequeña de registros.

    2) Busqueda Difusa: la evaluacion de trigramas (pg_trgm) se ejecuta sobre el conjunto ya filtrado.
    
    3) Relevancia Jerarquica: 