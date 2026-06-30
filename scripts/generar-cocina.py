#!/usr/bin/env python3
"""Genera preguntas y respuestas para el catálogo Cocina."""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preguntas_parrilla import PARRILLA_LIMPIEZA, PARRILLA_TRAMPAS

ROOT = Path(__file__).resolve().parent.parent
PREGUNTAS_PATH = ROOT / "data" / "cocina" / "preguntas.json"
RESPUESTAS_PATH = ROOT / "data" / "cocina" / "respuestas.json"

COCINA_PREGUNTAS = [
    ("cocina-01", "¿Cuál es el tiempo de cocción de la carne 10:1?", "39 segundos"),
    ("cocina-02", "¿Cuál es el tiempo de cocción de la carne 4:1?", "110 segundos"),
    ("cocina-03", "¿Cuál es el tiempo de cocción de la carne 3:1?", "158 segundos"),
    ("cocina-04", "¿Cuál es el tiempo de cocción del tocino?", "160 +/- 5 segundos"),
    ("cocina-05", "¿Cuál es el tiempo de cocción de las grilles?", "225 el primer lado y 165 segundos el segundo lado"),
    ("cocina-06", "¿Cuál es el gap de la carne 10:1?", "Inicial es de 0.225 y final de 0.290 por 20 segundos"),
    ("cocina-07", "¿Cuál es el gap de la carne 4:1?", "Inicial es de 0.400 y terminal es de 0.450 por 20 segundos"),
    ("cocina-08", "¿Cuál es el gap de la carne 3:1?", "0.510 y final es de 0.545 por 20 segundos"),
    ("cocina-09", "¿Cuál es el gap del derretido y tostado?", "415"),
    ("cocina-10", "¿Cada cuánto se evaporan las parrillas?", "Cada 15 minutos"),
    ("cocina-11", "¿Qué es lo que espera el cliente de las carnes?", "Bien cocinada, bien sazonada, bien jugosa"),
    ("cocina-12", "¿Cuál es el rango de temperatura de los auxiliares?", "0°F a -10°F"),
    ("cocina-13", "¿A qué temperatura deben cocinarse las carnes?", "155°F"),
    ("cocina-14", "¿Cuál es el tiempo máximo para sacar las carnes?", "18 segundos"),
    ("cocina-15", "¿Cuál es el tiempo de la carne en el UHC?", "10 minutos"),
    ("cocina-16", "¿Cuál es el tiempo máximo para colocar las carnes?", "10 segundos"),
    ("cocina-17", "¿Cuál es la vida útil de las tortas grilles?", "60 minutos"),
    ("cocina-18", "¿Cuál es la vida útil de las crispy?", "60 minutos"),
    ("cocina-19", "¿Cuál es la vida útil de los nuggets en el UHC?", "20 minutos"),
    ("cocina-20", "¿Cuál es la vida útil de las M pollos en el UHC?", "30 minutos"),
    ("cocina-21", "¿Cuál es el tiempo de vida útil de la crispy USA en el UHC?", "60 minutos"),
    ("cocina-22", "¿Cuál es el tiempo de cocción de los nuggets?", "3:30 segundos"),
    ("cocina-23", "¿Cuál es el tiempo de cocción de la M pollo?", "3 minutos"),
    ("cocina-24", "¿Cuál es el tiempo de cocción de la crispy?", "5:45 segundos"),
    ("cocina-25", "¿Cuál es el tiempo de cocción de la cebolla empanizada?", "1:30 segundos"),
    ("cocina-26", "¿Cuál es el tiempo de cocción de los plátanos?", "75 segundos"),
    ("cocina-27", "¿Cuál es el tiempo de cocción de los huevos muffin?", "150 segundos"),
    ("cocina-28", "¿Cuál es el tiempo de cocción del huevo revuelto?", "35 segundos"),
    ("cocina-29", "¿Cuál es el tiempo de cocción del huevo del huerto?", "75 segundos"),
    ("cocina-30", "¿Cuál es el tiempo de cocción del huevo doblados?", "85 segundos"),
    ("cocina-31", "¿Cuál es la temperatura de las parrillas?", "Superior de 425°F e inferior a 350°F"),
    ("cocina-32", "¿Cuál es la temperatura de las parrillas del desayuno?", "265°F"),
    ("cocina-33", "¿Cuál es el tiempo de cocción del jamón?", "De 8 a 10 segundos"),
    ("cocina-34", "¿Cuál es el tiempo de vida de los huevos en el UHC?", "20 minutos"),
    ("cocina-35", "¿Cuál es el tiempo de vida de los panes muffins en el UHC?", "20 minutos"),
    ("cocina-36", "¿Cuál es el tiempo de cocción de los panes muffins?", "De 3 a 4 de 50 a 55 segundos y de 4 a 6 de 55 a 70 segundos"),
    ("cocina-37", "¿Cuánto tarda en calentarse la tostadora universal?", "20 minutos"),
    ("cocina-38", "¿Cuánto tarda en calentarse las parrillas clamshell?", "20 minutos"),
    ("cocina-39", "¿Qué es la regla 24/2?", "Abastecer 24 horas de suministro de papel y un máximo de 2 horas de porciones congeladas en el congelador terrestre"),
    ("cocina-40", "¿Cuál es el tiempo de cocción de las salchichas?", "82 segundos"),
    ("cocina-41", "¿Cuál es la temperatura de la plancha de los hot cake?", "375°F"),
    ("cocina-42", "¿Cuál es el tiempo máximo para batir la mezcla de los hot cake?", "2 minutos"),
    ("cocina-43", "¿Cuántas onzas rinde un lote de hot cake?", "38.5 onzas"),
    ("cocina-44", "¿Qué cantidad de agua se le aplica a la mezcla de hot cake?", "48 onzas de agua fría"),
    ("cocina-45", "¿Cuáles son los utensilios para hacer mezcla de hot cake?", "Dispensador de hot cake, espátula para hot cake, recipiente medidor, taza blix, batidor de acero inoxidable, espátula de goma pastelera, plancha plana de 365°F y plancha de 375°F"),
    ("cocina-46", "¿Qué espera el cliente de los hot cake?", "Amarillo dorado, esponjoso y suave, bien uniformes"),
    ("cocina-47", "¿Cuál es el diámetro de los hot cake?", "De 12 a 13.5"),
    ("cocina-48", "¿Cuánto debe rendir una bolsa de hot cake?", "De 13 a 15"),
    ("cocina-49", "¿Qué espera el invitado de las carnes?", "Bien cocida, bien jugosa, bien sazonada"),
    ("cocina-50", "¿Cuáles son las características de calidad de la carne?", "Porciones ligeramente rosadas, fáciles de separar, planas, redondas, con grosor y diámetro uniforme"),
    ("cocina-51", "¿Cuáles son las características de la carne deshidratada?", "Color rojo brillante, café o blanco; difícil de separar; muchos cristales de hielo en la superficie"),
    ("cocina-52", "¿Cuál es la zona de temperatura de peligro?", "40°F a 140°F"),
    ("cocina-53", "¿Cuál es la temperatura del baño maría de los topping?", "133°F a 145°F"),
    ("cocina-54", "¿Cuál es la temperatura de las topineras?", "115°F a 125°F"),
    ("cocina-55", "¿Por cuánto se deben batir un McFlurry?", "De 5 a 8 segundos"),
    ("cocina-56", "¿Qué se usa como guía para abastecer el área de servicio?", "Daily"),
    ("cocina-57", "¿Cuál es la temperatura de la payera?", "150°F a 180°F"),
    ("cocina-58", "¿Qué espera el invitado de un buen pan?", "Pan caliente, bien tostado y sin aplastar"),
    ("cocina-59", "¿Qué hay que hacer en caso de que el pan esté lastimado?", "Notificar al gerente"),
    ("cocina-60", "¿Cuál es la temperatura de la placa A de la tostadora modelo HEBT-5V?", "520°F"),
    ("cocina-61", "¿Cuál es la temperatura de la placa B de la tostadora modelo HEBT-5V?", "520°F"),
    ("cocina-62", "¿Cuál es la temperatura de la placa C de la tostadora modelo HEBT-5V?", "490°F"),
    ("cocina-63", "¿Cuál es el tiempo de caramelizado del pan en la tostadora?", "22 segundos"),
    ("cocina-64", "¿Cuánto es el tiempo de calentamiento de la tostadora HEBT-5V?", "30 minutos"),
    ("cocina-65", "¿Cuánto es el tiempo de reacción al ver una orden en el KVS?", "5 segundos o menos"),
    *[(f"cocina-{66 + i}", preg, resp) for i, (_, preg, resp) in enumerate(PARRILLA_LIMPIEZA)],
]

