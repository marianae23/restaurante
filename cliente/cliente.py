import json

RESERVAS_PATH = "reservas.json"  # ← caminho relativo à pasta onde o script está

def reservar_mesa(nome_cliente):
    data = input("Data da reserva (DD/MM/AAAA): ")
    hora = input("Hora da reserva (HH:MM): ")
    pessoas = input("Número de pessoas: ")

    reserva = {
        "cliente": nome_cliente,
        "data": data,
        "hora": hora,
        "pessoas": pessoas
    }

    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        reservas = []

    reservas.append(reserva)

    with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
        json.dump(reservas, f, indent=2, ensure_ascii=False)

    print("✅ Reserva realizada com sucesso!")
