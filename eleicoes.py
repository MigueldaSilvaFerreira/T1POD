from .erros import ErroCadastro




class Partido:
    erros_validacao = 0

    @classmethod
    def incremento_erros(cls):
        cls.erros_validacao+=1


    def __init__(self, numero, sigla, nome, cnpj):

        if len(nome) > 50:
            Partido.incremento_erros()
            raise ErroCadastro("Partido", "NOME", nome)

        if len(cnpj) != 14 or not cnpj.isdigit():
            Partido.incremento_erros()
            raise ErroCadastro("Partido", "CNPJ", cnpj)
        
        self.numero = numero
        self.sigla = sigla
        self._nome = nome
        self._cnpj = cnpj


    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, novo_nome):
        if len(novo_nome) > 50:
            raise ErroCadastro("Partido", "NOME", novo_nome)
        self._nome = novo_nome

    @property
    def cnpj(self):
        return self._cnpj
    @cnpj.setter
    def cnpj(self, novo_cnpj):
        if len(novo_cnpj) != 14 or not novo_cnpj.isdigit():
            raise ErroCadastro("Partido", "CNPJ", novo_cnpj)
        self._cnpj = novo_cnpj

class Eleitor:
    
    def __init__(self, nome_eleitor, cpf, data_nascimento, titulo_eleitor, zona, secao):

        if len(nome_eleitor) > 50:
            raise ErroCadastro("Eleitor", "NOME", nome_eleitor)

        if len(cpf) != 11 or not cpf.isdigit():
            raise ErroCadastro("Eleitor", "CPF", cpf)

        self._nome_eleitor = nome_eleitor
        self._cpf = cpf
        self.data_nascimento = data_nascimento
        self.titulo_eleitor = titulo_eleitor
        self.zona = zona
        self.secao = secao

    @property
    def nome_eleitor(self):
        return self._nome_eleitor
    @nome_eleitor.setter
    def nome_eleitor(self, novo_nome):
        if len(novo_nome) > 50:
            raise ErroCadastro("Eleitor", "NOME", novo_nome)
        self._nome_eleitor = novo_nome

    @property
    def cpf(self):
        return self._cpf
    @cpf.setter
    def cpf(self, novo_cpf):
        if len(novo_cpf) != 11 or not novo_cpf.isdigit():
            raise ErroCadastro("Eleitor", "CPF", novo_cpf)
        self._cpf = novo_cpf
