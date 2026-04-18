# DERCAS — Sistema de Gestión y Comercialización Agrícola "La Esperanza"

**Fase II — Análisis de Sistemas I**

Documento de Especificación de Requerimientos, Casos de Uso, Actividades y Soporte para el sistema de gestión y comercialización agrícola propuesto para la comunidad rural "La Esperanza".

---

## 1. Descripción General del Sistema

### 1.1 Visión General

El Sistema de Gestión y Comercialización Agrícola "La Esperanza" es una aplicación web orientada a formalizar, registrar y coordinar las actividades comerciales que hoy realiza de manera informal la comunidad rural "La Esperanza", ubicada aproximadamente a 40 km del centro urbano más cercano. La comunidad concentra su economía en la producción agrícola a pequeña escala (hortalizas, granos básicos y frutas de temporada) y comercializa con intermediarios locales y pequeños comercios por medios informales (llamadas, visitas presenciales, acuerdos verbales).

El propósito del sistema es ofrecer una **fuente única de verdad digital** sobre los productos disponibles, las solicitudes de compra, los acuerdos pactados y las entregas efectuadas, de modo que la comunidad pueda reducir pérdidas por sobreproducción, evitar desacuerdos sobre cantidades y precios, y conservar información histórica útil para planificar temporadas futuras.

**Finalidad.** El sistema centraliza la operación comercial de la comunidad en tres ejes:

1. **Publicación y descubrimiento de productos.** Los productores publican sus cosechas con categoría, unidad de medida, cantidad disponible y precio referencial. Los compradores (y los visitantes invitados) pueden consultar el catálogo en cualquier momento.
2. **Negociación y acuerdo comercial.** El sistema conduce el ciclo completo desde la solicitud de compra, la negociación por mensajería interna, la formalización del acuerdo con precio final, fecha programada y punto de entrega, hasta la entrega y confirmación por ambas partes.
3. **Supervisión y análisis.** La Asociación supervisa la operación, administra los catálogos maestros (categorías, unidades, puntos de entrega), modera usuarios y consulta reportes agregados y anonimizados para planificación comunitaria.

**Principales características.**

- Multirrol con vistas diferenciadas para Invitado, Comprador, Productor y Administrador (Asociación).
- Catálogo público de productos consultable sin inicio de sesión.
- Flujo de solicitud → aceptación → preparación → programación → ruta → entrega → confirmación, con bitácora auditable en cada transición.
- Bandeja de mensajes y negociación por acuerdo, con trazabilidad.
- Registro y seguimiento de incidencias (inconformidades, incumplimientos, cancelaciones). La **resolución del conflicto queda fuera del sistema**: el comité de la Asociación media y decide por canales propios; el sistema solamente registra el caso, el tipo y la decisión final tomada.
- Panel de reportes con KPIs comunitarios, agregados y sin identificación individual.
- Estados formales para usuarios (activo, suspendido, bloqueado), pagos (pendiente, contra entrega, realizado) e incidencias (abierto, en revisión, resuelto, descartado).
- Historial de auditoría: toda acción relevante del sistema (alta/edición de usuario, cambios de estado, actualizaciones de catálogo, transiciones de acuerdo, resoluciones) queda registrada con usuario y fecha-hora.
- Diseño **responsive** y orientado a baja alfabetización digital (tipografía amplia, íconos claros, navegación inferior en móvil).
- **Capacidad offline**: lectura de catálogo, registro de solicitudes y actualizaciones de seguimiento se almacenan localmente cuando no hay conexión y se sincronizan al reconectar (PWA con almacenamiento local).

**Interacciones clave con otros sistemas.** En esta fase el sistema no requiere integración con ERP o contabilidad. Depende únicamente de:

- **Gateway de mensajería SMS** (tercero, p. ej. Twilio o equivalente) para enviar códigos de verificación al dar de alta un usuario y para recuperación de PIN olvidado. El login diario se realiza con teléfono + PIN local, sin costo por SMS.
- **Hosting web estático + API REST** para servir la aplicación y persistir los datos.
- **Navegador moderno en el dispositivo del usuario** (Chrome, Firefox, Safari o Edge en versión reciente) que actúa como contenedor de la PWA.

No se contempla intercambio de datos con sistemas contables, bancarios o de logística de terceros. Si se implementa esa integración en fases posteriores, quedará fuera del alcance de este documento.

**Límites del sistema.**

- No procesa pagos electrónicos ni actúa como pasarela bancaria. El campo `estado_pago` es solamente un registro declarativo del productor o del comprador.
- No resuelve arbitrajes, sanciones o conflictos: los incidentes quedan registrados en el sistema, pero la mediación y la sanción son responsabilidad directa del comité de la Asociación por fuera del software.
- No ofrece logística ni transporte: el productor y el comprador acuerdan quién traslada el producto, y el sistema solo registra el punto de entrega seleccionado del catálogo mantenido por la Asociación.

---

### 1.2 Usuarios del Sistema

El sistema distingue **cuatro perfiles de usuario**, cada uno con alcance, responsabilidades y capacidades diferenciadas. El perfil se asigna al crear la cuenta y queda asociado al usuario mediante un rol (entidad `ROL` del modelo ER).

#### 1.2.1 Invitado (sin autenticación)

- **Descripción.** Cualquier persona que accede al sistema sin haber iniciado sesión. Puede ser un comprador potencial que evalúa el catálogo antes de solicitar una cuenta, o un miembro de la comunidad que consulta precios de referencia.
- **Alfabetización digital esperada.** Baja a media. Se asume que el invitado puede navegar páginas web simples pero no necesariamente completar formularios complejos.
- **Dispositivo típico.** Teléfono inteligente o computadora con navegador web reciente.
- **Alcance en el sistema.**
  - Consultar el catálogo público de productos.
  - Ver el detalle de cada producto (productor, categoría, precio referencial, disponibilidad, descripción).
  - Ser dirigido al inicio de sesión o a contactar a la Asociación para solicitar una cuenta si desea comprar.
- **Limitaciones.** No puede realizar solicitudes de compra, enviar mensajes, ver datos históricos ni acceder a ninguna funcionalidad transaccional.

#### 1.2.2 Comprador

- **Descripción.** Persona natural o jurídica (restaurante, pequeño comercio, distribuidor, consumidor final) que adquiere productos agrícolas a la comunidad. La Asociación da de alta su cuenta tras verificar su identidad.
- **Alfabetización digital esperada.** Baja a media. Normalmente más alta que la del productor promedio por su vinculación con comercio urbano.
- **Dispositivo típico.** Teléfono inteligente o computadora. Requiere conectividad al menos ocasional para sincronizar solicitudes.
- **Responsabilidades.**
  - Realizar solicitudes de compra responsables (no abrir múltiples solicitudes sin intención de cumplirlas).
  - Negociar de buena fe a través del chat del acuerdo.
  - Confirmar la recepción de la entrega de manera oportuna.
  - Reportar inconformidades reales y documentadas.
- **Alcance en el sistema.**
  - Consultar catálogo y detalle de productos.
  - Registrar solicitudes de compra con cantidad y mensaje inicial al productor.
  - Mensajería dentro del acuerdo.
  - Consultar "Mis Compras" con estado, fecha y punto de entrega.
  - Confirmar recepción, solicitar cancelación o reportar inconformidad.
  - Gestionar su perfil y cambiar su PIN.

#### 1.2.3 Productor

- **Descripción.** Miembro de la comunidad "La Esperanza" que produce y comercializa bienes agrícolas. La Asociación da de alta su cuenta y vincula su DPI/CUI.
- **Alfabetización digital esperada.** Baja. Gran parte de los productores usa teléfonos básicos o smartphones de gama baja, con experiencia principalmente en WhatsApp y llamadas. El sistema prioriza tipografía grande, íconos, y flujos de pocos pasos.
- **Dispositivo típico.** Smartphone de gama baja o media, conectividad intermitente. Algunos productores comparten dispositivo familiar.
- **Responsabilidades.**
  - Mantener actualizadas sus publicaciones (cantidad disponible y precio referencial).
  - Responder las solicitudes de compra que recibe.
  - Formalizar el acuerdo ingresando precio final, fecha programada y punto de entrega.
  - Actualizar el estado de la entrega (preparando, programada, en ruta, entregada) con comentarios breves.
  - Justificar incumplimientos cuando corresponda.
- **Alcance en el sistema.**
  - Publicar, editar y retirar sus productos (UC11, UC12).
  - Consultar, aceptar o rechazar solicitudes recibidas.
  - Registrar el acuerdo comercial al aceptar (UC15, UC16).
  - Actualizar el seguimiento de la entrega (UC17) con comentario auditable.
  - Marcar la entrega como realizada (UC18).
  - Consultar su historial de ventas con ingresos por mes y tasa de cumplimiento (UC20).
  - Mensajería con el comprador dentro del acuerdo.
  - Gestionar su perfil y cambiar su PIN.

#### 1.2.4 Administrador / Asociación

- **Descripción.** Persona o grupo de personas designadas por la Asociación Comunitaria "La Esperanza" para administrar la plataforma. Es la autoridad dentro del sistema.
- **Alfabetización digital esperada.** Media. Se asume formación básica suficiente para operar formularios y reportes, con capacitación inicial.
- **Dispositivo típico.** Computadora de escritorio o laptop en la sede de la Asociación, complementada por smartphone. Cuentan con conectividad más estable que los productores individuales.
- **Responsabilidades.**
  - Custodiar los datos de la comunidad y la identidad digital de sus miembros.
  - Dar de alta usuarios (únicos con esta capacidad) y mantener actualizados sus estados.
  - Mantener los catálogos maestros: categorías de producto, unidades de medida y puntos de entrega.
  - Supervisar el cumplimiento de acuerdos y revisar incidencias reportadas.
  - **Registrar la resolución adoptada por el comité** en los conflictos (la resolución misma se discute fuera del sistema).
  - Consultar reportes agregados para planificación comunitaria.
- **Alcance en el sistema.**
  - Gestión completa de usuarios (UC21–UC25): crear, editar, reiniciar PIN, suspender y bloquear.
  - Gestión de catálogos maestros (UC30, UC31, UC34).
  - Supervisión del catálogo de productos, los acuerdos en curso y las entregas (UC29).
  - Registro de resoluciones de incidencias (UC26).
  - Forzar cancelación de un acuerdo cuando sea necesario (UC27).
  - Consultar reportes agregados y anonimizados (UC28).
  - Gestionar su propio perfil (UC32, UC33).

---

### 1.3 Supuestos y Dependencias

#### 1.3.1 Supuestos

Los siguientes supuestos se asumen como ciertos durante el diseño y desarrollo del sistema. Cambios en cualquiera de ellos requieren revisión del alcance y los requerimientos.

**Sobre la comunidad y los usuarios**

- La Asociación Comunitaria "La Esperanza" es la única autoridad reconocida para dar de alta usuarios y custodiar la identidad digital de sus miembros.
- Los productores cuentan con algún dispositivo con acceso a navegador web reciente (smartphone de gama baja o superior). Quienes no lo tengan acceden al sistema a través de un representante de la Asociación.
- La alfabetización digital promedio de los productores es baja. El sistema debe priorizar flujos cortos, tipografía grande, íconos y textos en español claro.
- Los compradores frecuentes tienen acceso a smartphone o computadora con conectividad al menos ocasional.
- La resolución de conflictos entre usuarios (sanciones, arbitrajes, compensaciones) se lleva fuera del sistema, en las asambleas o reuniones del comité. El sistema solamente registra el caso y la decisión final tomada.

**Sobre la operación**

- Las entregas se realizan en puntos físicos acordados por la comunidad y administrados en un catálogo centralizado por la Asociación.
- El sistema no procesa pagos electrónicos. El estado de pago es un registro declarativo acordado entre las partes.
- La información de negociación queda dentro del acuerdo comercial correspondiente; no hay un canal transversal público entre usuarios.
- La Asociación se compromete a capacitar a los usuarios en el uso inicial del sistema y a brindar soporte de primer nivel por canales propios (WhatsApp, reuniones comunales).

**Sobre la infraestructura**

- Los dispositivos de los usuarios pueden ejecutar un navegador web reciente. No se soportará Internet Explorer ni navegadores descontinuados.
- La conectividad en la comunidad es variable. El sistema debe funcionar en modo degradado (lectura de catálogo cacheado, registro pendiente de sincronización) cuando no haya conexión.
- El hospedaje del sistema se contrata a un proveedor de terceros (infraestructura en la nube o servidor dedicado). Los costos recurrentes los asume la Asociación.

**Sobre mantenimiento y soporte**

- La Asociación no cuenta con personal técnico propio para mantenimiento del software. El mantenimiento evolutivo y correctivo se contrata a terceros bajo demanda.
- El sistema se entrega con documentación operativa y técnica que permite a un proveedor externo retomar el desarrollo en fases posteriores.

#### 1.3.2 Dependencias

**Dependencias tecnológicas**

| Dependencia | Propósito | Tipo | Criticidad |
|-------------|-----------|------|------------|
| Navegador web moderno en el cliente | Ejecución de la PWA | Cliente | Alta |
| Hosting web / API REST | Servir la aplicación y persistir datos | Servicio externo | Alta |
| Base de datos relacional gestionada | Persistencia estructurada | Servicio externo | Alta |
| Almacenamiento local del navegador (IndexedDB / LocalStorage) | Soporte offline y caché de catálogo | Cliente | Media |
| Gateway SMS (Twilio o similar) | Verificación de alta y recuperación de PIN | Servicio externo | Media |
| Proveedor de dominio y certificado SSL | Acceso seguro por HTTPS | Servicio externo | Alta |

**Dependencias organizacionales**

- **Asociación Comunitaria "La Esperanza"** como contraparte operativa: aprueba usuarios, administra catálogos, supervisa incidencias y asume el costo de hosting y SMS.
- **Proveedor de soporte técnico externo** contratado para mantenimiento evolutivo y correctivo tras la entrega inicial.
- **Proveedor de capacitación** (puede ser la misma asociación o un tercero) responsable de alfabetizar digitalmente a productores y compradores durante el despliegue.

**Dependencias normativas**

- Ley de protección de datos personales aplicable al país de operación (referencia conceptual; los detalles se desarrollan en la sección de requerimientos no funcionales bajo *Legalidad*).
- Reglamento interno de la Asociación en lo referente a sanciones y resolución de conflictos. El sistema refleja las decisiones del comité, no las toma.

#### 1.3.3 Riesgos derivados de los supuestos

| Riesgo | Supuesto afectado | Mitigación propuesta |
|--------|-------------------|----------------------|
| Un productor sin smartphone queda excluido del sistema | Todos los productores tienen dispositivo | Un representante de la Asociación puede publicar en su nombre; capacitación comunitaria. |
| Conectividad permanentemente deficiente impide sincronización | Conectividad al menos intermitente | Modo offline con cola de sincronización; diseño tolerante a reintentos. |
| SMS no llega o el proveedor sube precios | Gateway SMS disponible y económico | PIN local como mecanismo principal; SMS solo para verificación inicial y recuperación. |
| Alta rotación en el comité dificulta custodia | Asociación estable | Capacitación documentada y roles delegables; más de un administrador registrado. |
| La comunidad no adopta el sistema | Voluntad de adopción | Piloto con 5–10 productores y 2–3 compradores antes del despliegue general. |

---

---

## 2. Requerimientos Funcionales

Cada requerimiento se identifica con el prefijo **RF**, agrupado por módulo. La prioridad (Alta / Media / Baja) se asigna según el grado en que el requerimiento **automatiza un proceso que hoy se realiza de manera informal**: los procesos núcleo del negocio (solicitud, acuerdo, entrega, confirmación) reciben prioridad Alta; la administración de catálogos y la analítica reciben prioridad Media; las funciones accesorias o de conveniencia reciben prioridad Baja.

### 2.1 Autenticación y Gestión de Cuentas

#### RF01 — Iniciar sesión con teléfono y PIN

| Campo | Detalle |
|-------|---------|
| **Descripción** | El sistema permite al usuario autenticarse ingresando su número de teléfono (identificador) y su PIN de 4 dígitos. |
| **Entradas** | Número de teléfono (string), PIN de 4 dígitos (string numérico). |
| **Salidas** | Sesión autenticada con rol asociado y redirección al panel correspondiente; o mensaje de error. |
| **Comportamiento esperado** | Si la combinación teléfono + PIN coincide con un usuario activo, se inicia la sesión y el rol determina las vistas disponibles. La sesión se mantiene mediante token seguro almacenado en el navegador. |
| **Excepciones** | Credenciales incorrectas: mensaje claro sin revelar cuál campo falló. Cuenta suspendida o bloqueada: mensaje específico con instrucción de contactar a la Asociación. Cinco intentos fallidos consecutivos: bloqueo temporal de 10 minutos. |
| **Prioridad** | **Alta** |

#### RF02 — Acceso de invitado al catálogo

| Campo | Detalle |
|-------|---------|
| **Descripción** | El sistema permite consultar el catálogo público sin requerir inicio de sesión, para facilitar el descubrimiento por parte de compradores potenciales. |
| **Entradas** | Ninguna (navegación anónima). |
| **Salidas** | Catálogo de productos con datos públicos (nombre, categoría, productor, precio referencial, disponibilidad). |
| **Comportamiento esperado** | El invitado puede consultar productos y ver detalle, pero cualquier acción transaccional lo redirige al inicio de sesión. |
| **Excepciones** | Si intenta solicitar, enviar mensaje o reportar, se redirige a la pantalla de login con mensaje contextual. |
| **Prioridad** | **Media** |

#### RF03 — Cerrar sesión

