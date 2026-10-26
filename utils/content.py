"""Contenido estructurado del dashboard.

Fuentes:
- Propuesta de tesis: "Modelo de Optimización Robusta Distribucional (DRO) con
  Aprendizaje por Refuerzo (RL) y Conformal Prediction (CP) para la Programación
  Operativa de Sistemas Eléctricos con Alta Penetración de Fuentes de Energía
  Renovable" — Carlos Manuel Romero Rojas (82 pp).
- Concepto del jurado: Camilo Andrés Cortés Guerrero (5 pp).
"""
from __future__ import annotations

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Ficha de la tesis
# ---------------------------------------------------------------------------
TESIS = {
    "titulo": (
        "Modelo de Optimización Robusta Distribucional (DRO) con Aprendizaje por "
        "Refuerzo (RL) y Conformal Prediction (CP) para la Programación Operativa "
        "de Sistemas Eléctricos con Alta Penetración de Fuentes de Energía Renovable"
    ),
    "corto": "DRO + RL + CP para programación operativa con alta penetración renovable",
    "proponente": "Carlos Manuel Romero Rojas",
    "identificacion": "CC 1.023.902.292",
    "programa": "Doctorado en Ingeniería Eléctrica — Universidad Nacional de Colombia",
    "director": "Sergio Raúl Rivera Rodríguez, PhD (UNAL — Depto. de Ingeniería Eléctrica y Electrónica)",
    "codirector": "Eduardo Alirio Mojica Nava, PhD (UNAL — Depto. de Ingeniería Eléctrica y Electrónica)",
    "linea": "Sistemas de potencia",
    "jurado": "Camilo Andrés Cortés Guerrero, PhD — Universidad Nacional de Colombia",
    "normativa": "Acuerdo 104 de 2020, artículos 38 al 42",
}

# ---------------------------------------------------------------------------
# 2. Evaluación del jurado (criterio, calificación, observación textual)
#    Escala: 1=Insuficiente  2=Aceptable  3=Bueno  4=Excelente
# ---------------------------------------------------------------------------
SCORE_LABELS = {1: "Insuficiente", 2: "Aceptable", 3: "Bueno", 4: "Excelente"}

JURY_EVAL = [
    {
        "id": "introduccion",
        "componente": "Introducción",
        "criterio": (
            "La introducción permite enmarcar el tema del trabajo, desde lo general a lo "
            "específico, y permite llegar al planteamiento del problema que se quiere resolver."
        ),
        "score": 3,
        "observacion": (
            "Contextualiza adecuadamente el tema y presenta las técnicas propuestas. Sin embargo, "
            "debe delimitar mejor el alcance, pues mezcla programación del día siguiente con "
            "operación en tiempo real. También anticipa beneficios de optimalidad, rapidez y "
            "factibilidad que deben plantearse como resultados por demostrar."
        ),
    },
    {
        "id": "antecedentes",
        "componente": "Antecedentes",
        "criterio": (
            "Descripción del estado del arte (trabajos previos) y elementos de contexto que "
            "constituyen el soporte de las problemáticas expuestas."
        ),
        "score": 3,
        "observacion": (
            "Incluye literatura amplia y pertinente, pero predomina la enumeración de aplicaciones "
            "sobre la comparación crítica de sus aportes y limitaciones. Se requiere identificar con "
            "mayor precisión la brecha científica. El marco teórico es excesivamente extenso y se "
            "apoya en solo tres fuentes distintas; conviene reducirlo y fortalecer su relación con "
            "la propuesta."
        ),
    },
    {
        "id": "problema",
        "componente": "Planteamiento del Problema",
        "criterio": (
            "Describe las causas, las consecuencias del problema y el problema mismo. "
            "Presenta la pregunta de investigación."
        ),
        "score": 3,
        "observacion": (
            "Identifica una problemática relevante, pero se concentra en la ausencia de integración "
            "de técnicas sin precisar suficientemente la limitación operativa o científica que se "
            "resolverá. Debe delimitar el horizonte de decisión, las incertidumbres consideradas y "
            "el significado medible de «calidad de las decisiones»."
        ),
    },
    {
        "id": "justificacion",
        "componente": "Justificación",
        "criterio": (
            "Describe claramente las razones por las cuales es importante solucionar el problema, "
            "incluyendo el aporte a la disciplina."
        ),
        "score": 2,
        "observacion": (
            "Reitera argumentos del problema y los antecedentes, sin desarrollar suficientemente el "
            "aporte a la disciplina. Debe explicar qué conocimiento nuevo producirá la investigación "
            "y por qué es necesario integrar las técnicas propuestas. La ausencia de una combinación "
            "idéntica en la literatura no basta para sustentar la contribución doctoral."
        ),
    },
    {
        "id": "objetivos",
        "componente": "Objetivos",
        "criterio": (
            "Son claros, medibles y alcanzables; están claramente relacionados con el "
            "planteamiento del problema y con la pregunta de investigación."
        ),
        "score": 3,
        "observacion": (
            "Son comprensibles, pero presentan desajustes con la hipótesis y el diseño. La "
            "incertidumbre de demanda no aparece consistentemente y los comparadores cambian entre "
            "apartados. Deben unificarse el alcance y los criterios de evaluación, además de mantener "
            "una terminología uniforme en español e inglés."
        ),
    },
    {
        "id": "diseno",
        "componente": "Diseño de la investigación",
        "criterio": (
            "Describe clara y detalladamente el plan general que se realizará para responder a la "
            "pregunta de investigación y alcanzar los objetivos propuestos."
        ),
        "score": 1,
        "observacion": (
            "Identifica herramientas y un enfoque cuantitativo, pero no desarrolla un procedimiento "
            "reproducible. Debe precisar la formulación operativa, la representación del agente, la "
            "integración CP–DRO–RL y el protocolo experimental."
        ),
    },
    {
        "id": "actividades",
        "componente": "Actividades a desarrollar",
        "criterio": (
            "Describe las actividades a desarrollar con base en el diseño de la investigación, de "
            "forma acorde con los objetivos y el diseño de la investigación."
        ),
        "score": 1,
        "observacion": (
            "Se relacionan con los objetivos, pero son demasiado generales para valorar su ejecución "
            "y cumplimiento. Deben desagregarse las tareas de calibración, integración y validación, "
            "indicando productos verificables. Es necesario establecer actividades explícitas para "
            "comprobar restricciones, comparar métodos y evaluar la contribución de cada técnica."
        ),
    },
    {
        "id": "cronograma",
        "componente": "Cronograma",
        "criterio": (
            "Presenta el cronograma de desarrollo de las actividades con base en el diseño de la "
            "investigación propuesto y en el alcance de la tesis."
        ),
        "score": 2,
        "observacion": (
            "El horizonte de 48 meses no permite identificar el avance actual ni el tiempo restante "
            "para concluir la investigación. Debe distinguir actividades realizadas, en curso y "
            "pendientes, e incorporar hitos de validación, escritura y sustentación. También debe "
            "corregirse la referencia a «Tesis de Maestría» conservada en el encabezado."
        ),
    },
    {
        "id": "presupuesto",
        "componente": "Presupuesto y fuentes de financiación",
        "criterio": "Presenta el presupuesto acorde con las actividades propuestas.",
        "score": 2,
        "observacion": (
            "El aporte universitario de $15 millones para congresos debe respaldarse mediante una "
            "fuente de financiación identificada. Si no está aprobado, debe registrarse como "
            "financiación por gestionar y no como recurso asegurado. Se recomienda justificar los "
            "rubros y diferenciar aportes confirmados, recursos en especie y apoyos esperados."
        ),
    },
    {
        "id": "redaccion",
        "componente": "Presentación y redacción",
        "criterio": (
            "El documento se presenta de manera clara y ordenada, sin faltas ortográficas ni "
            "gramaticales."
        ),
        "score": 2,
        "observacion": (
            "Conserva instrucciones de plantilla, referencias a maestría y términos utilizados "
            "indistintamente en español e inglés. Requiere corregir errores de redacción y uniformar "
            "la numeración de las ecuaciones centrales. También debe verificarse la coherencia entre "
            "expresiones matemáticas, tablas y resultados, no solo la presentación editorial."
        ),
    },
    {
        "id": "bibliografia",
        "componente": "Bibliografía",
        "criterio": (
            "Las fuentes bibliográficas consultadas son pertinentes, actuales y son citadas "
            "correctamente."
        ),
        "score": 3,
        "observacion": (
            "Las 72 entradas ofrecen una base amplia y reciente, pero el marco teórico depende de "
            "solo tres fuentes distintas. La cantidad de referencias no sustituye su análisis crítico."
        ),
    },
]

