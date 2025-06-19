import json
from typing import List, Dict

def carregar_menu(caminho_arquivo: str) -> List[Dict]:
    """
    Carrega o menu de um arquivo JSON.

    Parâmetros:
        caminho_arquivo (str): Caminho para o arquivo JSON do menu.

    Retorna:
        List[Dict]: Lista de pratos disponíveis.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo de menu não encontrado.")
        return []
    except json.JSONDecodeError:
        print("Erro: Arquivo de menu está mal formatado.")
        return []

def exibir_menu(menu: List[Dict]) -> None:
    """
    Exibe o menu de forma formatada no terminal.

    Parâmetros:
        menu (List[Dict]): Lista de pratos.
    """
    print("\n📋 MENU DO RESTAURANTE\n" + "-" * 30)
    for item in menu:
        print(f"{item['id']}. {item['nome']} - {item['categoria']} - €{item['preco']:.2f}")