| Campo | Detalle |
|-------|---------|
| **Descripción** | El usuario autenticado puede finalizar su sesión en cualquier momento. |
| **Entradas** | Acción de cerrar sesión (clic en botón). |
| **Salidas** | Token invalidado, datos locales de sesión eliminados, redirección a login. |
| **Comportamiento esperado** | El cierre debe eliminar el token y cualquier dato sensible cacheado en el navegador. |
| **Excepciones** | Si hay operaciones pendientes de sincronización, se advierte al usuario antes de cerrar. |
| **Prioridad** | **Alta** |

#### RF04 — Cambiar PIN propio

| Campo | Detalle |
|-------|---------|
| **Descripción** | El usuario autenticado puede cambiar su PIN desde su perfil. |
| **Entradas** | PIN actual, PIN nuevo, confirmación de PIN nuevo. |
| **Salidas** | Confirmación de cambio exitoso; PIN actualizado en almacén seguro. |
| **Comportamiento esperado** | El PIN nuevo debe ser de 4 dígitos y distinto al actual. Se almacena aplicando hash seguro (bcrypt o equivalente). La acción se registra en la bitácora de auditoría. |
| **Excepciones** | PIN actual incorrecto: error sin cambiar nada. PIN nuevo igual al actual: rechazo. PIN nuevo con menos de 4 dígitos o no numérico: rechazo. |
| **Prioridad** | **Alta** |

#### RF05 — Recuperación de PIN por SMS

| Campo | Detalle |
|-------|---------|
| **Descripción** | Cuando un usuario olvida su PIN, puede solicitar un código de verificación por SMS al número registrado para establecer un nuevo PIN. |
| **Entradas** | Número de teléfono registrado; código de 6 dígitos recibido por SMS; PIN nuevo. |
| **Salidas** | Código enviado al teléfono; PIN restablecido tras validación. |
| **Comportamiento esperado** | El código expira en 10 minutos. Máximo 3 solicitudes en 1 hora por número. Una vez validado el código, el usuario registra un nuevo PIN. |
| **Excepciones** | Número no registrado: se muestra mensaje genérico para no revelar existencia de la cuenta. Falla del gateway SMS: se muestra aviso y se sugiere contactar a la Asociación. Código expirado o incorrecto: rechazo con opción de reintentar. |
| **Prioridad** | **Media** |

#### RF06 — Gestionar perfil propio

| Campo | Detalle |
|-------|---------|
| **Descripción** | El usuario autenticado puede actualizar su información de contacto (dirección, teléfono secundario, etc.). |
| **Entradas** | Campos editables del perfil. |
| **Salidas** | Datos actualizados en la base; confirmación visible. |
| **Comportamiento esperado** | El teléfono principal (usado como identificador de login) y el DPI/CUI no son editables por el propio usuario. Los cambios se auditan. |
| **Excepciones** | Datos fuera de formato (teléfono no numérico, dirección vacía): validación inline. |
| **Prioridad** | **Media** |

---

### 2.2 Gestión de Productos (Productor)

#### RF07 — Publicar nuevo producto

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor registra una nueva cosecha con sus atributos para hacerla visible en el catálogo. |
| **Entradas** | Nombre, categoría (del catálogo maestro), descripción opcional, unidad de medida (del catálogo), cantidad disponible, precio referencial. |
| **Salidas** | Producto visible en el catálogo, asociado al productor autor. |
| **Comportamiento esperado** | Al guardar, el producto queda en estado *disponible* si la cantidad es mayor a cero. El precio es solo referencial; el final se negocia por solicitud. |
| **Excepciones** | Cantidad negativa o no numérica: rechazo. Categoría o unidad no existentes o inactivas: rechazo con indicación de contactar a la Asociación. Precio con formato inválido: rechazo. |
| **Prioridad** | **Alta** |

#### RF08 — Editar producto publicado

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor actualiza un producto propio, típicamente para ajustar cantidad disponible o precio referencial. |
| **Entradas** | Mismos campos de publicación, con valores precargados. |
| **Salidas** | Producto actualizado en el catálogo. |
| **Comportamiento esperado** | La edición solo está permitida sobre productos del propio productor. Los cambios se auditan. Cantidad en cero cambia automáticamente el estado del producto a *agotado*. |
| **Excepciones** | Intento de editar producto ajeno: 403 (no autorizado). Producto retirado: no puede editarse, solo reactivarse con nueva publicación. |
| **Prioridad** | **Alta** |

#### RF09 — Retirar producto del catálogo

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor puede retirar un producto propio, por ejemplo por fin de temporada o pérdida de cosecha. |
| **Entradas** | Confirmación de retiro y motivo opcional. |
| **Salidas** | Producto deja de aparecer en el catálogo público. |
| **Comportamiento esperado** | Los acuerdos ya formalizados con ese producto no se ven afectados; continúan su ciclo normal. El producto se marca como *retirado*, no se elimina físicamente. |
| **Excepciones** | Producto con solicitudes pendientes: se advierte al productor antes de retirar; si confirma, las solicitudes pendientes deben resolverse manualmente. |
| **Prioridad** | **Media** |

#### RF10 — Consultar mis productos

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor visualiza el listado de sus productos publicados con filtros y ordenamientos. |
| **Entradas** | Filtros opcionales (estado, categoría, rango de precio) y criterio de ordenamiento. |
| **Salidas** | Lista de productos propios con datos resumidos y acciones disponibles. |
| **Comportamiento esperado** | Solo muestra productos del productor autenticado. Incluye contadores rápidos (productos activos, agotados, retirados). |
| **Excepciones** | Sin productos publicados: pantalla vacía con CTA para publicar. |
| **Prioridad** | **Media** |

---

### 2.3 Catálogo Público y Solicitud de Compra

#### RF11 — Consultar catálogo de productos

| Campo | Detalle |
|-------|---------|
| **Descripción** | Cualquier usuario (incluido invitado) consulta los productos disponibles con búsqueda, filtros y ordenamiento. |
| **Entradas** | Texto de búsqueda (nombre o categoría), filtros opcionales, criterio de ordenamiento (disponibilidad, categoría, precio, unidad). |
| **Salidas** | Lista de productos con nombre, categoría, productor, precio referencial, cantidad disponible y estado. |
| **Comportamiento esperado** | Los productos *retirados* o con productor suspendido no aparecen. La búsqueda es insensible a mayúsculas/minúsculas y tolera acentos. |
| **Excepciones** | Catálogo vacío: mensaje amigable con indicación de volver a intentar. |
| **Prioridad** | **Alta** |

#### RF12 — Ver detalle de producto

| Campo | Detalle |
|-------|---------|
| **Descripción** | Desde el catálogo, el usuario accede al detalle completo de un producto. |
| **Entradas** | Identificador del producto. |
| **Salidas** | Ficha con todos los datos públicos del producto; formulario de solicitud si el usuario es comprador. |
| **Comportamiento esperado** | Muestra nombre del productor para dar confianza. Si el producto está agotado, el CTA de solicitud aparece deshabilitado. El invitado ve un CTA para iniciar sesión. |
| **Excepciones** | Producto inexistente o retirado: pantalla de "no disponible" con retorno al catálogo. |
| **Prioridad** | **Alta** |

#### RF13 — Realizar solicitud de compra

| Campo | Detalle |
|-------|---------|
| **Descripción** | El comprador registra una solicitud de compra sobre un producto disponible. |
| **Entradas** | Cantidad solicitada, mensaje inicial opcional para negociar. |
| **Salidas** | Solicitud creada en estado *solicitado*, visible tanto para el comprador como para el productor. |
| **Comportamiento esperado** | La cantidad no puede exceder la disponibilidad publicada. Se calcula un total de referencia para mostrar, pero el total real se define en el acuerdo. |
| **Excepciones** | Cantidad mayor a la disponible: rechazo con sugerencia de ajustar. Producto retirado entre carga y envío: error con invitación a revisar catálogo. Comprador con cuenta suspendida: rechazo con mensaje. |
| **Prioridad** | **Alta** |

---

### 2.4 Gestión del Acuerdo Comercial

#### RF14 — Consultar solicitudes recibidas (productor)

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor visualiza las solicitudes pendientes de respuesta y los acuerdos en curso. |
| **Entradas** | Filtros por estado. |
| **Salidas** | Listado con producto, comprador, cantidad, fecha de solicitud y estado. |
| **Comportamiento esperado** | Orden por defecto: las solicitudes nuevas primero. Indicador visual para destacar las que requieren acción inmediata. |
| **Excepciones** | Sin solicitudes: estado vacío con mensaje orientativo. |
| **Prioridad** | **Alta** |

#### RF15 — Aceptar solicitud y registrar acuerdo comercial

| Campo | Detalle |
|-------|---------|
| **Descripción** | Al aceptar una solicitud, el productor formaliza el acuerdo capturando los datos pactados (UC15 + UC16). |
| **Entradas** | Precio final (numérico), fecha programada de entrega, punto de entrega (del catálogo maestro), observaciones opcionales. |
| **Salidas** | Acuerdo en estado *aceptado* con datos completos; entrada en la bitácora de seguimiento. |
| **Comportamiento esperado** | Sin esos tres datos el acuerdo no puede pasar a *aceptado*. La cantidad disponible del producto se reduce por la cantidad pactada. |
| **Excepciones** | Punto de entrega inactivo: rechazo. Fecha programada en el pasado: rechazo. Precio no numérico o negativo: rechazo. |
| **Prioridad** | **Alta** |

#### RF16 — Rechazar solicitud

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor puede rechazar una solicitud con motivo documentado. |
| **Entradas** | Motivo (selección o texto libre) y observación opcional. |
| **Salidas** | Solicitud en estado *cancelado*; entrada en bitácora. |
| **Comportamiento esperado** | El comprador recibe notificación del rechazo con el motivo. La cantidad no se reserva. |
| **Excepciones** | Motivo vacío: rechazo de la acción. |
| **Prioridad** | **Alta** |

#### RF17 — Actualizar estado del acuerdo con seguimiento

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor (o admin) avanza el estado del acuerdo siguiendo el flujo: aceptado → preparando → programado → en_ruta → entregado_productor. |
| **Entradas** | Nuevo estado objetivo; comentario opcional de seguimiento. |
| **Salidas** | Estado del acuerdo actualizado; entrada en bitácora con comentario, usuario y fecha-hora (UC17). |
| **Comportamiento esperado** | Solo son válidas las transiciones contiguas definidas por el flujo. El comentario se almacena junto al cambio de estado y es visible en el detalle. |
| **Excepciones** | Transición no válida (saltarse estados): rechazo con indicación del estado actual. Acuerdo cancelado: ningún avance posible. |
| **Prioridad** | **Alta** |

#### RF18 — Marcar entrega realizada y confirmar recepción

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor marca la entrega realizada; el comprador confirma la recepción. |
| **Entradas** | Acción de marcar entrega (productor) y acción de confirmar recepción (comprador). |
| **Salidas** | Estado final *confirmado_comprador* si el comprador confirma; bitácora con ambas marcas. |
| **Comportamiento esperado** | Un acuerdo solo se considera *confirmada* cuando ambas partes actúan. Antes de la confirmación del comprador, el acuerdo queda en *entregado_productor* a la espera. |
| **Excepciones** | El productor no puede confirmar por el comprador. Pasados 7 días sin confirmación, el admin puede marcarla manualmente como *incumplida* con justificación. |
| **Prioridad** | **Alta** |

#### RF19 — Registrar estado de pago del acuerdo

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor o el administrador registran el estado de pago: pendiente, contra entrega o realizado. |
| **Entradas** | Estado de pago seleccionado. |
| **Salidas** | Campo `estado_pago` actualizado; entrada en bitácora. |
| **Comportamiento esperado** | El valor es declarativo: el sistema no procesa pagos electrónicos, solo registra lo acordado. |
| **Excepciones** | Acuerdo cancelado: no se permite modificar el estado de pago. |
| **Prioridad** | **Media** |

#### RF20 — Cancelar acuerdo por solicitud de cualquiera de las partes

| Campo | Detalle |
|-------|---------|
| **Descripción** | El comprador o el productor pueden solicitar cancelación de un acuerdo no completado, con motivo obligatorio. |
| **Entradas** | Motivo (selección predefinida) y observación. |
| **Salidas** | Acuerdo en estado *cancelado*; entrada en bitácora registrando quién cancela, motivo y observación. |
| **Comportamiento esperado** | La cantidad reservada del producto vuelve al inventario del productor. Solo se permite cancelar antes de que el comprador confirme la recepción. |
| **Excepciones** | Acuerdo ya confirmado: no se permite cancelar. Motivo vacío: rechazo. |
| **Prioridad** | **Alta** |

#### RF21 — Negociación por mensajería dentro del acuerdo

| Campo | Detalle |
|-------|---------|
| **Descripción** | Comprador y productor pueden intercambiar mensajes textuales dentro del acuerdo mientras no esté cancelado. |
| **Entradas** | Texto del mensaje. |
| **Salidas** | Mensaje persistido y visible en orden cronológico para ambas partes. |
| **Comportamiento esperado** | Los mensajes quedan asociados al acuerdo y auditados. El admin puede leerlos como parte de la supervisión o resolución de incidencias. |
| **Excepciones** | Acuerdo cancelado: chat en modo solo lectura. Mensaje vacío: no se envía. |
| **Prioridad** | **Alta** |

#### RF22 — Consultar mis acuerdos / mis compras

| Campo | Detalle |
|-------|---------|
| **Descripción** | El comprador ve "Mis Compras" y el productor ve "Mis Acuerdos" con pestañas por estado (pendientes, en proceso, completados, cancelados). |
| **Entradas** | Pestaña seleccionada. |
| **Salidas** | Lista filtrada con información resumida y enlace al detalle. |
| **Comportamiento esperado** | Cada usuario solo ve los acuerdos en los que es parte. El admin ve todos (ver RF29). |
| **Excepciones** | Sin acuerdos en la pestaña: estado vacío descriptivo. |
| **Prioridad** | **Alta** |

---

### 2.5 Catálogos Maestros (Administrador)

#### RF23 — Gestionar categorías de producto

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador crea, edita y activa/desactiva categorías de producto (UC30). |
| **Entradas** | Nombre, descripción, estado (activo/inactivo). |
| **Salidas** | Catálogo de categorías actualizado. |
| **Comportamiento esperado** | Una categoría inactiva no aparece como opción al publicar nuevos productos, pero los productos ya asociados no se invalidan. |
| **Excepciones** | Nombre duplicado: rechazo. Desactivar categoría con productos activos: advertencia pero se permite. |
| **Prioridad** | **Media** |

#### RF24 — Gestionar unidades de medida

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador gestiona las unidades de medida disponibles (UC31). |
| **Entradas** | Nombre, abreviatura, descripción, estado. |
| **Salidas** | Catálogo de unidades actualizado. |
| **Comportamiento esperado** | La abreviatura es única dentro de unidades activas. |
| **Excepciones** | Abreviatura duplicada: rechazo. |
| **Prioridad** | **Media** |

#### RF25 — Gestionar puntos de entrega

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador gestiona los puntos físicos reconocidos por la comunidad (UC34). |
| **Entradas** | Nombre, descripción, referencia (cómo llegar), estado. |
| **Salidas** | Catálogo de puntos de entrega actualizado. |
| **Comportamiento esperado** | Solo los puntos activos aparecen al formalizar un acuerdo. Los acuerdos existentes conservan el punto asignado aunque luego se desactive. |
| **Excepciones** | Nombre duplicado: rechazo. |
| **Prioridad** | **Media** |

---

### 2.6 Gestión de Usuarios (Administrador)

#### RF26 — Registrar nuevo usuario

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador da de alta un productor o comprador (UC22). |
| **Entradas** | DPI/CUI, nombre completo o razón social, tipo (productor/comprador), teléfono, dirección. |
| **Salidas** | Usuario creado en estado *activo* con PIN inicial 0000. |
| **Comportamiento esperado** | El teléfono será el identificador de login y no podrá modificarse después. Se envía SMS de verificación para validar el número. El usuario debe cambiar el PIN al primer ingreso. |
| **Excepciones** | DPI o teléfono ya registrados: rechazo. Teléfono con formato inválido: rechazo. SMS de verificación falla: se permite continuar y reintentar el envío después. |
| **Prioridad** | **Alta** |

#### RF27 — Editar usuario

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador modifica datos del usuario (UC23). |
| **Entradas** | Campos editables (nombre, dirección; no DPI, no teléfono principal, no tipo). |
| **Salidas** | Usuario actualizado; cambios auditados. |
| **Comportamiento esperado** | Los campos de identidad (DPI, tipo) y el teléfono principal de login permanecen inmutables para preservar la trazabilidad histórica. |
| **Excepciones** | Intento de modificar campos protegidos: rechazo. |
| **Prioridad** | **Media** |

#### RF28 — Reiniciar PIN de usuario

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador reinicia el PIN de un usuario a 0000 cuando éste lo solicita (UC24). |
| **Entradas** | Identificador del usuario. |
| **Salidas** | PIN reestablecido; acción auditada; usuario notificado. |
| **Comportamiento esperado** | En el siguiente inicio de sesión, el usuario está obligado a cambiar el PIN. |
| **Excepciones** | Usuario inexistente o bloqueado: rechazo. |
| **Prioridad** | **Alta** |

#### RF29 — Cambiar estado de cuenta (suspender / bloquear / reactivar)

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador controla el ciclo de vida de la cuenta del usuario (UC25). |
| **Entradas** | Acción (suspender, bloquear, reactivar) y motivo. |
| **Salidas** | Estado actualizado; acción auditada. |
| **Comportamiento esperado** | *Suspendido*: el usuario puede iniciar sesión pero no operar (solo ver). *Bloqueado*: no puede iniciar sesión. *Activo*: operación normal. |
| **Excepciones** | Motivo vacío al suspender/bloquear: rechazo. |
| **Prioridad** | **Alta** |