# ---------------------------------------------------------------------------
# 3. Respuestas didácticas + plan de acción por observación
# ---------------------------------------------------------------------------
JURY_RESPONSES = {
    "introduccion": {
        "interpretacion": (
            "La introducción «enmarca bien», pero el jurado detecta ambigüedad de alcance: la "
            "propuesta describe dos escalas de decisión (día siguiente e intradía/tiempo real) sin "
            "jerarquizarlas, y presenta ventajas (optimalidad, rapidez, factibilidad) como hechos "
            "cuando, en una tesis doctoral, son hipótesis que deben probarse."
        ),
        "respuesta": [
            "**Delimitación formal del alcance (2 escalas, 1 objetivo).** Horizonte primario = "
            "programación del día siguiente (compromiso de unidades + despacho horario, 24 pasos) "
            "resuelta con DRO. Horizonte de ajuste = re-dispacho intradía cada 15 min (96 pasos) "
            "ejecutado por la política RL. La operación en tiempo real (AGC/EMS) queda "
            "**explícitamente fuera de alcance** y se declara en un cuadro «dentro / fuera».",
            "**Beneficios reformulados como hipótesis H1–H3** con métrica, umbral de éxito y método "
            "de prueba declarados antes de los experimentos (ver página «Problema e Hipótesis»).",
            "**Coherencia de tiempos:** cada técnica se asigna a la escala donde aporta (DRO → "
            "decisiones aquí-y-ahora con garantías; RL → decisiones frecuentes con costo "
            "computacional marginal).",
        ],
        "acciones": [
            {"texto": "Cuadro de alcance (dentro/fuera) en §Introducción", "estado": "En curso"},
            {"texto": "Tabla de hipótesis verificables H1–H3 con métricas y umbrales", "estado": "Hecho"},
            {"texto": "Reescritura de la última parte de la Introducción (beneficios → hipótesis)", "estado": "En curso"},
        ],
        "productos": ["§1.1 Alcance y delimitación", "Tabla H1–H3", "Diagrama de escalas temporales"],
    },
    "antecedentes": {
        "interpretacion": (
            "Una revisión de literatura doctoral debe comparar y juzgar, no solo listar. Además, un "
            "marco teórico de 56 páginas sostenido en 3 fuentes desbalancea el documento: la "
            "profundidad teórica debe estar al servicio de la propuesta, no ser una enciclopedia."
        ),
        "respuesta": [
            "**Matriz comparativa crítica:** cada trabajo clave se resume en fila "
            "(enfoque, incertidumbre modelada, métrica de ambigüedad, ¿calibra estadísticamente el "
            "radio?, comparadores, métricas, limitación). La enumeración se convierte en análisis.",
            "**Brecha científica explícita y verificable:** ningún trabajo calibra el radio del "
            "conjunto de ambigüedad de Wasserstein con garantías de cobertura finita (CP) dentro de "
            "un marco DRO–RL de programación operativa. La brecha se muestra como vacío en una "
            "matriz técnica × garantía (ver página «Antecedentes y Brecha»).",
            "**Marco teórico recortado:** de 56 a ~18 páginas organizadas en 4 fundamentos "
            "(CP, DRO, Wasserstein, MDP/RL) con **fuentes primarias múltiples por fundamento**; "
            "las demostraciones auxiliares y variantes (p. ej. APS) pasan a anexos.",
        ],
        "acciones": [
            {"texto": "Mapa de brecha científica (matriz técnica × garantía)", "estado": "Hecho"},
            {"texto": "Tabla comparativa crítica de ~20 trabajos cercanos", "estado": "En curso"},
            {"texto": "Recorte del marco teórico (56 → ~18 pp) + traslado a anexos", "estado": "Pendiente"},
            {"texto": "Tabla «afirmación central → fuente primaria» (20 afirmaciones)", "estado": "Pendiente"},
        ],
        "productos": ["Matriz comparativa", "Mapa de brecha", "Marco teórico reducido + anexos"],
    },
    "problema": {
        "interpretacion": (
            "Decir «nadie integra estas técnicas» describe un vacío de literatura, no una limitación "
            "operativa. El jurado pide la limitación concreta que se resolverá, con horizonte, "
            "incertidumbres y una noción medible de «calidad de las decisiones»."
        ),
        "respuesta": [
            "**Limitación que se resuelve:** los operadores carecen de un mecanismo que (i) asigne "
            "parámetros de robustez (radio de ambigüedad) con validez estadística demostrable y "
            "(ii) traduzca ese programa robusto en decisiones ágiles cuando la incertidumbre se "
            "materializa. Hoy: ε se elige ad-hoc (sin garantía) y la re-optimización es demasiado "
            "lenta para el ajuste intradía.",
            "**Horizonte de decisión delimitado:** día siguiente (24 h, pasos horarios) + ajuste "
            "intradía (15 min). Sin tiempo real (AGC).",
            "**Incertidumbres consideradas (vector ξ):** error de pronóstico de generación eólica, "
            "error de pronóstico solar y error de pronóstico de demanda (por nodo/zona). Fallas de "
            "equipos y disponibilidad hidráulica: fuera de alcance declarado.",
            "**«Calidad de las decisiones» = 6 métricas medibles:** costo operativo total, CVaR₉₅ "
            "del costo, tasa de violación de restricciones fuera de muestra, cobertura empírica "
            "(1−α), tiempo de cómputo y holgura de reservas. Cada una con dirección de mejora y "
            "umbral de éxito (H1–H3).",
        ],
        "acciones": [
            {"texto": "Sección «Alcance, horizonte e incertidumbres» con cuadro formal", "estado": "Hecho"},
            {"texto": "Diccionario de métricas de calidad de decisiones (6 KPIs)", "estado": "Hecho"},
            {"texto": "Reformulación del problema en el documento (limitación operativa explícita)", "estado": "En curso"},
        ],
        "productos": ["Cuadro de alcance", "Diccionario de métricas", "Diagrama del vector ξ"],
    },
    "justificacion": {
        "interpretacion": (
            "Es la observación más profunda del concepto: «nadie ha hecho esta combinación» es una "
            "observación de novedad, no una contribución doctoral. El jurado exige nombrar el "
            "conocimiento nuevo y demostrar por qué la integración es necesaria (y no un agregado)."
        ),
        "respuesta": [
            "Reformulamos la contribución en **tres piezas de conocimiento nuevo**, cada una con "
            "pregunta, método de validación y producto:",
            "**(C1) Método de calibración:** un procedimiento CP que convierte el radio ε de la bola "
            "de Wasserstein —hoy un hiperparámetro heurístico— en un parámetro con garantía de "
            "cobertura en muestras finitas. *Conocimiento nuevo: teórico-metodológico.* "
            "Validación: demostración de cobertura + simulación Monte Carlo.",
            "**(C2) Arquitectura de decisión en dos tiempos:** DRO (día siguiente, garantías worst-case) "
            "+ RL (intradía, milisegundos) articulados por el mismo conjunto calibrado, de modo que la "
            "política aprendida opere dentro de la holgura del programa robusto. *Conocimiento nuevo: "
            "arquitectura de decisión.* Validación: protocolo experimental comparativo.",
            "**(C3) Evidencia empírica reproducible:** la región costo–robustez–cobertura del sistema "
            "colombiano (datos XM + IEEE 39) con código y benchmark abiertos. *Conocimiento nuevo: "
            "empírico-recurrente.* Validación: experimentos de ablación C0–C5.",
            "**Por qué la integración es necesaria (no decorativa):** CP sin DRO produce intervalos que "
            "nadie consume en decisiones; DRO sin CP produce robustez sin nivel de confianza; RL sin "
            "DRO produce velocidad sin factibilidad garantizada. La integración cierra exactamente "
            "esas tres carencias. La novedad se mide frente a los trabajos más cercanos "
            "(Cho & Yang 2022 [6]; Li et al. 2023 [7]; Zhu et al. 2025 [18]), no frente a la ausencia "
            "de combinaciones.",
        ],
        "acciones": [
            {"texto": "Reescritura de §Justificación en torno a C1–C3", "estado": "En curso"},
            {"texto": "Tabla de diferenciación vs. 3 trabajos más cercanos", "estado": "Hecho"},
            {"texto": "Preguntas de investigación asociadas a cada contribución", "estado": "Hecho"},
        ],
        "productos": ["§Justificación reformulado", "Tabla de diferenciación", "Mapa C1–C3"],
    },
    "objetivos": {
        "interpretacion": (
            "Los objetivos son comprensibles aislados, pero el jurado encontró tres desajustes de "
            "trazabilidad: la incertidumbre de demanda desaparece en algunos apartados, los "
            "comparadores cambian de nombre entre secciones y la terminología ES/EN se mezcla."
        ),
        "respuesta": [
            "**Matriz única de trazabilidad** (la única fuente de verdad): Objetivo → Pregunta → "
            "Hipótesis → Actividad → Métrica → Comparador. Cualquier mención en el documento debe "
            "referenciar esta matriz.",
            "**OE1 corregido:** la incertidumbre de **demanda** se incorpora explícitamente junto con "
            "solar y eólica («…la generación solar y eólica y la demanda…») en todos los apartados.",
            "**Comparadores fijos C0–C5** en todo el documento (ver «Arquitectura integrada»): "
            "C0 determinista · C1 estocástico · C2 robusto (caja) · C3 DRO-W sin CP · "
            "C4 DRO-W + CP (propuesto) · C5 RL sin capa DRO.",
            "**Glosario ES/EN obligatorio:** un único término por concepto en español con su "
            "equivalente inglés al primer uso (p. ej. programación operativa / operational "
            "scheduling; compromiso de unidades / unit commitment).",
        ],
        "acciones": [
            {"texto": "Matriz de trazabilidad Objetivo–Hipótesis–Métrica–Comparador", "estado": "Hecho"},
            {"texto": "Corrección de OE1 (demanda explícita) en todo el documento", "estado": "En curso"},
            {"texto": "Unificación de comparadores C0–C5", "estado": "Hecho"},
            {"texto": "Glosario ES/EN (25 términos)", "estado": "Pendiente"},
        ],
        "productos": ["Matriz de trazabilidad", "Glosario ES/EN", "Tabla de comparadores C0–C5"],
    },
    "diseno": {
        "interpretacion": (
            "Media página de metodología es insuficiente para un doctorado: sin formulación "
            "explícita, representación del agente y protocolo, el proyecto no es reproducible. Es la "
            "calificación más baja del concepto y el frente de trabajo principal."
        ),
        "respuesta": [
            "**(a) Formulación operativa completa:** UC entero-mixto con Pmín/Pmáx, rampas horarias, "
            "tiempos mínimos de encendido/apagado, reserva up/down, balance por barra (IEEE 39) y "
            "límites de línea; extensión W-DRO con dualización explícita (reformulación del tipo "
            "Mohajerin Esfahani–Kuhn) que produce un problema tratable para solvers.",
            "**(b) Representación del agente (MDP):** estado, acción, transición y recompensa "
            "definidos operativamente (ver página «RL y MDP»), con enmascaramiento de acciones para "
            "restricciones intertemporales y entorno Gymnasium con Pyomo embebido como oráculo.",
            "**(c) Integración CP–DRO–RL en 4 pasos:** pronóstico puntual → calibración CP de "
            "residuos → radio ε(n, α) → DRO resuelve el programa del día siguiente → RL ajusta "
            "intradía dentro de la holgura robusta. Cada paso con entradas/salidas declaradas.",
            "**(d) Protocolo experimental reproducible:** datos de la API de XM (generación por "
            "tecnología, demanda por zona, precios) + sistema IEEE 39; partición temporal "
            "60/20/20 (entrenamiento/calibración/prueba) con validación rodante (rolling origin), "
            "**30 semillas**, intervalos de confianza al 95 % (bootstrap), prueba de hipótesis "
            "Wilcoxon firmada por pares y métricas pre-registradas.",
            "**(e) Garantías y sus supuestos** declarados expresamente (ver página «CP calibra el "
            "radio»): cobertura marginal bajo intercambiabilidad, validez del recourse para toda "
            "distribución de la bola, y límites de la cobertura condicional.",
        ],
        "acciones": [
            {"texto": "Capítulo de diseño ampliado (formulación + agente + integración + protocolo)", "estado": "En curso"},
            {"texto": "Especificación formal del MDP (estados/acciones/transiciones/recompensa)", "estado": "Hecho"},
            {"texto": "Protocolo de datos: API XM + IEEE 39, partición temporal y semillas", "estado": "Hecho"},
            {"texto": "Sección explícita «Supuestos y garantías»", "estado": "Hecho"},
            {"texto": "Formulación dual W-DRO completa en el documento", "estado": "Pendiente"},
        ],
        "productos": [
            "§Diseño ampliado (≈ 8–10 pp)",
            "Diagrama de integración CP→DRO→RL",
            "Protocolo experimental pre-registrado",
            "Repositorio de código (este dashboard + librerías)",
        ],
    },
    "actividades": {
        "interpretacion": (
            "Actividades demasiado generales no permiten auditar el avance. El jurado pide "
            "desagregación con productos verificables y actividades explícitas de verificación de "
            "restricciones, comparación de métodos y contribución marginal de cada técnica."
        ),
        "respuesta": [
            "**WBS de 8 paquetes** (A1–A8), cada tarea con responsable, producto verificable y "
            "criterio de aceptación (ver página «Plan y Presupuesto»).",
            "**A2 Calibración CP** → producto: librería de calibración + notebook de verificación de "
            "cobertura (criterio: cobertura empírica dentro de 1−α ± tolerancia en Monte Carlo).",
            "**A3 Formulación DRO** → producto: módulo Pyomo reproducible con tests unitarios "
            "(criterio: factibilidad verificada en 100 % de los escenarios de prueba).",
            "**A5 Integración** → producto: pipeline orquestado end-to-end (criterio: corrida "
            "automatizada completa desde datos crudos hasta tablas de resultados).",
            "**A6 Verificación de restricciones** (actividad explícita): suite de factibilidad "
            "fuera de muestra —balance, rampas, límites de unidad, reserva— reportada como "
            "**% de escenarios factibles** (métrica de la H3).",
            "**A7 Ablaciones** (actividad explícita): quitar CP, quitar DRO y quitar RL por turnos "
            "para medir la **contribución marginal** de cada técnica (experimentos C3/C5).",
            "**A8 Escritura y publicación** → productos: capítulos y artículos con calendario.",
        ],
        "acciones": [
            {"texto": "WBS A1–A8 con productos y criterios de aceptación", "estado": "Hecho"},
            {"texto": "Suite de verificación de restricciones fuera de muestra", "estado": "En curso"},
            {"texto": "Diseño de experimentos de ablación (contribución marginal por técnica)", "estado": "Hecho"},
            {"texto": "Tablero de seguimiento de productos verificables", "estado": "En curso"},
        ],
        "productos": ["WBS detallado", "Suite de factibilidad", "Protocolo de ablaciones"],
    },
    "cronograma": {
        "interpretacion": (
            "Un Gantt de 48 meses sin estado ni posición actual no comunica avance ni riesgo. "
            "Además, el encabezado aún decía «Tesis de Maestría»."
        ),
        "respuesta": [
            "**Cronograma con estados** (realizado / en curso / pendiente) y **posición actual** "
            "marcada (ver página «Plan y Presupuesto» — Gantt interactivo).",
            "**Hitos explícitos:** H1 calibración CP validada · H2 integración end-to-end · "
            "H3 resultados finales y ablaciones · H4 borrador de tesis · H5 sustentación.",
            "**Corrección editorial:** «Tesis de Maestría» → «Tesis de Doctorado» en encabezados y "
            "en el texto del cronograma/presupuesto.",
            "**Nota de transparencia:** las fechas absolutas se fijarán con el director según acta "
            "de inicio; aquí se muestran en meses relativos (M0–M48) con el estado real de cada "
            "frente, que es lo que el jurado solicitó poder verificar.",
        ],
        "acciones": [
            {"texto": "Gantt con estados y posición actual", "estado": "Hecho"},
            {"texto": "Hitos H1–H5 (validación, escritura, sustentación)", "estado": "Hecho"},
            {"texto": "Corrección «Maestría» → «Doctorado»", "estado": "En curso"},
            {"texto": "Fijación de fechas absolutas con el director", "estado": "Pendiente"},
        ],
        "productos": ["Gantt interactivo actualizado", "Tabla de hitos", "Documento corregido"],
    },
    "presupuesto": {
        "interpretacion": (
            "Un recurso no aprobado no puede aparecer como asegurado: eso distorsiona la planeación. "
            "El jurado pide clasificación honesta y justificación de rubros."
        ),
        "respuesta": [
            "**Reclasificación en tres categorías** (ver página «Plan y Presupuesto»): "
            "**Confirmados** (recursos del grupo de investigación: horas investigador, cómputo), "
            "**En especie** (acceso a datos vía API de XM, infraestructura de cómputo UNAL, "
            "licencias académicas de solver), **Por gestionar** (los $15 M COP para congresos → "
            "postulación a convocatorias internas de apoyo a presentación de trabajos y fondos de "
            "proyectos del grupo).",
            "**Los $15 M COP se registran explícitamente como «financiación por gestionar»**, con "
            "las fuentes identificadas y su probabilidad de éxito, no como recurso asegurado.",
            "**Justificación por rubro:** publicación en revista indexada (APC), 2 congresos "
            "(matrícula, viáticos, traslado), cómputo GPU para entrenamiento RL y repositorio de "
            "datos. Cada rubro se ata a una actividad del WBS (A1–A8).",
        ],
        "acciones": [
            {"texto": "Tabla presupuestal con categorías Confirmado / En especie / Por gestionar", "estado": "Hecho"},
            {"texto": "Reclasificación de los $15 M como «por gestionar» + fuentes identificadas", "estado": "Hecho"},
            {"texto": "Justificación de cada rubro vinculada al WBS", "estado": "Hecho"},
            {"texto": "Radificación de postulaciones a convocatorias de apoyo", "estado": "Pendiente"},
        ],
        "productos": ["Presupuesto reclasificado", "Ficha de fuentes de financiación"],
    },
    "redaccion": {
        "interpretacion": (
            "Los defectos editoriales restan credibilidad y esconden inconsistencias reales "
            "(ecuaciones, tablas y resultados que no concuerdan). El jurado pide más que "
            "«cosmética»: coherencia de contenido."
        ),
        "respuesta": [
            "**Limpieza de plantilla:** eliminación de instrucciones del formato "
            "(«Utilice o amplíe los espacios…») y de texto de ejemplo.",
            "**Numeración única y secuencial** de ecuaciones en orden de aparición "
            "(el documento actual mezcla numeración por sección con saltos), y referencias "
            "consistentes «Eq. (n)» en el texto.",
            "**Tabla de consistencia** ecuación ↔ tabla ↔ resultado: cada símbolo declarado una "
            "vez (parámetro, símbolo, valor, unidad, dónde se usa), evitando redefiniciones.",
            "**Terminología uniforme ES/EN** (glosario) y revisión ortográfica completa; se "
            "corrigen erratas detectadas (p. ej. «Wassers tein» → «Wasserstein», espurios de "
            "espaciado como «al ta» → «alta»).",
            "**Verificación de coherencia numérica** entre expresiones matemáticas, tablas y "
            "resultados (incluye la aclaración de la Planta C — ver «Resultados preliminares»).",
        ],
        "acciones": [
            {"texto": "Eliminación de instrucciones de plantilla y textos de ejemplo", "estado": "En curso"},
            {"texto": "Renumeración única de ecuaciones + tabla de consistencia de símbolos", "estado": "Pendiente"},
            {"texto": "Revisión ortográfica y de erratas", "estado": "En curso"},
            {"texto": "Glosario ES/EN aplicado al documento", "estado": "Pendiente"},
        ],
        "productos": ["Documento depurado", "Tabla de consistencia de símbolos", "Glosario"],
    },
    "bibliografia": {
        "interpretacion": (
            "72 referencias muestran lectura amplia, pero un marco teórico apoyado en 3 fuentes "
            "sugiere que la profundidad teórica no está respaldada. La calidad del análisis importa "
            "más que el conteo."
        ),
        "respuesta": [
            "**Reorganización en 6 familias temáticas** con análisis crítico por familia "
            "(explorador interactivo en «Antecedentes y Brecha» con las 72 entradas).",
            "**Fuentes primarias múltiples por fundamento del marco teórico:** "
            "CP (Vovk/Gammerman/Shafer; Lei et al.; Romano et al.; Angelopoulos & Bates [10]) · "
            "W-DRO (Mohajerin Esfahani & Kuhn; Kuhn et al. [5]; Blanchet & Murthy) · "
            "RL (Sutton & Barto [9]; Mnih et al.; Lillicrap et al.) · "
            "UC/programación (Bertsimas et al.; O'Malley et al. [2]; Jiménez et al. [26]; "
            "Cho & Yang [6]).",
            "**Tabla «afirmación central → fuente»** para las ~20 afirmaciones teóricas del marco "
            "metodológico, de modo que ninguna sección dependa de una sola referencia.",
        ],
        "acciones": [
            {"texto": "Clasificación de las 72 referencias en familias temáticas", "estado": "Hecho"},
            {"texto": "Ampliación de fuentes primarias por fundamento teórico", "estado": "En curso"},
            {"texto": "Tabla afirmación → fuente (20 afirmaciones)", "estado": "Pendiente"},
        ],
        "productos": ["Explorador de referencias", "Tabla afirmación → fuente", "Marco teórico con ≥ 3 fuentes por fundamento"],
    },
}

