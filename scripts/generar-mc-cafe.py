#!/usr/bin/env python3
"""Genera preguntas.json y respuestas.json para Mc Café desde productos.json."""

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from medidas_recetas import MEDIDAS_RECETAS

PRODUCTOS_PATH = ROOT / "data" / "mc-cafe" / "productos.json"
PREGUNTAS_PATH = ROOT / "data" / "mc-cafe" / "preguntas.json"
RESPUESTAS_PATH = ROOT / "data" / "mc-cafe" / "respuestas.json"

CAMPOS_DEFAULT = ["temperatura", "tiempo_primario", "tiempo_secundario", "despues_abierto"]

PLANTILLAS = {
    "temperatura": "¿Qué temperatura debe tener el {nombre}?",
    "tiempo_primario": "¿Cuál es el tiempo de vida primario del {nombre}?",
    "tiempo_secundario": "¿Cuál es el tiempo de vida secundario del {nombre}?",
    "despues_abierto": "¿Cuál es el tiempo de vida después de abierto del {nombre}?",
}

LABELS = {
    "temperatura": "la temperatura",
    "tiempo_primario": "el tiempo de vida primario",
    "tiempo_secundario": "el tiempo de vida secundario",
    "despues_abierto": "el tiempo de vida después de abierto",
}

TRAMPAS_SERVICIO = [
    "Arriba de 170°F",
    "165°F +/- 5°F",
    "195°F +/- 5°F",
    "34 a 40 F",
    "34°F o 40°F",
    "4°C",
    "150 a 170 F",
    "150°F o 170°F",
    "150 a 170°F",
    "160°F +/- 5°F",
    "190°F +/- 5°F",
    "0 a -10 F",
]

TRAMPAS = {
    "temperatura": [
        "Ambiente",
        "34 a 40 F",
        "0 a -10 F",
        "34°F o 40°F",
        "Congelador",
        "Cuarto frio",
        "Cooler",
    ],
    "tiempo_primario": [
        "6 meses", "180 dias", "3 años", "60 dias", "542 dias", "540 dias", "365 dias",
        "2 meses", "120 dias", "90 dias", "30 dias", "N/A",
    ],
    "tiempo_secundario": [
        "7 dias", "6 horas", "72 horas", "96 horas", "48 horas", "15 dias", "3 dias",
        "12 horas", "90 dias", "6 meses", "1 mes", "5 dias",
        "48 horas incluyendo 1 de enfriamiento", "N/A",
    ],
    "despues_abierto": [
        "7 dias", "5 dias", "48 horas", "12 horas", "90 dias", "6 meses", "1 mes", "3 dias", "N/A",
    ],
}

TRAMPAS_MEDIDAS = [
    "1 Oz. de azúcar", "1.5 Oz. de azúcar", "2 Oz. de leche", "3 Oz. de leche",
    "4 Oz. de leche", "6 Oz. de leche", "8 Oz. de leche", "10 Oz. de leche",
    "1 Oz. de expreso", "1.5 Oz. de expreso", "2 Oz. de expreso", "3 Oz. de expreso", "4 Oz. de expreso",
    "1 Oz. de syrup", "1.5 Oz. de syrup", "2 Oz. de syrup", "0.75 Oz. de syrup",
    "1 Oz. de chocolate", "1.5 Oz. de chocolate", "2 Oz. de chocolate",
    "3 disparos de 1.5 Oz.", "4 disparos de 2 Oz.", "5 disparos de 1.25 Oz.", "8 disparos de 2 Oz.",
    "3 cucharones", "4 cucharones", "5 cucharones", "1 cucharon",
    "4 Oz. de agua/leche", "4 Oz. de base de fruta", "5 Oz. de base de fruta",
    "2 Oz. de oreo", "1/2 Oz. de azúcar",
    "lleva 2 Oz. de leche y 3 disparos de 1.5 Oz. de azúcar",
    "lleva 6 Oz. de leche y 1 Oz. de expreso",
    "lleva 10 Oz. de leche y 2 Oz. de expreso",
]


def normalizar(valor: str) -> str:
    if not valor or str(valor).strip() == "":
        return "N/A"
    return str(valor).strip()


def obtener_trampas(campo: str, correcta: str, pool: set[str]) -> list[str]:
    candidatos = [v for v in pool if v != correcta]
    trampas_fijas = [t for t in TRAMPAS[campo] if t != correcta]
    mezcla = list(dict.fromkeys(candidatos + trampas_fijas))
    random.shuffle(mezcla)
    return mezcla[:3]


