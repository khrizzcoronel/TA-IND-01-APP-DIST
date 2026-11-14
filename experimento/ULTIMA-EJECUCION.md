# Última ejecución real: sin capturas

- **Corrida UTC:** `20261114T022648Z`.
- **Fecha local:** 2026-11-13 21:26:48 -05 (America/Guayaquil).
- **Operador:** `asistente-IA`; no se atribuye al estudiante.
- **Versión:** Apache Kafka 3.9.1; tres nodos combinados broker/controlador.
- **Broker detenido:** `kafka3`.
- **Resultado:** **PASS**.
- **Capturas:** ninguna; el estudiante solicitó omitirlas.

## Comando ejecutado

```sh
python3 scripts/experimento.py --operador asistente-IA
```

## Resultados observados

| Fase | Registros conservados en ISR2 | Registros conservados en ISR3 |
|---|---:|---:|
| Inicial | 10 | 10 |
| Durante el fallo | 10 | 0 |
| Tras recuperar el nodo | 10 | 10 |
| Total | 30 | 20 |

Con mínimo ISR2, el productor pudo escribir durante el fallo. Con mínimo ISR3, la consola registró `NotEnoughReplicasException`; los intentos rechazados no aparecen como mensajes aceptados. Al volver el nodo se esperó ISR3 y se pudieron escribir los mensajes de recuperación. Se compararon valores y multiplicidades, no solo cantidades.

## Registros completos

- [Resumen verificable](resultados/20261114T022648Z/resumen.json).
- [Comandos, entradas, salidas, códigos y tiempos](resultados/20261114T022648Z/comandos.json).
- [Transcripción de terminal](resultados/20261114T022648Z/terminal.log).

Los tiempos de comandos incluyen inicio de CLI y esperas; no son latencias individuales de mensaje. La caída de un proceso no demuestra una partición de red. La prueba actual comprueba recuperación de un nodo; la comprobación anterior de recreación está fechada por separado en `persistencia.json`.

## Límite de la entrega

Los registros son reales y permiten revisar la prueba, pero no reemplazan las cuatro capturas originales que pide la consigna ni demuestran ejecución personal. No se generaron imágenes ni se cambiaron identificadores para simular evidencias.