# Observaciones globales del reporte del jurado (adicionales a la matriz de criterios)
JURY_REPORT_ITEMS = [
    {
        "titulo": "Metodología en media página es insuficiente",
        "detalle": (
            "«La metodología se describe en media página, lo cual es insuficiente para una propuesta "
            "doctoral. Se sugiere que se especifique la formulación del problema operativo, las "
            "restricciones físicas, la representación del agente y el mecanismo de integración de "
            "CP, DRO y RL.»"
        ),
        "frente": "Diseño de la investigación",
    },
    {
        "titulo": "Radio de Wasserstein por calibración conformal + supuestos de garantía",
        "detalle": (
            "«Particularmente, explicarse cómo se obtendrá el radio de Wasserstein mediante "
            "calibración conformal y bajo qué supuestos serán válidas las garantías anunciadas.»"
        ),
        "frente": "Página «CP calibra el radio» (respuesta metodológica central)",
    },
    {
        "titulo": "Protocolo: datos, partición, comparadores, métricas, repeticiones y contraste",
        "detalle": (
            "«También deberían definirse los datos, su partición temporal, los comparadores, las "
            "métricas, las repeticiones y los criterios de contraste de la hipótesis.»"
        ),
        "frente": "Protocolo experimental pre-registrado",
    },
    {
        "titulo": "Desajustes hipótesis–objetivos–diseño",
        "detalle": (
            "«Se identifican desajustes entre hipótesis, objetivos y diseño en relación con la "
            "incertidumbre de demanda, los métodos de comparación y el horizonte de decisión.»"
        ),
        "frente": "Matriz de trazabilidad única",
    },
    {
        "titulo": "Inconsistencia Planta C: 190 MW vs. límite de 150 MW",
        "detalle": (
            "«En los resultados preliminares debe aclararse la recomendación de instalar 190 MW en "
            "la planta C, cuyo límite declarado es de 150 MW. Esta inconsistencia debe explicarse, "
            "además de precisar las unidades económicas y el alcance de las conclusiones.»"
        ),
        "frente": "Página «Resultados preliminares» (laboratorio de corrección)",
    },
    {
        "titulo": "Depuración editorial y fuentes de financiación",
        "detalle": (
            "«Finalmente, se requiere depurar las instrucciones de plantilla, unificar terminología "
            "y numeración, ubicar el cronograma respecto del avance actual y acreditar las fuentes "
            "de financiación.»"
        ),
        "frente": "Presentación · Cronograma · Presupuesto",
    },
]

