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
