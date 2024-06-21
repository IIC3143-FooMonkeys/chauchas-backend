# Elección de tecnologías para la plataforma de beneficios bancarios

## Contexto y declaración del problema

El desarrollo de una plataforma que facilite el acceso a descuentos y beneficios ofrecidos por los distintos bancos en Chile presenta varios desafíos técnicos. Por esto, es crucial elegir un conjunto de tecnologías que pueda soportar las funcionalidades requeridas, que sea escalable para la adición de más bancos y usuarios a futuro y que permita una fácil integración con distintos formatos de las entidades bancarias.


## Factores decisivos

- **Escalabilidad**: La plataforma debe manejar un número creciente de usuarios y bancos.
- **Flexibilidad en el manejo de datos**: Diferentes bancos pueden tener formatos de datos variados que necesitan ser integrados.
- **Rendimiento y eficiencia**: Tiempos de respuesta rápidos para las consultas de los usuarios.
- **Facilidad de desarrollo y mantenimiento**: Importante para agilizar el desarrollo y el mantenimiento futuro del código.

## Opciones consideradas

1. **React + Node.js + MongoDB**
2. **React + Python (FastAPI) + MongoDB**
3. **Vue.js + Python (Django) + PostgreSQL**

## Resultado de la decisión

Se eligió la segunda opción, ya que esta ofrece la mejor combinación de rendimiento, facilidad de desarrollo y flexibilidad requeridas para manejar los diversos datos con los que se trabajaría. FastAPI tiene excelente soporte para operaciones asincrónicas (crucial para el rendimiento). La naturaleza sin schema de MongoDB es ideal para integrar distintas estructuras de dato. Por último, React fue elegido por su rendimiento eficiente y componentes reutilizables.

### Consecuencias

- **Bueno**, porque FastAPI soporta el manejo de solicitudes asincrónicas, lo que mejora la capacidad de la plataforma para manejar altas cargas.
- **Bueno**, porque MongoDB proporciona flexibilidad en el almacenamiento y recuperación de datos de varios formatos bancarios sin necesidad de un esquema de base de datos rígido.
- **Malo**, porque la curva de aprendizaje para FastAPI puede ser pronunciada para desarrolladores no familiarizados con esta tecnología.

## Decisiones adicionales sobre infraestructura y pruebas

### Infraestructura en AWS

- **AWS EC2**: Se utilizó Amazon EC2 para alojar las instancias de servidor, lo que permite escalar según la demanda y gestionar la carga de manera eficiente.
- **AWS S3**: Para almacenamiento de datos y backups, se utilizó Amazon S3 por su durabilidad, disponibilidad y escalabilidad.
- **AWS CloudFront**: Se implementó CloudFront para distribuir contenido dinámico y estático con baja latencia y altas velocidades de transferencia a nivel global.

### Proxy y balanceo de carga

- **NGINX**: Se seleccionó NGINX como proxy inverso y balanceador de carga por su rendimiento, configurabilidad y soporte para conexiones HTTPS.

### Testing del backend

- **Pytest**: Se utilizó pytest por su flexibilidad y facilidad de uso para escribir pruebas simples y complejas.
- **Pytest-asyncio**: Específico para probar código asincrónico en FastAPI, permitiendo un manejo eficiente de las pruebas asincrónicas.
- **Pytest-cov**: Se utilizó este plugin para generar reportes de cobertura de código, lo que ayuda a asegurar que las pruebas cubren una porción adecuada del código base.

## Pros y contras de las opciones de infraestructura y pruebas

### AWS EC2 + S3 + CloudFront + NGINX

- **Bueno**, porque la integración de estos servicios ofrece una solución robusta y escalable para el manejo de carga y almacenamiento de datos.
- **Bueno**, porque AWS CloudFront mejora la experiencia del usuario final al reducir la latencia de carga de la página.
- **Malo**, porque la configuración y mantenimiento de múltiples servicios AWS puede ser compleja y requiere conocimientos específicos en AWS.

### Pytest + Pytest-asyncio + Pytest-cov

- **Bueno**, porque proporcionan un entorno de testing robusto y flexible para un desarrollo rápido y eficiente.
- **Bueno**, porque la cobertura de código permite mantener altos estándares de calidad y detectar problemas antes de la implementación.
- **Malo**, porque configurar y mantener un entorno de pruebas para código asincrónico puede ser más complejo que para pruebas sincrónicas tradicionales.

### Testing del frontend

- **Jest**: Se optó por Jest para las pruebas del frontend debido a su compatibilidad con React, su facilidad de configuración y su capacidad para manejar pruebas de componentes de manera eficiente. Jest ofrece un entorno de pruebas con amplia variedad de utilidades para mocking y aserciones, haciéndolo ideal para proyectos dinámicos y componentes interactivos como los utilizados en React.

#### Pros y contras de usar Jest para el frontend

- **Bueno**, porque Jest integra funciones como la ejecución de pruebas en paralelo y snapshots que agilizan el proceso de testing.
- **Bueno**, porque su sistema de mocking integrado facilita la prueba de componentes complejos sin depender de la infraestructura externa.
- **Malo**, porque aunque Jest es muy poderoso, puede ser pesado en términos de tiempo de ejecución para proyectos muy grandes con miles de pruebas.

### Implementación de Web Scrapers

- **Selenium y BeautifulSoup**: Para la recolección de datos de las diferentes páginas web de entidades bancarias, se decidió utilizar Selenium y BeautifulSoup. Selenium permite interactuar con las páginas web como si fuese un usuario real, facilitando la navegación y el acceso a contenido que requiere interacción dinámica. BeautifulSoup se utiliza para parsear el HTML obtenido y extraer la información necesaria de manera eficiente.

#### Pros y contras de usar Selenium y BeautifulSoup para web scraping

- **Bueno**, porque Selenium permite automatizar la navegación en páginas complejas que requieren interacción del usuario, como clics o ingreso de datos, para acceder a la información.
- **Bueno**, porque BeautifulSoup es excelente para extraer datos de documentos HTML, proporcionando una manera sencilla y efectiva de parsear el contenido.
- **Malo**, porque la combinación de Selenium y BeautifulSoup puede ser lenta comparada con métodos de scraping más directos y requiere más recursos de sistema, especialmente en sitios web con muchas cargas dinámicas.

## Más información

Las decisiones tomadas se alinean con el objetivo establecido de construir una plataforma escalable y flexible, que pueda adaptarse a los requerimientos cambiantes y distintos formatos de datos obtenidos.