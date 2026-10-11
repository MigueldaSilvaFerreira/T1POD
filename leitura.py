from eleicao import Eleicao, ErroCadastro, Partido, Eleitor, Prefeito, Vereador, Urna, BRANCO

SEPARADOR = ";"
LINHAS_CABECALHO = 1  # ajustar quando souber o formato real


def _ler_linhas(caminho: str) -> list[str]:
    """Lê o arquivo, pula cabeçalho, linhas vazias e comentários."""
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo]
    return [l for l in linhas[LINHAS_CABECALHO:] if l and not l.startswith("#")]


def _separar(linha: str, tipo: str, esperado: int) -> list[str]:
    """Divide a linha em campos; se o número de colunas estiver errado, vira ErroCadastro."""
    campos = [c.strip() for c in linha.split(SEPARADOR)]
    if len(campos) != esperado:
        raise ErroCadastro(tipo, "LINHA", linha)
    return campos


def ler_partidos(caminho: str, eleicao: Eleicao) -> None:
    for linha in _ler_linhas(caminho):
        try:
            numero, sigla, nome, cnpj = _separar(linha, "Partido", 4)
            eleicao.inserir_partido(Partido(numero, sigla, nome, cnpj))
        except ErroCadastro as erro:
            eleicao.registrar_erro(str(erro))  # linha ignorada, segue o processamento


def _criar_eleitor(linha: str, eleicao: Eleicao) -> Eleitor:
    tipo = linha.split(SEPARADOR)[0].strip().upper()

    if tipo == "ELEITOR":
        _, nome, cpf, nasc, titulo, zona, secao = _separar(linha, "Eleitor", 7)
        return Eleitor(nome, cpf, nasc, titulo, zona, secao)

    if tipo in ("PREFEITO", "VEREADOR"):
        rotulo = tipo.capitalize()
        (_, nome, cpf, nasc, titulo, zona, secao,
         numero, num_partido, extra1, extra2) = _separar(linha, rotulo, 11)

        partido = eleicao.buscar_partido(num_partido)
        if partido is None:
            raise ErroCadastro(rotulo, "PARTIDO", num_partido)

        if tipo == "PREFEITO":  # extra1 = CPF do vice, extra2 = plano de governo
            return Prefeito(nome, cpf, nasc, titulo, zona, secao, numero, partido, extra1, extra2)
        # extra1 = bairro, extra2 = projeto de lei
        return Vereador(nome, cpf, nasc, titulo, zona, secao, numero, partido, extra1, extra2)

    raise ErroCadastro("Eleitor", "TIPO", tipo)


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
            zona, secao, voto_pref, voto_ver = _separar(linha, "Urna", 4)
            if not zona.isdigit():
                raise ErroCadastro("Urna", "ZONA", zona)
            if not secao.isdigit():
                raise ErroCadastro("Urna", "SECAO", secao)
        except ErroCadastro as erro:
            eleicao.registrar_erro(str(erro))
            continue

        urna = urnas.setdefault((zona, secao), Urna(zona, secao, {}, {}))
        _somar_voto(urna.votos_prefeito, voto_pref)
        _somar_voto(urna.votos_vereador, voto_ver)

    for urna in urnas.values():
        eleicao.inserir_urna(urna)