#!/usr/bin/env python3
"""Genera preguntas y respuestas para el catálogo Limpieza."""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preguntas_parrilla import PARRILLA_LIMPIEZA, PARRILLA_TRAMPAS

ROOT = Path(__file__).resolve().parent.parent
PREGUNTAS_PATH = ROOT / "data" / "limpieza" / "preguntas.json"
RESPUESTAS_PATH = ROOT / "data" / "limpieza" / "respuestas.json"

LIMPIEZA_PREGUNTAS = [
    (
        "limpieza-01",
        "¿Cada cuánto deben limpiarse las superficies de contacto?",
        "Según el cronograma (varias veces al día)",
    ),
    (
        "limpieza-02",
        "¿Qué color de paño usar para áreas de comida?",
        "El designado para alimentos (según código de colores)",
    ),
    (
        "limpieza-03",
        "¿Dónde va el trapo sucio después de usarlo?",
        "Al área de lavado designada",
    ),
]

TRAMPAS = [
    "Una vez al mes", "Según el cronograma (varias veces al día)", "Nunca", "Solo si hay suciedad visible",
    "El que haya", "El designado para alimentos (según código de colores)", "Paño de baño", "Cualquiera",
    "En el piso", "Al área de lavado designada", "En la basura de clientes", "Guardado en el bolsillo",
    *PARRILLA_TRAMPAS,
]


def obtener_trampas(correcta: str, pool: set[str]) -> list[str]:
    candidatos = [v for v in pool if v != correcta]
    fijas = [t for t in TRAMPAS if t != correcta]
    mezcla = list(dict.fromkeys(candidatos + fijas))
    random.shuffle(mezcla)
    return mezcla[:3]


def main() -> None:
    random.seed(42)
    PREGUNTAS_PATH.parent.mkdir(parents=True, exist_ok=True)

    todas = LIMPIEZA_PREGUNTAS + PARRILLA_LIMPIEZA
    pool = {r for _, _, r in todas}
    preguntas = []
    respuestas = {}

    for qid, pregunta, correcta in todas:
        trampas = obtener_trampas(correcta, pool)
        while len(trampas) < 3:
            extra = f"Opción similar ({len(trampas) + 1})"
            if extra not in trampas:
                trampas.append(extra)
        opciones = trampas[:3] + [correcta]
        random.shuffle(opciones)

        full_id = qid if qid.startswith("limpieza-") else f"limpieza-{qid}"

        preguntas.append({"id": full_id, "pregunta": pregunta, "campo": "limpieza"})
        respuestas[full_id] = {
            "correcta": opciones.index(correcta),
            "opciones": opciones,
            "explicacion": f"La respuesta correcta es: {correcta}.",
        }

    PREGUNTAS_PATH.write_text(
        json.dumps({"catalogo": "limpieza", "preguntas": preguntas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    RESPUESTAS_PATH.write_text(
        json.dumps({"catalogo": "limpieza", "respuestas": respuestas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Generadas {len(preguntas)} preguntas de limpieza")


if __name__ == "__main__":
    main()