# ---------------------------------------------------------------------------
# 4. Preguntas del examen de calificación (con respuestas estructuradas)
# ---------------------------------------------------------------------------
EXAM_Q1 = {
    "pregunta": (
        "¿Cómo deben determinarse y asignarse las reservas operativas en una programación del día "
        "siguiente con alta penetración renovable? Distinga suficiencia de capacidad, capacidad de "
        "rampa y disponibilidad efectiva de reservas. Explique por qué disponer de suficiente "
        "generación instalada no garantiza atender las variaciones de la demanda neta y proponga "
        "criterios para evaluar el compromiso entre costo, flexibilidad y confiabilidad."
    ),
    "tres_conceptos": [
        {
            "nombre": "Suficiencia de capacidad",
            "def": "¿Existe potencia instalada nominal suficiente para cubrir la demanda máxima "
                   "esperada más la reserva? Es una pregunta de *inventario* (MW instalados ≥ MW "
                   "requeridos).",
            "insuficiente_sola": "Responde «¿alcanza en el peor caso estático?», no «¿puede seguir la variación?».",
        },
        {
            "nombre": "Capacidad de rampa",
            "def": "¿La capacidad disponible puede cambiar de nivel a la velocidad que exige la "
                   "demanda neta? Se mide en MW/min o MW/h y depende del estado operativo "
                   "(encendido, sincronizado, en reserva girante) de cada unidad.",
            "insuficiente_sola": "De nada sirve una reserva de 300 MW en unidades apagadas si el "
                                 "despacho de arranque toma horas.",
        },
        {
            "nombre": "Disponibilidad efectiva",
            "def": "Probabilidad de que la reserva esté realmente disponible al momento de ser "
                   "llamada: fallas aleatorias, programas de mantenimiento, combustible/embalse, "
                   "degradación de renovables y congestión de red.",
            "insuficiente_sola": "El «nameplate» no es un activo disponible con certeza; por eso se "
                                 "descuenta (probabilidad de salida forzada, disponibilidad del "
                                 "recurso, factor de capacidad de transmisión).",
        },
    ],
    "por_que_no_basta": [
        "**La incertidumbre migra a la demanda neta** (demanda − viento − solar): su varianza y sus "
        "rampas crecen con la penetración renovable, incluso si la demanda total es estable.",
        "**Restricciones intertemporales:** tiempos de arranque, mínimos de encendido/apagado y "
        "rampas limitan cuánta capacidad nominal es realmente utilizable en cada hora.",
        "**Restricción energética:** hidráulica y combustible limitan la *energía* que puede "
        "entregar la reserva, no solo su potencia.",
        "**Correlación adversa:** la peor falta de generación renovable suele coincidir con picos "
        "de demanda (tarde/noche); la reserva debe dimensionarse para el evento conjunto.",
        "**Red:** congestión y criterio N-1 pueden aislar reservas existentes de la carga.",
    ],
    "criterios": [
        {"nombre": "Confiabilidad", "metrica": "LOLE / EENS / probabilidad de pérdida de carga, "
         "medida fuera de muestra sobre escenarios de viento, sol y demanda.", "lectura": "menor = mejor"},
        {"nombre": "Costo", "metrica": "Costo esperado de operación + CVaR₉₅ del costo (cola "
         "adversa), incluyendo costos de reserva y de arranque.", "lectura": "menor = mejor"},
        {"nombre": "Flexibilidad", "metrica": "Suficiencia de rampa: reserva de rampa ≥ cuantil "
         "(1−α) de la variación de la demanda neta en la ventana de respuesta.", "lectura": "cobertura ≥ 1−α"},
        {"nombre": "Robustez", "metrica": "Prima de robustez del DRO (costo extra frente al "
         "estocástico) y tasa de violación de restricciones bajo la peor distribución de la bola.",
         "lectura": "trade-off explícito"},
    ],
    "solucion_tesis": (
        "El enfoque de la tesis dimensiona reservas con **garantía estadística**: CP calibra el "
        "intervalo del error de pronóstico de la demanda neta con cobertura 1−α; ese intervalo fija "
        "el **radio de la bola de Wasserstein**; el DRO asigna entonces reserva de capacidad y de "
        "rampa que son factibles para toda distribución dentro de la bola. El criterio de asignación "
        "es un compromiso explícito costo–flexibilidad–confiabilidad: minimizar costo + CVaR sujeto "
        "a LOLE objetivo y a suficiencia de rampa con cobertura 1−α."
    ),
}

