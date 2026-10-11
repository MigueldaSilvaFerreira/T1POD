class ErroCadastro(Exception):
    def __init__(self, objeto, campo, valor):
        mensagem = f"Erro em {objeto}: campo '{campo}' inválido. Valor {valor} não está no formato correto."
        super().__init__(mensagem)