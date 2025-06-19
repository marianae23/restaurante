import json
from datetime import datetime

MENU_PATH = "menu.json"
RESERVAS_PATH = "reservas.json"
PEDIDOS_PATH = "pedidos.json"
AVALIACOES_PATH = "avaliacoes.json"

def ver_menu():
    try:
        with open(MENU_PATH, "r", encoding="utf-8") as f:
            menu = json.load(f)
    except FileNotFoundError:
        print("❌ Menu não disponível no momento.")
        return
    print("\n--- MENU ---")
    for prato in menu:
        print(f"{prato['nome']} - €{prato['preco']:.2f}")

def reservar_mesa(nome_cliente):
    data = input("Data da reserva (AAAA-MM-DD): ")
    hora = input("Hora da reserva (HH:MM): ")
    try:
        datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("Formato de data ou hora inválido.")
        return
    reserva = {
        "cliente": nome_cliente,
        "data": data,
        "hora": hora
    }
    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        reservas = []
    reservas.append(reserva)
    with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
        json.dump(reservas, f, indent=4)
    print("Reserva efetuada com sucesso!")

def consultar_reservas(nome_cliente):
    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        print("Nenhuma reserva encontrada.")
        return
    reservas_cliente = [r for r in reservas if r["cliente"].lower() == nome_cliente.lower()]
    if not reservas_cliente:
        print("Você não tem reservas feitas.")
        return
    print("\n--- Suas Reservas ---")
    for i, r in enumerate(reservas_cliente, 1):
        print(f"{i}. Data: {r['data']} Hora: {r['hora']}")

def cancelar_reserva(nome_cliente):
    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        print("Nenhuma reserva para cancelar.")
        return
    reservas_cliente = [r for r in reservas if r["cliente"].lower() == nome_cliente.lower()]
    if not reservas_cliente:
        print("Você não tem reservas para cancelar.")
        return
    print("\n--- Cancelar Reserva ---")
    for i, r in enumerate(reservas_cliente, 1):
        print(f"{i}. Data: {r['data']} Hora: {r['hora']}")
    try:
        escolha = int(input("Escolha o número da reserva para cancelar: "))
        if 1 <= escolha <= len(reservas_cliente):
            reserva_para_cancelar = reservas_cliente[escolha - 1]
            reservas.remove(reserva_para_cancelar)
            with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
                json.dump(reservas, f, indent=4)
            print("Reserva cancelada com sucesso.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")

def avaliar_pedido(nome_cliente):
    try:
        with open(PEDIDOS_PATH, "r", encoding="utf-8") as f:
            pedidos = json.load(f)
    except FileNotFoundError:
        print("Nenhum pedido encontrado para avaliação.")
        return
    pedidos_cliente = [p for p in pedidos if p["cliente"].lower() == nome_cliente.lower()]
    if not pedidos_cliente:
        print("Você não tem pedidos para avaliar.")
        return
    print("\n--- Avaliar Pedido ---")
    for i, pedido in enumerate(pedidos_cliente, 1):
        itens_str = ", ".join(f"{item['nome']} (x{item['quantidade']})" for item in pedido["itens"])
        print(f"{i}. Data: {pedido.get('data', 'N/D')} - Itens: {itens_str} - Total: €{pedido['total']:.2f}")
    try:
        escolha = int(input("Escolha o número do pedido para avaliar: "))
        if 1 <= escolha <= len(pedidos_cliente):
            nota = int(input("Dê uma nota de 1 a 5: "))
            if 1 <= nota <= 5:
                comentario = input("Comentário: ")
                avaliacao = {
                    "cliente": nome_cliente,
                    "pedido": pedidos_cliente[escolha - 1],
                    "nota": nota,
                    "comentario": comentario,
                    "data_avaliacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                try:
                    with open(AVALIACOES_PATH, "r", encoding="utf-8") as f:
                        avaliacoes = json.load(f)
                except FileNotFoundError:
                    avaliacoes = []
                avaliacoes.append(avaliacao)
                with open(AVALIACOES_PATH, "w", encoding="utf-8") as f:
                    json.dump(avaliacoes, f, indent=4)
                print("Avaliação registrada. Obrigado pelo feedback!")
            else:
                print("Nota inválida.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")

def consultar_historico_pedidos(nome_cliente):
    print("\n--- HISTÓRICO DE PEDIDOS ---")
    try:
        with open(PEDIDOS_PATH, "r", encoding="utf-8") as f:
            pedidos = json.load(f)
    except FileNotFoundError:
        print("❌ Nenhum pedido encontrado.")
        return

    pedidos_cliente = [p for p in pedidos if p["cliente"].lower() == nome_cliente.lower()]

    if not pedidos_cliente:
        print("Você ainda não realizou pedidos.")
        return

    for i, pedido in enumerate(pedidos_cliente, 1):
        itens_str = ", ".join(f"{item['nome']} (x{item['quantidade']})" for item in pedido["itens"])
        print(f"{i}. Data: {pedido.get('data', 'N/D')} - Itens: {itens_str} - Total: €{pedido['total']:.2f}")

def menu_cliente():
    nome = input("Digite seu nome: ")
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1. Ver menu")
        print("2. Fazer reserva")
        print("3. Consultar reservas")
        print("4. Cancelar reserva")
        print("5. Consultar histórico de pedidos")
        print("6. Avaliar pedido")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            ver_menu()
        elif opcao == "2":
            reservar_mesa(nome)
        elif opcao == "3":
            consultar_reservas(nome)
        elif opcao == "4":
            cancelar_reserva(nome)
        elif opcao == "5":
            consultar_historico_pedidos(nome)
        elif opcao == "6":
            avaliar_pedido(nome)
        elif opcao == "7":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_cliente()
