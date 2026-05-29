# -*- coding: utf-8 -*-
"""Genera módulos del framework (10 bloques) e inyecta en guide_IA.html y pasos.html."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def fw_block(label, body_html):
    return f"""<div class="fw-block">
  <div class="fw-block-label">{label}</div>
  <div class="fw-block-body">{body_html}</div>
</div>"""


def standards_html(items):
    tags = []
    for t, kind in items:
        cls = {"iso": "fw-std-iso", "owasp": "fw-std-owasp", "eng": "fw-std-eng"}.get(kind, "fw-std")
        tags.append(f'<span class="fw-std {cls}">{t}</span>')
    return '<div class="fw-standards">' + "".join(tags) + "</div>"


def metrics_html(items):
    cells = "".join(
        f'<div class="fw-metric"><div class="fw-metric-val">{v}</div><div class="fw-metric-label">{l}</div></div>'
        for v, l in items
    )
    return f'<div class="fw-metrics">{cells}</div>'


def prompt_accordion(step, pid, title, technique_note, body, open_first=False):
    open_cls = " open" if open_first else ""
    return f"""
<div class="accordion">
  <button class="acc-trigger{open_cls}" onclick="toggleAcc(this)" aria-expanded="{'true' if open_first else 'false'}">
    <span class="acc-label">{title}</span>
    <span class="acc-arrow" aria-hidden="true"><i data-lucide="chevron-down" class="icon-sm"></i></span>
  </button>
  <div class="acc-body{open_cls}">
    <p class="fw-prompt-tier"><strong>ID:</strong> {pid} · <strong>Técnica:</strong> {technique_note}</p>
    <div class="prompt-block" data-step="{step}">
      <div class="prompt-header">
        <div class="prompt-tag"><span class="dot"></span><span class="prompt-title">prompt · {pid.lower()}</span></div>
        <button type="button" class="copy-btn" onclick="copyP(this)">Copiar</button>
      </div>
      <div class="prompt-body">{body}</div>
    </div>
  </div>
</div>"""


def render_module(n, config):
    c = config
    blocks = [
        fw_block("01 · Objetivo", f"<p>{c['objective']}</p>"),
        fw_block("02 · Riesgo mitigado", f"<p>{c['risk']}</p>"),
        fw_block("03 · Estándares", standards_html(c["standards"])),
        fw_block(
            "04 · Prompt engineering",
            f'<p class="fw-technique">{c["technique_name"]}</p>'
            + "".join(f'<span class="fw-technique-tag">{t}</span>' for t in c["technique_tags"]),
        ),
    ]

    prompts_html = ""
    for i, p in enumerate(c["prompts"]):
        prompts_html += prompt_accordion(n, p["id"], p["title"], p["tech"], p["body"], open_first=(i == 0))
    blocks.append(fw_block("05 · Prompts avanzados", prompts_html))

    blocks.append(fw_block("06 · Resultado esperado", f"<p>{c['expected']}</p>"))
    blocks.append(fw_block("07 · Validación técnica", c["validation"]))
    blocks.append(fw_block("08 · Métricas", metrics_html(c["metrics"])))
    blocks.append(fw_block("09 · Auditoría", c["audit"]))
    blocks.append(
        fw_block(
            "10 · Evidencia",
            f'<div class="fw-evidence">{c["evidence"]}</div>'
            f'<p class="fw-trace" style="margin-top:12px">ISO: {c["iso_link"]}</p>',
        )
    )

    inner = "\n".join(blocks)
    return f"""<!-- ═══ MÓDULO P0{n} ═══ -->
<section id="paso{n}" class="section fw-module">
<div class="s-eyebrow">Módulo {n} de 6 · {c['code']}</div>
<div class="paso-card" data-step="{n}">
  <div class="paso-head">
    <div class="paso-num-badge" data-step="{n}">0{n}</div>
    <div class="paso-head-info">
      <h3>{c['title']}</h3>
      <p>{c['subtitle']}</p>
    </div>
  </div>
  <div class="paso-body">
    <div class="fw-module-grid">
{inner}
    </div>
  </div>
</div>
</section>
"""


MODULES = {
    1: {
        "code": "P01-DEF",
        "title": "Definición del propósito y especificación",
        "subtitle": "Establecer trazabilidad requisito→diseño antes de cualquier generación de código asistida.",
        "objective": "Desarrollar la capacidad de elaborar especificaciones técnicas verificables que delimiten el alcance humano vs. asistido por IA, alineadas con completitud y pertinencia funcional (ISO 25010).",
        "risk": "Dependencia cognitiva por delegación del problema completo; soluciones genéricas que violan pertinencia funcional; ausencia de criterios de aceptación medibles.",
        "standards": [
            ("ISO 25010 · Adecuación", "iso"),
            ("ISO 25010 · Fiabilidad", "iso"),
            ("SOLID · SRP (alcance)", "eng"),
            ("Clean Code · nombres/significado", "eng"),
            ("NIST AI RMF · GOVERN 1.1", "iso"),
        ],
        "technique_name": "Chain-of-Thought + Meta-prompting + Reflection",
        "technique_tags": ["CoT", "Meta-prompt", "Reflection"],
        "prompts": [
            {
                "id": "P01-ADV-001",
                "title": "Especificación técnica con razonamiento explícito (CoT)",
                "tech": "CoT · Meta-prompting",
                "body": """Actúa como arquitecto de software senior. NO generes código.

