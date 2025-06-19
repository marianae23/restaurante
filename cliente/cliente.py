import json
from datetime import datetime
from menu import carregar_menu

MENU_PATH = "../menu.json"
RESERVAS_PATH = "reservas.json"
PEDIDOS_PATH = "pedidos.json"

def ver_menu():
    print("\n--- MENU DO RESTAURANTE ---")
    try:
        menu = carregar_menu()
        for i, item in enumerate(menu):
            print(f"{i + 1}. {item['nome']} - €{item['preco']:.2f}")
    except FileNotFoundError:
        print("❌ Menu não encontrado.")

def fazer_reserva(nome_cliente):
    print("\n--- RESERVAR MESA ---")
    data = input("Data da reserva (AAAA-MM-DD): ")
    hora = input("Hora da reserva (HH:MM): ")
    pessoas = input("Número de pessoas: ")

    try:
        datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("❌ Data ou hora inválida.")
        return

    nova_reserva = {
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

    reservas.append(nova_reserva)

    with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
        json.dump(reservas, f, indent=2, ensure_ascii=False)

    print("✅ Reserva feita com sucesso!")

def fazer_pedido_online(nome_cliente):
    menu = carregar_menu()
    pedido = []

    print("\n--- FAZER PEDIDO ONLINE ---")
    for i, item in enumerate(menu):
        print(f"{i + 1}. {item['nome']} - €{item['preco']:.2f}")

    while True:
        escolha = input("Digite o número do prato (ou ENTER para finalizar): ")
        if escolha == "":
            break
        try:
            idx = int(escolha) - 1
            if 0 <= idx < len(menu):
                pedido.append(menu[idx])
                print(f"✔ {menu[idx]['nome']} adicionado.")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")

    if not pedido:
        print("❌ Nenhum item selecionado.")
        return

    total = sum(item["preco"] for item in pedido)

    try:
        with open(PEDIDOS_PATH, "r", encoding="utf-8") as f:
            pedidos = json.load(f)
    except FileNotFoundError:
        pedidos = []

    pedidos.append({
        "cliente": nome_cliente,
        "itens": pedido,
        "total": total
    })

    with open(PEDIDOS_PATH, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=2, ensure_ascii=False)

    print(f"✅ Pedido realizado com sucesso! Total: €{total:.2f}")

def consultar_reservas(nome_cliente):
    print("\n--- MINHAS RESERVAS ---")
    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        print("❌ Nenhuma reserva encontrada.")
        return

    minhas_reservas = [r for r in reservas if r["cliente"].lower() == nome_cliente.lower()]

    if not minhas_reservas:
        print("🔍 Nenhuma reserva encontrada para este nome.")
        return

    for i, r in enumerate(minhas_reservas, 1):
        print(f"{i}. Data: {r['data']} - Hora: {r['hora']} - Pessoas: {r['pessoas']}")

def cancelar_reserva(nome_cliente):
    print("\n--- CANCELAR RESERVA ---")
    data = input("Informe a data da reserva a cancelar (AAAA-MM-DD): ")

    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        print("❌ Nenhuma reserva encontrada.")
        return

    reservas_antes = len(reservas)
    reservas = [r for r in reservas if not (r["cliente"].lower() == nome_cliente.lower() and r["data"] == data)]

    if len(reservas) == reservas_antes:
        print("❌ Reserva não encontrada para esse nome e data.")
        return

    with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
        json.dump(reservas, f, indent=2, ensure_ascii=False)

    print("✅ Reserva cancelada com sucesso!")

def menu_cliente():
    nome = input("Digite seu nome: ")
    while True:
        print("\n--- MENU DO CLIENTE ---")
        print("1. Ver menu")
        print("2. Reservar mesa")
        print("3. Fazer pedido online")
        print("4. Consultar reservas feitas")
        print("5. Cancelar reserva")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            ver_menu()
        elif opcao == "2":
            fazer_reserva(nome)
        elif opcao == "3":
            fazer_pedido_online(nome)
        elif opcao == "4":
            consultar_reservas(nome)
        elif opcao == "5":
            cancelar_reserva(nome)
        elif opcao == "0":
            print("Volte sempre!")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    menu_cliente()
