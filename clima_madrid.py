#!/usr/bin/env python3
"""Muestra el clima actual en Madrid usando la API publica de Open-Meteo.

No requiere API key ni dependencias externas (solo la libreria estandar).

Uso:
    python3 clima_madrid.py
    python3 clima_madrid.py --json
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://api.open-meteo.com/v1/forecast"

LATITUD = 40.4165
LONGITUD = -3.7026
ZONA_HORARIA = "Europe/Madrid"

# Codigos WMO devueltos por Open-Meteo en `weather_code`.
DESCRIPCIONES = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla engelante",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna intensa",
    56: "Llovizna engelante ligera",
    57: "Llovizna engelante intensa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia intensa",
    66: "Lluvia engelante ligera",
    67: "Lluvia engelante intensa",
    71: "Nieve ligera",
    73: "Nieve moderada",
    75: "Nieve intensa",
    77: "Granos de nieve",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    85: "Chubascos de nieve ligeros",
    86: "Chubascos de nieve intensos",
    95: "Tormenta",
    96: "Tormenta con granizo ligero",
    99: "Tormenta con granizo fuerte",
}


def obtener_clima(timeout=10):
    """Devuelve el bloque `current` de la respuesta de Open-Meteo."""
    params = urllib.parse.urlencode(
        {
            "latitude": LATITUD,
            "longitude": LONGITUD,
            "timezone": ZONA_HORARIA,
            "current": ",".join(
                [
                    "temperature_2m",
                    "apparent_temperature",
                    "relative_humidity_2m",
                    "precipitation",
                    "wind_speed_10m",
                    "weather_code",
                ]
            ),
        }
    )
    with urllib.request.urlopen(f"{API_URL}?{params}", timeout=timeout) as respuesta:
        datos = json.load(respuesta)
    return datos["current"]


def formatear(actual):
    descripcion = DESCRIPCIONES.get(actual["weather_code"], "Desconocido")
    return "\n".join(
        [
            f"Clima en Madrid ({actual['time'].replace('T', ' ')} hora local)",
            f"  Estado........: {descripcion}",
            f"  Temperatura...: {actual['temperature_2m']} °C",
            f"  Sensacion.....: {actual['apparent_temperature']} °C",
            f"  Humedad.......: {actual['relative_humidity_2m']} %",
            f"  Precipitacion.: {actual['precipitation']} mm",
            f"  Viento........: {actual['wind_speed_10m']} km/h",
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Clima actual en Madrid")
    parser.add_argument(
        "--json", action="store_true", help="imprime la respuesta cruda en JSON"
    )
    args = parser.parse_args()

    try:
        actual = obtener_clima()
    except urllib.error.URLError as error:
        print(f"Error al consultar la API: {error}", file=sys.stderr)
        return 1
    except (KeyError, ValueError) as error:
        print(f"Respuesta inesperada de la API: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(actual, indent=2, ensure_ascii=False))
    else:
        print(formatear(actual))
    return 0


if __name__ == "__main__":
    sys.exit(main())
