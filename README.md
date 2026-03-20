# Proyecto-Analisis-de-sistemas
## Diagrama de Casos de uso 
flowchart LR
    Invitado[Invitado]
    Comprador[Comprador]
    Productor[Productor]
    Admin[Asociación / Administrador]

    subgraph Sistema["Sistema La Esperanza - Gestión Agrícola"]
        UC1((Iniciar sesión))
        UC2((Consultar catálogo de productos))
        UC3((Ver detalle de producto))
        UC4((Realizar solicitud de compra))
        UC5((Enviar mensaje / negociar acuerdo))
        UC6((Consultar mis compras))
        UC7((Consultar seguimiento de entrega))
        UC8((Confirmar recepción))
        UC9((Solicitar cancelación))
        UC10((Reportar inconformidad))

        UC11((Gestionar mis productos))
        UC12((Actualizar cantidades y precio referencial))
        UC13((Consultar solicitudes recibidas))
        UC14((Aceptar o rechazar solicitud))
        UC15((Registrar acuerdo comercial))
        UC16((Programar entrega))
        UC17((Actualizar seguimiento de entrega))
        UC18((Marcar entrega realizada))
        UC19((Justificar incumplimiento))
        UC20((Consultar historial de ventas))

        UC21((Gestionar usuarios))
        UC22((Crear usuario))
        UC23((Editar usuario))
        UC24((Reiniciar PIN de usuario))
        UC25((Suspender / bloquear cuenta))
        UC26((Resolver incidencias))
        UC27((Forzar cancelación))
        UC28((Ver estadísticas generales))
        UC29((Supervisar productos, acuerdos y entregas))

        UC30((Gestionar mi perfil))
        UC31((Cambiar PIN))
    end

    Invitado --> UC2
    Invitado --> UC3

    Comprador --> UC1
    Comprador --> UC2
    Comprador --> UC3
    Comprador --> UC4
    Comprador --> UC5
    Comprador --> UC6
    Comprador --> UC7
    Comprador --> UC8
    Comprador --> UC9
    Comprador --> UC10
    Comprador --> UC30
    Comprador --> UC31

    Productor --> UC1
    Productor --> UC5
    Productor --> UC11
    Productor --> UC12
    Productor --> UC13
    Productor --> UC14
    Productor --> UC15
    Productor --> UC16
    Productor --> UC17
    Productor --> UC18
    Productor --> UC19
    Productor --> UC20
    Productor --> UC30
    Productor --> UC31

    Admin --> UC1
    Admin --> UC21
    Admin --> UC22
    Admin --> UC23
    Admin --> UC24
    Admin --> UC25
    Admin --> UC26
    Admin --> UC27
    Admin --> UC28
    Admin --> UC29
    Admin --> UC30
    Admin --> UC31

    UC4 -. incluye .-> UC5
    UC14 -. incluye .-> UC15
    UC15 -. incluye .-> UC16
    UC16 -. incluye .-> UC17
    UC17 -. incluye .-> UC18
    UC9 -. extiende .-> UC26
    UC10 -. extiende .-> UC26
    UC19 -. extiende .-> UC26
    UC21 -. incluye .-> UC22
    UC21 -. incluye .-> UC23
    UC21 -. incluye .-> UC24
    UC21 -. incluye .-> UC25
