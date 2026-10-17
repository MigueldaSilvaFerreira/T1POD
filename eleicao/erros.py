class ErroCadastro(Exception):
    def __init__(self, objeto: str, campo: str, valor: str, relato: str) -> None:
        mensagem = f"Erro em {objeto}: campo '{campo}' inválido. Valor {valor} {relato}."
        super().__init__(mensagem)