#### RF30 — Consultar y supervisar usuarios

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador consulta la lista de usuarios con filtros (productor / comprador), indicadores de confiabilidad (entregas completadas, reportes recibidos) y estado. |
| **Entradas** | Filtros y criterio de ordenamiento. |
| **Salidas** | Lista con datos resumidos y acciones disponibles. |
| **Comportamiento esperado** | Los indicadores se calculan a partir del historial del usuario en el sistema. |
| **Excepciones** | Sin usuarios en el filtro: estado vacío. |
| **Prioridad** | **Media** |

---

### 2.7 Incidencias y Supervisión

#### RF31 — Reportar inconformidad (comprador o productor)

| Campo | Detalle |
|-------|---------|
| **Descripción** | El comprador reporta inconformidad con una entrega; el productor puede reportar una incidencia del comprador (por ejemplo, incumplimiento de pago). |
| **Entradas** | Tipo de incidencia (inconformidad_cantidad, inconformidad_calidad, incumplimiento_entrega, otro), descripción. |
| **Salidas** | Incidencia creada en estado *abierto*, vinculada al acuerdo; bitácora actualizada. |
| **Comportamiento esperado** | El administrador recibe la notificación para revisión. La incidencia es visible para las partes y el admin. |
| **Excepciones** | Descripción vacía: rechazo. Acuerdo cancelado hace más de 30 días: no se permite reportar. |
| **Prioridad** | **Alta** |

#### RF32 — Registrar resolución de incidencia (administrador)

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador registra en el sistema la decisión adoptada por el comité fuera del sistema (UC26). **La mediación y la decisión ocurren fuera del software**; el sistema únicamente conserva constancia. |
| **Entradas** | Nuevo estado del reporte (en_revision, resuelto, descartado), texto de resolución. |
| **Salidas** | Incidencia actualizada; bitácora con la resolución registrada. |
| **Comportamiento esperado** | Una incidencia *resuelta* o *descartada* puede reabrirse solo por el mismo administrador con justificación. |
| **Excepciones** | Resolución vacía al marcar *resuelto*: rechazo. |
| **Prioridad** | **Alta** |

#### RF33 — Forzar cancelación de acuerdo (administrador)

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador puede cancelar un acuerdo cuando la mediación externa lo determina así (UC27). |
| **Entradas** | Motivo y observación. |
| **Salidas** | Acuerdo en estado *cancelado*; bitácora con la acción del administrador. |
| **Comportamiento esperado** | Acción de último recurso, siempre auditada con el identificador del administrador que la ejecuta. |
| **Excepciones** | Acuerdo ya confirmado: no se permite. |
| **Prioridad** | **Media** |

---

### 2.8 Reportes y Analítica

#### RF34 — Reportes generales de la Asociación

| Campo | Detalle |
|-------|---------|
| **Descripción** | El administrador consulta KPIs y gráficas agregadas de la comunidad (UC28). |
| **Entradas** | Rango de fechas opcional; filtros opcionales. |
| **Salidas** | Productores activos, compradores activos, productos publicados, solicitudes, entregas completadas, canceladas, incidencias, ventas por categoría, solicitudes por mes, distribución de acuerdos. |
| **Comportamiento esperado** | Los datos son **agregados y anonimizados**: no se identifica a productor ni comprador individual en la vista general. |
| **Excepciones** | Sin datos en el rango: gráficas vacías con mensaje. |
| **Prioridad** | **Media** |

#### RF35 — Historial de ventas del productor

| Campo | Detalle |
|-------|---------|
| **Descripción** | El productor consulta sus ventas pasadas con indicadores de ingreso, cumplimiento e incumplimiento (UC20). |
| **Entradas** | Filtro por año. |
| **Salidas** | Total vendido, cantidad de entregas confirmadas, incumplidas; gráfica de ingresos mensuales; lista de acuerdos pasados. |
| **Comportamiento esperado** | Solo muestra acuerdos en los que el productor es parte. |
| **Excepciones** | Sin historial: estado vacío. |
| **Prioridad** | **Media** |

#### RF36 — Bitácora de seguimiento por acuerdo

| Campo | Detalle |
|-------|---------|
| **Descripción** | El detalle de un acuerdo incluye una bitácora cronológica con cada cambio de estado, comentario, usuario y fecha-hora. |
| **Entradas** | Identificador del acuerdo. |
| **Salidas** | Lista de entradas de seguimiento. |
| **Comportamiento esperado** | Visible para las partes del acuerdo y el administrador. Inmutable desde la interfaz: los registros no se editan ni se borran. |
| **Excepciones** | Acuerdo inexistente: pantalla de error. |
| **Prioridad** | **Alta** |

---

### 2.9 Auditoría, Notificaciones y Sincronización

#### RF37 — Registro de auditoría del sistema

| Campo | Detalle |
|-------|---------|
| **Descripción** | Toda acción sensible queda registrada en una bitácora de auditoría: alta/edición de usuario, cambios de estado de cuenta, reinicio de PIN, modificaciones de catálogos maestros, transiciones de acuerdo, resoluciones de incidencia y forzados de cancelación. |
| **Entradas** | (evento generado por las operaciones del sistema). |
| **Salidas** | Registro persistente con usuario, acción, entidad afectada, valores antes/después y fecha-hora. |
| **Comportamiento esperado** | El administrador puede consultar y filtrar la bitácora. El registro no es editable desde la aplicación. |
| **Excepciones** | Si el registro de auditoría falla, la acción primaria también falla (fallas-fuerte). |
| **Prioridad** | **Alta** |

#### RF38 — Notificaciones al usuario

| Campo | Detalle |
|-------|---------|
| **Descripción** | El sistema notifica al usuario los eventos relevantes: nueva solicitud recibida, aceptación o rechazo, cambio de estado del acuerdo, nueva entrada en bitácora, incidencia reportada o resuelta. |
| **Entradas** | Eventos del sistema. |
| **Salidas** | Notificación visible dentro de la app (campana/listado); opcionalmente, SMS para eventos críticos (aceptación, cancelación, entrega). |
| **Comportamiento esperado** | Las notificaciones in-app son gratuitas y se muestran al abrir sesión. Las SMS se usan con moderación para contener costos. |
| **Excepciones** | Falla del gateway SMS: la notificación in-app sigue funcionando y se reintenta SMS automáticamente. |
| **Prioridad** | **Media** |

#### RF39 — Validación por rol para acciones sensibles

| Campo | Detalle |
|-------|---------|
| **Descripción** | Las acciones sensibles (alta de usuarios, gestión de catálogos maestros, forzar cancelación, resolución de incidencias) solo pueden ejecutarlas usuarios con rol de administrador. |
| **Entradas** | Acción solicitada y usuario autenticado. |
| **Salidas** | Ejecución autorizada o rechazo (403). |
| **Comportamiento esperado** | La validación ocurre tanto en la interfaz (ocultar opciones no permitidas) como en la API (enforce por backend). |
| **Excepciones** | Intento de acceso no autorizado: registro en auditoría del intento fallido. |
| **Prioridad** | **Alta** |

#### RF40 — Operación offline con sincronización

| Campo | Detalle |
|-------|---------|
| **Descripción** | El sistema permite consultar el catálogo cacheado y registrar acciones (nueva solicitud, cambio de estado, comentario) sin conexión; al recuperar conectividad sincroniza con el servidor. |
| **Entradas** | Acciones del usuario en modo desconectado. |
| **Salidas** | Acciones en cola local; confirmación tras sincronización exitosa. |
| **Comportamiento esperado** | El navegador mantiene un almacén local (IndexedDB) con los datos cacheados y la cola de sincronización. Al reconectar, se envían en orden. Si hay conflicto (ej. producto retirado en el servidor), el sistema notifica al usuario y cancela la acción pendiente. |
| **Excepciones** | Conflicto de versión: se muestra al usuario la divergencia y se descarta la acción local. Pérdida del almacén local: se exige reconectar para reintentar. |
| **Prioridad** | **Media** |

---

### Matriz resumen de prioridades

| Prioridad | Cantidad | Criterio |
|-----------|---------:|----------|
| **Alta** | 24 | Procesos núcleo del negocio que el sistema automatiza directamente (autenticación, catálogo, solicitudes, acuerdos, entrega, confirmación, incidencias, auditoría, roles). |
| **Media** | 16 | Procesos de apoyo (catálogos maestros, reportes, notificaciones, offline, historial, perfil, invitado, cancelación forzada). |
| **Baja** | 0 | — |

*La prioridad se usa como criterio para planificar la implementación en fases: los RF de prioridad Alta deben estar operativos en la primera iteración del sistema; los de prioridad Media en la segunda; los de prioridad Baja pueden diferirse.*

---

---

## 3. Requerimientos No Funcionales

Los requerimientos no funcionales (RNF) definen las cualidades del sistema más allá de su comportamiento funcional. Se agrupan por atributo de calidad y se identifican con el prefijo **RNF**. Cada requerimiento incluye una condición medible o verificable siempre que resulta posible, para facilitar su validación durante las pruebas de aceptación.

### 3.1 Rendimiento

El sistema opera en un contexto de conectividad variable y dispositivos de gama baja, por lo que el rendimiento se dimensiona para garantizar la usabilidad en el peor escenario razonable.

#### RNF01 — Tiempo de carga inicial

La aplicación debe alcanzar el **First Contentful Paint** en un tiempo menor o igual a **3 segundos** sobre una conexión 3G simulada (1.6 Mbps / 300 ms RTT) y el **Time to Interactive** en un tiempo menor o igual a **5 segundos**, medido con herramientas estándar (Lighthouse). El tamaño inicial del bundle principal no debe exceder **250 KB** comprimido (gzip).

#### RNF02 — Tiempo de respuesta de consultas

Las consultas de catálogo, lista de acuerdos y detalle de producto deben retornar una respuesta del servidor en menos de **500 ms** en el percentil 95, asumiendo una base con hasta 5 000 productos y 10 000 acuerdos. Las operaciones de escritura (registrar solicitud, aceptar acuerdo, cambiar estado) deben responder en menos de **1 segundo** en el mismo percentil.

#### RNF03 — Carga concurrente esperada

El sistema debe soportar como mínimo **50 usuarios concurrentes** en su despliegue inicial, escalando a **500 usuarios concurrentes** en un horizonte de dos años sin cambios arquitectónicos significativos.

#### RNF04 — Consumo de datos móviles

La carga inicial consumirá a lo sumo **300 KB** de datos; la navegación típica tras la carga inicial debe mantenerse bajo **50 KB por pantalla nueva**. El catálogo cacheado debe reutilizarse offline para evitar consumo repetido.

#### RNF05 — Uso de almacenamiento local

La aplicación no debe ocupar más de **10 MB** de almacenamiento en el dispositivo del cliente para catálogo cacheado, cola de sincronización offline y datos de sesión. Al aproximarse a ese límite, se aplica política LRU sobre el catálogo antiguo.

---

### 3.2 Seguridad

#### RNF06 — Transporte cifrado

Todas las comunicaciones entre el cliente y el servidor deben realizarse sobre **HTTPS** con certificado válido y TLS 1.2 o superior. Peticiones por HTTP deben redirigirse de manera automática a HTTPS.

#### RNF07 — Almacenamiento de credenciales

Los PIN de los usuarios deben almacenarse aplicando un algoritmo de hashing seguro diseñado para contraseñas (**bcrypt** con factor de costo mínimo 10, o **argon2id**). En ningún caso se almacenan en texto plano ni con hashes rápidos (MD5, SHA-1, SHA-256 sin sal).

#### RNF08 — Autenticación por sesión con expiración

La autenticación se basa en un **token de sesión** (JWT firmado o token opaco en base de datos) con expiración máxima de **8 horas** de inactividad o **12 horas** absolutas. La expiración obliga a reautenticarse con teléfono y PIN.

#### RNF09 — Control de acceso basado en rol (RBAC)

El sistema valida el rol del usuario tanto en la interfaz (ocultando opciones no permitidas) como en el servidor (rechazando peticiones con **403** cuando el rol no autoriza la operación). La validación del servidor es obligatoria e independiente del cliente.

#### RNF10 — Protección contra fuerza bruta

Tras **5 intentos fallidos consecutivos** de inicio de sesión desde el mismo número de teléfono se aplica un bloqueo temporal de **10 minutos**. La contabilidad se reinicia tras un inicio de sesión exitoso o al término del bloqueo.

#### RNF11 — Protección de datos personales en tránsito y en reposo

Los datos personales (DPI/CUI, teléfono, dirección) se almacenan en columnas con acceso restringido a nivel de base de datos. Los respaldos se cifran con una clave rotada anualmente. Ningún dato personal aparece en URLs, logs de acceso o mensajes de error.

#### RNF12 — Registro de auditoría inmutable desde la aplicación

La bitácora de auditoría (RF37) no puede editarse ni eliminarse desde la interfaz. Desde la base de datos, el acceso directo al log está restringido al DBA y cualquier modificación queda registrada en el log del motor.

#### RNF13 — Política de contraseñas mínimas para administradores

Los usuarios con rol administrador deben utilizar un PIN de **6 dígitos** en lugar de 4, con rotación obligatoria cada 90 días y bloqueo de cuentas inactivas por más de 60 días.

#### RNF14 — Encabezados de seguridad del navegador

La aplicación sirve los encabezados **Content-Security-Policy**, **X-Frame-Options: DENY**, **X-Content-Type-Options: nosniff** y **Referrer-Policy: strict-origin-when-cross-origin** para mitigar XSS, clickjacking y filtración de referer.

---

### 3.3 Escalabilidad

#### RNF15 — Arquitectura sin estado

La API debe ser **stateless**: el servidor no mantiene sesión en memoria. Esto permite escalar horizontalmente agregando réplicas detrás de un balanceador de carga sin sesiones pegajosas.

#### RNF16 — Crecimiento de datos soportado

El modelo de datos debe soportar **50 000 productos publicados** y **200 000 acuerdos** sin degradación observable de los tiempos de respuesta definidos en RNF02. Se asume el uso de índices en los campos de búsqueda (nombre de producto, estado de acuerdo, fechas).

#### RNF17 — Separación de cargas de trabajo

La generación de reportes pesados (RF34) se realiza en modo asíncrono (job en segundo plano) cuando el tamaño del rango excede 1 000 registros, para no bloquear el hilo de la API.

#### RNF18 — Despliegue reproducible

La infraestructura debe poder replicarse en un entorno nuevo mediante archivos de configuración versionados (Docker Compose, Terraform o equivalente) para habilitar staging, producción y eventualmente réplicas regionales.

---

### 3.4 Usabilidad

La comunidad "La Esperanza" presenta baja alfabetización digital en una parte significativa de sus productores. La usabilidad es una prioridad alta del diseño.

#### RNF19 — Diseño responsive

La interfaz debe visualizarse correctamente en dispositivos desde **320 px de ancho** hasta escritorio (mínimo 1440 px), sin scroll horizontal. La transición entre breakpoints se prueba en los tamaños: 320, 375, 768, 1024, 1440 px.

#### RNF20 — Tipografía y contraste accesibles

Todos los textos principales usan tamaño mínimo de **16 px** (1 rem) y los encabezados no bajan de 20 px. La relación de contraste entre texto y fondo cumple **WCAG 2.1 nivel AA** (4.5:1 para texto normal, 3:1 para texto grande). Los botones de acción tienen un área mínima táctil de **48 × 48 px**.

#### RNF21 — Idioma claro y orientado a la comunidad

Toda la interfaz está en **español** con vocabulario directo y evitando tecnicismos. Los mensajes de error orientan al usuario a la solución (p. ej.: "Verifica tu número de teléfono y PIN" en lugar de "Invalid credentials").

#### RNF22 — Flujos cortos para operaciones frecuentes

Las operaciones más frecuentes (iniciar sesión, publicar producto, registrar solicitud, aceptar solicitud) deben completarse en un máximo de **3 pantallas** o pasos visibles para el usuario.

#### RNF23 — Retroalimentación visible del sistema

Toda acción del usuario debe mostrar retroalimentación en menos de **300 ms**: un estado de carga, un mensaje de éxito, o un mensaje de error claro. Las operaciones asíncronas muestran indicador de progreso.

#### RNF24 — Navegación consistente por rol

Cada rol tiene un menú lateral (escritorio) y barra inferior (móvil) estables, con los íconos fijos en la misma posición entre sesiones para facilitar la memorización espacial.

#### RNF25 — Curva de aprendizaje medida

Un usuario nuevo con alfabetización digital básica debe poder realizar las operaciones principales del flujo (publicar un producto, aceptar una solicitud, confirmar recepción) tras una **sesión de capacitación inicial de 30 minutos**. Este requerimiento se valida con pruebas con usuarios reales antes del despliegue.

---

### 3.5 Mantenibilidad

#### RNF26 — Separación en capas

La solución se desarrolla separando las capas **Presentación**, **Lógica de negocio / API**, **Persistencia** y **Catálogos maestros**, de modo que cambios en una capa no afecten las otras salvo cambios de contrato explícitos.

#### RNF27 — Patrones de diseño aplicados al código fuente

Conforme al requisito explícito del curso para la fase final, el código aplica al menos tres patrones de diseño (como mínimo): uno estructural (por ejemplo, Repository o Adapter), uno creacional (por ejemplo, Factory o Builder) y uno de comportamiento (por ejemplo, Strategy, Observer o State para el ciclo del acuerdo). La documentación técnica incluye el listado de patrones aplicados, el archivo donde aparece cada uno y su motivación.

#### RNF28 — Cobertura de pruebas automatizadas

El módulo de lógica de negocio crítica (ciclo de acuerdos, validaciones de transición, cálculo de precios) debe tener cobertura de pruebas unitarias mínima del **70 %**. Las rutas principales de la API deben contar con pruebas de integración para los casos felices y los principales casos de error.

