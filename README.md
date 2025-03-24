Challenge Segurarse
===================

Este proyecto implementa una aplicación simple de FastAPI desplegada en Google Cloud Run mediante un pipeline CI/CD automatizado. La aplicación expone un endpoint básico que devuelve un mensaje de saludo y está containerizada con Docker. Además, incluye notificaciones en Telegram y análisis estático de código con Bandit.

Instrucciones de Configuración
------------------------------

### Requisitos Previos

*   Docker: Instalado localmente para construir y probar la imagen.
    
*   Cuenta de DockerHub: Para almacenar la imagen Docker.
    
*   Cuenta de Google Cloud: Con un proyecto creado y las APIs de Cloud Run y Container Registry habilitadas.
    
*   Telegram: Un bot y un grupo para recibir notificaciones.
    
*   GitHub: Un repositorio con secretos configurados.
    

### Configuración Local

Paso 1: Clonar el Repositorio

*   Ejecuta el siguiente comando en tu terminal:git clone [git@github.com](mailto:git@github.com):R3NZ0FR5NCH377O/challenge-segurarse.git
    
*   Luego, accede al directorio del proyecto:cd challenge-segurarse
    

Paso 2: Construir y Probar la Imagen Localmente

*   Construye la imagen Docker con este comando:docker build -t /challenge-segurarse:latest .
    
*   Ejecuta el contenedor para probarlo:docker run -p 8080:8080 /challenge-segurarse:latest
    
