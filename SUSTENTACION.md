# Guía para preparar tu video y defensa

Esta guía ayuda a comprender el trabajo. No sustituye el video con tu rostro y voz ni tus capturas originales. Debes explicar una captura de TU sesión, sin leer un texto preparado.

## Recorrido sugerido: cuatro minutos

- **0:00–0:35.** Presenta la pregunta: qué ocurre con las escrituras al perder un broker y cómo depende del mínimo ISR.
- **0:35–1:10.** Identifica productor, broker líder, seguidores y consumidores. Separa ISR de partición y mayoría KRaft de metadatos.
- **1:10–2:20.** Muestra tu captura del fallo. Señala el comando y los ISR; explica por qué un tópico admite escritura y el otro registra `NotEnoughReplicas`.
- **2:20–3:15.** Explica cómo comprobaste mensajes confirmados, cómo se recuperó el nodo y dónde guardaste comandos y resultados. Evita interpretar el arranque de cada CLI como latencia de un mensaje.
- **3:15–4:00.** Concluye qué compromiso observaste y qué no probaste: una caída de proceso no es automáticamente una partición de red. Declara la ayuda de IA y qué revisaste o ejecutaste personalmente.

## Preguntas para practicar

1. **¿`acks=all` significa todas las réplicas asignadas?** No: la confirmación considera las réplicas ISR actuales; el mínimo ISR exige un umbral para habilitar la escritura.
2. **¿Por qué ISR2 continúa con tres réplicas asignadas y un nodo caído?** Porque aún quedan dos ISR y se satisface su mínimo; hay una política distinta de la del tópico que exige tres.
3. **¿Es el mismo cuórum que KRaft?** No. KRaft coordina metadatos; ISR describe réplicas sincronizadas de una partición. Aquí los procesos tienen ambos roles, pero no son el mismo mecanismo.
4. **¿Se perdieron los diez mensajes rechazados de ISR3?** No se cuentan como mensajes confirmados perdidos: la aplicación recibió un error de entrega. Debe decidir qué hacer con esos datos.
5. **¿Un proceso con código de salida cero prueba entrega?** La consola productora puede registrar errores y aun así terminar con cero. Se revisan errores y se consume el tópico para comparar conjuntos y multiplicidades.
6. **¿Se garantizó exactamente una vez en cualquier aplicación?** No. La idempotencia del productor no prueba que un consumidor no duplique un efecto externo.
7. **¿Qué diferencia hay entre reiniciar y recrear un contenedor?** Reiniciar conserva su capa; recrearlo la reemplaza. Los volúmenes deben contener la ruta real de datos para conservarlos.
8. **¿Se midió que RabbitMQ sea más rápido o lento?** No. La comparación actual es de mecanismos documentados, no un benchmark de RabbitMQ.
9. **¿El reporte de goroutines demuestra que la replicación de Kafka falla?** No: describe problemas en el ciclo de vida del cliente y de sus recursos. Hay que distinguir cliente, broker y efecto observado.
10. **¿Por qué WhatsApp lento no demuestra que use Kafka o consistencia eventual?** Una observación de interfaz admite distintas causas. Sin documentación o prueba no se atribuye una implementación interna.

Antes de grabar, ejecuta la prueba y asegúrate de poder modificar un parámetro y anticipar su efecto. No memorices respuestas que no puedas demostrar.

## Commits y trazabilidad

El estudiante autorizó al asistente registrar esta continuación con la identidad configurada en Git, sin trailers de coautoría. Los dos commits iniciales mantienen su autoría de Codex. Esto no transforma los registros de ejecución asistida en evidencias personales.

Para los siguientes avances, revisa `git diff` y los archivos nuevos con `git status`, registra en BITACORA.md lo que comprendiste y verificaste personalmente, y escribe mensajes descriptivos. Un commit no reemplaza las capturas, lecturas o la explicación oral. Conserva fechas reales y la declaración de asistencia.