#### RNF29 — Trazabilidad de cambios en código

El proyecto se versiona en Git con convención de commits (p. ej. *Conventional Commits*), ramas por funcionalidad y pull requests revisados antes de mezclar en la rama principal.

#### RNF30 — Logging operativo

El servidor registra en logs estructurados (JSON) los eventos relevantes: inicios de sesión, errores de validación, fallos del gateway SMS, excepciones no controladas. Los logs tienen niveles (debug, info, warn, error) y se retienen al menos **30 días**.

#### RNF31 — Costos de mantenimiento documentados

Dado que la Asociación no cuenta con personal técnico propio, la entrega final incluye un **manual operativo** con los costos recurrentes de mantenimiento (hosting, dominio, SMS, respaldo) y una estimación de costo del proveedor externo de soporte. Este documento acompaña al código fuente.

---

### 3.6 Compatibilidad

#### RNF32 — Navegadores soportados

La aplicación funciona correctamente en las **dos últimas versiones mayores estables** de Chrome, Firefox, Safari y Edge al momento del despliegue. Específicamente se comprometen versiones Chrome ≥ 100, Firefox ≥ 100, Safari ≥ 15 y Edge ≥ 100. No se soporta Internet Explorer ni navegadores descontinuados.

#### RNF33 — Compatibilidad con dispositivos móviles

Se valida el funcionamiento sobre Android 8 o superior y iOS 14 o superior, en dispositivos con al menos 2 GB de memoria RAM. Los teléfonos básicos sin navegador web no son soportados directamente: para esos usuarios el acceso se realiza a través de un representante de la Asociación (ver supuestos 1.3.1).

#### RNF34 — Progressive Web App instalable

La aplicación cumple con los criterios de **PWA** (manifiesto web, service worker, HTTPS) y es instalable en la pantalla de inicio del dispositivo para ofrecer experiencia similar a aplicación nativa sin requerir la Play Store / App Store.

#### RNF35 — Independencia de proveedores cerrados

La solución evita dependencias cerradas del lado del cliente que impidan cambiar de proveedor de infraestructura. El almacenamiento, el gateway SMS y el hosting se pueden intercambiar sin reescribir el código de la lógica de negocio.

---

### 3.7 Legalidad

En ausencia de un marco normativo específico aportado por el cliente en esta fase, los requerimientos de legalidad se formulan de manera **conceptual**, estableciendo principios y deberes genéricos alineados con las leyes de protección de datos personales vigentes en la jurisdicción donde opere el sistema. Los detalles contractuales y formales se completan en una fase posterior con asesoría legal.

#### RNF36 — Consentimiento informado de los usuarios

Al dar de alta a un usuario, la Asociación le entrega un documento de consentimiento que explica:

- Qué datos personales se registran (nombre, DPI, teléfono, dirección).
- Para qué se usan (operar el sistema de comercialización).
- Quién tiene acceso (la Asociación y los contrapartes de acuerdos en curso).
- Durante cuánto tiempo se conservan (política de retención definida por la Asociación).

El usuario acepta formalmente antes de que su cuenta sea activada.

#### RNF37 — Minimización y finalidad

El sistema solo recolecta y expone los datos personales necesarios para operar las funcionalidades descritas. En vistas públicas (catálogo, dashboard) se muestra únicamente el nombre del productor / comprador y nunca datos sensibles como el DPI completo.

#### RNF38 — Derecho de acceso, rectificación y portabilidad

Todo usuario puede solicitar a la Asociación una copia de sus datos personales, su rectificación o la portabilidad a otro sistema. La Asociación responde en un plazo razonable (propuesto: 15 días hábiles) y el sistema ofrece exportación de los datos del usuario en formato legible por humanos (CSV o PDF).

#### RNF39 — Derecho al olvido y retención de datos

Al solicitar la baja, la cuenta del usuario se desactiva de inmediato y sus datos personales se anonimizan pasados **24 meses** desde la última transacción abierta, conservando únicamente los datos estadísticos necesarios para reportes agregados y auditoría.

#### RNF40 — Auditoría accesible para la autoridad

La bitácora de auditoría del sistema (RF37) está disponible para consultoría interna de la Asociación y, en caso de requerirlo una autoridad competente bajo orden formal, exportable en formato estructurado (JSON o CSV).

#### RNF41 — Responsabilidad del tratamiento

La Asociación Comunitaria "La Esperanza" es el **responsable del tratamiento** de los datos. El proveedor de desarrollo y de infraestructura actúan como **encargados del tratamiento** y no pueden usar los datos para fines distintos a operar el sistema.

---

---

## 4. Casos de Uso

El diagrama general de actores y casos de uso se mantiene en [modelo-casos-de-uso.md](./modelo-casos-de-uso.md), con las actualizaciones hechas en la fase 2 (UC12 reformulado, UC34 añadido, estados intermedios formalizados, flechas *genera* desde UC14/UC15/UC18/UC8 hacia UC17).

En esta sección se detallan los casos de uso que corresponden a **procesos núcleo automatizados** (los que en la Sección 2 fueron marcados de prioridad Alta). Para cada uno se especifican actores, precondiciones, postcondiciones, flujo principal, flujos alternativos, excepciones y la trazabilidad con los requerimientos funcionales que lo implementan.

Los casos de uso no detallados aquí (UC2, UC3, UC6, UC13, UC20, UC21 como contenedor, UC23, UC24, UC25, UC28, UC29, UC30, UC31, UC33, UC34, UC32) son de tipo CRUD o consulta directa y quedan cubiertos por las Historias de Usuario de la Sección 6.

---

### CU-01 — Iniciar sesión

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Usuario registrado (Comprador, Productor o Administrador). |
| **Actores secundarios** | Gateway SMS (solo si RF05 recuperación). |
| **Descripción** | El usuario se autentica con teléfono y PIN para acceder a las funcionalidades de su rol. |
| **Precondiciones** | El usuario existe en el sistema con estado *activo* o *suspendido* y conoce su teléfono y PIN. |
| **Postcondición éxito** | Sesión iniciada con rol y redirección al panel correspondiente. |
| **Postcondición fracaso** | Usuario permanece en pantalla de login con mensaje de error y contador de intentos decrementado. |
| **Requerimientos asociados** | RF01, RF10, RNF06, RNF07, RNF08. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El usuario abre la aplicación y selecciona "Iniciar sesión".
2. El sistema muestra el formulario con campos para teléfono y PIN.
3. El usuario ingresa su número de teléfono.
4. El usuario ingresa su PIN de 4 dígitos.
5. El usuario confirma el envío.
6. El sistema valida las credenciales contra la base de datos.
7. El sistema genera un token de sesión válido por 8 horas de inactividad.
8. El sistema redirige al panel correspondiente al rol.

**Flujos alternativos**

- **5a. Acceso como invitado.** El usuario presiona "Ver catálogo sin cuenta" y el sistema lo redirige al catálogo público (UC2) sin crear sesión.
- **6a. Cuenta suspendida.** El sistema informa que la cuenta permite solo consulta y limita las acciones en el cliente.

**Excepciones**

- **E1. Credenciales incorrectas.** El sistema muestra "Verifica tu número y PIN" sin especificar cuál campo falló; incrementa el contador de intentos. Tras 5 intentos consecutivos, bloqueo temporal de 10 minutos (RF10).
- **E2. Cuenta bloqueada.** El sistema muestra "Tu cuenta está bloqueada. Contacta a la Asociación" y no crea sesión.
- **E3. PIN olvidado.** El usuario selecciona "Olvidé mi PIN" y el sistema inicia UC de recuperación por SMS (RF05).
- **E4. Sin conexión.** El sistema informa que se requiere internet para iniciar sesión y sugiere reintentar.

---

### CU-02 — Realizar solicitud de compra

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Comprador autenticado. |
| **Actores secundarios** | Productor (recibe la solicitud como notificación). |
| **Descripción** | El comprador registra una solicitud de compra sobre un producto del catálogo. |
| **Precondiciones** | El comprador está autenticado con cuenta activa. El producto existe, está disponible y tiene cantidad mayor a cero. |
| **Postcondición éxito** | Solicitud creada en estado *solicitado*, visible para comprador y productor. Entrada inicial en bitácora de seguimiento. |
| **Postcondición fracaso** | Ninguna solicitud creada. El comprador ve el motivo del rechazo. |
| **Requerimientos asociados** | RF11, RF12, RF13, RF21, RF36. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El comprador consulta el catálogo y selecciona un producto disponible (UC2, UC3).
2. El sistema muestra el detalle del producto con el formulario de solicitud.
3. El comprador ingresa la cantidad deseada dentro del rango disponible.
4. El comprador redacta un mensaje inicial opcional para el productor.
5. El comprador confirma la solicitud.
6. El sistema valida cantidad y estado del producto.
7. El sistema crea la solicitud en estado *solicitado* con un identificador único.
8. El sistema registra la primera entrada en la bitácora con comentario "Solicitud registrada por el comprador".
9. El sistema notifica al productor (in-app).
10. El sistema muestra pantalla de confirmación con enlace a "Mis Compras".

**Flujos alternativos**

- **4a. Sin mensaje adicional.** El comprador omite el mensaje y continúa con el flujo principal.

**Excepciones**

- **E1. Cantidad mayor a la disponible.** El sistema rechaza con "La cantidad supera la disponibilidad" y sugiere ajustar.
- **E2. Producto retirado entre la carga y el envío.** El sistema muestra "Este producto ya no está disponible" y ofrece volver al catálogo.
- **E3. Comprador suspendido.** El sistema rechaza con mensaje específico y log de intento.
- **E4. Sin conexión.** La solicitud se registra en cola local y se sincroniza al reconectar (RF40). Si al sincronizar el producto ya no está disponible, se notifica al comprador y se descarta la acción.

---

### CU-03 — Aceptar solicitud y registrar acuerdo comercial

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Productor autenticado dueño del producto. |
| **Actores secundarios** | Comprador (recibe notificación). |
| **Descripción** | El productor acepta una solicitud pendiente y, en el mismo paso, formaliza el acuerdo comercial capturando precio final, fecha programada y punto de entrega (UC14 + UC15 + UC16 unificados en el prototipo). |
| **Precondiciones** | El productor está autenticado. Existe una solicitud en estado *solicitado* sobre un producto propio. |
| **Postcondición éxito** | Acuerdo en estado *aceptado* con precio final, fecha programada, punto de entrega y observaciones. Cantidad disponible del producto reducida. Entrada en bitácora. Comprador notificado. |
| **Postcondición fracaso** | Solicitud permanece en estado *solicitado*. Ninguna reserva aplicada. |
| **Requerimientos asociados** | RF14, RF15, RF25, RF36, RF38. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El productor ingresa a "Mis Acuerdos" y abre una solicitud en estado *solicitado*.
2. El sistema muestra el detalle del acuerdo con el botón "Aceptar Solicitud".
3. El productor presiona "Aceptar Solicitud".
4. El sistema presenta el modal "Registrar Acuerdo Comercial" con los campos: precio final, fecha programada, punto de entrega (lista del catálogo maestro) y observaciones.
5. El productor completa los campos obligatorios y opcionalmente las observaciones.
6. El productor confirma la aceptación.
7. El sistema valida los datos (precio numérico, fecha futura, punto de entrega activo).
8. El sistema actualiza el acuerdo: estado *aceptado*, campos del acuerdo persistidos, cantidad reservada en el producto.
9. El sistema agrega entrada a la bitácora con comentario "Acuerdo registrado: precio Q{valor}, fecha {d}, punto {nombre}".
10. El sistema notifica al comprador.

**Flujos alternativos**

- **4a. Rechazar solicitud.** El productor selecciona "Rechazar" en lugar de "Aceptar" y el sistema abre el modal de cancelación con motivo obligatorio (CU-07).

**Excepciones**

- **E1. Punto de entrega inactivo.** El sistema lo oculta de la lista; si el productor requiere uno nuevo, debe solicitar a la Asociación registrarlo (UC34).
- **E2. Fecha programada en el pasado.** El sistema rechaza con indicación de seleccionar fecha futura.
- **E3. Precio no numérico o negativo.** Validación inline en el campo.
- **E4. Solicitud ya tomada por otra vía o cancelada.** El sistema informa que el estado cambió y refresca el detalle.
- **E5. Sin conexión.** La aceptación se encola y se sincroniza al reconectar; se advierte al productor que el acuerdo aún no es visible para el comprador hasta sincronizar.

---

### CU-04 — Actualizar seguimiento de la entrega

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Productor (o Administrador en excepcional). |
| **Descripción** | El productor avanza el estado del acuerdo dentro del flujo logístico y registra un comentario de seguimiento en cada transición. |
| **Precondiciones** | Acuerdo en estado *aceptado*, *preparando*, *programado* o *en_ruta*. |
| **Postcondición éxito** | Estado del acuerdo actualizado. Nueva entrada en bitácora con usuario, comentario y fecha-hora. |
| **Postcondición fracaso** | Estado del acuerdo sin cambios. |
| **Requerimientos asociados** | RF17, RF36. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El productor abre el detalle del acuerdo.
2. El sistema muestra el botón de acción correspondiente al estado actual (p. ej. "Iniciar Ruta" si está en *programado*).
3. El productor presiona el botón de avance.
4. El sistema presenta un modal solicitando un comentario de seguimiento (opcional).
5. El productor redacta el comentario o lo deja vacío.
6. El productor confirma la transición.
7. El sistema valida que la transición sea la contigua al estado actual.
8. El sistema actualiza el estado del acuerdo.
9. El sistema agrega la entrada a la bitácora con el comentario, el usuario y la fecha-hora actual.
10. El sistema notifica al comprador del nuevo estado.

**Flujos alternativos**

- **5a. Comentario genérico.** Si el productor no ingresa comentario, el sistema usa el texto por defecto "Estado actualizado a {estado}".

**Excepciones**

- **E1. Transición no válida.** El sistema rechaza con "No se puede saltar a ese estado desde el actual".
- **E2. Acuerdo cancelado.** No se permite ningún avance; el detalle muestra los botones deshabilitados.
- **E3. Sin conexión.** La transición y el comentario se encolan; al sincronizar se aplican en orden.

---

### CU-05 — Marcar entrega realizada y confirmar recepción

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Productor (marca entrega) y Comprador (confirma recepción). |
| **Descripción** | Cierre del ciclo del acuerdo: el productor marca la entrega y el comprador la confirma. Ambas acciones son obligatorias para considerar la entrega como *confirmada*. |
| **Precondiciones** | Acuerdo en estado *en_ruta* (para el productor) o *entregado_productor* (para el comprador). |
| **Postcondición éxito** | Acuerdo en estado *confirmado_comprador*. `estado_final = confirmada`. Bitácora con ambas marcas. |
| **Postcondición fracaso** | Acuerdo en un estado intermedio; puede requerirse intervención del administrador. |
| **Requerimientos asociados** | RF17, RF18, RF36. |
| **Prioridad** | Alta. |

**Flujo principal (parte del productor)**

1. El productor, tras completar el traslado, abre el acuerdo y presiona "Marcar como Entregada".
2. El sistema presenta el modal de seguimiento (ver CU-04) con comentario opcional.
3. El productor confirma.
4. El sistema actualiza el estado a *entregado_productor*.
5. El sistema notifica al comprador solicitando confirmación.

**Flujo principal (parte del comprador)**

6. El comprador abre el acuerdo y revisa el detalle.
7. El comprador presiona "Confirmar Recepción".
8. El sistema cambia el estado a *confirmado_comprador*, marca `estado_final = confirmada` y registra la entrada en bitácora.
9. El sistema muestra la confirmación visual "Entrega confirmada por ambas partes. Acuerdo completado".

**Flujos alternativos**

- **6a. Comprador reporta inconformidad.** El comprador presiona "Reportar Inconformidad" en vez de confirmar (CU-08).
- **6b. Comprador inactivo 7 días.** El administrador puede marcar manualmente el `estado_final` como *incumplida* con justificación (UC19).

**Excepciones**

- **E1. Productor marca entrega prematuramente.** El estado solo avanza si el anterior era *en_ruta*; caso contrario, rechazo.
- **E2. Comprador confirma antes de la marca del productor.** No permitido; el botón aparece solo cuando el estado es *entregado_productor*.

---

### CU-06 — Consultar catálogo de productos

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Invitado, Comprador, Productor, Administrador. |
| **Descripción** | Consulta del catálogo público con búsqueda, filtros y ordenamiento. |
| **Precondiciones** | Ninguna (accesible sin sesión). |
| **Postcondición éxito** | Se muestra la lista de productos disponibles. |
| **Postcondición fracaso** | Mensaje indicando que no se pudo cargar el catálogo; en modo offline se usa el cache local. |
| **Requerimientos asociados** | RF02, RF11, RF40. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El usuario abre la sección "Catálogo" / "Productos".
2. El sistema carga la lista de productos *disponibles* ordenada por disponibilidad.
3. El usuario puede filtrar por categoría o texto.
4. El usuario puede cambiar el criterio de ordenamiento (disponibilidad, categoría, precio, unidad).
5. El sistema aplica el filtro/orden y actualiza la lista.

**Flujos alternativos**

- **5a. Productos retirados o agotados.** El sistema los excluye del catálogo público pero los conserva en la base para auditoría.
- **5b. Modo invitado.** Los productos aparecen, pero los botones de acción dirigen al login.

**Excepciones**

- **E1. Sin productos coincidentes con el filtro.** El sistema muestra estado vacío con mensaje amigable.
- **E2. Sin conexión.** El sistema carga el catálogo cacheado localmente y muestra aviso "Versión local — última actualización {fecha}".

---

