# Fuentes: lo comprobado y lo pendiente

## Identidad bibliográfica

Los cinco registros con DOI se cotejaron con Crossref: título, nombres completos y orden de autores, publicación, tipo de artículo, año, volumen, fascículo y páginas/eid. Los cinco resolvieron con HTTP 302 al recurso editorial registrado. Ver `verificacion-doi.json`.

Esto prueba identidad bibliográfica por cotejo, no acceso integral al artículo. IEEE respondió 202; ACM y algunos destinos de Elsevier limitaron la consulta automática. No se desactivó TLS ni se usaron credenciales o rutas de evasión.

## Manuscritos consultados por el asistente

Los PDF se conservan fuera del repositorio, en `/workspace/lecturas-ta-ind/`. Los enlaces públicos permiten que el estudiante los descargue y lea. Se citan las publicaciones editoriales; las localizaciones siguientes corresponden a los manuscritos indicados.

| Artículo | Versión de lectura | Localización | Qué respalda y qué no |
|---|---|---|---|
| Henning y Hasselbring, JSS 2024, DOI 10.1016/j.jss.2023.111879 | [2303.11088v2](https://arxiv.org/pdf/2303.11088v2) | Página PDF 1, abstract | Comparación de escalabilidad y dependencia de recursos. El estudio abarca más de 740 horas y hasta 110 instancias; no es una medida del laboratorio de tres brokers. |
| Vogel et al., DEBS 2024, DOI 10.1145/3629104.3666040 | [2404.06203v3](https://arxiv.org/pdf/2404.06203v3) | Página PDF 4, secciones 4.2 y 5.2 | Versión Kafka Streams 3.5 e inyección de fallos sobre 1, 2 o 4 workers cada cinco minutos. No prueba el mismo comportamiento para caída de brokers. |
| Chen et al., ICPE Companion 2026, DOI 10.1145/3777911.3800636 | [2603.04027v1](https://arxiv.org/pdf/2603.04027v1) | Página PDF 4, sección 4.2.2; página PDF 5, sección 4.3 | Evaluación piloto de configuración, mejora aproximada del 23 % y discusión de latencia. No es mejora garantizada para cualquier versión, carga o aplicación. |

`lecturas-consultadas.json` registra las versiones, DOI editoriales y hashes de los archivos descargados. El asistente revisó los pasajes que respaldan el informe; no se atribuye al estudiante la lectura ni se afirma una revisión exhaustiva de cada resultado del artículo.

## Dos versiones editoriales recuperadas en Zenodo

| Artículo | Copia disponible | Pasajes consultados y límites |
|---|---|---|
| Raptis y Passarella, IEEE Access 2023, DOI 10.1109/ACCESS.2023.3303810 | [PDF](textos/raptis2023.pdf), [depósito](https://zenodo.org/records/8300814) | Abstract p. 85333, arquitectura y modelo de consumo p. 85336, conclusión p. 85348. La taxonomía organiza el tema; para el protocolo concreto se contrasta la afirmación push/pull con Fetch en la documentación 3.9.1. |
| Raptis, Cicconetti y Passarella, FGCS 2024, DOI 10.1016/j.future.2023.12.028 | [PDF](textos/raptis2024.pdf), [depósito](https://zenodo.org/records/10489464) | Secciones 2.1–3.3, pp. 174–177; mensajes de evaluación y conclusión p. 186. Distinguir supuestos, simulación, prototipo y aplicación real. El modelo supone un grupo de consumidores. |

Las copias son originales sin anotaciones del asistente. Coinciden con los checksums MD5 publicados por Zenodo y se registró además su SHA-256; los DOI del texto coinciden con los editoriales. Ambos trabajos tienen licencia CC BY 4.0, con atribución y procedencia conservadas en `textos/README.md`.

El asistente consultó los pasajes que fundamentan el informe. Obtener el texto íntegro no acredita que el estudiante lo haya leído ni sustituye su lectura y anotación personal.

## Indexación

`indexacion.json` documenta IEEE Access mediante su página editorial, que enumera Scopus y Web of Science. FGCS y JSS se corroboran mediante sus fichas SCImago, cuya metodología declara datos Scopus. Es una fuente secundaria, no acceso al catálogo de suscripción de Scopus ni una comprobación directa de Web of Science para esas dos revistas.

## Evidencia personal que debe producir el estudiante

Leer tres artículos citados, escoger pasajes vinculados a afirmaciones del informe, anotarlos y obtener capturas propias donde se identifique la página. Las cinco copias identificadas arriba permiten preparar esas lecturas; no se han creado capturas para simular que el estudiante ya las hizo.
