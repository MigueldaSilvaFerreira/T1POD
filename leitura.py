from eleicao import Eleicao, ErroCadastro, Partido, Eleitor, Prefeito, Vereador, Urna, BRANCO

SEPARADOR = ","
LINHAS_CABECALHO = 0  # ajustar quando souber o formato real


def _ler_linhas(caminho: str) -> list[str]:
    """Lê o arquivo, pula cabeçalho, linhas vazias e comentários."""
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo]
    return [l for l in linhas[LINHAS_CABECALHO:] if l and not l.startswith("#")]

def _dividir_tipo(linha: str, objeto: str) -> tuple[str, str]:
    """divide o tipo, exemplo: ELEITOR: Rogerio ...  -> 'ELEITOR' 'Rogerio ...'."""
    if ":" not in linha:
        raise ErroCadastro(objeto, "LINHA", linha[:60], "não tem o formato 'TIPO: campos'")
    
    tipo, resto = linha.split(":", 1)
    return tipo.strip().upper(), resto.strip()

def _separar(linha: str, tipo: str, esperado: int) -> list[str]:
    """Divide a linha em campos; se o número de colunas estiver errado, vira ErroCadastro."""
    campos = [c.strip() for c in linha.split(SEPARADOR)]
    if len(campos) != esperado:
        raise ErroCadastro(tipo, "LINHA", linha, f"deve ter exatamente {esperado} campos")
    return campos


def ler_partidos(caminho: str, eleicao: Eleicao) -> None:
    for linha in _ler_linhas(caminho):
        try:
            _ , resto = _dividir_tipo(linha, "Partido")
            numero, sigla, nome, cnpj = _separar(resto, "Partido", 4)
            eleicao.inserir_partido(Partido(numero, sigla, nome, cnpj))
        except ErroCadastro as erro:
            eleicao.registrar_erro(str(erro))  # linha ignorada, segue o processamento


def _criar_eleitor(linha: str, eleicao: Eleicao) -> Eleitor:
    tipo, resto = _dividir_tipo(linha, "Eleitor")

    if tipo == "ELEITOR":
        nome, cpf, nasc, titulo, zona, secao = _separar(resto, "Eleitor", 6)
        return Eleitor(nome, cpf, nasc, titulo, zona, secao)

    if tipo in ("PREFEITO", "VEREADOR"):
        rotulo = tipo.capitalize()
        (nome, cpf, nasc, titulo, zona, secao,
         numero, num_partido, extra1, extra2) = _separar(resto, rotulo, 10)

        partido = eleicao.buscar_partido(num_partido)
        if partido is None:
            raise ErroCadastro(rotulo, "PARTIDO", num_partido, "não corresponde a nenhum partido cadastrado")

        if tipo == "PREFEITO":  # extra1 = CPF do vice, extra2 = plano de governo
            return Prefeito(nome, cpf, nasc, titulo, zona, secao, numero, partido, extra1, extra2)
        # extra1 = bairro, extra2 = projeto de lei
        return Vereador(nome, cpf, nasc, titulo, zona, secao, numero, partido, extra1, extra2)

    raise ErroCadastro("Eleitor", "TIPO", tipo, "deve ser ELEITOR, PREFEITO ou VEREADOR")


def ler_eleitores(caminho: str, eleicao: Eleicao) -> None:
    for linha in _ler_linhas(caminho):
        try:
            eleicao.inserir_eleitor(_criar_eleitor(linha, eleicao))
        except ErroCadastro as erro:
            eleicao.registrar_erro(str(erro))


def _somar_voto(votos: dict[str, int], valor: str) -> None:
    chave = valor if valor else BRANCO
    votos[chave] = votos.get(chave, 0) + 1


def ler_urnas(caminho: str, eleicao: Eleicao) -> None:
    urnas: dict[tuple[str, str], Urna] = {}  

    for linha in _ler_linhas(caminho):
        try:
            tipo , resto = _dividir_tipo(linha, "Urna")
            if tipo != "VOTO":
                raise ErroCadastro("Urna", "TIPO", tipo, "deve ser VOTO")
            zona, secao, _, cargo, numero = _separar(resto, "Urna", 5)
            if not zona.isdigit():
                raise ErroCadastro("Urna", "ZONA", zona, "deve ser numérica")
            if not secao.isdigit():
                raise ErroCadastro("Urna", "SECAO", secao, "deve ser numérica")
            if cargo not in ("PREFEITO","VEREADOR"):
                raise ErroCadastro("Urna", "CARGO",cargo, "deve ser um cargo válido")
        except ErroCadastro as erro:
            eleicao.registrar_erro(str(erro))
            continue

        urna = urnas.setdefault((zona, secao), Urna(zona, secao, {}, {}))
        if cargo == "PREFEITO":
            _somar_voto(urna.votos_prefeito, numero)
        else:
            _somar_voto(urna.votos_vereador, numero)


    for urna in urnas.values():
        eleicao.inserir_urna(urna)