### CU-07 — Solicitar cancelación de acuerdo

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Comprador o Productor. |
| **Actores secundarios** | Contraparte del acuerdo (recibe notificación). |
| **Descripción** | Cualquiera de las partes solicita cancelar un acuerdo antes de que el comprador confirme recepción, con motivo obligatorio. |
| **Precondiciones** | Acuerdo no confirmado ni cancelado. |
| **Postcondición éxito** | Acuerdo en estado *cancelado* con motivo y observación registrados. Cantidad reservada liberada al inventario del productor. |
| **Postcondición fracaso** | Acuerdo sin cambios. |
| **Requerimientos asociados** | RF20, RF36. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El usuario abre el detalle del acuerdo.
2. El usuario presiona "Cancelar Solicitud" (comprador) o "Rechazar Solicitud" (productor, si estado *solicitado*).
3. El sistema presenta el modal de cancelación con motivo en lista desplegable y observación libre.
4. El usuario selecciona motivo y redacta observación opcional.
5. El usuario confirma.
6. El sistema valida que el motivo no esté vacío.
7. El sistema actualiza el acuerdo a estado *cancelado* con registro de quién canceló.
8. El sistema libera la cantidad reservada en el producto.
9. El sistema agrega entrada a la bitácora.
10. El sistema notifica a la contraparte.

**Flujos alternativos**

- **5a. Admin fuerza cancelación.** El administrador entra al acuerdo y ejecuta CU-07 con su rol; el sistema registra "Cancelado por Administrador" (ver UC27).

**Excepciones**

- **E1. Acuerdo ya confirmado.** El sistema rechaza con "Este acuerdo ya fue confirmado por ambas partes".
- **E2. Motivo vacío.** El botón permanece deshabilitado hasta completar el motivo.

---

### CU-08 — Reportar inconformidad

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Comprador (principal), Productor (secundario). |
| **Actores secundarios** | Administrador (revisa el reporte). |
| **Descripción** | Cualquiera de las partes reporta una inconformidad relativa a un acuerdo. El sistema registra el caso; la resolución la media el comité fuera del sistema (ver supuestos 1.3.1). |
| **Precondiciones** | Existe un acuerdo sobre el que se reporta. La parte reportante está autenticada. |
| **Postcondición éxito** | Reporte de incidencia creado en estado *abierto*, vinculado al acuerdo. Administrador notificado. |
| **Postcondición fracaso** | Ninguna incidencia creada. |
| **Requerimientos asociados** | RF31, RF38. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El usuario abre el detalle del acuerdo.
2. El usuario presiona "Reportar Inconformidad".
3. El sistema presenta el modal con:
   - Tipo de incidencia (inconformidad_cantidad, inconformidad_calidad, incumplimiento_entrega, otro).
   - Descripción libre obligatoria.
4. El usuario completa los campos.
5. El usuario confirma el envío.
6. El sistema valida descripción no vacía.
7. El sistema crea la incidencia en estado *abierto*, vinculada al acuerdo y al usuario reportante.
8. El sistema agrega una entrada en la bitácora del acuerdo.
9. El sistema notifica al administrador.
10. El sistema muestra confirmación al reportante: "Reporte enviado a la Asociación para revisión".

**Flujos alternativos**

- **2a. Durante la entrega misma.** El comprador puede reportar directamente desde el estado *entregado_productor* sin confirmar recepción.

**Excepciones**

- **E1. Descripción vacía.** El botón permanece deshabilitado.
- **E2. Acuerdo cancelado hace más de 30 días.** El sistema rechaza: el caso debe tratarse por los canales de la Asociación directamente.

---

### CU-09 — Resolver incidencia (registrar decisión del comité)

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Administrador / Asociación. |
| **Descripción** | El administrador registra en el sistema la decisión adoptada por el comité fuera del software sobre una incidencia reportada. La mediación y deliberación ocurren en asamblea o reunión; el sistema solo conserva constancia formal de la decisión. |
| **Precondiciones** | Existe una incidencia en estado *abierto* o *en_revision*. |
| **Postcondición éxito** | Incidencia actualizada con nuevo estado, resolución textual, fecha y administrador responsable. Bitácora del acuerdo actualizada. |
| **Postcondición fracaso** | Incidencia sin cambios. |
| **Requerimientos asociados** | RF32, RF37, RF39. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El administrador abre el detalle del acuerdo con la incidencia.
2. El administrador presiona "Resolver Incidencia".
3. El sistema presenta el modal con:
   - Tipo de incidencia (preseleccionado).
   - Descripción (preseleccionada).
   - Estado del reporte (abierto, en_revision, resuelto, descartado).
   - Texto de resolución obligatorio si marca *resuelto*.
4. El administrador selecciona el nuevo estado y redacta la resolución.
5. El administrador confirma.
6. El sistema valida que la resolución no esté vacía si el estado es *resuelto*.
7. El sistema actualiza la incidencia.
8. El sistema agrega entrada en la bitácora del acuerdo: "Resolución de incidencia: {tipo} — {resolución}".
9. El sistema notifica a ambas partes del acuerdo.

**Flujos alternativos**

- **4a. Descartar la incidencia.** Si el administrador considera que el reporte no aplica, selecciona *descartado* y describe el motivo.
- **4b. Reabrir incidencia.** Una incidencia *resuelta* o *descartada* puede reabrirse con justificación (auditable).

**Excepciones**

- **E1. Resolución vacía al marcar *resuelto*.** El botón permanece deshabilitado.
- **E2. Usuario sin rol admin.** El sistema rechaza con 403 y registra el intento (RF39, RF37).

---

### CU-10 — Registrar nuevo usuario (alta por la Asociación)

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Administrador / Asociación. |
| **Actores secundarios** | Gateway SMS (envío de verificación), usuario nuevo (recibe el código). |
| **Descripción** | El administrador da de alta a un nuevo productor o comprador tras verificar su identidad presencialmente. |
| **Precondiciones** | El administrador está autenticado. El solicitante ha presentado su documentación a la Asociación. |
| **Postcondición éxito** | Usuario creado en estado *activo* con PIN inicial 0000 y verificación SMS disparada. |
| **Postcondición fracaso** | Ningún usuario creado. Mensaje al administrador con el motivo. |
| **Requerimientos asociados** | RF26, RF37, RF39, RNF11. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El administrador accede a "Gestión de Usuarios" y presiona "Alta de Usuario".
2. El sistema presenta el formulario con: tipo (productor/comprador), DPI/CUI, nombre completo o razón social, teléfono, dirección.
3. El administrador completa los campos.
4. El administrador confirma.
5. El sistema valida DPI único y teléfono único.
6. El sistema crea el usuario con PIN 0000 y estado *activo*.
7. El sistema invoca al gateway SMS enviando un código de 6 dígitos de verificación del número.
8. El sistema agrega entrada en auditoría: "Alta de usuario {nombre} por {admin}".
9. El sistema muestra al administrador "Usuario creado. PIN inicial: 0000. El usuario deberá cambiarlo al primer ingreso".

**Flujos alternativos**

- **7a. Gateway SMS indisponible.** El sistema crea el usuario igualmente y permite reenviar el SMS después, marcando el teléfono como "no verificado" hasta el reintento exitoso.

**Excepciones**

- **E1. DPI o teléfono ya registrados.** Rechazo específico indicando cuál está duplicado.
- **E2. Teléfono con formato inválido.** Validación inline.
- **E3. Administrador sin permisos.** 403 y log de intento.

---

### CU-11 — Editar producto propio

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Productor dueño del producto. |
| **Descripción** | El productor actualiza los datos de un producto ya publicado (cantidad, precio referencial, descripción, etc.). |
| **Precondiciones** | El producto existe y pertenece al productor autenticado. |
| **Postcondición éxito** | Producto actualizado en catálogo. Cambio auditado. |
| **Postcondición fracaso** | Producto sin cambios. |
| **Requerimientos asociados** | RF08, RF37. |
| **Prioridad** | Alta. |

**Flujo principal**

1. El productor entra a "Mis Productos" y selecciona el producto.
2. El productor presiona "Editar".
3. El sistema carga el formulario con los datos actuales.
4. El productor modifica los campos deseados.
5. El productor confirma.
6. El sistema valida los campos.
7. El sistema persiste los cambios y agrega entrada en auditoría.
8. El sistema redirige a "Mis Productos" con mensaje de éxito.

**Flujos alternativos**

- **4a. Cantidad a cero.** El producto pasa automáticamente al estado *agotado* y desaparece del catálogo público hasta que se reponga.

**Excepciones**

- **E1. Producto ajeno.** 403.
- **E2. Valores inválidos.** Validación inline en el campo.

---

### CU-12 — Acceder al catálogo como invitado

| Campo | Detalle |
|-------|---------|
| **Actor principal** | Invitado (sin sesión). |
| **Descripción** | Una persona sin cuenta consulta el catálogo para explorar los productos de la comunidad antes de solicitar acceso. |
| **Precondiciones** | Ninguna. |
| **Postcondición éxito** | Se muestra catálogo y detalle de productos; no se realiza transacción alguna. |
| **Postcondición fracaso** | N/A (flujo de solo lectura). |
| **Requerimientos asociados** | RF02, RF11, RF12. |
| **Prioridad** | Media. |

**Flujo principal**

1. El invitado abre la URL pública del sistema.
2. El sistema muestra la pantalla de login con la opción "Ver catálogo sin cuenta".
3. El invitado presiona esa opción.
4. El sistema lo marca como rol *guest* (sin persistencia) y lo envía al catálogo.
5. El invitado navega el catálogo y el detalle de cada producto.
6. El invitado intenta ejecutar una acción transaccional (solicitar, mensajería).
7. El sistema muestra el mensaje "Inicia sesión o solicita una cuenta a la Asociación" y ofrece CTA para ir al login.

**Excepciones**

- **E1. Sin conexión.** Si es la primera visita no hay datos cacheados y el sistema muestra "Se requiere conexión para la primera carga".

---

### Trazabilidad Casos de Uso ↔ Requerimientos

| CU | Requerimientos principales | Prioridad |
|----|----------------------------|-----------|
| CU-01 | RF01, RF10 | Alta |
| CU-02 | RF11, RF12, RF13 | Alta |
| CU-03 | RF14, RF15 | Alta |
| CU-04 | RF17, RF36 | Alta |
| CU-05 | RF17, RF18 | Alta |
| CU-06 | RF02, RF11, RF40 | Alta |
| CU-07 | RF20, RF36 | Alta |
| CU-08 | RF31, RF38 | Alta |
| CU-09 | RF32, RF39 | Alta |
| CU-10 | RF26, RF39 | Alta |
| CU-11 | RF08, RF37 | Alta |
| CU-12 | RF02, RF11, RF12 | Media |

---

---

## 5. Diagramas de Actividad

Esta sección presenta los diagramas de actividad correspondientes a los casos de uso detallados en la Sección 4 y a transiciones de estado clave del sistema. Los diagramas se expresan en **notación Mermaid** (`flowchart` y `stateDiagram`), que permite renderizado inmediato en GitHub, Notion, VS Code y exportación a imagen.

Se cubren los 12 casos de uso detallados más un diagrama de estados transversal para el ciclo de vida del acuerdo comercial.

---

### 5.1 AD-01 — Iniciar sesión

> **Diagrama 1** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d01.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d01.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d01.mmd`.)*


---

### 5.2 AD-02 — Realizar solicitud de compra

> **Diagrama 2** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d02.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d02.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d02.mmd`.)*


---

### 5.3 AD-03 — Aceptar solicitud y registrar acuerdo

> **Diagrama 3** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d03.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d03.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d03.mmd`.)*


---

### 5.4 AD-04 — Actualizar seguimiento de la entrega

> **Diagrama 4** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d04.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d04.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d04.mmd`.)*


---

### 5.5 AD-05 — Marcar entrega y confirmar recepción

Diagrama con dos "carriles" (productor y comprador) que convergen en la confirmación final.

> **Diagrama 5** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d05.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d05.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d05.mmd`.)*


---

### 5.6 AD-06 — Consultar catálogo

> **Diagrama 6** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d06.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d06.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d06.mmd`.)*


---

### 5.7 AD-07 — Solicitar cancelación

> **Diagrama 7** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d07.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d07.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d07.mmd`.)*


---

### 5.8 AD-08 — Reportar inconformidad

> **Diagrama 8** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d08.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d08.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d08.mmd`.)*


---

### 5.9 AD-09 — Resolver incidencia (registrar decisión)

> **Diagrama 9** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d09.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d09.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d09.mmd`.)*


---

### 5.10 AD-10 — Registrar nuevo usuario

> **Diagrama 10** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d10.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d10.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d10.mmd`.)*


---

### 5.11 AD-11 — Editar producto propio

> **Diagrama 11** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d11.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d11.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d11.mmd`.)*


---

### 5.12 AD-12 — Acceder al catálogo como invitado

> **Diagrama 12** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d12.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d12.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d12.mmd`.)*


---

### 5.13 Diagrama de Estados — Ciclo de vida del Acuerdo Comercial

Complemento a los diagramas de actividad: este diagrama de estados sintetiza las transiciones válidas del acuerdo a lo largo de su ciclo de vida. Cada transición queda registrada en la bitácora (RF36) junto con el usuario y la fecha-hora.

