# Modelo Entidad-Relación (ER) - Sistema La Esperanza

Diagrama ER para las entidades principales del sistema.

Notas de modelado:
- **ACUERDO_COMERCIAL** concentra tanto la formalización del acuerdo como los datos de la entrega (fechas, estado final, justificación). En el prototipo se mostraron como una sola entidad por simplicidad operativa; aquí se mantiene esa unificación para evitar una tabla `ENTREGA` con una relación 1:1 pobre.
- **SEGUIMIENTO_ENTREGA** registra cada transición del acuerdo con `estado`, `comentario`, `usuario` y `fecha_hora`. Es la bitácora auditable que alimenta el stepper visual.
- **PUNTO_ENTREGA** es un catálogo maestro administrado por la Asociación.
- **CATEGORIA_PRODUCTO** y **UNIDAD_MEDIDA** también son catálogos maestros.

```mermaid
erDiagram
    ROL ||--o{ USUARIO : tiene
    USUARIO ||--o{ PRODUCTO : publica
    CATEGORIA_PRODUCTO ||--o{ PRODUCTO : clasifica
    UNIDAD_MEDIDA ||--o{ PRODUCTO : define
    USUARIO ||--o{ SOLICITUD_COMPRA : realiza
    PRODUCTO ||--o{ SOLICITUD_COMPRA : recibe
    SOLICITUD_COMPRA ||--o| ACUERDO_COMERCIAL : genera
    ACUERDO_COMERCIAL }o--|| PUNTO_ENTREGA : se_programa_en
    ACUERDO_COMERCIAL ||--o{ SEGUIMIENTO_ENTREGA : registra
    ACUERDO_COMERCIAL ||--o{ MENSAJE_ACUERDO : contiene
    ACUERDO_COMERCIAL ||--o{ REPORTE_INCIDENCIA : puede_generar
    USUARIO ||--o{ MENSAJE_ACUERDO : envia
    USUARIO ||--o{ SEGUIMIENTO_ENTREGA : actualiza
    USUARIO ||--o{ REPORTE_INCIDENCIA : reporta

    ROL {
        int id_rol PK
        string nombre
        string descripcion
    }

    USUARIO {
        int id_usuario PK
        int id_rol FK
        string cui
        string nombre_completo
        string telefono
        string direccion
        string pin_hash
        string estado_cuenta
        date fecha_registro
    }

    CATEGORIA_PRODUCTO {
        int id_categoria PK
        string nombre
        string descripcion
        string estado
    }

    UNIDAD_MEDIDA {
        int id_unidad PK
        string nombre
        string abreviatura
        string descripcion
        string estado
    }

    PRODUCTO {
        int id_producto PK
        int id_productor FK
        int id_categoria FK
        int id_unidad FK
        string nombre
        string descripcion
        decimal cantidad_disponible
        decimal precio_referencial
        string estado_producto
        date fecha_publicacion
    }

    SOLICITUD_COMPRA {
        int id_solicitud PK
        int id_comprador FK
        int id_producto FK
        decimal cantidad_solicitada
        string mensaje_inicial
        string estado_solicitud
        datetime fecha_solicitud
    }

    ACUERDO_COMERCIAL {
        int id_acuerdo PK
        int id_solicitud FK
        int id_punto_entrega FK
        decimal precio_final
        datetime fecha_programada
        datetime fecha_entrega_productor
        datetime fecha_confirmacion_comprador
        string estado_acuerdo
        string estado_pago
        string estado_final
        string justificacion_incumplimiento
        string observaciones
    }

    PUNTO_ENTREGA {
        int id_punto_entrega PK
        string nombre
        string descripcion
        string referencia
        string estado
    }

    SEGUIMIENTO_ENTREGA {
        int id_seguimiento PK
        int id_acuerdo FK
        int id_usuario FK
        string estado
        string comentario
        datetime fecha_hora
    }

    MENSAJE_ACUERDO {
        int id_mensaje PK
        int id_acuerdo FK
        int id_remitente FK
        string mensaje
        datetime fecha_hora
    }

    REPORTE_INCIDENCIA {
        int id_reporte PK
        int id_acuerdo FK
        int id_reportante FK
        string tipo
        string descripcion
        string estado_reporte
        string resolucion
        datetime fecha_reporte
    }
```

## Dominios de valores

### `ACUERDO_COMERCIAL.estado_acuerdo`
Ciclo de vida del acuerdo, reflejado en el stepper del prototipo:

- `solicitado` — solicitud creada por el comprador, a la espera de respuesta.
- `aceptado` — productor aceptó y se registraron precio_final, fecha_programada y punto_entrega.
- `preparando` — productor está alistando la cosecha.
- `programado` — entrega confirmada en agenda.
- `en_ruta` — productor inició traslado.
- `entregado_productor` — productor marcó la entrega.
- `confirmado_comprador` — comprador confirmó recepción (estado terminal feliz).
- `cancelado` — acuerdo cancelado por cualquiera de las partes o por el administrador.

### `ACUERDO_COMERCIAL.estado_pago`
- `pendiente`
- `contra_entrega`
- `realizado`

### `ACUERDO_COMERCIAL.estado_final`
Se establece al cerrar el acuerdo:
- `confirmada` — entrega aceptada.
- `incumplida` — no se entregó o hubo reporte de inconformidad aceptado.
- `cancelada` — acuerdo cancelado antes de entrega.

### `REPORTE_INCIDENCIA.tipo`
- `inconformidad_cantidad`
- `inconformidad_calidad`
- `incumplimiento_entrega`
- `otro`

### `REPORTE_INCIDENCIA.estado_reporte`
- `abierto`
- `en_revision`
- `resuelto`
- `descartado`