EXAM_Q2 = {
    "pregunta": (
        "¿Cómo representaría la programación del día siguiente mediante un proceso de decisión de "
        "Markov y qué papel cumpliría el aprendizaje por refuerzo frente a un modelo de optimización "
        "convencional? Defina estados, acciones, transiciones y recompensa, justificando cómo "
        "incorporaría las restricciones intertemporales."
    ),
    "mdp": [
        {
            "nombre": "Estado  sₜ",
            "def": (
                "sₜ = [hora del horizonte; pronóstico de demanda por nodo (restante); pronóstico "
                "renovable (eólica, solar); generación disponible de cada unidad; estado ON/OFF de "
                "cada unidad y tiempo acumulado en ese estado; producción actual de cada unidad; "
                "reservas asignadas up/down; desvíos respecto al programa DRO]"
            ),
            "nota": "Incluir tiempo en estado y producción actual garantiza la propiedad de Markov "
                    "pese a las restricciones intertemporales (min up/down y rampas).",
        },
        {
            "nombre": "Acción  aₜ",
            "def": (
                "aₜ = [ΔPᵢ ∈ [−rᵢᵈᵒʷⁿ, +rᵢᵘᵖ] : ajuste de set-point de unidades comprometidas; "
                "decisiones ON/OFF (enmascaradas por min up/down); asignación de reserva up/down; "
                "reserva no girante]"
            ),
            "nota": "En el esquema híbrido de la tesis, la acción es un **ajuste respecto al "
                    "programa DRO**, dentro de la holgura robusta del día siguiente.",
        },
        {
            "nombre": "Transición  P(sₜ₊₁ | sₜ, aₜ)",
            "def": (
                "Respuesta física de las unidades (dinámica de generación, tiempos de arranque) + "
                "materialización de la incertidumbre ξₜ₊₁ (viento, sol, demanda) aprendida de datos "
                "históricos de XM. En el entorno Gymnasium la transición es simulada: determinista "
                "dado ξₜ₊₁, con ξ muestreado del modelo de escenarios."
            ),
            "nota": "La incertidumbre se modela en la transición (no en la recompensa), de modo que "
                    "las políticas aprenden a responder a la materialización real.",
        },
        {
            "nombre": "Recompensa  rₜ₊₁",
            "def": (
                "rₜ₊₁ = −[ costo de combustión + costos de arranque/parada + ρ·(violación de "
                "balance/rampas/límites) + λ·(desviación del programa DRO) + μ·(déficit de reserva) ]"
            ),
            "nota": "Los pesos (ρ, λ, μ) se seleccionan por validación; variantes con CVaR penalizan "
                    "la cola adversa del costo.",
        },
    ],
    "intertemporales": [
        "**Enmascaramiento de acciones:** en cada estado solo se ofrecen acciones factibles "
        "(rampas y min up/down), lo que acelera el entrenamiento y evita penalizar violaciones.",
        "**Augmentación del estado:** contadores de tiempo ON/OFF y producción previa hacen el "
        "proceso Markoviano pese a las restricciones con memoria.",
        "**CMDP / Lagrangiano:** las restricciones de reserva y de emisión se tratan como "
        "restricciones de expectativa con multiplicadores aprendidos.",
        "**Proyección de acciones (capa de seguridad):** la acción del agente se proyecta al "
        "conjunto factible con un solver ligero (QP/LP) si la política propone algo inviable.",
    ],
    "rl_vs_optimizacion": [
        {"eje": "Naturaleza de la solución", "optim": "Óptimo del modelo (con garantías del modelo)",
         "rl": "Aproximación aprendida de la política óptima (aproximación por función)"},
        {"eje": "Tiempo en operación", "optim": "Segundos a minutos; requiere re-resolución completa",
         "rl": "Milisegundos por decisión (solo inferencia)"},
        {"eje": "Adaptación", "optim": "Re-optimiza ante cada cambio de datos",
         "rl": "Se adapta a la materialización de ξ dentro de lo visto en entrenamiento"},
        {"eje": "Factibilidad", "optim": "Garantizada por el modelo (si es correcto)",
         "rl": "Garantizada por diseño (enmascaramiento + proyección)"},
        {"eje": "Rol en la tesis", "optim": "Oráculo/profesor del día siguiente (DRO)",
         "rl": "Capa de ajuste intradía entrenada con el oráculo"},
    ],
    "solucion_tesis": (
        "La tesis no sustituye la optimización por RL: las **articula**. El DRO resuelve el "
        "problema del día siguiente con garantías worst-case (una vez al día, minutos de cómputo). "
        "El agente RL aprende una política de ajuste intradía —entrenada imitando y mejorando al "
        "oráculo DRO— que ejecuta en milisegundos cuando se materializan viento, sol y demanda. "
        "Así, la velocidad del RL no sacrifica factibilidad (proyección) ni robustez (opera dentro "
        "de la holgura del programa robusto)."
    ),
}

