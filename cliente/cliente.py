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
        print("\n--- MENU ---")
        for item in menu:
            print(f"{item['id']}. {item['nome']} - €{item['preco']:.2f}")
    except FileNotFoundError:
        print("❌ Menu não disponível no momento.")

def reservar_mesa(nome):
    data = input("Digite a data da reserva (YYYY-MM-DD): ")
    hora = input("Digite a hora da reserva (HH:MM): ")
    try:
        reservas = []
        try:
            with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
                reservas = json.load(f)
        except FileNotFoundError:
            pass
        reserva = {
            "cliente": nome,
            "data": data,
            "hora": hora
        }
        reservas.append(reserva)
        with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
            json.dump(reservas, f, indent=2, ensure_ascii=False)
        print("✅ Reserva feita com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar reserva: {e}")

def consultar_reservas(nome):
    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
        reservas_cliente = [r for r in reservas if r["cliente"].lower() == nome.lower()]
        if reservas_cliente:
            print("\n--- Suas reservas ---")
            for r in reservas_cliente:
                print(f"Data: {r['data']}, Hora: {r['hora']}")
        else:
            print("Você não tem reservas.")
    except FileNotFoundError:
        print("Nenhuma reserva encontrada.")

def cancelar_reserva(nome):
    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        print("Nenhuma reserva encontrada.")
        return
    reservas_cliente = [r for r in reservas if r["cliente"].lower() == nome.lower()]
    if not reservas_cliente:
        print("Você não tem reservas para cancelar.")
        return
    print("\n--- Suas reservas ---")
    for i, r in enumerate(reservas_cliente, 1):
        print(f"{i}. Data: {r['data']}, Hora: {r['hora']}")
    escolha = input("Escolha o número da reserva para cancelar: ")
    try:
        idx = int(escolha) - 1
        if idx < 0 or idx >= len(reservas_cliente):
            print("Escolha inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    reserva_a_cancelar = reservas_cliente[idx]
    reservas = [r for r in reservas if r != reserva_a_cancelar]
    with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
        json.dump(reservas, f, indent=2, ensure_ascii=False)
    print("Reserva cancelada com sucesso!")

def avaliar_pedido(nome_cliente):
    print("\n--- AVALIAR PEDIDO ---")
    try:
        with open(PEDIDOS_PATH, "r", encoding="utf-8") as f:
            pedidos = json.load(f)
    except FileNotFoundError:
        print("❌ Nenhum pedido encontrado.")
        return

    pedidos_cliente = [p for p in pedidos if p["cliente"].lower() == nome_cliente.lower()]

    if not pedidos_cliente:
        print("❌ Você não tem pedidos para avaliar.")
        return

    for i, pedido in enumerate(pedidos_cliente, 1):
        itens_str = ", ".join(item["nome"] for item in pedido["itens"])
        print(f"{i}. Pedido com itens: {itens_str} - Total: €{pedido['total']:.2f}")

    escolha = input("Escolha o número do pedido que quer avaliar: ")
    try:
        idx = int(escolha) - 1
        if idx < 0 or idx >= len(pedidos_cliente):
            print("❌ Escolha inválida.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    nota = input("Digite a nota para o pedido (1 a 5): ")
    try:
        nota_int = int(nota)
        if nota_int < 1 or nota_int > 5:
            print("❌ Nota deve ser entre 1 e 5.")
            return
    except ValueError:
        print("❌ Nota inválida.")
        return

    comentario = input("Deixe um comentário sobre o pedido: ")

    avaliacao = {
        "cliente": nome_cliente,
        "pedido_id": idx,  # Considerar aprimorar com ID real do pedido
        "nota": nota_int,
        "comentario": comentario,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(AVALIACOES_PATH, "r", encoding="utf-8") as f:
            avaliacoes = json.load(f)
    except FileNotFoundError:
        avaliacoes = []

    avaliacoes.append(avaliacao)

    with open(AVALIACOES_PATH, "w", encoding="utf-8") as f:
        json.dump(avaliacoes, f, indent=2, ensure_ascii=False)

    print("✅ Obrigado pela avaliação!")

def menu_cliente():
    nome = input("Digite seu nome: ")
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1. Ver menu")
        print("2. Fazer reserva")
        print("3. Consultar reservas")
        print("4. Cancelar reserva")
        print("5. Sair")
        print("6. Avaliar pedido")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            ver_menu()
        elif opcao == "2":
            reservar_mesa(nome)
        elif opcao == "3":
            consultar_reservas(nome)
        elif opcao == "4":
            cancelar_reserva(nome)
        elif opcao == "6":
            avaliar_pedido(nome)
        elif opcao == "5":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_cliente()
