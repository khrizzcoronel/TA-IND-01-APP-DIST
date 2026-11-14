# Validación técnica del borrador

Operador: Codex/ChatGPT, no atribuido al estudiante.

## Laboratorio

| Corrida UTC | Resultado | Mensajes ISR2 | Mensajes ISR3 | Broker detenido |
|---|---|---|---|---|
| `20261114T003313Z` | PASS | 30 | 20 | kafka3 |
| `20261114T003807Z` | PASS | 30 | 20 | kafka1 |

En ambas corridas se comparó el contenido completo y su multiplicidad, se observó rechazo `NotEnoughReplicasException` en ISR3 durante el fallo y se restauró ISR=3. Los tópicos tienen identificadores únicos, por lo que la segunda corrida también comprueba repetición sin borrar el estado anterior. Logs y comandos completos están en cada carpeta de resultados. Los tres servicios quedaron activos y saludables.

## Compilación

- Imagen TeX construida con Debian trixie, pdfLaTeX y Biber.
- Compilación completa satisfactoria desde copia de fuentes sin PDFs ni auxiliares. También se compiló desde un clon Git local independiente (`git clone --no-local`), sin depender del estado auxiliar del checkout original. Orden: pdfLaTeX, Biber, pdfLaTeX, pdfLaTeX.
- `informe/main.pdf`: nueve páginas totales; al menos seis páginas enteras de contenido antes de que empiecen las referencias, excluyendo la carátula. Conserva pendientes explícitos.
- Resumen: 170 palabras según separación por espacios.
- `entrega-sga.pdf`: una página A4. Se extrajo la URL íntegra como un único elemento con `pdftotext -bbox`: no está partida en varias líneas.
- Revisión visual del diagrama y su página: legibles, sin recortes.
- No se afirma validación académica final por estas comprobaciones de formato.

## Fuentes

Se recuperaron cuatro documentos técnicos oficiales de GitHub, fijados por tag de Kafka y commit de RabbitMQ; `fuentes/documentacion.json` registra procedencia y SHA-256. Las cinco referencias académicas proceden de FORM-FB-01; su verificación automatizada en esta sesión devolvió HTTP 403. Ver `fuentes/verificacion-doi.json`. Bloqueado no significa verificado.

## Estado del entorno y límites

Se guardaron `install_script`, `start_skill` y los dominios adicionales de red en el borrador del entorno. Guardar no aplica las reglas de red ni publica la configuración; las consultas de DOI siguieron bloqueadas. No se necesitan secretos nuevos para Kafka ni para compilar.

No se accedió al SGA ni se entregó el trabajo. No se fabricaron evidencias personales, un incidente de producción, lecturas, video o días previos. Ver `PENDIENTES.md`.