# ---------------------------------------------------------------------------
# 5. Alcance, métricas, hipótesis, comparadores
# ---------------------------------------------------------------------------
ALCANCE = {
    "dentro": [
        "Programación del **día siguiente**: compromiso de unidades (UC) + despacho horario (24 pasos).",
        "Ajuste **intradía** cada 15 min (96 pasos) con política de RL.",
        "Incertidumbre: error de pronóstico de **generación eólica, solar y demanda** (vector ξ).",
        "Conjuntos de ambigüedad por **distancia de Wasserstein** con radio **calibrado por CP**.",
        "Sistemas de potencia con **alta penetración renovable** (caso colombiano + IEEE 39).",
        "Comparación rigurosa con determinista, estocástico, robusto y variantes ablativas.",
    ],
    "fuera": [
        "Operación en **tiempo real** (AGC/EMS) y mercados de balance.",
        "Incertidumbre por **fallas de equipos** y disponibilidad hidráulica (trabajo futuro).",
        "Expansión de generación/transmisión (se usa solo como **ejercicio preliminar**).",
        "Estabilidad electromecánica y calidad de la potencia.",
        "Diseño de mercado y formación de precios.",
    ],
}

METRICAS = [
    {"kpi": "Costo operativo total", "def": "Suma de costos de energía, arranque y reserva en el horizonte",
     "dir": "↓ menor", "meta": "≤ costo del comparador C1 + prima ≤ 10 %", "hipotesis": "H1"},
    {"kpi": "CVaR₉₅ del costo", "def": "Valor en riesgo condicional al 95 % (cola adversa del costo)",
     "dir": "↓ menor", "meta": "reducción vs. C1 y C3", "hipotesis": "H1"},
    {"kpi": "Tasa de violación de restricciones", "def": "% de escenarios fuera de muestra con alguna violación física",
     "dir": "↓ menor", "meta": "≤ 1 % de escenarios", "hipotesis": "H3"},
    {"kpi": "Cobertura empírica", "def": "Frecuencia con que el conjunto predicho contiene la realización",
     "dir": "≈ 1−α", "meta": "|cobertura − (1−α)| ≤ tolerancia estadística", "hipotesis": "H2"},
    {"kpi": "Tiempo de cómputo", "def": "Tiempo de resolución/decisión en operación",
     "dir": "↓ menor", "meta": "ajuste intradía < 1 s (RL); día siguiente < 15 min (DRO)", "hipotesis": "H2"},
    {"kpi": "Holgura de reservas", "def": "Reserva de capacidad y de rampa disponible por escenario",
     "dir": "↑ suficiente", "meta": "rampa ≥ cuantil (1−α) de Δ demanda neta", "hipotesis": "H3"},
]

HIPOTESIS = [
    {"id": "H1", "texto": "El modelo integrado reduce el costo operativo esperado y el CVaR₉₅ "
     "frente a los enfoques determinista y estocástico (prima de robustez acotada).",
     "prueba": "Comparación C0–C5 sobre el conjunto de prueba, 30 semillas, Wilcoxon firmado, IC 95 %."},
    {"id": "H2", "texto": "La calibración CP del radio ε alcanza cobertura empírica 1−α en muestras "
     "finitas, y la política RL ejecuta decisiones en milisegundos sin pérdida de calidad.",
     "prueba": "Monte Carlo de cobertura (≥ 1000 réplicas) + medición de latencia en operación."},
    {"id": "H3", "texto": "Las decisiones del modelo son factibles fuera de muestra (balance, rampas, "
     "límites, reserva) con tasa de violación ≤ 1 %, incluyendo escenarios adversos.",
     "prueba": "Suite de factibilidad sobre 10.000 escenarios fuera de muestra generados con "
     "desplazamientos de distribución."},
]

COMPARADORES = [
    {"id": "C0", "nombre": "Determinista", "desc": "UC con pronósticos puntuales (sin incertidumbre).", "rol": "línea base"},
    {"id": "C1", "nombre": "Estocástico", "desc": "UC con escenarios y distribución conocida (esperanza).", "rol": "estado del arte clásico"},
    {"id": "C2", "nombre": "Robusto (caja)", "desc": "RO con conjunto de incertidumbre tipo caja.", "rol": "conservadurismo extremo"},
    {"id": "C3", "nombre": "DRO-W sin CP", "desc": "DRO con bola de Wasserstein y radio elegido heurísticamente.", "rol": "abla el aporte de CP"},
    {"id": "C4", "nombre": "DRO-W + CP (propuesto)", "desc": "DRO con radio calibrado por predicción conforme + ajuste RL.", "rol": "modelo de la tesis"},
    {"id": "C5", "nombre": "RL sin capa DRO", "desc": "Agente RL puro sobre el mismo entorno.", "rol": "abla el aporte del DRO"},
]

GLOSARIO = [
    ("Programación operativa", "Operational scheduling"),
    ("Compromiso de unidades", "Unit commitment (UC)"),
    ("Despacho económico", "Economic dispatch"),
    ("Optimización robusta distribucional", "Distributionally robust optimization (DRO)"),
    ("Conjunto de ambigüedad", "Ambiguity set"),
    ("Distancia de Wasserstein", "Wasserstein distance / optimal transport"),
    ("Predicción conforme", "Conformal prediction (CP)"),
    ("Función de no conformidad", "Nonconformity score"),
    ("Aprendizaje por refuerzo", "Reinforcement learning (RL)"),
    ("Proceso de decisión de Markov", "Markov decision process (MDP)"),
    ("Demanda neta", "Net load"),
    ("Reserva operativa", "Operating reserve"),
    ("Prima de robustez", "Robustness premium"),
]

