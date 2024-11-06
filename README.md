# NitrogenAI API Prediction

NitrogenAI Prediction API, es una API REST que permite predecir la cantidad de nitrógeno en cultivos de piña usando imágenes multiespectrales (nir, red, blue, green, red edge) y datos IoT como humedad, pH, temperatura del suelo y clorofila; ayudando a los agricultores a optimizar su manejo de recursos y reducir los costos como el pago de muestras.

## Créditos

Este proyecto es la mera implementación de todo un [trabajo investigativo doctoral](https://scholar.google.com/citations?view_op=view_citation&hl=es&user=fZyJzlgAAAAJ&citation_for_view=fZyJzlgAAAAJ:W7OEmFMy1HYC) a cargo del doctor Jorge Enrique Chaparro Mesa, que culmina en el entrenamiento de un modelo capaz de predecir la cantidad de nitrógeno en cultivos de piña usando las variables mencionadas en la introducción, teniendo un margen de error del 13.45%.

✨Por ahora, el sistema está configurado para trabajar con cámaras multiespectrales "micasense" ya que así fue encontrado en el proyecto investigativo

[Instalación del modelo en un jupyter](/doc/setup.ipynb)
[Ejemplo de caso de uso en jupyter](/doc/setup.ipynb)

## Cómo funciona?

Actualmente el sistema provee 6 endpoints. Por ahora no utiliza oauth2 ni ningún método de autenticación.

| Método | Endpoint                                                            | Parámetros                                                                                                                                                                 | Descripción                                                                                                                                                                                                                                                                                         |
| ------ | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GET    | /up                                                                 | Permite saber si el servicio está en linea                                                                                                                                 |
| POST   | /upload-images                                                      | bands: Array<File>(5) panels: Array<File>(5)                                                                                                                               | Permite subir la foto multiespectral (bands) y el panel de refractancia (panels) cargando para ambos un array que contenga 5 archivos (uno por cada banda: NIR, RED, GREEN, REDEDGE, BLUE), una vez finaliza la subida retorna un string que será el **session-id** usado en el resto de peticiones |
| POST   | /\<session-id>/process                                              |                                                                                                                                                                            | Una vez se ejecute esta petición el sistema empezará a tratar los archivos cargados para extraer de ellos multiple información como distintos filtros de la imágen y permitir en siguientes peticiones predecir el valor de nitrógeno                                                               |
| GET    | /\<session-id>/status                                               |                                                                                                                                                                            | Está petición es **temporal**, simplemente retorna un arreglo con todos los filtros de imágen que se están creando y un status que determina si ya se ha creado o no. En el futuro deberia utilizar sockets para enviar esta información usando el proceso del endpoint anterior.                   |
| GET    | /\<session-id>/storage/<bands \| panels>/<tipo de filtro de imágen> | crop?: Boolean x: String y: String width: String height: String                                                                                                            | Usando la anterior petición podemos tomar algun registro de estos y usando el id de filtro obtener la imágen final. También si agregamos el parametro "crop" intentará devolver la sección descrita en x, y, width, height **(importante, estas medidas deben ser % a la imágen)**                  |
| POST   | /\<session-id>/predict                                              | roi_coordinates:{ x: String, y: String, width: String, height: String } <br/> data_iot: { soil_humedity: Number, soild_temperature: Number, pH: Number, avg_spad: Number } | Esta ruta recibe la sección de la imágen que queremos predecir, e información IoT (humedad, temperatura, pH y promedio de clorofila en el suelo), retorna el valor de nitrogeno predecido                                                                                                           |

## Tecnologías detrás

Como se comentó en los créditos, el sistema utiliza en su core todo un ambiente de funcionalidades entregadas por micasense. Nosotros tomamos el proyecto investigativo y lo cubrimos en flask para permitir usarlo como una Api.

- Flask: Permite levantar rápidamente un servidor en python y usarlo como api rest.
- Docker: Nos permitió poder levantar rápidamente toda la configuración y prerequisitos que tenia el modelo para funcionar.
- Joblib y xgboost: Nos permitió recuperar el modelo ya entrenado (.pkl) y usarlo.

## Cómo levantar el servidor?

Como la configuración del proyecto es muy especifica para poder trabajar con el modelo, te recomendamos tener Docker y ejecutar el dockerfile que ya tiene toda la configuración programática del despliegue.

```sh
docker build -t nitrogen-prediction-back .
docker run -d -p 5000:5000 nitrogen-prediction-back
```

O si lo prefieres, puedes usar docker-compose para levantarlo aún más rápido.

```sh
#Desplegar solo la api
docker-compose up back

#Desplegar api y página web
docker-compose up
```

Este último tipo de despliegue también te permitirá levantar una pequeña página web que transmite todos los flujos de la api usando una interfaz gráfica, [revisa el repositorio aquí](https://github.com/rdzPedraos/NitrogenPrediction-front)