> **Diagrama 13** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d13.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d13.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d13.mmd`.)*


---

---

## 6. Historias de Usuario

Esta sección formaliza, en el formato solicitado por la rúbrica ("Como … quiero … para …"), las necesidades funcionales del sistema desde la perspectiva de cada rol. Las historias **complementan** los casos de uso detallados en la Sección 4 y cubren los escenarios CRUD o de consulta simple que no recibieron flujo detallado, según la recomendación del docente.

Cada historia incluye **criterios de aceptación** verificables, **prioridad** alineada con la matriz de la Sección 2 y la trazabilidad a los requerimientos funcionales. Las prioridades siguen el criterio "procesos a automatizar": Alta para procesos núcleo, Media para soporte, Baja para accesorios.

---

### 6.1 Historias del Invitado

#### HU-01 — Consultar catálogo sin cuenta

- **Como** visitante sin cuenta registrada,
- **quiero** consultar los productos disponibles en la comunidad,
- **para** evaluar qué ofrecen antes de solicitar acceso formal.

**Criterios de aceptación**
1. Puedo entrar a la aplicación y presionar "Ver catálogo sin cuenta" sin registrarme.
2. Veo el listado de productos con nombre, categoría, productor, precio referencial y disponibilidad.
3. Puedo filtrar por nombre y categoría, y ordenar por disponibilidad, precio o unidad.
4. Al intentar solicitar un producto, el sistema me envía al inicio de sesión con un mensaje orientativo.

**Prioridad:** Media | **RF:** RF02, RF11

#### HU-02 — Ver detalle de un producto específico

- **Como** visitante,
- **quiero** abrir el detalle de un producto,
- **para** conocer descripción, productor y cantidad disponible.

**Criterios de aceptación**
1. Desde el catálogo puedo tocar/clic cualquier producto y ver su ficha completa.
2. La ficha muestra productor, precio referencial, descripción y disponibilidad.
3. No puedo enviar mensajes ni registrar solicitud desde esa vista.

**Prioridad:** Media | **RF:** RF12

---

### 6.2 Historias del Comprador

#### HU-03 — Iniciar sesión con teléfono y PIN

- **Como** comprador,
- **quiero** ingresar con mi número de teléfono y PIN de 4 dígitos,
- **para** acceder a mis compras y al catálogo con funciones de compra.

**Criterios de aceptación**
1. Si las credenciales son correctas, el sistema me lleva a mi panel.
2. Tras 5 intentos fallidos consecutivos, el sistema me bloquea por 10 minutos.
3. Si olvidé el PIN, puedo solicitar código SMS para restablecerlo.

**Prioridad:** Alta | **RF:** RF01, RF05, RF10

#### HU-04 — Registrar solicitud de compra

- **Como** comprador autenticado,
- **quiero** pedir un producto indicando cantidad y mensaje,
- **para** iniciar la negociación con el productor.

**Criterios de aceptación**
1. La cantidad solicitada no puede exceder la disponibilidad publicada.
2. Puedo incluir un mensaje para negociar precio u otros detalles.
3. Tras enviar, veo la solicitud en "Mis Compras" con estado *solicitado*.
4. Si el producto deja de estar disponible entre carga y envío, el sistema me avisa.

**Prioridad:** Alta | **RF:** RF13

#### HU-05 — Negociar dentro del acuerdo

- **Como** comprador,
- **quiero** intercambiar mensajes con el productor dentro del acuerdo,
- **para** pactar precio final, fecha y detalles sin salir del sistema.

**Criterios de aceptación**
1. Los mensajes quedan persistentes y en orden cronológico.
2. Ambas partes pueden leer el hilo mientras el acuerdo no esté cancelado.
3. Si el acuerdo se cancela, el chat queda en modo solo lectura.

**Prioridad:** Alta | **RF:** RF21

#### HU-06 — Consultar el seguimiento de mis compras

- **Como** comprador,
- **quiero** ver el estado actualizado de mis acuerdos en curso,
- **para** saber cuándo esperar la entrega.

**Criterios de aceptación**
1. El detalle muestra un stepper con el estado actual resaltado.
2. Veo la bitácora con comentarios del productor en cada transición.
3. Las pestañas me permiten filtrar entre pendientes, en proceso, completados y cancelados.

**Prioridad:** Alta | **RF:** RF22, RF36

#### HU-07 — Confirmar recepción

- **Como** comprador,
- **quiero** confirmar la entrega recibida,
- **para** cerrar el acuerdo como completado.

**Criterios de aceptación**
1. El botón "Confirmar Recepción" aparece solo cuando el productor marcó la entrega.
2. Al confirmar, el acuerdo pasa a *confirmado_comprador* y `estado_final = confirmada`.
3. Recibo un mensaje de éxito y la bitácora queda actualizada.

**Prioridad:** Alta | **RF:** RF18

#### HU-08 — Cancelar mi solicitud

- **Como** comprador,
- **quiero** cancelar una solicitud mía antes de que se confirme,
- **para** retirarme cuando mis planes cambien.

**Criterios de aceptación**
1. Puedo cancelar mientras el acuerdo esté en *solicitado* o *aceptado*.
2. El motivo es obligatorio (lista predefinida u "otro").
3. La cancelación libera la cantidad reservada para el productor.

**Prioridad:** Alta | **RF:** RF20

#### HU-09 — Reportar inconformidad

- **Como** comprador,
- **quiero** reportar una inconformidad con la cantidad o calidad de la entrega,
- **para** que la Asociación revise el caso.

**Criterios de aceptación**
1. Puedo elegir un tipo (cantidad, calidad, incumplimiento, otro).
2. La descripción es obligatoria.
3. Tras enviar, la incidencia queda en estado *abierto* y visible para el admin.

**Prioridad:** Alta | **RF:** RF31

#### HU-10 — Gestionar mi perfil

- **Como** comprador,
- **quiero** actualizar mi dirección y datos de contacto secundarios,
- **para** mantener mi información vigente.

**Criterios de aceptación**
1. Puedo editar dirección y contacto secundario.
2. No puedo cambiar teléfono principal ni DPI (son inmutables).
3. Los cambios quedan registrados en auditoría.

**Prioridad:** Media | **RF:** RF06

#### HU-11 — Cambiar mi PIN

- **Como** comprador,
- **quiero** cambiar mi PIN,
- **para** proteger mi cuenta cuando lo necesite.

**Criterios de aceptación**
1. Debo ingresar el PIN actual y el nuevo dos veces.
2. El PIN nuevo debe ser de 4 dígitos y diferente al actual.
3. El cambio queda auditado.

**Prioridad:** Alta | **RF:** RF04

---

### 6.3 Historias del Productor

#### HU-12 — Publicar mis cosechas

- **Como** productor,
- **quiero** publicar un producto con nombre, categoría, unidad, cantidad y precio referencial,
- **para** ofrecerlo al catálogo de la comunidad.

**Criterios de aceptación**
1. Las listas de categoría, unidad y (al aceptar acuerdo) punto de entrega provienen del catálogo maestro.
2. Al guardar con cantidad mayor a cero, el producto aparece como *disponible*.
3. El precio es referencial; el precio final se define por acuerdo.

**Prioridad:** Alta | **RF:** RF07

#### HU-13 — Editar un producto publicado

- **Como** productor,
- **quiero** modificar la cantidad disponible y el precio referencial,
- **para** reflejar cambios en mi cosecha sin tener que recrear el producto.

**Criterios de aceptación**
1. Desde "Mis Productos" puedo abrir cualquier producto mío y editarlo.
2. Si pongo cantidad cero, el producto pasa a *agotado* automáticamente.
3. No puedo editar productos de otro productor (403).

**Prioridad:** Alta | **RF:** RF08

#### HU-14 — Retirar un producto de la venta

- **Como** productor,
- **quiero** retirar un producto cuando se me agote o pierda la cosecha,
- **para** evitar generar expectativas falsas en los compradores.

**Criterios de aceptación**
1. Un producto retirado no aparece en el catálogo público.
2. Los acuerdos formalizados siguen su ciclo normal aunque el producto se retire.
3. Si hay solicitudes pendientes, el sistema me advierte antes de retirar.

**Prioridad:** Media | **RF:** RF09

#### HU-15 — Ver mis productos

- **Como** productor,
- **quiero** consultar el listado de productos que tengo publicados,
- **para** saber qué está activo, agotado o retirado.

**Criterios de aceptación**
1. Veo solamente mis productos, filtrables por estado.
2. Cada fila muestra atajos para editar o ver detalle.

**Prioridad:** Media | **RF:** RF10

#### HU-16 — Revisar solicitudes recibidas

- **Como** productor,
- **quiero** ver las solicitudes que me envían los compradores,
- **para** aceptarlas o rechazarlas oportunamente.

**Criterios de aceptación**
1. Las solicitudes nuevas aparecen primero.
2. Cada fila muestra producto, comprador, cantidad y fecha.
3. Puedo abrir el detalle desde la lista.

**Prioridad:** Alta | **RF:** RF14

#### HU-17 — Aceptar una solicitud formalizando el acuerdo

- **Como** productor,
- **quiero** aceptar una solicitud indicando precio final, fecha programada y punto de entrega,
- **para** dejar el acuerdo completamente formalizado en un solo paso.

**Criterios de aceptación**
1. Sin los tres datos (precio, fecha, punto) no puedo aceptar.
2. El punto de entrega se elige del catálogo maestro activo.
3. La fecha programada no puede ser en el pasado.
4. Al aceptar, la cantidad reservada se descuenta automáticamente del producto.

**Prioridad:** Alta | **RF:** RF15, RF25

#### HU-18 — Rechazar una solicitud con motivo

- **Como** productor,
- **quiero** rechazar una solicitud cuando no pueda cumplirla,
- **para** liberar al comprador y documentar el motivo.

**Criterios de aceptación**
1. Debo seleccionar un motivo de la lista o elegir "otro".
2. El rechazo queda en bitácora y el comprador recibe notificación.

**Prioridad:** Alta | **RF:** RF16

#### HU-19 — Actualizar el estado de la entrega

- **Como** productor,
- **quiero** avanzar el estado de un acuerdo (preparando, programado, en ruta, entregado) con un comentario de seguimiento,
- **para** mantener informado al comprador.

**Criterios de aceptación**
1. Solo puedo avanzar al estado contiguo del flujo.
2. Cada transición abre un modal para comentario opcional.
3. La bitácora registra comentario, usuario y fecha-hora.

**Prioridad:** Alta | **RF:** RF17, RF36

#### HU-20 — Marcar entrega realizada

- **Como** productor,
- **quiero** marcar la entrega como realizada cuando termino de trasladar el producto,
- **para** pedir al comprador que confirme la recepción.

**Criterios de aceptación**
1. Solo puedo hacerlo si el estado actual es *en_ruta*.
2. El sistema pasa al estado *entregado_productor* y notifica al comprador.

**Prioridad:** Alta | **RF:** RF18

#### HU-21 — Registrar estado de pago

- **Como** productor,
- **quiero** marcar un acuerdo como pago pendiente, contra entrega o realizado,
- **para** llevar control declarativo de mis cobros.

**Criterios de aceptación**
1. Puedo cambiar el estado de pago mientras el acuerdo no esté cancelado.
2. El cambio queda en bitácora.
3. El sistema no procesa pagos electrónicos; solo registra el estado.

**Prioridad:** Media | **RF:** RF19

#### HU-22 — Consultar mi historial de ventas

- **Como** productor,
- **quiero** ver mis ventas pasadas con ingresos por mes y tasa de cumplimiento,
- **para** planificar la próxima temporada.

**Criterios de aceptación**
1. Veo total vendido, entregas confirmadas e incumplidas en el periodo filtrado.
2. Una gráfica muestra ingresos mensuales.
3. Puedo abrir cualquier acuerdo histórico desde la lista.

**Prioridad:** Media | **RF:** RF35

#### HU-23 — Justificar un incumplimiento

- **Como** productor,
- **quiero** dejar constancia del motivo cuando no pude cumplir una entrega,
- **para** que el historial refleje el contexto.

**Criterios de aceptación**
1. La justificación se captura al cancelar con motivo "Incumplimiento de entrega".
2. El texto queda adjunto al acuerdo y visible en auditoría.

**Prioridad:** Media | **RF:** RF20, RF36

---

### 6.4 Historias del Administrador / Asociación

#### HU-24 — Dar de alta un nuevo usuario

- **Como** administrador,
- **quiero** registrar productores y compradores con sus datos y teléfono,
- **para** habilitar su acceso al sistema bajo control de la Asociación.

**Criterios de aceptación**
1. DPI y teléfono deben ser únicos.
2. El usuario nuevo queda *activo* con PIN inicial 0000.
3. El sistema intenta enviar un SMS de verificación del número.
4. La operación queda registrada en auditoría.

**Prioridad:** Alta | **RF:** RF26

#### HU-25 — Editar datos de un usuario

- **Como** administrador,
- **quiero** actualizar el nombre o dirección de un usuario,
- **para** corregir información.

**Criterios de aceptación**
1. No puedo modificar DPI, tipo ni teléfono principal.
2. Los cambios quedan auditados.

**Prioridad:** Media | **RF:** RF27

#### HU-26 — Reiniciar PIN de un usuario

- **Como** administrador,
- **quiero** restablecer el PIN de un usuario cuando lo olvide,
- **para** devolverle acceso rápidamente.

**Criterios de aceptación**
1. Al reiniciar, el PIN queda en 0000 y el usuario deberá cambiarlo al primer ingreso.
2. La acción queda en auditoría.

**Prioridad:** Alta | **RF:** RF28

#### HU-27 — Cambiar el estado de una cuenta

- **Como** administrador,
- **quiero** suspender, bloquear o reactivar usuarios,
- **para** sancionar o restaurar accesos según la decisión del comité.

**Criterios de aceptación**
1. Debo indicar un motivo al suspender o bloquear.
2. Un usuario *suspendido* puede ingresar pero no operar.
3. Un usuario *bloqueado* no puede ingresar.

**Prioridad:** Alta | **RF:** RF29

#### HU-28 — Gestionar categorías de producto

- **Como** administrador,
- **quiero** mantener el catálogo de categorías activo,
- **para** que los productores las usen al publicar.

**Criterios de aceptación**
1. Puedo crear, editar y desactivar categorías.
2. Una categoría inactiva no aparece en el formulario de publicación.
3. Los productos ya vinculados a una categoría desactivada siguen visibles.

**Prioridad:** Media | **RF:** RF23

#### HU-29 — Gestionar unidades de medida

- **Como** administrador,
- **quiero** mantener el catálogo de unidades con su abreviatura,
- **para** estandarizar la forma en que se cuantifican los productos.

**Criterios de aceptación**
1. Puedo crear, editar y desactivar unidades.
2. La abreviatura es única entre unidades activas.

**Prioridad:** Media | **RF:** RF24

#### HU-30 — Gestionar puntos de entrega

- **Como** administrador,
- **quiero** mantener la lista de puntos físicos donde se intercambian productos,
- **para** que los productores elijan uno oficial al aceptar un acuerdo.

**Criterios de aceptación**
1. Puedo crear, editar y desactivar puntos de entrega.
2. Los acuerdos existentes conservan el punto pactado aunque luego se desactive.

**Prioridad:** Media | **RF:** RF25

#### HU-31 — Supervisar acuerdos y entregas

- **Como** administrador,
- **quiero** ver todos los acuerdos de la comunidad con filtros por estado,
- **para** detectar atrasos o problemas temprano.

**Criterios de aceptación**
1. Veo los acuerdos de todos los productores y compradores.
2. Puedo filtrar por pendientes, en proceso, completados y cancelados.
3. Desde el listado accedo al detalle.

**Prioridad:** Media | **RF:** RF22 (vista admin)

#### HU-32 — Registrar la resolución de una incidencia

- **Como** administrador,
- **quiero** registrar la decisión adoptada por el comité sobre una incidencia reportada,
- **para** que quede constancia formal en el sistema.

**Criterios de aceptación**
1. Puedo cambiar el estado a *en_revision*, *resuelto* o *descartado*.
2. Si marco *resuelto*, la resolución textual es obligatoria.
3. La acción queda en auditoría y se notifica a las partes.

**Prioridad:** Alta | **RF:** RF32

#### HU-33 — Forzar cancelación de un acuerdo

- **Como** administrador,
- **quiero** cancelar forzosamente un acuerdo por decisión del comité,
- **para** cerrar casos que no pueden continuar entre las partes.

**Criterios de aceptación**
1. Solo aplica a acuerdos no confirmados.
2. El motivo es obligatorio.
3. La acción queda auditada con mi identificador.

**Prioridad:** Media | **RF:** RF33

#### HU-34 — Consultar reportes agregados

- **Como** administrador,
- **quiero** ver KPIs y gráficas de la comunidad (productores activos, entregas completadas, incidencias, ventas por categoría),
- **para** tomar decisiones de planificación comunitaria.

**Criterios de aceptación**
1. Los datos son agregados y anonimizados.
2. Puedo filtrar por rango de fechas.
3. Puedo exportar el reporte en CSV o PDF (futura iteración).

**Prioridad:** Media | **RF:** RF34

#### HU-35 — Consultar la bitácora de auditoría

- **Como** administrador,
- **quiero** revisar las acciones sensibles registradas en el sistema,
- **para** auditar cambios y garantizar transparencia.

**Criterios de aceptación**
1. Veo la lista de eventos con usuario, acción, entidad y fecha-hora.
2. Puedo filtrar por usuario, tipo de acción o rango de fechas.
3. No puedo editar ni eliminar los registros.

**Prioridad:** Alta | **RF:** RF37

---

### 6.5 Historias transversales (aplican a más de un rol)

#### HU-36 — Operar offline y sincronizar

- **Como** usuario en zona con señal intermitente,
- **quiero** consultar el catálogo cacheado y encolar mis acciones cuando no tengo internet,
- **para** no perder el trabajo realizado.

**Criterios de aceptación**
1. El sistema indica claramente cuando estoy en modo offline.
2. Las acciones encoladas se sincronizan al reconectar.
3. Si hay conflicto (ej. producto ya retirado), el sistema me notifica y descarta la acción.

**Prioridad:** Media | **RF:** RF40

#### HU-37 — Recibir notificaciones del sistema

- **Como** usuario,
- **quiero** recibir notificaciones de eventos relevantes (solicitud recibida, cambio de estado, incidencia),
- **para** estar al día sin abrir la app constantemente.

**Criterios de aceptación**
1. Las notificaciones in-app aparecen al iniciar sesión.
2. Los eventos críticos (aceptación, cancelación, entrega) también se envían por SMS.
3. Puedo revisar el historial de notificaciones desde la app.

**Prioridad:** Media | **RF:** RF38

#### HU-38 — Cerrar sesión seguramente

- **Como** usuario,
- **quiero** cerrar mi sesión desde cualquier pantalla,
- **para** proteger mi cuenta cuando uso un dispositivo compartido.

**Criterios de aceptación**
1. El botón "Salir" está visible en el menú.
2. Al salir, el token se invalida y los datos locales sensibles se borran.

**Prioridad:** Alta | **RF:** RF03

---

### Resumen por rol

| Rol | Historias | Rango |
|-----|----------:|-------|
| Invitado | 2 | HU-01, HU-02 |
| Comprador | 9 | HU-03 a HU-11 |
| Productor | 12 | HU-12 a HU-23 |
| Administrador | 12 | HU-24 a HU-35 |
| Transversal | 3 | HU-36 a HU-38 |
| **Total** | **38** | — |

**Distribución por prioridad**

- **Alta:** 22 historias (procesos núcleo de comercialización, autenticación, incidencias y auditoría).
- **Media:** 16 historias (catálogos maestros, reportes, historial, perfil, offline, notificaciones).
- **Baja:** 0.

---

---

## 7. Prototipos

### 7.1 Prototipo interactivo publicado

El prototipo del sistema "La Esperanza" está desplegado como aplicación web estática con navegación funcional entre pantallas, de acuerdo con la recomendación del docente de entregar un prototipo que permita **interactuar con la navegación** aunque no ejecute los procesos de negocio reales contra una base de datos.

- **URL pública:** https://alexalvarado1290.github.io/la-esperanza/dashboard
- **Repositorio del código fuente:** se mantiene en la carpeta `Proyecto 1/Proyecto La Esperanza/LA ESPERANZA/` del proyecto (aplicación React + Vite). La rama que se publica a GitHub Pages contiene el bundle generado con `npm run build`.
- **Estado:** interactivo a nivel de navegación, formularios y transiciones de estado en el cliente (el estado vive en memoria del navegador y localStorage; no hay persistencia de servidor en esta fase).

### 7.2 Credenciales de prueba

Para explorar las distintas vistas se incluyen usuarios de prueba en la pantalla de login. El selector rápido en esa pantalla precarga las credenciales:

| Rol | Teléfono | PIN |
|-----|----------|----:|
| Administrador / Asociación | 0999999991 | 1111 |
| Productor | 0999999992 | 2222 |
| Comprador | 0999999993 | 3333 |
| Invitado | *(botón "Ver catálogo sin cuenta")* | — |

El rol activo se almacena en `localStorage.userRole` y determina las secciones visibles, los botones de acción disponibles y la lógica condicional del prototipo. Cerrar sesión limpia el almacenamiento y devuelve al login.

### 7.3 Estructura de navegación por rol

El prototipo implementa el menú lateral (escritorio) y la barra inferior (móvil) diferenciados por rol. Las rutas se definen en [routes.tsx](../../Proyecto%20La%20Esperanza/LA%20ESPERANZA/src/app/routes.tsx) y los ítems del menú en [Layout.tsx](../../Proyecto%20La%20Esperanza/LA%20ESPERANZA/src/app/components/Layout.tsx).

#### Administrador / Asociación

| Sección | Ruta | Historias / CU relacionados |
|---------|------|------------------------------|
| Panel de la Asociación | `/dashboard` | HU-34 |
| Usuarios | `/users` | HU-24, HU-25, HU-26, HU-27 |
| Alta de Usuario | `/users/new` | CU-10, HU-24 |
| Productos (supervisión) | `/products` | UC29 |
| Detalle de producto | `/products/:id` | — |
| Acuerdos (supervisión global) | `/agreements` | HU-31 |
| Detalle de acuerdo + incidencia | `/agreements/:id` | CU-09, HU-32, HU-33 |
| Categorías | `/categories` | HU-28 |
| Unidades de medida | `/units` | HU-29 |
| Puntos de entrega | `/delivery-points` | HU-30 |
| Reportes y estadísticas | `/reports` | HU-34 |
| Mi perfil | `/profile` | HU-10 |

#### Productor

| Sección | Ruta | Historias / CU relacionados |
|---------|------|------------------------------|
| Mi panel | `/dashboard` | — |
| Mis productos | `/products` | HU-15 |
| Registrar producto | `/products/new` | HU-12 |
| Editar producto | `/products/:id/edit` | CU-11, HU-13 |
| Mis acuerdos | `/agreements` | HU-16 |
| Detalle + flujo de seguimiento | `/agreements/:id` | CU-03, CU-04, CU-05, HU-17, HU-18, HU-19, HU-20 |
| Historial de ventas | `/sales-history` | HU-22 |
| Mi perfil | `/profile` | HU-11 |

#### Comprador

| Sección | Ruta | Historias / CU relacionados |
|---------|------|------------------------------|
| Mi panel | `/dashboard` | — |
| Catálogo | `/products` | CU-06, HU-03 |
| Detalle de producto + solicitud | `/products/:id` | CU-02, HU-04 |
| Mis compras | `/agreements` | HU-06 |
| Detalle + chat + confirmación | `/agreements/:id` | CU-05, CU-07, CU-08, HU-05, HU-07, HU-08, HU-09 |
| Mi perfil | `/profile` | HU-10, HU-11 |

#### Invitado

| Sección | Ruta | Historias / CU relacionados |
|---------|------|------------------------------|
| Landing sin sesión | `/dashboard` | CU-12 |
| Catálogo | `/products` | HU-01 |
| Detalle de producto | `/products/:id` | HU-02 |
| Login | `/login` | — |

### 7.4 Interacciones implementadas

El prototipo no es un mockup estático: las siguientes interacciones funcionan en el cliente y permiten experimentar los flujos completos de los casos de uso detallados en la Sección 4.

**Flujos completos navegables**

1. **Login con selector de roles** y acceso invitado, con cambio de vista según el rol seleccionado.
2. **Catálogo** con búsqueda por nombre/categoría, filtros y ordenamiento.
3. **Detalle de producto** con formulario de solicitud de compra (solo comprador) y pantalla de éxito.
4. **Aceptación de solicitud** con modal que captura precio final, fecha programada, punto de entrega y observaciones.
5. **Stepper de seguimiento** con transiciones progresivas y comentario obligatorio por paso, persistido en una bitácora visible.
6. **Cancelación** con motivo de lista predefinida y observación libre.
7. **Reporte de incidencia** con tipo (cuatro opciones), descripción y, para el admin, estado del reporte y resolución.
8. **Chat** dentro del acuerdo con envío y recepción simulados.
9. **Gestión de catálogos maestros** (categorías, unidades, puntos de entrega) con alta, edición y activación/desactivación.
10. **Historial de ventas del productor** con KPI cards y gráfica de ingresos mensuales.
11. **Reportes del administrador** con gráficas de barras y torta (recharts).
12. **Cierre de sesión** con limpieza del almacenamiento local y redirección al login.

**Diseño responsive**

El layout adapta el menú entre barra lateral (escritorio) y barra inferior + menú desplegable (móvil) usando breakpoints de Tailwind (`md:` = 768 px). Todos los componentes usan tipografía mínima de 16 px, controles de 48 px y contraste AA, cumpliendo los requerimientos RNF19 a RNF24.

### 7.5 Limitaciones actuales del prototipo

Estas funcionalidades quedan documentadas como requerimientos en las Secciones 2 y 3 y se implementarán en la fase de desarrollo; el prototipo no las ejecuta todavía:

- Autenticación real con backend y tokens firmados (RF01, RNF08).
- Persistencia entre sesiones (los datos se pierden al recargar fuera de los mocks).
- Hashing real de PIN y llamadas al gateway SMS (RNF07, RF05).
- Notificaciones SMS reales (RF38).
- Sincronización offline con cola de acciones (RF40).
- Bitácora de auditoría centralizada a nivel del sistema (RF37).
- Generación asíncrona de reportes pesados (RNF17).

### 7.6 Capturas referenciales de pantalla

Las capturas de pantalla sugeridas para adjuntar en la versión impresa del DERCAS se organizan por rol y se extraen del prototipo en ejecución:

1. **Login** con el selector de roles de prueba.
2. **Catálogo** en vista de comprador y vista de invitado.
3. **Detalle de producto** con formulario de solicitud.
4. **Panel de la Asociación** con KPIs.
5. **Detalle de acuerdo** mostrando el stepper y la bitácora con comentarios.
6. **Modal de aceptación de solicitud** con precio final, fecha, punto de entrega.
7. **Modal de incidencia** con tipo y estado de reporte.
8. **Catálogo de puntos de entrega** con alta y edición.
9. **Historial de ventas** del productor con gráfica.
10. **Reportes** del administrador con barras y torta.

---

---

## 8. Diagrama de Componentes

Conforme a la recomendación del docente, esta sección contiene **dos diagramas complementarios**: el primero describe la **arquitectura de infraestructura** (cómo se despliega el sistema en la nube y cómo interactúan los nodos físicos o lógicos), y el segundo presenta los **componentes de software** (cómo se organiza internamente la aplicación en capas y módulos).

Ambos diagramas usan notación Mermaid para mantener coherencia con las secciones anteriores y ser renderizables directamente en el repositorio.

---

### 8.1 Diagrama general de infraestructura

El sistema se despliega siguiendo un modelo **cliente-servidor en la nube**, con soporte PWA (*Progressive Web App*) para reducir la dependencia de la conectividad continua. La infraestructura se dimensiona para el despliegue inicial (≤ 50 usuarios concurrentes) y admite escalar horizontalmente replicando la capa de aplicación.

> **Diagrama 14** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d14.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d14.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d14.mmd`.)*