# ---------------------------------------------------------------------------
# 6. WBS, hitos, cronograma (meses relativos M0–M48), presupuesto
# ---------------------------------------------------------------------------
GANTT = [
    {"fase": "A1 · Datos", "tarea": "Recolección API XM + IEEE 39, diccionario de datos",
     "inicio": 0, "duracion": 4, "estado": "Realizado", "producto": "Dataset versionado + diccionario"},
    {"fase": "A1 · Datos", "tarea": "Análisis exploratorio y calidad de datos",
     "inicio": 2, "duracion": 3, "estado": "Realizado", "producto": "Notebook EDA + informe"},
    {"fase": "A2 · Calibración CP", "tarea": "Revisión de estado del arte: CP y scores de no conformidad",
     "inicio": 1, "duracion": 4, "estado": "Realizado", "producto": "Estado del arte CP"},
    {"fase": "A3 · Formulación DRO", "tarea": "Ejercicio preliminar DRO (expansión 2 etapas)",
     "inicio": 3, "duracion": 3, "estado": "Realizado", "producto": "Resultados preliminares + código"},
    {"fase": "A2 · Calibración CP", "tarea": "Implementación de calibración y verificación de cobertura",
     "inicio": 5, "duracion": 6, "estado": "En curso", "producto": "Librería de calibración + tests de cobertura"},
    {"fase": "A3 · Formulación DRO", "tarea": "Formulación UC + W-DRO y dualización (H1: radio calibrado)",
     "inicio": 5, "duracion": 7, "estado": "En curso", "producto": "Formulación completa + módulo Pyomo"},
    {"fase": "A8 · Escritura", "tarea": "Artículo 1 (calibración CP de conjuntos W-DRO)",
     "inicio": 6, "duracion": 10, "estado": "En curso", "producto": "Borrador de artículo"},
    {"fase": "A4 · Agente RL", "tarea": "Entorno Gymnasium + implementación formal del MDP",
     "inicio": 11, "duracion": 8, "estado": "Pendiente", "producto": "Entorno + agente baseline"},
    {"fase": "A5 · Integración", "tarea": "Pipeline CP → ε → DRO → RL end-to-end (H2)",
     "inicio": 18, "duracion": 9, "estado": "Pendiente", "producto": "Pipeline orquestado + pruebas"},
    {"fase": "A6 · Validación", "tarea": "Experimentos C0–C5, 30 semillas, suite de factibilidad (H3)",
     "inicio": 28, "duracion": 7, "estado": "Pendiente", "producto": "Tablas de resultados + IC 95 %"},
    {"fase": "A7 · Ablaciones", "tarea": "Contribución marginal de CP, DRO y RL",
     "inicio": 35, "duracion": 4, "estado": "Pendiente", "producto": "Informe de ablaciones"},
    {"fase": "A8 · Escritura", "tarea": "Artículo 2 (arquitectura DRO+RL) y capítulos de tesis (H4)",
     "inicio": 30, "duracion": 15, "estado": "Pendiente", "producto": "Borrador de tesis + artículo 2"},
    {"fase": "A8 · Escritura", "tarea": "Depuración editorial (plantilla, glosario, ecuaciones)",
     "inicio": 44, "duracion": 3, "estado": "Pendiente", "producto": "Documento depurado"},
]

HITOS = [
    {"id": "H1", "nombre": "Calibración CP validada (cobertura 1−α)", "mes": 12, "estado": "En curso"},
    {"id": "H2", "nombre": "Integración end-to-end operativa", "mes": 27, "estado": "Pendiente"},
    {"id": "H3", "nombre": "Resultados finales + ablaciones", "mes": 35, "estado": "Pendiente"},
    {"id": "H4", "nombre": "Borrador de tesis", "mes": 45, "estado": "Pendiente"},
    {"id": "H5", "nombre": "Sustentación de la tesis", "mes": 48, "estado": "Pendiente"},
]

HOY_MES = 6  # posición actual sobre el horizonte de 48 meses

PRESUPUESTO = [
    {"rubro": "APC publicación revista indexada (Q1/Q2)", "monto": 8_000_000, "tipo": "Por gestionar",
     "fuente": "Convocatorias internas UNAL / fondos de proyecto del grupo",
     "justificacion": "Artículo 1 (calibración CP de conjuntos W-DRO) — actividad A8."},
    {"rubro": "Congresos internacionales (2): matrícula, viáticos, traslado", "monto": 15_000_000,
     "tipo": "Por gestionar", "fuente": "Apoyo universitario a presentación de trabajos (postular)",
     "justificacion": "Socialización de avances A2–A5 y retroalimentación de pares. **No asegurado.**"},
    {"rubro": "Cómputo GPU (entrenamiento de agentes RL)", "monto": 4_000_000, "tipo": "En especie",
     "fuente": "Infraestructura de cómputo UNAL / grupo de investigación",
     "justificacion": "Entrenamiento A4–A5 (30 semillas × configuraciones)."},
    {"rubro": "Acceso a datos operativos (API XM, históricos)", "monto": 0, "tipo": "En especie",
     "fuente": "API pública del operador XM + datos abiertos UPME",
     "justificacion": "Base del protocolo experimental (A1)."},
    {"rubro": "Licencias académicas de solver (Gurobi/CPLEX) y software", "monto": 0, "tipo": "Confirmado",
     "fuente": "Programas académicos de los proveedores (licencia gratuita educativa)",
     "justificacion": "Resolución de modelos UC-DRO (A3, A5)."},
    {"rubro": "Horas investigador (asistente de investigación)", "monto": 12_000_000, "tipo": "Confirmado",
     "fuente": "Proyecto de investigación vinculado / horas del grupo",
     "justificacion": "Implementación y experimentos A1–A7."},
]

# ---------------------------------------------------------------------------
# 7. Aportes y potencial
# ---------------------------------------------------------------------------
APORTES = [
    {
        "id": "C1",
        "titulo": "Calibración CP del radio de ambigüedad (ε) con garantías de cobertura",
        "tipo": "Teórico-metodológico",
        "problema": "Hoy el radio de la bola de Wasserstein se elige por heurística o validación "
                    "informal: la «robustez» no tiene nivel de confianza declarado.",
        "aporte": "Un procedimiento de predicción conforme que asigna ε(n, α) de modo que la bola "
                  "cubra la distribución real de los errores con probabilidad ≥ 1−α en muestras "
                  "finitas, convirtiendo la robustez en un contrato estadístico explícito.",
        "validacion": "Demostración de cobertura + verificación Monte Carlo + sensibilidad a α y n.",
        "publicacion": "Revista Q1 en optimización bajo incertidumbre / energía.",
    },
    {
        "id": "C2",
        "titulo": "Arquitectura de decisión en dos tiempos DRO (día siguiente) + RL (intradía)",
        "tipo": "Arquitectura de decisión",
        "problema": "Los modelos robustos son lentos de re-resolver; los agentes RL son rápidos pero "
                    "sin garantías de factibilidad ni de robustez.",
        "aporte": "Un marco donde el DRO provee el programa robusto del día siguiente y el agente RL "
                  "ajusta intradía dentro de la holgura de ese programa, con factibilidad por "
                  "enmascaramiento y proyección de acciones.",
        "validacion": "Protocolo experimental comparativo C0–C5 + ablaciones + medición de latencia.",
        "publicacion": "Revista Q1/Q2 en sistemas de potencia + congreso internacional.",
    },
    {
        "id": "C3",
        "titulo": "Evidencia empírica reproducible para el sistema colombiano (XM + IEEE 39)",
        "tipo": "Empírico-recurrente",
        "problema": "Faltan benchmarks reproducibles que cuantifiquen la región costo–robustez–"
                    "cobertura en sistemas con alta penetración renovable tipo Colombia.",
        "aporte": "Corpus de datos, código abierto y resultados con IC 95 % que permiten auditar y "
                  "extender los hallazgos; enfoque relevante también para zonas no interconectadas.",
        "validacion": "Repositorio público + replicación independiente + extensión a ZNI (trabajo futuro).",
        "publicacion": "Artículo de datos/benchmark + repositorio citable (DOI).",
    },
]

