#!/usr/bin/env python3
import collections
import pathlib
import subprocess
import tempfile

from typing import Any


def notify(msg):
    print(msg)
    subprocess.run(["notify-send", msg], check=True)


def capture_area_screenshot_to_filename(filename):
    subprocess.run(["gnome-screenshot", "-a", "-f", filename], check=True)


def scan_barcode_from_filename(filename) -> str:
    cmd = ["zbarimg", "-q", "--raw", str(filename)]
    try:
        barcode = subprocess.run(
            cmd, encoding="ascii", errors="replace", stdout=subprocess.PIPE, check=True
        ).stdout
    except subprocess.CalledProcessError as e:
        if e.returncode == 4:
            return ""
        else:
            raise
    return barcode.strip()


def mod10_digit(digits: str) -> str:
    "Modulo 10"
    alternating_multiplication = [
        int(digit) * (position % 2 + 1)
        for position, digit in enumerate(reversed(digits), start=1)
    ]
    digits_sum = sum(sum(divmod(part, 10)) for part in alternating_multiplication)
    digit = (10 - (digits_sum % 10)) % 10
    return str(digit)


def append_mod10_digit(digits: str) -> str:
    return digits + mod10_digit(digits)


BOLETO_FIELD_LENGTH_MAP = dict(
    banco_moeda=1 + 3,
    digito_vencimento_valor=1 + 4 + 10,
    campo_livre_1_5=5,
    campo_livre_6_15=10,
    campo_livre_16_25=10,
)


BoletoFields = collections.namedtuple(  # type: ignore
    "BoletoFields", BOLETO_FIELD_LENGTH_MAP.keys()
)


BOLETO_FIELD_INDEX_MAP = {}


current_index = 0
for name, length in BOLETO_FIELD_LENGTH_MAP.items():
    BOLETO_FIELD_INDEX_MAP[name] = (current_index, current_index + length)
    current_index += length


del current_index, name, length


def get_typeable_line_from_barcode(barcode: str):
    if barcode[0:1] == "8":
        # Convênio:
        # https://portal.febraban.org.br/pagina/3166/33/pt-br/layour-arrecadacao
        return " ".join(
            append_mod10_digit(barcode[i * 11 : (i + 1) * 11]) for i in range(4)
        )
    # Boleto
    # https://boletobancario-codigodebarras.blogspot.com/2016/04/linha-digitavel.html
    f: Any = BoletoFields(
        *(barcode[start:end] for start, end in BOLETO_FIELD_INDEX_MAP.values())
    )
    typeable = "".join(
        (
            append_mod10_digit(f.banco_moeda + f.campo_livre_1_5),
            append_mod10_digit(f.campo_livre_6_15),
            append_mod10_digit(f.campo_livre_16_25),
            f.digito_vencimento_valor,
        )
    )

    return typeable


def send_to_clipboard(line: str):
    subprocess.Popen(
        ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, encoding="ascii"
    ).communicate(line)


def main():
    notify("Drag to capture barcode from screen")
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = pathlib.Path(tmpdir) / "screenshot.png"
        capture_area_screenshot_to_filename(filename)

        if not filename.is_file():
            notify("Barcode scan operation canceled")
            return 1

        barcode: str = scan_barcode_from_filename(filename)
        if not barcode:
            notify("No barcode found")
            return 4

    if len(barcode) != 44 or not barcode.isdigit():
        notify(f"Bad barcode or incorrect scan: {barcode!r}")
        return 2

    typeable_line = get_typeable_line_from_barcode(barcode)
    send_to_clipboard(typeable_line)
    notify(f"Scanned barcode to clipboard: {typeable_line}")


if __name__ == "__main__":
    print("starting")
    raise SystemExit(main())