## Contexto del sistema
- Dominio: <span class="pv">[ej. gestión académica, e-commerce, IoT]</span>
- Stack permitido: <span class="pv">[lenguaje, framework, BD]</span>
- Restricciones normativas: <span class="pv">[Ley 1581, licencias, etc.]</span>
- Enunciado del problema (versión del estudiante/desarrollador):
<span class="pv">[pegar enunciado en sus propias palabras]</span>

## Instrucción (Chain-of-Thought obligatorio)
Responde en fases numeradas. En cada fase muestra tu razonamiento antes de la conclusión.

### Fase 1 — Análisis del problema
1. Identifica actores, entradas, salidas y límites del sistema.
2. Lista ambigüedades del enunciado y preguntas que deben resolverse ANTES de codificar.
3. Propón 3 criterios de aceptación medibles (formato: dado/cuando/entonces o métrica numérica).

### Fase 2 — Diseño conceptual (sin código)
1. Compara 2 enfoques algorítmicos/arquitectónicos (ventajas, trade-offs, complejidad estimada O(n)).
2. Señala qué principios SOLID aplican y cuál componente violaría SRP si se mezcla.
3. Identifica 5 casos borde (vacío, null, overflow, concurrencia, fallo de red).

### Fase 3 — Meta-reflexión (Reflection)
1. ¿Qué partes DEBE resolver el humano sin IA y por qué?
2. ¿Qué riesgos de alucinación tendría un LLM si pidiera código directo?
3. Entregable: tabla Markdown | Requisito | Tipo (RF/RNF) | Criterio verificación | ISO 25010 |

## Formato de salida
Solo Markdown estructurado. Sin código fuente.""",
            },
            {
                "id": "P01-ADV-002",
                "title": "Threat modeling ligero pre-implementación",
                "tech": "Tree-of-thoughts · Adversarial",
                "body": """Rol: analista de seguridad en fase de diseño (OWASP ASVS nivel 1).

Problema definido:
<span class="pv">[resumen de spec P01-ADV-001]</span>

## Tree-of-thoughts (3 ramas)
Para cada amenaza STRIDE relevante, desarrolla 3 ramas:
- Rama A: explotación más probable
- Rama B: impacto en confidencialidad/integridad
- Rama C: control mitigador en diseño (sin código)

## Salida requerida
1. Diagrama textual de flujo de datos (entrada → proceso → almacenamiento)
2. Tabla | Amenaza | OWASP 2021 | Control diseño | Evidencia futura |
3. Lista de datos que NUNCA deben enviarse a un LLM en prompts posteriores

No implementar. Solo diseño defensivo.""",
            },
        ],
        "expected": "Documento de especificación (1–3 páginas) con requisitos RF/RNF, criterios de aceptación medibles, delimitación humano/IA y tabla de trazabilidad ISO.",
        "validation": """<ul>
<li>Existen ≥3 criterios de aceptación cuantificables o verificables por test</li>
<li>Tabla de trazabilidad requisito → característica ISO 25010 completada</li>
<li>Threat model ligero con ≥3 amenazas y controles de diseño</li>
<li>Ningún dato real/sensible en borradores de prompt</li>
</ul>""",
        "metrics": [
            ("≥3", "Criterios de aceptación"),
            ("100%", "Requisitos con ID único"),
            ("0", "Datos sensibles en prompts"),
        ],
        "audit": """<ul>
<li>¿El estudiante puede explicar el problema sin leer el output de la IA?</li>
<li>¿Los requisitos son verificables con prueba automatizada o inspección?</li>
<li>¿Se documentó qué decisiones son humanas vs. asistidas?</li>
</ul>""",
        "evidence": "EVID-P01: spec-v1.md · threat-model.md · checklist-pre-IA.pdf · commit hash o fecha en bitácora",
        "iso_link": '<a href="iso-evaluation.html">Preguntas adec_*, fiab_*</a>',
    },
    2: {
        "code": "P02-VAL",
        "title": "Validación técnica del output",
        "subtitle": "Verificación sistemática del código generado: corrección, pruebas, complejidad y alineación con la spec.",
        "objective": "Instaurar validación basada en evidencia (tests, revisión estática, ejecución) que detecte alucinaciones, APIs inexistentes y regresiones antes de integrar.",
        "risk": "Alucinaciones de APIs/librerías; código que compila pero falla en casos borde; deuda técnica invisible; falsa sensación de corrección.",
        "standards": [
            ("ISO 25010 · Fiabilidad", "iso"),
            ("ISO 25010 · Mantenibilidad", "iso"),
            ("OWASP A03 Injection", "owasp"),
            ("Clean Code · funciones pequeñas", "eng"),
            ("Testing · pirámide de pruebas", "eng"),
        ],
        "technique_name": "Self-consistency + Few-shot + Reflection",
        "technique_tags": ["Self-consistency", "Few-shot", "Reflection"],
        "prompts": [
            {
                "id": "P02-ADV-001",
                "title": "Auditoría de corrección con self-consistency",
                "tech": "Self-consistency · CoT",
                "body": """Eres revisor de código senior. El siguiente código fue generado con asistencia de IA.