def obtener_trampas_medidas(correcta: str, pool: set[str]) -> list[str]:
    candidatos = [v for v in pool if v != correcta]
    trampas_fijas = [t for t in TRAMPAS_MEDIDAS if t != correcta]
    mezcla = list(dict.fromkeys(candidatos + trampas_fijas))
    random.shuffle(mezcla)
    return mezcla[:3]


def agregar_pregunta_simple(preguntas, respuestas, qid, item, pool_medidas, campo="medida_receta"):
    correcta = item["respuesta"]
    trampas = obtener_trampas_medidas(correcta, pool_medidas)
    while len(trampas) < 3:
        extra = f"Medida alternativa ({len(trampas) + 1})"
        if extra not in trampas and extra != correcta:
            trampas.append(extra)
    opciones = trampas[:3] + [correcta]
    random.shuffle(opciones)
    preguntas.append({
        "id": qid,
        "producto": "Recetas Mc Café",
        "campo": campo,
        "pregunta": item["pregunta"],
    })
    respuestas[qid] = {
        "correcta": opciones.index(correcta),
        "opciones": opciones,
        "explicacion": f"La medida correcta es: {correcta}.",
    }


def main() -> None:
    random.seed(42)

    with PRODUCTOS_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    productos = data["productos"]

    pools = {campo: set() for campo in CAMPOS_DEFAULT}
    for p in productos:
        for campo in CAMPOS_DEFAULT:
            pools[campo].add(normalizar(p.get(campo, "N/A")))

    preguntas = []
    respuestas = {}

    for p in productos:
        campos = p.get("campos_quiz", CAMPOS_DEFAULT)
        nombre_q = p.get("nombre_pregunta", p["nombre"]).lower()
        nombre = p["nombre"]

        for campo in campos:
            if campo not in PLANTILLAS:
                continue

            qid = f"mc-cafe-{p['id']}-{campo}"
            correcta = normalizar(p.get(campo, "N/A"))
            pregunta_texto = PLANTILLAS[campo].format(nombre=nombre_q)

            preguntas.append({
                "id": qid,
                "producto": nombre,
                "campo": campo,
                "pregunta": pregunta_texto,
            })

            trampas = obtener_trampas(campo, correcta, pools[campo])
            while len(trampas) < 3:
                extra = f"Opción similar ({len(trampas) + 1})"
                if extra not in trampas and extra != correcta:
                    trampas.append(extra)

            opciones = trampas[:3] + [correcta]
            random.shuffle(opciones)

            label = LABELS[campo]
            lugar = p.get("lugar", "")
            explicacion = f"Para {nombre_q}, {label} correcto es: {correcta}."
            if lugar:
                explicacion += f" Lugar de almacenamiento: {lugar}."

            respuestas[qid] = {
                "correcta": opciones.index(correcta),
                "opciones": opciones,
                "explicacion": explicacion,
            }

    for b in data.get("bebidas_servicio", []):
        qid = f"mc-cafe-{b['id']}"
        correcta = b["respuesta"]
        trampas = [t for t in TRAMPAS_SERVICIO if t != correcta]
        random.shuffle(trampas)
        opciones = trampas[:3] + [correcta]
        random.shuffle(opciones)

        preguntas.append({
            "id": qid,
            "producto": b.get("producto", "Bebida"),
            "campo": "temperatura_servicio",
            "pregunta": b["pregunta"],
        })
        respuestas[qid] = {
            "correcta": opciones.index(correcta),
            "opciones": opciones,
            "explicacion": b["explicacion"],
        }

    pool_medidas = {m["respuesta"] for m in MEDIDAS_RECETAS}
    for m in MEDIDAS_RECETAS:
        qid = f"mc-cafe-medida-{m['id']}"
        agregar_pregunta_simple(preguntas, respuestas, qid, m, pool_medidas)

    PREGUNTAS_PATH.write_text(
        json.dumps({"catalogo": "mc-cafe", "preguntas": preguntas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    RESPUESTAS_PATH.write_text(
        json.dumps({"catalogo": "mc-cafe", "respuestas": respuestas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Generadas {len(preguntas)} preguntas en {PREGUNTAS_PATH.name}")
    print(f"Generadas {len(respuestas)} respuestas en {RESPUESTAS_PATH.name}")


if __name__ == "__main__":
    main()