*   Abre tu navegador y visita [http://localhost:8080](http://localhost:8080). Deberías ver el mensaje: {"message": "Hola Segurarse, soy Renzo"}.
    

Paso 3: Configurar Secretos en GitHub

*   Ve a la sección "Settings > Secrets and variables > Actions" en tu repositorio de GitHub y agrega las siguientes variables:
    
    *   DOCKERHUB\_USERNAME: Tu usuario de DockerHub.
        
    *   DOCKERHUB\_TOKEN: Token de acceso de DockerHub.
        
    *   GCP\_SA\_KEY: JSON de la clave de cuenta de servicio de GCP.
        
    *   GCP\_PROJECT\_ID: ID de tu proyecto en GCP.
        
    *   TELEGRAM\_TOKEN: Token del bot de Telegram (obtenido de @BotFather).
        
    *   TELEGRAM\_CHAT\_ID: ID del grupo de Telegram (número negativo, obtenido con getUpdates).
        

Paso 4: Configurar Telegram

*   Crea un bot en Telegram usando @BotFather y obtén el token.
    
*   Añade el bot a un grupo de Telegram.
    
*   Para obtener el chat\_id del grupo, ejecuta este comando en tu terminal:curl [https://api.telegram.org/bot](https://api.telegram.org/bot)/getUpdates
    
*   Busca el número negativo correspondiente al chat\_id en la respuesta.
    

Paso 5: Configuración en GCP

*   Habilita las APIs necesarias con este comando:gcloud services enable run.googleapis.com containerregistry.googleapis.com
    
*   Crea una cuenta de servicio ejecutando:gcloud iam service-accounts create github-actions-sa --display-name="GitHub Actions SA"
    
*   Asigna permisos a la cuenta de servicio con estos comandos:gcloud projects add-iam-policy-binding \--member="serviceAccount:github-actions-sa@.iam.gserviceaccount.com" --role="roles/run.admin"gcloud projects add-iam-policy-binding \--member="serviceAccount:github-actions-sa@.iam.gserviceaccount.com" --role="roles/storage.admin"gcloud iam service-accounts add-iam-policy-binding [\-compute@developer.gserviceaccount.com](mailto:-compute@developer.gserviceaccount.com) --member="serviceAccount:github-actions-sa@.iam.gserviceaccount.com" --role="roles/iam.serviceAccountUser"
    
*   Genera una clave para la cuenta de servicio:gcloud iam service-accounts keys create gcp-sa-key.json --iam-account=github-actions-sa@.iam.gserviceaccount.com
    

### Enfoque de Containerización

*   Base: Utilizo python:3.9-slim como imagen base para mantener el tamaño ligero y optimizado.
    
*   Dependencias: Instalo fastapi y uvicorn mediante pip en el Dockerfile para asegurar un entorno reproducible.
    
*   Puerto: Exponemos el puerto 8080, que es el estándar de Cloud Run, y configuro uvicorn para escuchar en él de forma estática (port = 8080) para simplicidad, aunque idealmente debería usar os.getenv("PORT", 8080) para mayor flexibilidad.
    
*   Ejecución: El CMD \["python", "main.py"\] ejecuta el script principal, que inicia el servidor uvicorn con la aplicación FastAPI.
    
*   Este enfoque prioriza simplicidad y rapidez para un desafío, asegurando que la aplicación sea portable y fácil de desplegar en Cloud Run.
    

Detalles del Pipeline CI/CD
---------------------------

El pipeline, definido en .github/workflows/main.yaml, automatiza el proceso de construcción, publicación y despliegue con los siguientes pasos:

*   Clonar Repositorio: Descarga el código fuente.
    
*   Iniciar Sesión en DockerHub: Autentica con credenciales seguras.
    
*   Construir Imagen Docker: Crea una imagen con un tag único basado en el commit SHA (${{ github.sha }}).
    
*   Subir Imagen Docker: Publica la imagen en DockerHub.
    
*   Autenticar en Google Cloud: Usa una cuenta de servicio para acceder a GCP.
    
*   Configurar gcloud CLI: Prepara el entorno para comandos gcloud.
    
*   Analizar Código con Bandit: Ejecuta un análisis estático y envía el reporte a Telegram.
    
*   Desplegar en Google Cloud Run: Despliega la imagen en Cloud Run y captura la URL.
    
*   Notificaciones: Cada paso envía un mensaje a un grupo de Telegram, incluyendo éxitos y fallos, con la URL del despliegue al final si todo sale bien.
    

URL de la Aplicación Desplegada
-------------------------------

*   La aplicación está desplegada en:[https://challenge-segurarse-abc123-uc.a.run.app](https://challenge-segurarse-abc123-uc.a.run.app)
    
*   Nota: Reemplaza esta URL con la real obtenida del comando:gcloud run services describe challenge-segurarse --region=us-central1 --format='value(status.url)'después del despliegue.
    

Desafíos Enfrentados y Soluciones
---------------------------------

*   Permisos en Cloud Run:
    
    *   Problema: El despliegue fallaba por falta de permisos iam.serviceaccounts.actAs en la cuenta de servicio.
        
    *   Solución: Otorgué el rol roles/iam.serviceAccountUser a github-actions-sa sobre la cuenta de servicio predeterminada de Compute Engine.
        
*   Puerto Incorrecto:
    
    *   Problema: La aplicación escuchaba en el puerto 80 en lugar de 8080, causando fallos en las revisiones de Cloud Run.
        
    *   Solución: Cambié el puerto a 8080 en main.py y ajusté el Dockerfile para exponerlo correctamente.
        
*   Imagen Desactualizada:
    
    *   Problema: El pipeline desplegaba una imagen antigua de DockerHub.
        
    *   Solución: Usé tags únicos (${{ github.sha }}) para asegurar que siempre se subiera y desplegara la versión más reciente.
        
*   Errores de Sintaxis en el Pipeline:
    
    *   Problema: Un typo (if: failure stray()) invalidaba el workflow.
        
    *   Solución: Corregí a if: failure() para activar notificaciones de fallo correctamente.
        

Sugerencias para Mejorar el Despliegue en Producción
----------------------------------------------------

*   Uso de Variables de Entorno: Modificar main.py para usar port = int(os.getenv("PORT", 8080)) en lugar de un puerto fijo, aumentando la flexibilidad.
    
*   Secretos y Configuración: Almacenar configuraciones sensibles (como el mensaje de saludo) en variables de entorno en Cloud Run, en lugar de hardcoded en el código.
    
*   Monitoreo y Logging: Integrar Google Cloud Monitoring y Logging para rastrear métricas y errores en tiempo real.
    
*   Pruebas Automatizadas: Agregar un paso de pruebas unitarias con pytest antes de construir la imagen, asegurando la calidad del código.
    
*   Escalabilidad: Configurar autoescalado en Cloud Run con límites de CPU y memoria adecuados para manejar tráfico variable.
    
*   Seguridad:
    
    *   Usar un registro privado (como Google Container Registry) en lugar de DockerHub público.
        
    *   Habilitar autenticación en Cloud Run (remover --allow-unauthenticated) y usar IAM para accesos autorizados.
        
*   Optimización de Imagen: Usar multi-stage builds en el Dockerfile para reducir el tamaño de la imagen final, eliminando dependencias innecesarias.
    
*   Notificaciones Avanzadas: Enviar logs detallados o capturas de errores a Telegram en caso de fallo, usando APIs adicionales o herramientas como curl.