TRAMPAS = [
    "39 segundos", "110 segundos", "158 segundos", "75 segundos", "82 segundos",
    "18 segundos", "10 segundos", "35 segundos", "85 segundos", "150 segundos",
    "20 minutos", "30 minutos", "60 minutos", "10 minutos", "2 minutos",
    "3 minutos", "3:30 segundos", "5:45 segundos", "1:30 segundos",
    "160 +/- 5 segundos", "225 el primer lado y 165 segundos el segundo lado",
    "155°F", "265°F", "375°F", "425°F", "350°F",
    "0°F a -10°F", "40°F a 140°F", "133°F a 145°F", "115°F a 125°F", "150°F a 180°F",
    "34°F a 40°F", "De 0 a -10 F", "De 40 a 140 F°",
    "Cada 15 minutos", "Cada 30 minutos", "20 minutos",
    "38.5 onzas", "48 onzas de agua fría", "De 12 a 13.5", "De 13 a 15",
    "415", "0.510 y final es de 0.545 por 20 segundos",
    "Bien cocida, bien sazonada, bien jugosa",
    "Bien cocida, bien jugosa, bien sazonada",
    "Daily", "Weekly", "FIFO",
    "De 5 a 8 segundos", "De 8 a 10 segundos",
    "Amarillo dorado, esponjoso y suave, bien uniformes",
    "Porciones muy oscuras y difíciles de separar",
    "Pan caliente, bien tostado y sin aplastar",
    "Pan frío y sin tostar",
    "Desecharlo sin avisar",
    "Notificar al gerente",
    "520°F", "490°F", "265°F", "375°F",
    "22 segundos", "30 minutos", "20 minutos",
    "5 segundos o menos", "10 segundos", "18 segundos",
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

    pool = {r for _, _, r in COCINA_PREGUNTAS}
    preguntas = []
    respuestas = {}

    for qid, pregunta, correcta in COCINA_PREGUNTAS:
        trampas = obtener_trampas(correcta, pool)
        while len(trampas) < 3:
            extra = f"Opción similar ({len(trampas) + 1})"
            if extra not in trampas:
                trampas.append(extra)
        opciones = trampas[:3] + [correcta]
        random.shuffle(opciones)

        preguntas.append({"id": qid, "pregunta": pregunta, "campo": "cocina"})
        respuestas[qid] = {
            "correcta": opciones.index(correcta),
            "opciones": opciones,
            "explicacion": f"La respuesta correcta es: {correcta}.",
        }

    PREGUNTAS_PATH.write_text(
        json.dumps({"catalogo": "cocina", "preguntas": preguntas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    RESPUESTAS_PATH.write_text(
        json.dumps({"catalogo": "cocina", "respuestas": respuestas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Generadas {len(preguntas)} preguntas de cocina")


if __name__ == "__main__":
    main()
