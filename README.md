#  Portal Cautivo Inalámbrico Seguro con Autenticación AAA (FreeRADIUS) y Control de Red en Linux

Este repositorio contiene la implementación completa de una arquitectura de red inalámbrica cerrada y controlada sobre Linux. El sistema despliega un punto de acceso físico (`hostapd`), gestión de direccionamiento DHCP/DNS (`dnsmasq`), enrutamiento y filtrado de paquetes mediante cortafuegos (`nftables`), y un servidor de autenticación centralizada AAA a través de `FreeRADIUS`, gestionado por una interfaz web interactiva desarrollada en `Flask`.

---

##  Características Principales
* **Punto de Acceso Autónomo (AP):** Configuración de tarjeta inalámbrica en modo Maestro mediante `hostapd`.
* **Servicios de Red Integrados:** Asignación dinámica de IP y resolución de nombres con `dnsmasq`.
* **Seguridad y Control de Tráfico:** Filtrado de paquetes, NAT y redirección HTTP mediante reglas de `nftables`.
* **Autenticación Centralizada (AAA):** Validación de credenciales y atributos de sesión con `FreeRADIUS` (soporte de perfiles por roles: invitados, estudiantes, docentes y staff).
* **Portal Cautivo Web:** Aplicación en `Flask` con micro-quizzes interactivos, contadores de tiempo de sesión y control dinámico de listas blancas.
* **Auditoría de Contabilidad:** Registro cronológico de eventos `Accounting-Start` y `Accounting-Stop`.

---

##  Estructura del Proyecto
```text
portal-cautivo/
├── portal/
│   ├── portal.py             # Aplicación principal en Flask y lógica de integración RADIUS
│   ├── templates/
│   │   └── login.html        # Plantilla HTML interactiva con temporizador y micro-quiz
│   └── dict/
│       └── dictionary        # Diccionario de atributos personalizados RADIUS
├── config/
│   ├── hostapd.conf          # Configuración del punto de acceso inalámbrico
│   ├── dnsmasq.conf          # Configuración de red y DHCP
│   └── users                 # Base de datos de usuarios y perfiles en FreeRADIUS
├── iniciar.sh                # Script automatizado para encender todos los servicios
└── detener.sh                # Script automatizado para apagar y limpiar procesos de red
--

--

##  Requisitos del Sistema

* Sistema operativo Linux (probado en Ubuntu / Debian).
* Tarjeta de red inalámbrica compatible con modo AP (Master).
* Dependencias e instalaciones previas:
  * `hostapd`
  * `dnsmasq`
  * `freeradius`
  * `nftables`
  * Python 3 con librerías `Flask` y `pyrad`.

---
