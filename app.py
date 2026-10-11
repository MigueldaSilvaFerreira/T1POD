import sys

from eleicao import Eleicao
from leitura import ler_partidos, ler_eleitores, ler_urnas


def salvar(nome_arquivo: str, texto: str) -> None:
    with open(f"output/{nome_arquivo}", "w", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")


def main() -> None:
    if len(sys.argv) != 4:
        print("Uso: python3 app.py Partidos.txt Eleitores.txt Urnas.txt")
        sys.exit(1)

    _, arq_partidos, arq_eleitores, arq_urnas = sys.argv
    eleicao = Eleicao()

    try:
        ler_partidos(arq_partidos, eleicao)    # priemiros candidatos dependem dos partidos
        ler_eleitores(arq_eleitores, eleicao)
        ler_urnas(arq_urnas, eleicao)
    except FileNotFoundError as erro:
        print(f"Arquivo não encontrado: {erro.filename}")
        sys.exit(1)

    relatorios = {
        "eleitores.txt": eleicao.relatorio_eleitores(),
        "partidos.txt": eleicao.relatorio_partidos(),
        "urnas.txt": eleicao.relatorio_urnas(),
        "resultado_geral.txt": eleicao.relatorio_resultado_geral(),
        "erros.txt": eleicao.relatorio_erros(),
    }
    for nome, texto in relatorios.items():
        salvar(nome, texto)
        print(texto, "\n")


if __name__ == "__main__":
    main()