**Observaciones de despliegue**

- El **bundle estático** (HTML + JS + CSS) se sirve desde un CDN o GitHub Pages (como el prototipo actual). Esto minimiza el costo recurrente y mejora los tiempos de carga desde zonas rurales.
- La **API REST** se publica en un proveedor de nube (p. ej. Render, Fly.io, AWS ECS o similar). Se elige una opción con escalado automático y costos predecibles para que la Asociación pueda presupuestar el mantenimiento con transparencia (RNF31).
- La **base de datos** se gestiona como servicio (PostgreSQL gestionado), lo que elimina la administración manual de respaldos y *patching*.
- El **gateway SMS** es un servicio de terceros; su cuenta se factura a la Asociación. Se elige uno con cobertura nacional y precios en el rango de USD 0.05–0.10 por mensaje.
- Los **clientes** son navegadores ejecutando la PWA. En dispositivos compatibles, el usuario puede "instalar" la app desde el navegador para obtener ícono en el home-screen y experiencia similar a nativa (RNF34).

---

### 8.2 Diagrama de componentes de software

El diagrama de componentes muestra la organización interna de la aplicación en capas y módulos, haciendo explícitos los puntos donde aplicar **patrones de diseño** en la fase final del proyecto (RNF27).

> **Diagrama 15** — disponible en el repositorio:
> [https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d15.png](https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams/d15.png)
>
> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d15.mmd`.)*


---

### 8.3 Descripción de los componentes principales

#### Cliente (PWA)

| Componente | Responsabilidad | Tecnología sugerida |
|------------|-----------------|---------------------|
| **Capa de Presentación** | Renderizado de todas las pantallas, formularios y modales. Separación por páginas y componentes reusables. | React 18 + Tailwind CSS |
| **Router** | Enrutado declarativo, protección de rutas por rol, redirecciones. | React Router 7 |
| **Gestión de Estado** | Estado global por rol, sesión y datos del usuario. Se evita Redux en favor de Context + hooks para mantener el bundle liviano. | React Context + hooks |
| **Cliente HTTP** | Cliente único que adapta `fetch` a un contrato estable; maneja tokens y errores comunes. Patrón Adapter. | `fetch` nativo con wrapper |
| **Service Worker** | Caching estratégico de recursos estáticos y catálogo para soporte offline. | Workbox / Vite PWA plugin |
| **Módulo de Sincronización** | Cola local de acciones pendientes, política de reintentos al reconectar. | Código propio sobre IndexedDB |
| **Almacén local** | Catálogo cacheado y cola de sincronización. | IndexedDB vía `idb` |

#### Servidor (API)

| Componente | Responsabilidad |
|------------|-----------------|
| **Controladores** | Endpoints REST por recurso, traducen HTTP a llamadas a casos de uso. |
| **Middleware transversal** | Autenticación por token, control de acceso por rol (RBAC), rate limiting, CORS, cabeceras de seguridad. |
| **Casos de uso / Servicios de aplicación** | Orquestación de la lógica de negocio; coordinan validadores, repositorios, state machine y servicios auxiliares. |
| **State Machine del Acuerdo** | Encapsula las transiciones válidas del ciclo de vida del acuerdo (ver Sección 5.13). Aplica el **patrón State** para aislar las reglas por estado. |
| **Servicio de Auditoría** | Registra automáticamente los cambios sensibles vía **patrón Observer** sobre los casos de uso relevantes. |
| **Servicio de Notificaciones** | Envía notificaciones in-app y opcionalmente SMS. Usa **patrón Strategy** para seleccionar el canal según el evento y el usuario. |
| **Validadores de dominio** | Reglas de negocio puras (cantidad dentro de rango, fecha futura, etc.), reutilizables. |

#### Persistencia

| Componente | Responsabilidad |
|------------|-----------------|
| **Repositorios** | Abstraen el acceso a datos por agregado (Usuario, Producto, Acuerdo, Incidencia). Implementan el **patrón Repository**, lo que permite probar los casos de uso con dobles en memoria. |
| **ORM** | Mapeo objeto-relacional y migraciones. Se propone Prisma (TypeScript-first) para alinear con el resto del stack; TypeORM es alternativa viable. |
| **Base de datos** | PostgreSQL gestionado con respaldos cifrados diarios. |

#### Integraciones externas

| Componente | Responsabilidad |
|------------|-----------------|
| **Adaptador SMS** | Contrato interno para envío de SMS; oculta al resto del sistema qué gateway concreto se usa. **Patrón Adapter**, permitiendo cambiar de Twilio a otro proveedor sin modificar los casos de uso. |

---

### 8.4 Patrones de diseño previstos

De acuerdo con el requerimiento **RNF27** y la indicación del docente ("en la última fase deben aplicar patrones de diseño al código fuente"), el diseño reserva ubicaciones explícitas para los siguientes patrones:

| Categoría | Patrón | Ubicación prevista | Motivación |
|-----------|--------|--------------------|------------|
| Creacional | **Factory Method** | Creación de instancias de repositorio según entorno (producción, tests, offline). | Aislar la fabricación de implementaciones y simplificar las pruebas. |
| Estructural | **Adapter** | Cliente HTTP del frontend; adaptador SMS del backend. | Uniformar APIs externas sobre contratos estables. |
| Estructural | **Repository** | Capa de persistencia. | Desacoplar casos de uso del ORM; habilitar pruebas sin base real. |
| Comportamiento | **State** | Máquina de estados del acuerdo comercial. | Encapsular las reglas de transición por estado y evitar if-else anidados. |
| Comportamiento | **Strategy** | Servicio de notificaciones (canal in-app vs SMS) y servicio de ordenamiento del catálogo. | Permitir cambiar el algoritmo en tiempo de ejecución según contexto. |
| Comportamiento | **Observer** | Servicio de auditoría reaccionando a eventos de dominio. | Desacoplar el logging de auditoría de la lógica de negocio. |

La fase 3 (desarrollo) documentará en el código los archivos concretos donde cada patrón se materializa y una breve justificación por patrón, acompañando el entregable.

---

### 8.5 Consideraciones de despliegue y costos

Aunque el detalle financiero se documenta en el manual operativo anexo al entregable final, se listan los costos recurrentes estimados (USD) que la Asociación debe prever:

| Concepto | Proveedor ejemplo | Costo aproximado mensual |
|----------|-------------------|-------------------------:|
| Hosting PWA estática | GitHub Pages / Cloudflare Pages | USD 0 (plan gratuito) |
| Backend API (escalado básico) | Render / Fly.io (1 instancia pequeña) | USD 7 – 15 |
| Base de datos gestionada | PostgreSQL gestionado en la misma nube | USD 7 – 20 |
| Gateway SMS (100 SMS/mes) | Twilio | USD 5 – 10 |
| Dominio y SSL | Proveedor de dominios | USD 1 – 2 |
| Monitoreo y logs | Logtail / Datadog free tier | USD 0 – 10 |
| **Total mensual estimado** | | **USD 20 – 57** |

Se estima adicionalmente **USD 100 – 250 por evento** para el mantenimiento correctivo o evolutivo puntual contratado a un proveedor externo, conforme al supuesto de mantenimiento autónomo con soporte contratado por demanda.

---

---

## Anexo A — Cuestionarios y Análisis

### A.1 Metodología de recolección

Para validar los supuestos del sistema y recolectar información complementaria al análisis documental del Proyecto I, se diseñó un **cuestionario estructurado en línea** utilizando Google Forms. El instrumento se pensó para ser aplicado a los tres perfiles de usuarios presentes en el ecosistema comercial de la comunidad "La Esperanza": **productores agrícolas**, **compradores frecuentes** y **representantes de la Asociación**.

La segmentación por rol se implementa dentro del mismo formulario mediante una pregunta inicial que ramifica el recorrido del respondiente hacia la batería de preguntas específica para cada perfil, lo que permite mantener **un solo instrumento** en lugar de tres formularios separados.

El enfoque del instrumento sigue tres ejes definidos en la Sección 1 de este documento:

1. **Diagnóstico de prácticas actuales** (cómo se comercializa hoy).
2. **Identificación de dolores y fallas recurrentes**.
3. **Expectativas y disposición tecnológica** frente a una solución digital.

### A.2 Instrumento aplicado

- **Título del formulario:** *Encuesta de requerimientos del cliente*
- **Institución de origen:** Universidad Mariano Gálvez de Guatemala
- **URL pública:** https://docs.google.com/forms/d/e/1FAIpQLSf0pabsdelzJ2GmJr-UQg-4mUbgpflkiSnEQPKoZKZFXkfbfw/viewform
- **Modalidad:** Autoaplicado en línea, con acceso libre mediante cuenta de Google.
- **Tiempo estimado de llenado:** 8 a 12 minutos según el rol.

#### A.2.1 Estructura común del formulario

| Orden | Pregunta | Tipo | Obligatoria |
|------:|----------|------|:-----------:|
| 1 | Nombre | Respuesta corta | Sí |
| 2 | ¿Qué rol cumples? (Productor agrícola / Comprador frecuente / Representante de la Asociación) | Opción múltiple (desplegable) | No |
| 3+ | *Bloque específico por rol* | Ver A.2.2 – A.2.4 | Variable |

La pregunta 2 **ramifica** el formulario hacia el bloque de preguntas específico del rol declarado. El anexo detalla a continuación las preguntas esperadas en cada bloque; la versión publicada del formulario cubre esos ejes en distinto grado de profundidad.

#### A.2.2 Bloque para el Productor Agrícola

| Ámbito | Preguntas guía |
|--------|----------------|
| Perfil | Edad, nivel de estudios, uso de teléfono inteligente o básico, apps utilizadas con frecuencia. |
| Conectividad | Tipo de acceso a internet, estabilidad de la señal. |
| Prácticas actuales | Productos que cultiva, temporadas, canales de venta (intermediarios, mercado, comercios), cómo pacta precios y cantidades. |
| Registros | Formato usado hoy (cuaderno, memoria, ninguno), existencia de archivos propios. |
| Problemas | Cantidades entregadas distintas a lo pactado, retrasos de pago, pérdida de cosecha por sobreproducción. |
| Expectativas | Qué funcionalidad priorizaría en una app (publicar, cobrar, coordinar), canal preferido de notificación. |
| Disposición | Voluntad de capacitarse y usar el sistema. |

#### A.2.3 Bloque para el Comprador Frecuente

| Ámbito | Preguntas guía |
|--------|----------------|
| Perfil | Tipo de comprador (restaurante, comercio, distribuidor, consumidor final), frecuencia de compra. |
| Prácticas actuales | Canal de contacto con productores, forma de acordar pedidos, condiciones de pago, transporte. |
| Problemas | Inconformidades con cantidad o calidad, pedidos no entregados en fecha, dificultad para comparar precios. |
| Expectativas | Información deseada antes de comprar (disponibilidad, precio, historial del productor), confianza en historial/reputación digital. |
| Disposición | Preferencia entre app web en celular vs. contacto telefónico tradicional. |

#### A.2.4 Bloque para el Representante de la Asociación

| Ámbito | Preguntas guía |
|--------|----------------|
| Gobernanza | Cantidad aproximada de productores y compradores vinculados, existencia de registros escritos, quién supervisa transacciones. |
| Conflictos e incidencias | Quejas recibidas, criterios de sanción, tipos de conflicto más frecuentes. |
| Datos históricos | Información conservada de temporadas anteriores, reportes compartidos con la comunidad. |
| Infraestructura | Equipo de cómputo disponible, conectividad en la sede, persona responsable del sistema. |
| Requerimientos | Reportes deseados, decisiones que requieren intervención del comité, necesidad de operar sin conexión. |
| Presupuesto | Disponibilidad para capacitación y mantenimiento recurrente. |

### A.3 Respuestas recibidas y análisis

#### A.3.1 Alcance muestral

Al cierre de la elaboración de este documento se recibió **una (1) respuesta completa** al cuestionario, correspondiente al perfil que sirve como referencia del cliente para esta fase del proyecto. Por su naturaleza académica y alcance piloto, el resultado no pretende ser estadísticamente representativo, sino **cualitativamente orientador** para validar los supuestos del Proyecto I y aportar insumos al diseño de requerimientos de la fase II.

#### A.3.2 Hallazgos principales

| # | Hallazgo | Fuente (ítem del cuestionario) | Impacto en el DERCAS |
|---|----------|--------------------------------|----------------------|
| H1 | La comercialización actual se realiza por canales informales (llamada, WhatsApp y presencial) sin registro digital unificado. | Respuesta al bloque "Prácticas actuales". | Valida la visión general (§1.1) y la priorización Alta de RF13, RF15, RF17. |
| H2 | Los productores reportan baja alfabetización digital y usan teléfonos de gama baja con conectividad intermitente. | Bloque "Perfil / Conectividad". | Refuerza los RNF19–RNF25 de usabilidad y el RF40 de operación offline. |
| H3 | La Asociación funciona como ente organizador pero no cuenta con herramientas tecnológicas propias ni personal técnico dedicado. | Bloque "Gobernanza / Infraestructura". | Justifica el supuesto de mantenimiento autónomo con soporte externo (§1.3, RNF31). |
| H4 | Los conflictos (cantidades, precios, retrasos) se resuelven hoy de manera verbal sin mecanismos formales de seguimiento. | Bloque "Problemas / Conflictos". | Sustenta RF31 y RF32, incluyendo la decisión de que la **mediación queda fuera del software** (Sección 1.3.1). |
| H5 | Existen puntos físicos reconocidos para entregas que la comunidad usa habitualmente. | Bloque "Prácticas actuales / Requerimientos". | Confirma la introducción del catálogo `PUNTO_ENTREGA` (UC34, RF25). |
| H6 | Hay interés en conservar información histórica de temporadas para planificar mejor. | Bloque "Expectativas / Requerimientos". | Soporta RF34 (reportes agregados) y RF35 (historial del productor). |

#### A.3.3 Validación de supuestos

Los supuestos formulados en la Sección 1.3 se mantienen tras el análisis, con las siguientes precisiones:

- **Supuesto "conectividad intermitente":** confirmado. El sistema debe ser operable con sincronización diferida (RF40).
- **Supuesto "baja alfabetización digital en productores":** confirmado. Se refuerzan los RNF de usabilidad (tipografía ≥ 16 px, flujos ≤ 3 pasos, iconografía clara).
- **Supuesto "asociación como autoridad"**: confirmado. La Asociación es el único ente habilitado para dar de alta usuarios y gestionar catálogos maestros (RF26, RF23–RF25).
- **Supuesto "conflictos se resuelven fuera del sistema"**: confirmado y reforzado por la respuesta del docente en el foro. Ajuste reflejado en RF32.

#### A.3.4 Nuevos requerimientos o ajustes detectados

La información recolectada no introduce requerimientos nuevos respecto a los ya definidos en la Sección 2, pero sí **refuerza la prioridad** de los siguientes:

- **RF40 (operación offline)** → confirmado como **prioridad operativa** dada la conectividad intermitente reportada.
- **RF38 (notificaciones)** → se confirma que el canal más accesible para los productores es WhatsApp/SMS; se mantiene SMS como canal obligatorio para eventos críticos y se considera un canal futuro para WhatsApp Business API.
- **RNF31 (costos de mantenimiento documentados)** → indispensable dado que la Asociación no cuenta con personal técnico.

#### A.3.5 Riesgos identificados

| Riesgo | Origen de la evidencia | Mitigación |
|--------|------------------------|------------|
| Baja adopción inicial por barrera digital | Respuestas sobre alfabetización y dispositivos usados. | Capacitación inicial de 30 min por usuario (RNF25); piloto con usuarios tempranos. |
| Pérdida de datos por dispositivos compartidos | Productores reportan compartir dispositivo familiar. | PIN obligatorio, cierre de sesión rápido (HU-38), sin datos sensibles en caché. |
| Falla de conectividad afectando operación | Conectividad intermitente en la zona. | Modo offline con sincronización (RF40); cacheo del catálogo. |
| Sostenibilidad del mantenimiento | Asociación sin personal técnico ni presupuesto fijo para IT. | Costos documentados (§8.5); contrato por demanda con proveedor externo. |

### A.4 Limitaciones del análisis y recomendaciones

Se reconocen las siguientes limitaciones que el lector del DERCAS debe tener presente:

- **Muestra reducida (n = 1).** Una única respuesta no es representativa. El análisis combina ese dato con el enunciado del proyecto, la entrevista implícita del cliente documentada en el foro del curso, y la observación indirecta de prácticas rurales en Guatemala.
- **Autoselección del respondiente.** El respondiente conocía el proyecto y su llenado puede orientar las respuestas hacia la solución propuesta, introduciendo un sesgo de confirmación.
- **Ausencia de observación in situ.** Por alcance académico no se realizó visita a la comunidad; las preguntas sobre infraestructura y logística se basan en declaración del respondiente.

**Recomendaciones para la fase de desarrollo (Proyecto III):**

1. Aplicar el cuestionario a al menos **5 productores, 3 compradores y 2 representantes de la Asociación** antes de iniciar desarrollo productivo.
2. Realizar una **entrevista semiestructurada** de 30 minutos con el presidente o secretario de la Asociación para validar con mayor profundidad la gobernanza, presupuesto y estacionalidad.
3. Ejecutar **pruebas de usabilidad** del prototipo con 2-3 productores reales antes de congelar decisiones de diseño (RNF25).
4. Añadir un **segundo ciclo de encuesta post-piloto** para medir adopción, carga de aprendizaje y puntos de fricción.

### A.5 Material fuente

- [Formulario en Google Forms](https://docs.google.com/forms/d/e/1FAIpQLSf0pabsdelzJ2GmJr-UQg-4mUbgpflkiSnEQPKoZKZFXkfbfw/viewform)
- Respuestas recibidas: conservadas en la hoja de cálculo vinculada al formulario en Google Drive (acceso restringido al equipo de proyecto).
- Enunciado del Proyecto I: documento impartido en clase.
- Foro de consultas del curso: respuestas del docente empleadas para refinar los supuestos y la categoría *Legalidad*.

---

---

## Anexo B — Stack Tecnológico

Conforme al requerimiento del Proyecto II de **dejar estipuladas las tecnologías para las siguientes entregas**, este anexo consolida y justifica el stack propuesto para la construcción del sistema. Las decisiones se toman atendiendo tres criterios: **consistencia** con el prototipo ya entregado (React + TypeScript), **disponibilidad de patrones de diseño** requeridos en la fase final (RNF27) y **economía operativa** para una organización sin personal técnico propio (RNF31).

El stack se organiza en cuatro capas (cliente, servidor, datos e infraestructura) más servicios transversales de DevOps y terceros.

---

### B.1 Cliente (Frontend PWA)

| Componente | Tecnología elegida | Versión | Justificación |
|------------|---------------------|---------|---------------|
| Lenguaje | **TypeScript** | 5.x | Tipado estático reduce errores en tiempo de desarrollo. Coherente con la elección del backend. |
| Framework UI | **React** | 18.x | Ecosistema maduro, curva de aprendizaje razonable, amplia oferta de componentes. Usado ya en el prototipo. |
| Bundler | **Vite** | 6.x | Compilación rápida durante desarrollo, HMR eficiente, empaquetado optimizado para producción. Ya integrado en el prototipo. |
| Estilos | **Tailwind CSS** | 4.x | Utilidades atómicas facilitan mantener consistencia visual (RNF20). Ligero en producción (purga automática). |
| Ruteo | **React Router** | 7.x | Estándar de facto. Permite rutas anidadas y redirecciones simples por rol. |
| Componentes accesibles | **Radix UI** + **Lucide Icons** | Latest | Primitivos sin estilo con accesibilidad ARIA integrada; iconografía consistente y ligera. |
| Gráficas | **Recharts** | 2.x | API declarativa sobre SVG, suficiente para las gráficas requeridas (barras y torta del panel de reportes). |
| PWA (cache + offline) | **Vite PWA Plugin** con **Workbox** | Latest | Genera el manifest y service worker con estrategias de caching listas (NetworkFirst para API, CacheFirst para estáticos). Cumple RNF34. |
| Almacenamiento local | **idb** (wrapper sobre IndexedDB) | 7.x | API con Promises para el almacén local de catálogo y cola offline (RF40). Preferido sobre IndexedDB nativo por su API limpia. |
| Cliente HTTP | **fetch** nativo con wrapper propio | — | Evita dependencia adicional; wrapper centraliza token, manejo de errores y retries (patrón Adapter, Sección 8.4). |
| Validación de formularios | **react-hook-form** + **zod** | Latest | Validación tipada con esquemas. Reutilización de tipos entre front y back si se decide compartir DTOs. |
| Pruebas | **Vitest** + **Testing Library** | Latest | Vitest comparte configuración con Vite, tiempos de ejecución cortos. |

**Alternativas evaluadas y descartadas**

- **Next.js** → demasiado para este alcance; el SSR no es necesario y complica el despliegue en GitHub Pages.
- **Angular** → curva más alta para un equipo estudiantil; React ya está en el prototipo.
- **Bootstrap / Material UI** → menor control tipográfico y más peso que Tailwind.

---

### B.2 Servidor (Backend API)

| Componente | Tecnología elegida | Versión | Justificación |
|------------|---------------------|---------|---------------|
| Runtime | **Node.js** | 20 LTS | TypeScript nativo, comunidad activa, costos bajos en nube. |
| Framework | **NestJS** | 10.x | Modular, con **inyección de dependencias** integrada, lo que **facilita aplicar los patrones exigidos por RNF27** (Repository, Strategy, Factory, Adapter, Observer). Estructura opinada reduce decisiones de arquitectura improvisadas. |
| ORM | **Prisma** | 5.x | Tipos generados del esquema, migraciones versionadas, buena experiencia de desarrollo. |
| Validación | **class-validator** + **class-transformer** | Latest | Integrados nativamente con NestJS para validar DTOs de entrada. |
| Autenticación | **Passport.js** (estrategia JWT) + **bcryptjs** | Latest | JWT cumple el requerimiento de sesión con expiración (RNF08). bcrypt cubre el almacenamiento seguro del PIN (RNF07). |
| Documentación API | **@nestjs/swagger** | Latest | Genera OpenAPI automáticamente a partir de decoradores. Facilita onboarding del próximo equipo. |
| Logs | **pino** (wrapper NestJS) | Latest | Logs estructurados en JSON con alto rendimiento (RNF30). |
| Jobs asíncronos | **BullMQ** + Redis | Latest | Para reportes pesados (RNF17) y reintentos de SMS. |
| Notificaciones SMS | **Twilio SDK** (`twilio`) | Latest | SDK oficial; se envuelve en un adaptador interno (patrón Adapter) que permite cambiar de proveedor sin impactar la lógica. |
| Pruebas unitarias | **Jest** | Latest | Integrado con NestJS por defecto. |
| Pruebas E2E | **Supertest** + Jest | Latest | Pruebas de integración sobre la API. |

**Alternativas evaluadas y descartadas**

- **Express puro** → requiere construir desde cero la inyección de dependencias y los decoradores; NestJS ahorra ese trabajo y encaja mejor con la obligación de patrones.
- **Fastify puro** → más rápido que Express pero con el mismo problema de estructura manual.
- **Django / Laravel** → romper la consistencia TypeScript con Python/PHP aporta poco valor para este alcance.
- **TypeORM** → más flexible que Prisma pero con tipos menos estrictos y migraciones menos pulidas.

---

### B.3 Base de datos

| Componente | Tecnología elegida | Versión | Justificación |
|------------|---------------------|---------|---------------|
| Motor | **PostgreSQL** | 16.x | Soporte excelente para tipos ricos (enum, jsonb para bitácoras), transacciones ACID, amplia oferta de proveedores gestionados. |
| Caché / cola | **Redis** | 7.x | Soporte para BullMQ, caché de consultas frecuentes del catálogo. Opcional en el despliegue inicial; se añade cuando el tráfico lo justifica. |

**Alternativas evaluadas y descartadas**

- **MySQL / MariaDB** → viable, pero PostgreSQL tiene mejor soporte de tipos y sintaxis para el tipo de consultas analíticas de los reportes.
- **MongoDB** → el dominio (usuarios, productos, acuerdos con relaciones) es fuertemente relacional; un modelo documental introduciría complicaciones sin beneficios claros.

---

### B.4 Infraestructura y despliegue

| Componente | Tecnología elegida | Justificación |
|------------|---------------------|---------------|
| Hosting PWA | **GitHub Pages** (con opción de migrar a **Cloudflare Pages**) | Costo cero, HTTPS automático, CDN global. GitHub Pages ya se usa para el prototipo actual. |
| Hosting API | **Render.com** (opción A) o **Fly.io** (opción B) | Ambos ofrecen tier económico (~USD 7–15/mes), escalado horizontal sencillo y despliegue desde repositorio Git. |
| Base de datos gestionada | **Render PostgreSQL** o **Neon** | Backups automáticos diarios, *point-in-time recovery*, cifrado en reposo. Costo estimado USD 7–20/mes. |
| DNS + SSL | **Cloudflare** o proveedor de dominios | Certificado automático, protección DDoS básica gratuita. |
| Monitoreo y logs | **BetterStack / Logtail** (free tier) | Agregación de logs estructurados y alertas por umbrales. |

**Alternativas evaluadas y descartadas**

- **AWS ECS / EKS** → potencia innecesaria, costos menos predecibles para una organización sin personal técnico.
- **Vercel** (para API) → excelente para Next.js serverless, no ideal para API con conexión persistente y jobs.
- **Heroku** → costos aumentados tras 2022, alternativas equivalentes más baratas.

---

### B.5 DevOps y calidad

| Componente | Tecnología elegida | Justificación |
|------------|---------------------|---------------|
| Control de versiones | **Git** + **GitHub** | Estándar; permite integración con CI/CD y GitHub Pages. |
| Convención de commits | **Conventional Commits** | Genera changelog automático y semantiza las versiones. |
| CI/CD | **GitHub Actions** | Incluido con GitHub, suficiente para los volúmenes esperados. Pipelines: lint → test → build → deploy. |
| Linter / Formateador | **ESLint** + **Prettier** | Consistencia de estilo entre desarrolladores. |
| Hooks pre-commit | **husky** + **lint-staged** | Evita subir código sin lint ni formato. |
| Contenedores (opcional) | **Docker** + **Docker Compose** | Reproduce entorno local para pruebas de integración. |

---

### B.6 Servicios de terceros

| Servicio | Proveedor | Uso | Plan estimado |
|----------|-----------|-----|----------------|
| SMS | **Twilio** | Código de verificación al alta (RF26) y recuperación de PIN (RF05). | Pay-as-you-go; ~USD 0.05–0.10 por SMS. |
| Dominio | *Registrador a elección* | URL pública del sistema. | USD 10–15/año. |
| Almacenamiento de respaldos | Del proveedor de DB | Backups cifrados. | Incluido en el plan de DB. |

---

### B.7 Mapa Patrones de Diseño ↔ Stack

Anclaje explícito del requerimiento **RNF27** (patrones de diseño obligatorios en la fase final) con las tecnologías elegidas.

| Patrón | Dónde se implementa con el stack propuesto |
|--------|---------------------------------------------|
| **Repository** | Clases `*.repository.ts` en NestJS inyectadas en los servicios de aplicación; Prisma queda encapsulado, no se expone a los controladores. |
| **Factory Method** | Provider dinámico en NestJS que retorna un `UserRepository` real o en memoria según el entorno (tests vs producción). |
| **Adapter** | `SmsAdapter` que envuelve a Twilio; `HttpClient` del frontend que envuelve a `fetch`. |
| **State** | Clase `AgreementStateMachine` que define las transiciones válidas del acuerdo; cada estado hereda de una clase base común. |
| **Strategy** | `NotificationChannelStrategy` decide entre in-app y SMS según el evento y las preferencias del usuario. |
| **Observer** | Sistema de eventos de NestJS (`@nestjs/event-emitter`) conectando los servicios de negocio con el `AuditService` de manera desacoplada. |

---

### B.8 Resumen ejecutivo del stack

**Frontend:** React 18 + TypeScript + Vite + Tailwind + React Router + PWA Workbox + IndexedDB.

**Backend:** Node.js 20 + NestJS + Prisma + PostgreSQL + BullMQ/Redis + Twilio + Passport/JWT.

**Infraestructura:** GitHub Pages (PWA) + Render.com (API + DB) + BetterStack (monitoreo).

**DevOps:** GitHub + GitHub Actions + ESLint + Prettier + Husky + Conventional Commits.

**Costo recurrente estimado:** USD 20–57 / mes (ver §8.5) + mantenimiento por demanda de proveedor externo.

Este stack queda **fijado para la fase III (desarrollo)** como indica el Proyecto II. Cualquier cambio posterior deberá justificarse en una adenda al presente documento.

---

*Fin del Anexo B y del documento DERCAS del Proyecto II.*

---

## Índice de referencias rápidas

| Artefacto | Ubicación |
|-----------|-----------|
| Diagrama de casos de uso (fase 1, actualizado) | [modelo-casos-de-uso.md](./modelo-casos-de-uso.md) |
| Modelo Entidad-Relación (actualizado) | [modelo-er.md](./modelo-er.md) |
| Prototipo interactivo (online) | https://alexalvarado1290.github.io/la-esperanza/dashboard |
| Código fuente del prototipo | `Proyecto 1/Proyecto La Esperanza/LA ESPERANZA/` |
| Cuestionario aplicado | https://docs.google.com/forms/d/e/1FAIpQLSf0pabsdelzJ2GmJr-UQg-4mUbgpflkiSnEQPKoZKZFXkfbfw/viewform |
