from menu import carregar_menu, exibir_menu

def main():
    caminho_menu = 'data/menu.json'
    menu = carregar_menu(caminho_menu)
    if menu:
        exibir_menu(menu)

if __name__ == '__main__':
    main()