## Artefactos
```<span class="pv">[lenguaje]</span>
<span class="pv">[pegar código]</span>
```

Especificación de referencia (P01):
<span class="pv">[criterios de aceptación]</span>

## Procedimiento Self-consistency (3 pasadas independientes)
Realiza TRES revisiones separadas (Pass A, B, C). En cada pass:
1. Verifica alineación con cada criterio de aceptación (tabla ✓/✗/parcial + evidencia).
2. Detecta APIs, imports o métodos potencialmente alucinados (indica cómo verificar en documentación oficial).
3. Estima complejidad ciclomática por función (baja/media/alta) y señala funciones > 10 de complejidad.

## Consenso
Fusiona las 3 pasadas: lista solo hallazgos confirmados en ≥2 passes.
Prioriza: Critical / High / Medium / Low.

## Salida
Markdown: Resumen ejecutivo · Tabla de hallazgos · Casos de prueba faltantes (mín. 8: 2 happy, 3 borde, 2 error, 1 seguridad)""",
            },
            {
                "id": "P02-ADV-002",
                "title": "Anti black-box: explicación forzada (Reflection)",
                "tech": "Reflection · Few-shot",
                "body": """El siguiente código fue generado con IA. El desarrollador DEBE poder defenderlo oralmente.

```<span class="pv">[código]</span>```

## Reflection (sin simplificar)
1. Explica el flujo de control en lenguaje natural (máx. 15 líneas).
2. Para cada función pública: precondición, postcondición, efectos secundarios.
3. Identifica 3 líneas que el desarrollador DEBE entender sin IA — si no puede, el código es black-box.
4. Propón refactor mínimo para reducir complejidad ciclomática > 10.

## Few-shot de salida
| Función | CC | ¿Explicable? | Acción |
|---------|----|--------------|--------|

Prohibido: "el código es correcto" sin evidencia.""",
            },
        ],
        "expected": "Informe de revisión con hallazgos consensuados, suite mínima de casos de prueba y registro de APIs verificadas.",
        "validation": """<ul>
<li>Código ejecutado localmente sin errores en happy path</li>
<li>≥80% de criterios P01 verificados con evidencia</li>
<li>Lista de APIs validadas contra documentación oficial</li>
<li>Complejidad ciclomática documentada para funciones críticas</li>
</ul>""",
        "metrics": [
            ("≥2/3", "Passes con consenso"),
            ("≥8", "Casos de prueba definidos"),
            ("0", "Critical sin mitigar"),
        ],
        "audit": """<ul>
<li>¿Cada hallazgo Critical tiene test o fix asociado?</li>
<li>¿Se probó al menos un caso borde no contemplado por la IA?</li>
<li>¿El desarrollador explica el código línea crítica sin leer comentarios IA?</li>
</ul>""",
        "evidence": "EVID-P02: review-report.md · test-plan.md · salida de tests · captura ejecución",
        "iso_link": '<a href="iso-evaluation.html">fiab_*, mant_*</a>',
    },
    3: {
        "code": "P03-SEC",
        "title": "Auditoría de seguridad y cumplimiento",
        "subtitle": "Evaluación OWASP Top 10, protección de datos y controles antes de merge o entrega.",
        "objective": "Aplicar auditoría de seguridad estructurada al código asistido por IA, mapeando hallazgos a OWASP e ISO 25010 Seguridad/Protección.",
        "risk": "Vulnerabilidades OWASP (inyección, XSS, secrets); exposición de PII en logs; dependencias con CVEs críticos.",
        "standards": [
            ("OWASP Top 10 2021", "owasp"),
            ("ISO 25010 · Seguridad", "iso"),
            ("ISO 25010 · Protección", "iso"),
            ("Ley 1581 / GDPR", "iso"),
            ("CWE/SANS Top 25", "eng"),
        ],
        "technique_name": "Adversarial prompting + Tree-of-thoughts",
        "technique_tags": ["Adversarial", "ToT", "CoT"],
        "prompts": [
            {
                "id": "P03-ADV-001",
                "title": "Auditoría OWASP adversarial (rol atacante)",
                "tech": "Adversarial · ToT",
                "body": """Modo dual obligatorio:

## Rol 1 — Desarrollador defensor
Describe brevemente el sistema y el código:
<span class="pv">[contexto + código o rutas críticas]</span>

## Rol 2 — Atacante (Adversarial)
Asume que el código fue escrito por un LLM optimista. Intenta explotar:
- A01 Broken Access Control
- A02 Cryptographic Failures
- A03 Injection (SQL/NoSQL/OS)
- A05 Security Misconfiguration
- A06 Vulnerable Components
- A07 Auth failures
- A09 Logging failures

Por cada categoría OWASP aplicable:
1. Vector de ataque concreto (payload ejemplo, NO ejecutar)
2. Línea o módulo vulnerable
3. Severidad CVSS estimada (baja/media/alta/crítica)
4. Remediación con patrón seguro (parametrización, CSP, etc.)

## Rol 3 — Auditor neutro
Consolida en matriz | OWASP | Hallazgo | ISO 25010 | Fix | Estado |

Prohibido: consejos genéricos sin referencia al código subido.""",
            },
            {
                "id": "P03-ADV-002",
                "title": "SBOM y deuda de dependencias (Few-shot)",
                "tech": "Few-shot · CoT",
                "body": """Analiza dependencias del proyecto para amplificación de deuda técnica y CVEs.

## Input
- Gestor: <span class="pv">[npm / pip / maven / gradle]</span>
- Salida de audit: <span class="pv">[pegar npm audit / pip-audit / equivalente]</span>
- lockfile presente: <span class="pv">[sí/no]</span>

## CoT
1. Clasifica dependencias: directas vs transitivas.
2. Señala paquetes con mantenimiento dudoso o typosquatting risk.
3. Mapea CVEs a OWASP A06.

## Salida
Tabla | Paquete | Versión | CVE | Severidad | Acción (update/pin/replace) | ISO impacto |""",
            },
        ],
        "expected": "Informe de auditoría OWASP con matriz de hallazgos, remediaciones priorizadas y verificación de dependencias (npm audit / pip-audit).",
        "validation": """<ul>
<li>Matriz OWASP con ≥5 categorías evaluadas explícitamente</li>
<li>0 secretos hardcodeados (grep + revisión manual)</li>
<li>Dependencias: 0 vulnerabilidades Critical abiertas</li>
<li>Datos personales: principios Ley 1581 documentados</li>
</ul>""",
        "metrics": [
            ("0", "Secrets en repo"),
            ("0", "CVE Critical"),
            ("100%", "OWASP aplicables cubiertos"),
        ],
        "audit": """<ul>
<li>¿Cada hallazgo High+ tiene ticket o commit de fix?</li>
<li>¿Se ejecutó herramienta SAST o audit de dependencias?</li>
<li>¿Logs y errores no exponen PII?</li>
</ul>""",
        "evidence": "EVID-P03: owasp-audit.md · npm-audit.txt · lista de redacción de secrets",
        "iso_link": '<a href="iso-evaluation.html">seg_*, prot_*</a>',
    },
    4: {
        "code": "P04-SUP",
        "title": "Supervisión humana y trazabilidad de decisiones",
        "subtitle": "Registro de decisiones técnicas, ADRs y control del sesgo de automatización.",
        "objective": "Garantizar supervisión humana efectiva (UE Art. 14) documentando alternativas evaluadas y decisiones finales sobre código asistido.",
        "risk": "Sesgo de automatización; delegación de decisiones arquitectónicas; imposibilidad de auditar quién decidió qué.",
        "standards": [
            ("Reglamento UE · Art. 14", "iso"),
            ("ISO 25010 · Mantenibilidad", "iso"),
            ("SOLID · DIP/OCP", "eng"),
            ("ADR (Architecture Decision Records)", "eng"),
            ("NIST AI RMF · MANAGE", "iso"),
        ],
        "technique_name": "Reflection prompting + Meta-prompting",
        "technique_tags": ["Reflection", "Meta-prompt"],
        "prompts": [
            {
                "id": "P04-ADV-001",
                "title": "ADR asistido con reflexión de alternativas",
                "tech": "Reflection · CoT",
                "body": """Genera un Architecture Decision Record (ADR) en formato estándar.

## Decisión pendiente
<span class="pv">[ej. elegir Redis vs PostgreSQL para cola, ORM vs SQL raw]</span>

## Contexto
<span class="pv">[restricciones del proyecto]</span>

## Instrucción Reflection
Antes de recomendar:
1. Enumera 3 alternativas con pros/contras técnicos (rendimiento, mantenibilidad, seguridad, costo).
2. Para cada alternativa, indica qué principio SOLID favorece o compromete.
3. Declara explícitamente: "Como supervisor humano, rechazo/reviso la sugerencia X porque..."
4. Registra qué fragmentos fueron propuestos por IA vs. formulados por el humano.