POTENCIAL = [
    ("Para la disciplina", [
        "Convierte el *tuning* de conjuntos de ambigüedad en un parámetro con garantía estadística — "
        "un cambio de práctica en DRO aplicado.",
        "Articula garantías worst-case (DRO) con velocidad de decisión (RL) sin sacrificar "
        "factibilidad física.",
        "Provee un protocolo experimental y un benchmark reproducibles para comparaciones futuras.",
    ]),
    ("Para el sector eléctrico colombiano", [
        "Operación más confiable con alta penetración solar/eólica (plan de descarbonización UPME).",
        "Herramientas para la gestión operativa de zonas no interconectadas (ZNI), donde la "
        "resiliencia es crítica.",
        "Cuantificación transparente del costo de la robustez (prima de seguro) para operadores.",
    ]),
    ("Para la formación y la academia", [
        "Artículos en revistas indexadas y participación en congresos internacionales.",
        "Código y datos abiertos que habilitan cursos, réplicas y tesis derivadas.",
        "Puente entre optimización, estadística (CP) y aprendizaje automático aplicado a energía.",
    ]),
]

PLAN_PUBLICACION = [
    {"momento": "Año 2", "producto": "Artículo 1 — Calibración CP de conjuntos de ambigüedad de "
     "Wasserstein para DRO (envío a revista Q1)", "estado": "En curso"},
    {"momento": "Año 3", "producto": "Artículo 2 — Arquitectura DRO + RL para programación operativa "
     "(revista Q1/Q2 + congreso)", "estado": "Pendiente"},
    {"momento": "Año 3", "producto": "Repositorio de benchmark + dataset citable (DOI)", "estado": "Pendiente"},
    {"momento": "Año 4", "producto": "Tesis doctoral + artículo derivado (extensión ZNI / operación "
     "resiliente)", "estado": "Pendiente"},
]

# ---------------------------------------------------------------------------
# 8. Resultados preliminares (ejercicio de expansión 2 etapas)
# ---------------------------------------------------------------------------
PRELIM = {
    "contexto": (
        "Ejercicio preliminar: expansión de generación en dos etapas bajo incertidumbre de "
        "generación renovable y demanda. 1ª etapa: inversión (qué y cuánta capacidad instalar). "
        "2ª etapa: despacho económico para cada realización de la incertidumbre. Se compara "
        "optimización estocástica vs. DRO con conjunto de ambigüedad basado en momentos (media), "
        "reformulado como LP mediante dualidad (Pyomo + solver abierto)."
    ),
    "costos": {"estocastico": 1_092_300, "dro": 1_202_100},
    "portafolio": {"ew": 0.0, "ef": 100.0, "ea": 190.0, "eb": 120.0, "ec": 190.0},
    "portafolio_nombres": {
        "ew": "Nueva eólica (Gw)", "ef": "Nueva solar (Gf)", "ea": "Nueva planta A",
        "eb": "Nueva planta B (6 unidades)", "ec": "Nueva planta C",
    },
    "limites": {"ea": 200, "eb": 180, "ec": 150, "ew": 100, "ef": 100},
    "hallazgos": [
        "DRO cuesta +10,05 % (prima de robustez: $109.800) — un «seguro» frente a distribuciones mal especificadas.",
        "Ambos enfoques recomendaron el mismo portafolio (los costos fijos dominan la decisión de inversión).",
        "El despacho sí difiere: con DRO la planta G02 ajusta su producción con mayor frecuencia bajo los peores escenarios.",
        "Conclusión preliminar: los conjuntos de momentos son una primera aproximación; la tesis avanzará a conjuntos de Wasserstein calibrados con CP.",
    ],
    "aclaracion_planta_c": (
        "El jurado identificó correctamente una inconsistencia: los resultados reportan **190 MW** "
        "para la planta C, pero la Tabla 10 fija su límite técnico en **150 MW**. Causas probables: "
        "(i) discrepancia entre los parámetros de la tabla y los usados en el código de la corrida; "
        "(ii) error de transcripción del valor reportado; (iii) agregación de variables en la "
        "exportación de resultados. **Acción:** re-corregir el modelo con los parámetros bloqueados "
        "por tabla (Emax_C = 150 MW), actualizar tablas y figuras, y publicar el código con los "
        "parámetros versionados para que la corrida sea auditable. El laboratorio de abajo permite "
        "re-verificar el efecto de la corrección en vivo."
    ),
    "unidades": (
        "Unidades económicas: los valores del ejercicio preliminar están expresados en **unidades "
        "monetarias normalizadas del ejercicio** (pesos de modelo: costos de inversión y operación "
        "por MW). No representan escala financiera real; en el modelo completo se reportarán en "
        "COP constantes (miles de COP/MW·h) con año base declarado. El alcance de las conclusiones "
        "preliminares es **metodológico** (viabilidad de la reformulación DRO), no de planeación real."
    ),
}

# ---------------------------------------------------------------------------
# 9. Mapeo CP → radio de Wasserstein (usado en varias páginas)
# ---------------------------------------------------------------------------
CADENA_CP = [
    ("1", "Datos de operación", "Series históricas de pronóstico y realización (viento, sol, demanda) — API XM."),
    ("2", "Modelo de pronóstico puntual", "Cualquier regresor (el modelo base no se modifica por CP)."),
    ("3", "Residuos de calibración", "Errores eᵢ = realización − pronóstico sobre el conjunto de calibración."),
    ("4", "Scores de no conformidad", "sᵢ = ‖eᵢ‖ (o score monótono en la magnitud del error multivariado)."),
    ("5", "Cuantil conforme q̂", "q̂ = cuantil ⌈(n+1)(1−α)⌉/n de los scores ordenados."),
    ("6", "Radio de ambigüedad ε", "ε := q̂ (o transformación g(q̂)) define la bola de Wasserstein 𝔹(Q̂₀, ε)."),
    ("7", "DRO con bola calibrada", "min_x max_{P ∈ 𝔹(Q̂₀,ε)} E_P[f(x,ξ)] → programa del día siguiente."),
    ("8", "Garantía declarada", "P(ξ_real ∈ bola) ≥ 1−α bajo intercambiabilidad; decisión robusta para toda P de la bola."),
]

SUPUESTOS = [
    ("Intercambiabilidad", "Los scores de calibración y el dato futuro son intercambiables "
     "(i.i.d. es el caso particular). En series temporales se requiere estabilidad o dependencia "
     "controlada (β-mixing), o CP ponderado por covariables."),
    ("Score bien especificado", "La función de no conformidad debe crecer con la magnitud del error "
     "relevante para la decisión (norma del error multivariado de ξ)."),
    ("Cobertura marginal", "La garantía es marginal (1−α en promedio sobre el muestreo), no "
     "condicional por escenario; la cobertura condicional es un objetivo activo de investigación "
     "(CP con covariables / adaptativo)."),
    ("Recourse in-bola", "La optimalidad worst-case del DRO vale para toda distribución dentro de "
     "la bola (reformulación dual exacta bajo momento finito de orden ρ y conjunto factible cerrado)."),
    ("Recalibración", "Ante cambios de régimen (cambios climáticos, nuevas plantas) el radio se "
     "recalibra con ventanas rodantes; la validez se monitorea con pruebas de cobertura en operación."),
]


# ---------------------------------------------------------------------------
# 10. Utilidades
# ---------------------------------------------------------------------------
def load_references() -> list[dict]:
    """Carga las 72 referencias parseadas del documento."""
    path = Path(__file__).resolve().parent.parent / "data" / "references.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def jury_score_scale() -> dict:
    return SCORE_LABELS


def actions_progress(actions: list[dict]) -> tuple[int, int, float]:
    """(hechos, total, fracción) de una lista de acciones."""
    total = len(actions)
    done = sum(1 for a in actions if a["estado"] == "Hecho")
    return done, total, (done / total if total else 0.0)
