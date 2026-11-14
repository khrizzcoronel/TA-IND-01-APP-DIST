# Bitácora de trabajo

Las fechas describen sesiones reales. Esta entrada no acredita días previos del estudiante.

## 2026-11-13 — Sesión asistida (America/Guayaquil)

- **Operador:** asistente Codex/ChatGPT, por solicitud del estudiante.
- **Qué se hizo:** revisión de repositorios formativos; preparación del clúster Kafka 3.9.1, scripts, borrador LaTeX y documento SGA; ejecución automatizada y compilación con pdfLaTeX/Biber.
- **Problemas:** Crossref y páginas editoriales bloqueados por HTTP 403; paquetes TeX/Biber ausentes en el host; incompatibilidad inicial de caracteres activos de babel con TikZ.
- **Revisión de persistencia:** se corrigió el montaje del directorio real de Kafka, migrando los datos existentes; se recrearon los contenedores y se verificó conservación de seis tópicos.
- **Soluciones:** se guardaron dominios requeridos en la configuración, se consultó documentación oficial versionada en GitHub, se construyó un contenedor TeX y se activó la biblioteca babel de TikZ. La verificación de artículos permanece pendiente.
- **Tiempo instrumentado:** 257.804 segundos sumados de los comandos de las tres pruebas (no incluye edición, preparación ni esperas entre comandos). Corridas iniciadas a las 00:33:13, 00:38:07 y 00:44:32 UTC del 14 de noviembre, correspondientes al 13 de noviembre en America/Guayaquil. No se atribuye ese tiempo a trabajo personal del estudiante.
- **Evidencia:** logs y JSON de `experimento/resultados/`; PDF compilado; verificación DOI registra el bloqueo.
- **Límite de autoría:** no se han producido capturas personales, bosquejo a mano, experiencias personales ni video; no se han inventado días o commits del estudiante.

### Continuación de la revisión — misma fecha local

- **Operador de los cambios:** asistente Codex/ChatGPT; el estudiante solicitó ejemplos generales y reservó el siguiente commit para sí mismo.
- **Avances:** se documentó uso de Kafka por Grab a escala TB/hour mediante el sitio oficial versionado, y se analizó el reporte kafka-go #1358 diferenciando impacto declarado, diagnóstico de un participante y recuperación no confirmada. Se corroboró el tratamiento de Transport en el código de la versión 0.4.47.
- **Redacción:** se incorporaron tres corridas reales y verificación de persistencia al informe; se escribieron escenarios ilustrativos de WhatsApp y SGA, claramente pendientes de vincular con experiencias personales.
- **Verificación:** se recompiló con pdfLaTeX/Biber; el PDF pasó a once páginas. Crossref y la página candidata de Cloudflare siguen bloqueados por HTTP 403; no se inventó su lectura.
- **Tiempo:** la compilación limpia final duró 19,09 segundos medidos; no se midió la duración total de la interacción ni se asigna una duración ficticia al estudiante.
- **Commit:** cambios locales sin commit ni push, por instrucción expresa del estudiante. Debe registrar su revisión y lo que verificó realmente antes de hacer su commit.

### Control de entrega y acceso de red — misma fecha local

- El asistente comprobó que los dominios están guardados en el borrador pero no activos en la máquina; la consulta de DOI aún devuelve HTTP 403.
- Se añadieron instrucciones de aplicación en ajustes y un control de los archivos de entrega; verificó ocho condiciones de formato/estructura y mantuvo pendientes los requisitos sin evidencia.
- Se marcó como completada la recompilación limpia ya ejecutada; las evidencias de lectura y autoría siguen pendientes.
- Cambios sin commit ni push, para revisión y commit real del estudiante. No se midió duración total ni se inventaron días adicionales de trabajo.

### Verificación bibliográfica con acceso habilitado — misma fecha local

- **Operador:** asistente Codex/ChatGPT, por solicitud de continuar del estudiante.
- **Avances:** cotejo de los cinco DOI con Crossref, incluyendo nombres completos y destinos de redirección. Los cinco coinciden; se separó ese resultado de los límites de acceso editorial.
- **Lectura asistida:** consulta de tres manuscritos de autores y revisión de los pasajes que fundamentan las afirmaciones incorporadas. No se atribuye lectura personal al estudiante. Quedan dos textos completos pendientes.
- **Indexación:** IEEE Access corroborada por editorial; FGCS y JSS mediante SCImago con datos Scopus. Se documenta que esa última comprobación es secundaria.
- **Verificación:** informe compilado de doce páginas, resumen de 170 palabras y control de entrega con diez condiciones PASS y seis grupos pendientes.
- **Problemas restantes:** algunas editoriales limitan solicitudes automatizadas; faltan las evidencias originales y requisitos administrativos.
- **Commit:** el estudiante autorizó ahora hacer el commit con la identidad Git configurada, sin trailers de coautoría. Se registran cambios reales; no se alteran fechas ni autores anteriores.
- **Tiempo:** no se midió la duración total de esta revisión; no se inventa dedicación personal del estudiante.

## Plantilla para cada sesión real del estudiante

- Fecha y horario (zona horaria):
- Duración real:
- Qué hice y qué comprendí:
- Problema encontrado:
- Cómo lo resolví y cómo lo comprobé:
- Archivos y commit correspondientes:
- Herramientas de IA usadas y revisión realizada:
