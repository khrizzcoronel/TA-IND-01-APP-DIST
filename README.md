# TA-IND-01 — Kafka frente a RabbitMQ

**Estado: borrador asistido por IA. No es una entrega académica terminada.**

Estudiante: Khriz Alexander Coronel Gómez · Aplicaciones Distribuidas (ISR-701), UTEQ · Séptimo A.

Pregunta: ¿cómo afectan la replicación y el mínimo ISR a la conservación de mensajes y a la disponibilidad de escritura cuando falla un broker de Kafka?

## Archivos

- `informe/main.tex`, `informe/referencias.bib`, `informe/main.pdf`: informe editable y PDF.
- `entrega-sga.tex`, [entrega-sga.pdf](entrega-sga.pdf): documento separado de una página que contiene únicamente la URL completa del repositorio en una sola línea, por indicación del estudiante. Generarlo no equivale a entregarlo en el SGA.
- `compose.yaml`: tres nodos Kafka 3.9.1 con imagen fijada por SHA-256, red interna y volúmenes persistentes.
- `scripts/experimento.py`: experimento real con verificaciones de mensajes.
- `experimento/resultados/`: comandos, entradas, salidas, códigos y resultados de ejecuciones reales. Los JSON declaran el operador.
- `fuentes/`: documentación técnica, cotejo de DOI, guía de lectura y dos artículos originales CC BY 4.0 en `fuentes/textos/`.
- `evidencia/`: instrucciones para incorporar evidencias originales. No contiene capturas personales fabricadas.
- `BITACORA.md`: registro honesto de la sesión asistida y plantilla para las sesiones personales.
- `PENDIENTES.md`: requisitos que impiden considerar el trabajo listo para entrega.
- `SUSTENTACION.md`: guía de explicación técnica y preparación del video, y cómo registrar tu siguiente commit.

## Requisitos

Docker Engine y Docker Compose v2, Python 3.10 o posterior y Git. Espacio para una imagen TeX y Kafka; la primera construcción descarga paquetes Debian. No se requieren credenciales de Kafka ni puertos públicos. El montaje PLAINTEXT está aislado en la red Docker: es un laboratorio, no una configuración de producción.

### Compilar el informe

Desde la raíz del repositorio:

```sh
./scripts/compilar.sh
```

El script construye `ta-ind-tex:trixie` desde `.environment/Dockerfile.tex` si falta. Usa **pdfLaTeX**, archivo principal `informe/main.tex`, y ejecuta exactamente:

```sh
cd informe
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
pdflatex -interaction=nonstopmode -halt-on-error entrega-sga.tex
```

Con herramientas instaladas localmente también se puede ejecutar ese orden sin Docker. Dependencias: `texlive-latex-extra`, `texlive-lang-spanish`, `texlive-bibtex-extra` (incluye `biblatex` e IEEE), `texlive-fonts-recommended`, `biber`, `lmodern`. Se usan TikZ, babel, csquotes, graphicx, booktabs, longtable, array, geometry, hyperref y fancyhdr.

### Iniciar Kafka y ejecutar la prueba

```sh
docker compose up -d --wait --wait-timeout 180
python3 scripts/experimento.py --operador estudiante --pausas
```

La opción `estudiante` solo corresponde si tú ejecutas, observas y comprendes la prueba. El script hace pausas para tomar cuatro capturas, mostrando el usuario y hostname reales y la fecha UTC. No crea capturas automáticamente. Explica después los resultados con tus propias palabras.

Para una validación automatizada asistida, sin atribuir la ejecución al estudiante:

```sh
python3 scripts/experimento.py --operador asistente-IA
```

El experimento crea tópicos únicos; no elimina datos de sesiones anteriores. Produce diez mensajes por fase y tópico, detiene el líder del tópico ISR2, espera ISR2, contrasta aceptación y rechazo, recupera el nodo y compara el contenido completo. Un `PASS` exige 30 mensajes para ISR2 y 20 para ISR3, sin faltantes, extras ni duplicados, y un error explícito `NotEnoughReplicas` durante la fase de rechazo.

La CLI productora puede salir con código cero aunque no entregue; el script comprueba su salida y el consumo. El resultado **no demuestra** comportamiento ante partición de red, pérdida física de discos ni una garantía universal de procesamiento exactamente una vez.

Los brokers configuran explícitamente `KAFKA_LOG_DIRS=/tmp/kafka-logs`, ubicado en el volumen de cada nodo. Para comprobar conservación de los conjuntos de mensajes tras recrear los contenedores del proyecto (reinicia el laboratorio):

```sh
python3 scripts/verificar_persistencia.py --recrear
```

Conserva `experimento/persistencia.json`. No ejecutar durante una sesión de capturas.

Para detener el laboratorio conservando datos:

```sh
docker compose stop
```

Los procesos deben reiniciarse en una nueva sesión. `docker compose up -d --wait` es idempotente respecto a servicios y volúmenes; cada experimento agrega tópicos. No ejecutar `down -v` si necesitas conservar los datos.

### Verificar las fuentes

```sh
python3 scripts/verificar_fuentes.py
```

Guarda `fuentes/verificacion-doi.json`. El código 0 indica que los metadatos completos y la redirección inicial de cada DOI coinciden con el recurso editorial registrado en Crossref. Un error de consulta o una discrepancia impide ese resultado. El acceso posterior a la editorial se registra por separado: un 202 o 403 no acredita lectura integral ni invalida por sí solo un registro bibliográfico coincidente.

**Estado actual:** cinco referencias cotejadas sin discrepancias; las cinco redirecciones DOI coinciden con sus registros. `fuentes/indexacion.json` corrobora las tres revistas mediante IEEE y SCImago/Scopus. `fuentes/LECTURAS.md` identifica los tres manuscritos abiertos consultados y sus páginas. Se obtuvieron también las dos versiones editoriales completas de Raptis en Zenodo, con licencia CC BY 4.0 y checksums coincidentes; se incluyen con atribución en `fuentes/textos/`. Sigue pendiente la lectura personal del estudiante.

Las fuentes complementarias incluyen el testimonio de uso de Grab publicado por Apache Kafka y el reporte público kafka-go #1358, con límites y cronología explícitos. No reemplazan los tres artículos de revista requeridos.

## Evidencias y sustentación

Sigue `evidencia/README.md`. **Video de sustentación: PENDIENTE.** Sustituir este estado por enlace real de YouTube no listado o Drive con acceso de lectura. No se ha grabado ni publicado un video en nombre del estudiante.

## Historia y autoría

El contenido inicial fue preparado y validado con asistencia de Codex/ChatGPT. No debe presentarse como redacción o experimentación independiente. El informe declara esta intervención. No se inventaron sesiones, commits retrofechados, experiencias personales, capturas ni fuentes nuevas.

El requisito de ocho commits en tres días necesita trabajo real del estudiante. No se cumple dividiendo este borrador artificialmente en ocho commits. Registra avances reales: elección y alcance, lecturas verificadas, bosquejo, ejecución personal, interpretación, comparación, revisión bibliográfica y comprobación de entrega. Si no hay tres días disponibles, consultar al docente sobre el requisito; no falsear fechas.

## Commits autorizados

El estudiante autorizó registrar esta continuación con la identidad ya configurada en Git y sin trailers `Co-authored-by`. Los commits anteriores conservan sus autores. La asistencia y las ejecuciones automatizadas siguen declaradas en el informe y la bitácora; el commit no acredita por sí solo experimentación, lectura o redacción independiente. La publicación del entorno y la entrega en SGA son acciones distintas.

## Control previo de archivos

Desde la raíz, con Python, Git y Poppler (`pdfinfo` y `pdftotext`) disponibles:

```sh
python3 scripts/comprobar_entrega.py
```

Guarda `revision-entrega.json`. Comprueba página y URL del PDF SGA, extensión del informe, resumen, configuración IEEE/Biber, claves citadas, artículos candidatos y archivos de evidencia. El código 2 significa que quedan requisitos pendientes; no es un fallo inesperado del programa. Los conteos no acreditan autoría ni indexación. La revisión de DOI continúa separada. Cuando pasen los controles automáticos todavía hace falta confirmación humana final.

## Estado actual de red

El estudiante publicó un nuevo entorno con acceso a Internet sin restricciones. Crossref y el resolvedor DOI están accesibles. Algunas editoriales y repositorios todavía limitan solicitudes automatizadas, y sus respuestas quedan documentadas por fuente. No se desactivaron TLS ni controles de integridad. Los cambios actuales del trabajo no requieren volver a publicar el entorno.

## Incorporar las evidencias reales al PDF

El LaTeX ya incluye automáticamente estos archivos cuando existen:

- `evidencia/ejecucion/01-base.png`, `02-fallo.png`, `03-contraste.png`, `04-recuperacion.png`.
- `evidencia/bosquejo/arquitectura-inicial.jpg`.
- `evidencia/lecturas/01-raptis2023.png`, `02-raptis2024.png`, `03-henning2024.png`.

Sigue `evidencia/lecturas/PLANTILLA.md` para las páginas y citas propuestas. Después de añadir originales, ejecuta `./scripts/compilar.sh` y revisa orden, legibilidad, pies e interpretación. Ajusta los pies si eliges otro pasaje. Las advertencias de pendiente se retiran solo al comprobar el requisito completo; añadir archivos no verifica automáticamente su autoría ni cumple el video o el historial.

## Versión solicitada sin capturas

El estudiante pidió continuar sin capturas de pantalla. Se ejecutó el laboratorio automáticamente y se incorporó una cuarta corrida real PASS con 30 registros conservados en el tópico ISR2 y 20 en ISR3, rechazo explícito durante el fallo y recuperación del nodo. El detalle está en `experimento/ULTIMA-EJECUCION.md` y sus archivos originales enlazados.

Se entregan análisis, fuentes, comandos, resultados, LaTeX, PDF y documento de una página para el SGA. Esta versión no incluye capturas de ejecución ni lecturas anotadas. No reemplazan esa evidencia los archivos textuales: la consigna exige capturas y asocia la ausencia de la evidencia 1 a D3=0. La fotografía del bosquejo, el video y las confirmaciones personales/administrativas tampoco se declaran realizados. Se conserva el estado de borrador y los pendientes, sin simular su cumplimiento.