## Formato ADR
- Estado: Propuesto | Aceptado
- Consecuencias positivas/negativas
- Métricas de validación post-implementación
- Enlace a evidencia ISO (mantenibilidad, flexibilidad)""",
            },
            {
                "id": "P04-ADV-002",
                "title": "Log de supervisión continua (meta-prompt)",
                "tech": "Meta-prompt",
                "body": """Genera plantilla de log de supervisión para sesión de desarrollo con IA.

## Formato por entrada
| Timestamp | Prompt ID | Fragmento IA/humano | Decisión humana | Evidencia (commit/test) |

Incluye 5 entradas de ejemplo realistas y reglas:
- Ningún merge sin fila de validación P02
- Ningún secret en prompt
- Vendor/modelo documentado (mitigar vendor dependence)

Salida: Markdown listo para docs/supervision-log.md""",
            },
        ],
        "expected": "ADR firmado con alternativas descartadas, rol humano explícito y plan de validación post-decisión.",
        "validation": """<ul>
<li>≥3 alternativas documentadas con trade-offs</li>
<li>Decisión final atribuida a responsable humano nombrado</li>
<li>Métrica de seguimiento definida (plazo ≤ 2 semanas)</li>
</ul>""",
        "metrics": [
            ("≥3", "Alternativas evaluadas"),
            ("1", "ADR por decisión mayor"),
            ("100%", "Decisiones con owner humano"),
        ],
        "audit": """<ul>
<li>¿El ADR existe antes del merge de la decisión?</li>
<li>¿Se puede reconstruir el hilo IA→humano→código?</li>
</ul>""",
        "evidence": "EVID-P04: docs/adr/NNNN-titulo.md · log-supervision.md",
        "iso_link": '<a href="iso-evaluation.html">mant_*, flex_*</a>',
    },
    5: {
        "code": "P05-ETH",
        "title": "Ética, autoría y cumplimiento académico",
        "subtitle": "Transparencia de uso de IA, PI, licencias y declaración formal de autoría.",
        "objective": "Asegurar autenticidad, transparencia y cumplimiento de políticas institucionales y Ley 23/1982 sobre autoría y licencias.",
        "risk": "Fraude académico; violación de licencias open source; plagio de código generado sin atribución.",
        "standards": [
            ("ISO 25010 · Autenticidad", "iso"),
            ("Ley 23 / PI", "iso"),
            ("IEEE 7000", "iso"),
            ("CONPES 4144", "iso"),
            ("Licencias OSS (MIT, GPL, etc.)", "eng"),
        ],
        "technique_name": "Meta-prompting + Chain-of-Thought",
        "technique_tags": ["Meta-prompt", "CoT"],
        "prompts": [
            {
                "id": "P05-ADV-001",
                "title": "Declaración de autoría y licencias (meta-prompt institucional)",
                "tech": "Meta-prompt · CoT",
                "body": """Plantilla para declaración formal de entrega académica/profesional.

## Datos del proyecto
- Autor humano: <span class="pv">[nombre]</span>
- Herramientas IA: <span class="pv">[ChatGPT, Copilot, Claude, etc.]</span>
- Porcentaje estimado asistencia IA: <span class="pv">[rango justificado]</span>

## CoT — Desglose de autoría
Para cada componente del repositorio:
1. ¿Fue diseñado por humano, generado por IA, o híbrido?
2. ¿Hubo revisión línea a línea? (sí/no + alcance)
3. ¿Licencia de dependencias compatible con entrega institucional?

## Salida
Documento "Declaración de Uso de IA" con:
- Secciones obligatorias universidad
- Tabla de componentes y autoría
- Riesgos éticos residuales y mitigación
- Firma y fecha

NO minimizar el uso de IA. Transparencia completa.""",
            },
            {
                "id": "P05-ADV-002",
                "title": "Matriz de compatibilidad de licencias OSS",
                "tech": "CoT · Few-shot",
                "body": """Analiza licencias de dependencias y código generado.

## Input
<span class="pv">[package.json / requirements.txt / lista manual]</span>

## CoT
1. Identifica licencias (MIT, Apache-2.0, GPL, AGPL, etc.).
2. Evalúa compatibilidad con entrega académica/comercial del proyecto.
3. Señala riesgos de copyleft y obligaciones de atribución.

## Salida
Matriz | Componente | Licencia | Compatible | Acción requerida |""",
            },
        ],
        "expected": "Declaración de uso de IA firmada, tabla de licencias de dependencias y verificación de compatibilidad OSS.",
        "validation": """<ul>
<li>Declaración incluye herramientas, prompts tipo y nivel de asistencia</li>
<li>Licencias de terceros inventariadas (SPDX o equivalente)</li>
<li>Política académica citada y cumplida</li>
</ul>""",
        "metrics": [
            ("100%", "Componentes con autoría"),
            ("100%", "Deps con licencia"),
            ("1", "Declaración firmada"),
        ],
        "audit": """<ul>
