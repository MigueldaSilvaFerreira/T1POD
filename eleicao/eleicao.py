from .eleicoes import Partido, Eleitor, Prefeito, Vereador, Urna

BRANCO = "BRANCO"


def _ordem(valor: str) -> tuple[int, int | str]:
    """Ordena numericamente quando der, senão como texto."""
    return (0, int(valor)) if valor.isdigit() else (1, valor)


class Eleicao:
    def __init__(self) -> None:
        self.partidos: list[Partido] = []
        self.eleitores: list[Eleitor] = []  # inclui os candidatos
        self.urnas: list[Urna] = []
        self.erros: list[str] = []

    def inserir_partido(self, partido: Partido) -> None:
        self.partidos.append(partido)

    def inserir_eleitor(self, eleitor: Eleitor) -> None:
        self.eleitores.append(eleitor)

    def inserir_urna(self, urna: Urna) -> None:
        self.urnas.append(urna)

    def registrar_erro(self, mensagem: str) -> None:
        self.erros.append(mensagem)

    def buscar_partido(self, numero: str) -> Partido | None:
        for partido in self.partidos:
            if partido.numero == numero:
                return partido
        return None

# auxiliares 
    def _prefeitos(self) -> list[Prefeito]:
        return [e for e in self.eleitores if isinstance(e, Prefeito)]

    def _vereadores(self) -> list[Vereador]:
        return [e for e in self.eleitores if isinstance(e, Vereador)]

    @staticmethod
    def _classificar(votos: dict[str, int], validos: set[str]) -> tuple[int, int, int]:
        """Devolve (válidos, brancos, nulos) de um dicionário de votos."""
        n_validos = n_brancos = n_nulos = 0
        for chave, qtd in votos.items():
            if chave == BRANCO:
                n_brancos += qtd
            elif chave in validos:
                n_validos += qtd
            else:
                n_nulos += qtd
        return n_validos, n_brancos, n_nulos

  # 19.1 eleitores 
    def relatorio_eleitores(self) -> str:
        linhas = [
            "RELATÓRIO DE ELEITORES",
            f"Total de eleitores: {len(self.eleitores)}",
            f"Total de candidatos a prefeito: {len(self._prefeitos())}",
            f"Total de candidatos a vereador: {len(self._vereadores())}",
            "",
            "Seções por zona:",
        ]
        zonas: dict[str, dict[str, int]] = {}
        for eleitor in self.eleitores:
            secoes = zonas.setdefault(eleitor.zona, {})
            secoes[eleitor.secao] = secoes.get(eleitor.secao, 0) + 1

        for zona in sorted(zonas, key=_ordem):
            linhas.append(f"Zona {zona}:")
            for secao in sorted(zonas[zona], key=_ordem):
                linhas.append(f"  Seção {secao}: {zonas[zona][secao]} eleitores")
        return "\n".join(linhas)

# 19.2 partidos
    def relatorio_partidos(self) -> str:
        linhas = ["RELATÓRIO DE PARTIDOS", f"Total de partidos: {len(self.partidos)}", ""]
        for partido in self.partidos:
            n_pref = sum(1 for c in self._prefeitos() if c.partido.numero == partido.numero)
            n_ver = sum(1 for c in self._vereadores() if c.partido.numero == partido.numero)
            linhas.append(
                f"{partido.nome} ({partido.sigla}): "
                f"{n_pref} candidato(s) a prefeito, {n_ver} a vereador"
            )
        return "\n".join(linhas)

# 19.3 urnas 
    def relatorio_urnas(self) -> str:
        nums_pref = {c.numero for c in self._prefeitos()}
        nums_ver = {c.numero for c in self._vereadores()}
        linhas = ["RELATÓRIO DE URNAS"]
        for urna in self.urnas:
            vp, bp, np_ = self._classificar(urna.votos_prefeito, nums_pref)
            vv, bv, nv = self._classificar(urna.votos_vereador, nums_ver)
            linhas += [
                "",
                f"Urna zona {urna.zona}, seção {urna.secao}",
                f"  Prefeito: {vp} válidos, {bp} brancos, {np_} nulos",
                f"  Vereador: {vv} válidos, {bv} brancos, {nv} nulos",
            ]
        return "\n".join(linhas)

# 19.4 resultado geral 
    def relatorio_resultado_geral(self) -> str:
        total = Urna(None, None, {}, {})  # usa o __add__ do Miguel
        for urna in self.urnas:
            total = total + urna

        prefeitos = {p.numero: p.nome_eleitor for p in self._prefeitos()}
        vereadores = {v.numero: v.nome_eleitor for v in self._vereadores()}

        linhas = ["RESULTADO GERAL", "", "Prefeito:"]
        votos_pref = {n: q for n, q in total.votos_prefeito.items() if n in prefeitos}
        validos = sum(votos_pref.values())
        if validos > 0:
            top = max(votos_pref, key=lambda n: votos_pref[n])
            if votos_pref[top] * 2 >= validos:  # pelo menos 50% dos válidos
                linhas.append(f"  Eleito: {prefeitos[top]} ({votos_pref[top]} de {validos} votos válidos)")
            else:
                linhas.append("  Segundo Turno")
        else:
            linhas.append("  Segundo Turno")

        linhas += ["", "10 vereadores mais votados:"]
        ranking = [(n, q) for n, q in total.votos_vereador.items() if n in vereadores]
        ranking.sort(key=lambda par: (-par[1], vereadores[par[0]]))  # desempate por nome
        for numero, qtd in ranking[:10]:
            linhas.append(f"  {vereadores[numero]} (nº {numero}): {qtd} votos")
        return "\n".join(linhas)

# 19.5 erros 
    def relatorio_erros(self) -> str:
        linhas = ["RELATÓRIO DE ERROS", f"Total de mensagens: {len(self.erros)}"]
        linhas += [f"  - {mensagem}" for mensagem in self.erros]
        linhas += [
            "",
            "Contadores de erros de validação:",
            f"  Partido: {Partido.erros_validacao}",
            f"  Prefeito: {Prefeito.erros_validacao}",
            f"  Vereador: {Vereador.erros_validacao}",
        ]
        return "\n".join(linhas)