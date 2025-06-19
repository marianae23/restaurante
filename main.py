from cliente.cliente import fazer_pedido, reservar_mesa
from menu import mostrar_menu

def menu_cliente():
    nome = input("👤 Informe seu nome: ")
    while True:
        print(f"\n👋 Olá, {nome}! Bem-vindo ao Restaurante.")
        print("1. Ver menu")
        print("2. Fazer pedido")
        print("3. Reservar mesa")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            mostrar_menu()
        elif opcao == "2":
            fazer_pedido(nome)
        elif opcao == "3":
            reservar_mesa(nome)
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_cliente()