<li>¿La declaración coincide con el historial git y ADRs?</li>
<li>¿Hay código sin revisión humana declarado como propio?</li>
</ul>""",
        "evidence": "EVID-P05: declaracion-ia.pdf · LICENSES.md · SBOM si aplica",
        "iso_link": '<a href="iso-evaluation.html">seg_* (autenticidad)</a>',
    },
    6: {
        "code": "P06-CRT",
        "title": "Preservación del pensamiento crítico",
        "subtitle": "Autoevaluación cognitiva, brechas de conocimiento y plan de práctica autónoma.",
        "objective": "Contrarrestar dependencia cognitiva mediante reflexión estructurada y plan de mejora de competencias técnicas verificables.",
        "risk": "Erosión de competencias; incapacidad de resolver problemas medios sin IA; atrofia de debugging autónomo.",
        "standards": [
            ("ISO 25010 · Analizabilidad", "iso"),
            ("CONPES 4144 · talento digital", "iso"),
            ("IEEE 7000 · bienestar", "iso"),
            ("Deliberate practice (ciencia aprendizaje)", "eng"),
        ],
        "technique_name": "Reflection prompting + Few-shot",
        "technique_tags": ["Reflection", "Few-shot"],
        "prompts": [
            {
                "id": "P06-ADV-001",
                "title": "Autoevaluación cognitiva con plan de cierre de brechas",
                "tech": "Reflection · Few-shot",
                "body": """Cierra la sesión de desarrollo con IA con una autoevaluación honesta.

## Few-shot (ejemplo de formato esperado)
| Competencia | Sin IA (1-5) | Con IA (1-5) | Brecha |
| Autenticación JWT | 2 | 4 | Alta |
| Tests unitarios | 3 | 5 | Media |

## Tu sesión
Tareas realizadas: <span class="pv">[lista]</span>
Lo que delegaste a IA: <span class="pv">[lista]</span>

## Reflection obligatoria
1. ¿Qué concepto no podrías explicar en una defensa oral sin mirar la IA?
2. Define 2 ejercicios SIN IA para la próxima semana (tiempo, recurso, criterio éxito).
3. ¿Cómo cambiaría tu prompt inicial (P01) la próxima vez?

## Salida
Plan de práctica 7 días + riesgo cognitivo residual (bajo/medio/alto)""",
            },
        ],
        "expected": "Registro de autoevaluación, plan de práctica sin IA y acciones de mejora en prompts P01.",
        "validation": """<ul>
<li>Tabla de competencias completada con honestidad</li>
<li>≥2 ejercicios autónomos programados con fecha</li>
<li>Revisión de al menos 1 prompt anterior para mejora</li>
</ul>""",
        "metrics": [
            ("≤2", "Brechas altas sin plan"),
            ("≥2", "Ejercicios autónomos/semana"),
            ("1", "Registro por sesión"),
        ],
        "audit": """<ul>
<li>¿El plan es específico y medible, no genérico?</li>
<li>¿Hay seguimiento en la sesión siguiente?</li>
</ul>""",
        "evidence": "EVID-P06: autoeval-sesion-YYYYMMDD.md · plan-practica.md",
        "iso_link": '<a href="iso-evaluation.html">mant_* (analizabilidad)</a>',
    },
}


def inject_guide():
    path = ROOT / "guide_IA.html"
    html = path.read_text(encoding="utf-8")

    # Link framework css
    if "framework.css" not in html:
        html = html.replace(
            '<link rel="stylesheet" href="assets/styles.css">',
            '<link rel="stylesheet" href="assets/styles.css">\n  <link rel="stylesheet" href="assets/framework.css">',
            1,
        )

    # Replace intro hero
    html = re.sub(
        r'<section id="intro" class="section hero">.*?</section>',
        """<section id="intro" class="section hero">
  <p class="fw-hero-badge">FRAMEWORK METODOLÓGICO · v2.0 · 2025</p>
  <h1>Desarrollo, validación y auditoría<br><em>de software asistido por IA</em></h1>
  <p class="hero-lead">Handbook institucional para Ingeniería TIC: seis módulos operativos integrados con ISO/IEC 25010, OWASP Top 10, ingeniería de prompts avanzada y trazabilidad de evidencia. No sustituye el criterio profesional — lo fortalece.</p>
  <div class="hero-stats">
    <div class="stat-card"><div class="stat-num">6</div><div class="stat-label">Módulos P01–P06</div></div>
    <div class="stat-card"><div class="stat-num">10</div><div class="stat-label">Bloques por módulo</div></div>
    <div class="stat-card"><div class="stat-num">9</div><div class="stat-label">Características ISO 25010</div></div>
    <div class="stat-card"><div class="stat-num">10</div><div class="stat-label">OWASP en auditoría P03</div></div>
  </div>
  <div class="btn-group" style="margin-top: var(--sp-6);">
    <a href="framework.html" class="btn btn-primary">Ver arquitectura</a>
    <a href="#paso1" class="btn btn-secondary">Módulo P01</a>
  </div>
