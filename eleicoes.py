from .erros import ErroCadastro
from abc import ABC, abstractmethod



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




class Candidato(Eleitor, ABC):

    def __init__(self, nome, cpf, data_nascimento, titulo_eleitor, zona, secao, numero, partido):
        super().__init__(nome, cpf, data_nascimento, titulo_eleitor, zona, secao)
        self.validar_numero(numero)
        self.numero = numero
        self.partido = partido


    @abstractmethod
    def validar_numero(self, numero):
        pass




class Prefeito(Candidato):
    erros_validacao = 0

    @classmethod
    def incremento_erros(cls):
        cls.erros_validacao+=1

    def __init__(self, nome, cpf, data_nascimento, titulo_eleitor, zona, 
                 secao, numero, partido, cpf_vice, plano_governo):
        super().__init__(nome, cpf, data_nascimento, titulo_eleitor, zona, 
                 secao, numero, partido)

        if len(cpf_vice) != 11 or not cpf_vice.isdigit():
            raise ErroCadastro("Prefeito", "CPF VICE", cpf_vice)
        
        self.cpf_vice = cpf_vice
        self.plano_governo = plano_governo

    def validar_numero(self, numero):
        if len(numero) != 2 or not numero.isdigit():
            Prefeito.incremento_erros()
            raise ErroCadastro("Prefeito", "NUMERO", numero)


class Vereador(Candidato):
    erros_validacao = 0

    @classmethod
    def incremento_erros(cls):
        cls.erros_validacao+=1

    def __init__(self, nome, cpf, data_nascimento, titulo_eleitor, zona, 
                 secao, numero, partido, bairro, projeto_lei):

        super().__init__(nome, cpf, data_nascimento, titulo_eleitor, zona, 
                 secao, numero, partido)
        self.bairro = bairro
        self.projeto_lei = projeto_lei

    def validar_numero(self, numero):
        if len(numero) != 5 or not numero.isdigit():
            Vereador.incremento_erros()
            raise ErroCadastro("Vereador", "NUMERO", numero)



class Urna():
    def __init__(self, zona, secao, votos_prefeito, votos_vereador):
        self.zona = zona
        self.secao = secao
        self.votos_prefeito = votos_prefeito
        self.votos_vereador = votos_vereador

    def __add__(self, outra_urna):
        if not isinstance(outra_urna, Urna):
            return NotImplemented

        #Pesquisei e vou usar .copy() para nao direcinar o endereco
        #Do novo dicionario no antigo

        novos_votos_vereador = self.votos_vereador.copy()
        for candidato in outra_urna.votos_vereador:
            if candidato in novos_votos_vereador:
                novos_votos_vereador[candidato] += outra_urna.votos_vereador[candidato]
            else:
                novos_votos_vereador[candidato] = outra_urna.votos_vereador[candidato]

        novos_votos_prefeito = self.votos_prefeito.copy()
        for candidato in outra_urna.votos_prefeito:
            if candidato in novos_votos_prefeito:
                novos_votos_prefeito[candidato] += outra_urna.votos_prefeito[candidato]
            else:
                novos_votos_prefeito[candidato] = outra_urna.votos_prefeito[candidato]

        nova_urna = Urna(None, None, novos_votos_prefeito, novos_votos_vereador)
        return nova_urna
