# Validación técnica del borrador

## Resultado actual

El informe compila desde una copia limpia de fuentes con pdfLaTeX, Biber y dos pasadas finales de pdfLaTeX. Los cinco registros académicos con DOI coinciden con Crossref y sus destinos editoriales registrados. El control de archivos tiene diez comprobaciones PASS y seis grupos pendientes. El estado global sigue siendo **NO_LISTO_PARA_ENTREGA** por las evidencias y requisitos personales que faltan.

La validación técnica y lectura de pasajes fueron realizadas por el asistente. No se atribuyen al estudiante como ejecución o lectura personal.

## Bibliografía y lectura

- `fuentes/verificacion-doi.json`: cinco registros `METADATOS_Y_REDIRECCION_OK`, sin discrepancias de nombres completos y orden, título, publicación, tipo, volumen, fascículo, páginas/eid y año. Los cinco DOI responden con redirección al recurso editorial registrado. El verificador termina con código 0.
- El acceso editorial se informa por separado: IEEE devolvió 202; otros destinos limitan solicitudes automáticas. Eso no acredita acceso integral ni se confunde con el cotejo de identidad bibliográfica.
- `fuentes/indexacion.json`: IEEE Access corroborada mediante su editorial; FGCS y JSS mediante las fichas SCImago, con datos Scopus. Esta última comprobación es secundaria y no equivale a entrar al catálogo de suscripción de Scopus.
- Se consultaron los pasajes usados de tres manuscritos de autores: Henning y Hasselbring (2303.11088v2), Vogel et al. (2404.06203v3) y Chen et al. (2603.04027v1). Versión, URL y SHA-256 están en `fuentes/lecturas-consultadas.json`.
- Los PDF de lectura se guardan fuera del repositorio, en `/workspace/lecturas-ta-ind/`; `fuentes/LECTURAS.md` permite descargarlos desde sus fuentes y localiza los pasajes.
- La lectura integral de las dos obras de Raptis sigue pendiente. Tampoco se han creado capturas para simular lectura personal del estudiante.
- El uso por Grab se documenta mediante el sitio oficial de Kafka. El incidente kafka-go #1358 se presenta como reporte público, con diagnóstico y mitigaciones propuestos, sin atribuir una recuperación productiva medida que el hilo no confirma.

## PDF y estructura

- `informe/main.pdf`: doce páginas, con más de cinco páginas de contenido antes de las referencias y sin contar carátula ni anexos.
- Resumen: 170 palabras por separación de espacios.
- Bibliografía: `biblatex`, estilo IEEE y backend Biber.
- Compilación limpia final: sin referencias indefinidas, errores fatales ni desbordamientos de línea en el log de la última pasada.
- `entrega-sga.pdf`: una página A4. La URL del repositorio se extrajo íntegra como un solo elemento con `pdftotext -bbox`.
- El código de `scripts/comprobar_entrega.py` es 2 porque faltan requisitos. Ese resultado esperado no se presenta como entrega aprobada.

## Experimento

Resultados conservados de las ejecuciones automatizadas previas; no se repitieron porque el laboratorio no cambió en la revisión bibliográfica.

| Corrida UTC | Resultado | Mensajes ISR2 | Mensajes ISR3 | Broker detenido |
|---|---|---|---|---|
| `20261114T003313Z` | PASS | 30 | 20 | kafka3 |
| `20261114T003807Z` | PASS | 30 | 20 | kafka1 |
| `20261114T004432Z` | PASS | 30 | 20 | kafka2 |

En cada corrida se compararon valores y multiplicidades de todos los mensajes; se observó `NotEnoughReplicasException` con mínimo ISR3 durante el fallo y se restauró ISR=3. Los identificadores de tópico son distintos y los comandos, entradas y salidas están archivados.

La revisión inicial detectó una discrepancia entre ruta de datos y volumen. Se preservaron y migraron los datos, se fijó `KAFKA_LOG_DIRS=/tmp/kafka-logs` y se montó allí el volumen de cada nodo. La tercera corrida utilizó la corrección. Después, `scripts/verificar_persistencia.py --recrear` recreó los tres contenedores y comprobó los conjuntos de los seis tópicos anteriores: todos PASS. Ver `experimento/persistencia.json`.

Estos resultados no prueban particiones de red, pérdida física de discos ni procesamiento exactamente una vez de efectos externos. Tampoco reemplazan la sesión personal del estudiante.

## Red, commits y requisitos restantes

El estudiante publicó un nuevo entorno con red sin restricciones; Crossref y el resolvedor DOI están disponibles. Las limitaciones editoriales actuales se registran por fuente. No se desactivaron TLS ni controles de integridad ni se solicitaron credenciales nuevas.

El estudiante autorizó el commit con la identidad Git configurada y sin trailers de coautoría. Los autores y fechas de commits anteriores se conservan. La declaración real de uso de IA permanece en el informe y la bitácora.

Continúan pendientes las evidencias originales, video, revisión personal, historial progresivo requerido y confirmaciones del SGA; ver `PENDIENTES.md`. No se realizó entrega en SGA ni se publicó de nuevo el entorno.