</section>""",
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Replace como-usar
    html = re.sub(
        r'<section id="como-usar" class="section">.*?</section>',
        """<section id="como-usar" class="section">
  <div class="s-eyebrow">Protocolo de ejecución</div>
  <div class="s-title">Flujo del <em>framework</em></div>
  <div class="s-lead">Ejecuta P01→P06 en orden. Cada módulo produce evidencia (EVID-P0N) que alimenta la evaluación ISO 25010. No avances si la validación técnica del módulo actual no está completa.</div>
  <div class="alert alert-info">
    <div class="alert-icon"><i data-lucide="info" class="icon-md"></i></div>
    <p><strong>Principio de responsabilidad:</strong> El ingeniero humano es accountable del artefacto entregado. La IA es un acelerador bajo supervisión — Reglamento UE Art. 14, NIST GOVERN.</p>
  </div>
  <div class="onboard-table-wrap">
    <table class="dt">
      <thead><tr><th>Módulo</th><th>Fase</th><th>Duración</th><th>Entregable</th><th>ISO / OWASP</th></tr></thead>
      <tbody>
        <tr><td class="td-step" data-step="1">P01 Definición</td><td>Pre-IA</td><td>15–30 min</td><td>Spec + threat model</td><td>Adecuación · Fiabilidad</td></tr>
        <tr><td class="td-step" data-step="2">P02 Validación</td><td>Post-output</td><td>20–45 min</td><td>Review + test plan</td><td>Fiabilidad · Mantenibilidad</td></tr>
        <tr><td class="td-step" data-step="3">P03 Seguridad</td><td>Pre-merge</td><td>20–40 min</td><td>Informe OWASP</td><td>Seguridad · OWASP</td></tr>
        <tr><td class="td-step" data-step="4">P04 Supervisión</td><td>Continuo</td><td>Continuo</td><td>ADR + log</td><td>Mantenibilidad</td></tr>
        <tr><td class="td-step" data-step="5">P05 Ética</td><td>Pre-entrega</td><td>10–20 min</td><td>Declaración IA</td><td>Autenticidad</td></tr>
        <tr><td class="td-step" data-step="6">P06 Pensamiento</td><td>Post-sesión</td><td>10–15 min</td><td>Autoevaluación</td><td>Analizabilidad</td></tr>
      </tbody>
    </table>
  </div>
  <p class="fw-trace"><a href="framework.html#matriz">Matriz de trazabilidad completa →</a></p>
</section>""",
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Replace all paso sections
    for n in range(1, 7):
        pattern = rf'<!-- ═══+ MÓDULO P0{n}|<!-- ═══+ PASO {n}|<!-- ═══════════════ PASO {n}.*?</section>\s*\n<!-- ═══'
        replacement = render_module(n, MODULES[n]) + "\n<!-- ═══"
        html = re.sub(
            rf'<!-- (?:═══+ MÓDULO P0{n}|═══+ PASO {n}|═══════════════ PASO {n}).*?</section>\s*\n(?=\s*<!-- ═══)',
            replacement + "\n",
            html,
            count=1,
            flags=re.DOTALL,
        )

    # Restaurar sección ISO + comparativa si fueron eliminadas
    if 'id="iso-eval"' not in html:
        iso_body = (ROOT / "iso-evaluation.html").read_text(encoding="utf-8")
        start = iso_body.find('<div class="eval-intro">')
        end = iso_body.find("</section>", iso_body.find("<!-- CHARACTERISTICS -->")) + len("</section>")
        iso_chunk = iso_body[start:end]
        # botones y resultado
        extra = iso_body[iso_body.find("<!-- BUTTONS -->") : iso_body.find("</main>")]
        iso_section = f"""
<div class="divider-text"><span>Capa de aseguramiento · ISO 25010</span></div>
<section id="iso-eval" class="section iso-eval-section">
  <div class="s-eyebrow">Integración framework → ISO</div>
  <div class="s-title">Evaluación de calidad <em>SQuaRE</em></div>
  <div class="s-lead">Los entregables EVID-P01…P06 alimentan esta autoevaluación. Responde tras completar los módulos aplicables.</div>
{iso_chunk}
{extra}
</section>

