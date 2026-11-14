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

## Plantilla para cada sesión real del estudiante

- Fecha y horario (zona horaria):
- Duración real:
- Qué hice y qué comprendí:
- Problema encontrado:
- Cómo lo resolví y cómo lo comprobé:
- Archivos y commit correspondientes:
- Herramientas de IA usadas y revisión realizada:
