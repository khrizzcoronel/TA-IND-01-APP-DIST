# TA-IND-01 — Kafka frente a RabbitMQ

**Estado: borrador asistido por IA. No es una entrega académica terminada.**

Estudiante: Khriz Alexander Coronel Gómez · Aplicaciones Distribuidas (ISR-701), UTEQ · Séptimo A.

Pregunta: ¿cómo afectan la replicación y el mínimo ISR a la conservación de mensajes y a la disponibilidad de escritura cuando falla un broker de Kafka?

## Archivos

- `informe/main.tex`, `informe/referencias.bib`, `informe/main.pdf`: informe editable y PDF.
- `entrega-sga.tex`, `entrega-sga.pdf`: documento separado de una página para el SGA. No subirlo hasta completar los requisitos.
- `compose.yaml`: tres nodos Kafka 3.9.1 con imagen fijada por SHA-256, red interna y volúmenes persistentes.
- `scripts/experimento.py`: experimento real con verificaciones de mensajes.
- `experimento/resultados/`: comandos, entradas, salidas, códigos y resultados de ejecuciones reales. Los JSON declaran el operador.
- `fuentes/`: documentación técnica consultada, procedencia y estado de verificación de DOI.
- `evidencia/`: instrucciones para incorporar evidencias originales. No contiene capturas personales fabricadas.
- `BITACORA.md`: registro honesto de la sesión asistida y plantilla para las sesiones personales.
- `PENDIENTES.md`: requisitos que impiden considerar el trabajo listo para entrega.

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

Para detener el laboratorio conservando datos:

```sh
docker compose stop
```

Los procesos deben reiniciarse en una nueva sesión. `docker compose up -d --wait` es idempotente respecto a servicios y volúmenes; cada experimento agrega tópicos. No ejecutar `down -v` si necesitas conservar los datos.

### Verificar las fuentes

```sh
python3 scripts/verificar_fuentes.py
```

Guarda `fuentes/verificacion-doi.json`; un bloqueo o discrepancia produce código distinto de cero. Completar después revisión manual de cada DOI y datos editoriales, indexación y lectura. Los cinco artículos proceden de las fichas previas: su presencia no equivale a verificación en esta sesión. No entregar ninguna referencia sin comprobar.

Dominios requeridos adicionales a los gestores de paquetes: `api.crossref.org`, `doi.org`, `kafka.apache.org`, `www.rabbitmq.com`, `iris.cnr.it`, `arxiv.org`, `eprints.soton.ac.uk`, `ieeexplore.ieee.org`, `www.sciencedirect.com`, `dl.acm.org`. La configuración guardada debe aplicarse antes de reintentar los accesos bloqueados. La documentación oficial incluida sí se recuperó desde GitHub, con versión o commit identificado.

## Evidencias y sustentación

Sigue `evidencia/README.md`. **Video de sustentación: PENDIENTE.** Sustituir este estado por enlace real de YouTube no listado o Drive con acceso de lectura. No se ha grabado ni publicado un video en nombre del estudiante.

## Historia y autoría

El contenido inicial fue preparado y validado con asistencia de Codex/ChatGPT. No debe presentarse como redacción o experimentación independiente. El informe declara esta intervención. No se inventaron sesiones, commits retrofechados, experiencias personales, capturas ni fuentes nuevas.

El requisito de ocho commits en tres días necesita trabajo real del estudiante. No se cumple dividiendo este borrador artificialmente en ocho commits. Registra avances reales: elección y alcance, lecturas verificadas, bosquejo, ejecución personal, interpretación, comparación, revisión bibliográfica y comprobación de entrega. Si no hay tres días disponibles, consultar al docente sobre el requisito; no falsear fechas.