<div class="divider-text"><span>Síntesis</span></div>
<section id="comparativa" class="section">
  <div class="s-eyebrow">Trazabilidad</div>
  <div class="s-title">Matriz <em>módulo → entregable → estándar</em></div>
  <div class="comp-table-wrap">
    <table class="comp-t">
      <thead><tr><th>Módulo</th><th>Momento</th><th>Entregable</th><th>ISO 25010</th><th>OWASP / Norma</th></tr></thead>
      <tbody>
        <tr><td class="td-step" data-step="1">P01</td><td>Pre-IA</td><td>spec-v1.md · threat-model</td><td>Adecuación · Fiabilidad</td><td>NIST GOVERN</td></tr>
        <tr><td class="td-step" data-step="2">P02</td><td>Post-output</td><td>review-report · tests</td><td>Fiabilidad · Mantenibilidad</td><td>A03 Injection</td></tr>
        <tr><td class="td-step" data-step="3">P03</td><td>Pre-merge</td><td>owasp-audit.md</td><td>Seguridad · Protección</td><td>OWASP Top 10</td></tr>
        <tr><td class="td-step" data-step="4">P04</td><td>Continuo</td><td>ADR · log-supervisión</td><td>Mantenibilidad</td><td>UE Art. 14</td></tr>
        <tr><td class="td-step" data-step="5">P05</td><td>Pre-entrega</td><td>declaración-ia.pdf</td><td>Autenticidad</td><td>Ley 23 · CONPES</td></tr>
        <tr><td class="td-step" data-step="6">P06</td><td>Post-sesión</td><td>autoeval · plan práctica</td><td>Analizabilidad</td><td>IEEE 7000</td></tr>
      </tbody>
    </table>
  </div>
  <p class="fw-trace"><a href="framework.html#matriz">Ver matriz de trazabilidad extendida →</a></p>
</section>
"""
        html = html.replace("<!-- ═══ NORMATIVA ═══ -->", iso_section + "\n<!-- ═══ NORMATIVA ═══ -->")

    path.write_text(html, encoding="utf-8")
    print("guide_IA.html updated")


def write_pasos_summary():
    """Reescribe pasos.html con intro framework + enlace al handbook por módulo."""
    path = ROOT / "pasos.html"
    body_modules = ""
    for n, c in MODULES.items():
        body_modules += f"""
  <article class="paso-card fw-module" data-step="{n}" id="paso{n}">
    <div class="paso-head">
      <div class="paso-num-badge" data-step="{n}">0{n}</div>
      <div class="paso-head-info">
        <p class="fw-module-id">{c['code']}</p>
        <h3>{c['title']}</h3>
        <p>{c['subtitle']}</p>
      </div>
    </div>
    <div class="paso-body">
      <p>{c['objective'][:200]}…</p>
      <div class="fw-standards" style="margin: var(--sp-4) 0;">
        {''.join(f'<span class="fw-std {"fw-std-iso" if k=="iso" else "fw-std-owasp" if k=="owasp" else "fw-std-eng"}">{t}</span>' for t,k in c['standards'][:4])}
      </div>
      <p class="fw-technique" style="margin-bottom: var(--sp-4);">{c['technique_name']}</p>
      <a href="guide_IA.html#paso{n}" class="btn btn-primary">Abrir módulo completo (10 bloques + prompts)</a>
    </div>
  </article>
"""

    head = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Seis módulos operativos del framework de desarrollo y auditoría de software asistido por IA.">
  <title>Módulos P01–P06 — Framework IA</title>
  <link rel="stylesheet" href="assets/styles.css">
  <link rel="stylesheet" href="assets/framework.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js" defer></script>
</head>
<body>
<div id="progress-bar"></div>
<header class="header">
  <div class="header-content">
    <a href="index.html" class="header-logo"><span class="header-logo-mark" aria-hidden="true"></span><span>Framework IA</span></a>
    <nav class="header-nav" aria-label="Principal">
      <a href="index.html">Inicio</a>
      <a href="framework.html">Arquitectura</a>
      <a href="governance.html">Gobernanza</a>
      <a href="pasos.html" aria-current="page">Módulos</a>
      <a href="iso-evaluation.html">Evaluación ISO</a>
      <a href="normativa.html">Normativa</a>
      <a href="guide_IA.html">Handbook</a>
    </nav>
    <div class="header-actions">
      <button type="button" class="theme-toggle" aria-label="Cambiar tema"><i data-lucide="sun-moon" class="icon-md"></i></button>
    </div>
  </div>
</header>
<main class="main-container">
  <nav class="breadcrumb"><a href="index.html">Inicio</a><span class="breadcrumb-sep">/</span><span>Módulos</span></nav>
  <section class="hero" style="margin-bottom: var(--sp-10);">
    <p class="fw-hero-badge">MÓDULOS OPERATIVOS</p>
    <h1>Seis módulos <em>P01–P06</em></h1>
    <p class="hero-lead">Vista resumida. Cada módulo en el handbook incluye 10 bloques metodológicos, prompts de ingeniería avanzada, métricas, auditoría y evidencia trazable hacia ISO 25010.</p>
  </section>
"""

    foot = """
</main>
<footer class="footer"><div class="footer-content"><div class="footer-bottom">Framework metodológico · 2025</div></div></footer>
<button type="button" class="scroll-top" id="scrollTop" aria-label="Volver arriba" onclick="window.scrollTo({top:0,behavior:'smooth'})"><i data-lucide="arrow-up" class="icon-md"></i></button>
<script src="assets/app.js"></script>
</body>
</html>
"""

    path.write_text(head + body_modules + foot, encoding="utf-8")
    print("pasos.html rewritten")


if __name__ == "__main__":
    inject_guide()
    write_pasos_summary()
