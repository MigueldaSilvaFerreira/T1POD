# Sistema de Eleição

Programa em Python que lê os dados de uma eleição municipal (partidos, eleitores/candidatos e votos das urnas), valida tudo e gera relatórios em arquivos de texto.

## Autores

- Miguel da Silva Ferreira – classes do pacote `eleicao` (`Partido`, `Eleitor`, `Candidato`, `Prefeito`, `Vereador`, `Urna`, `ErroCadastro`)
- Matheus – classe `Eleicao`, leitura dos arquivos (`leitura.py`), `app.py` e relatórios

## Requisitos

- Python 3.10 ou mais novo
- Nenhuma biblioteca externa

## Como executar

Rodar, no terminal, sempre a partir da pasta que tem o `app.py`, passando os três arquivos de entrada nessa ordem:

```
python3 app.py Input/Partidos.txt Input/Eleitores.txt Input/Urnas.txt
```

Ou, se estiver no Windows:

```
py app.py Input/Partidos.txt Input/Eleitores.txt Input/Urnas.txt
```

Os resultados são mostrados no terminal e salvos em arquivos de texto na pasta `output/`.

## Formato dos arquivos de entrada

Linhas em branco ou que começam com `#` são ignoradas. As linhas têm o formato `TIPO: campos`.

**Partidos.txt**

```
PARTIDO: numero,sigla,nome,cnpj
```

**Eleitores.txt**

```
ELEITOR: nome,cpf,nascimento,titulo,zona,secao
PREFEITO: nome,cpf,nascimento,titulo,zona,secao,numero,numero_partido,cpf_vice,plano_de_governo
VEREADOR: nome,cpf,nascimento,titulo,zona,secao,numero,numero_partido,bairro,projeto_de_lei
```

**Urnas.txt**

```
VOTO: zona,secao,titulo,cargo,numero
```

Cada linha é um voto. Se o número estiver vazio, é considerado voto em branco. Número que não é de nenhum candidato é voto nulo. Os votos são organizados por zona e seção.

## Validação

| Campo | Regra |
|---|---|
| Nome (partido e eleitor) | no máximo 50 caracteres |
| CNPJ | exatamente 14 dígitos |
| CPF e CPF do vice | exatamente 11 dígitos |
| Número do prefeito | 2 dígitos |
| Número do vereador | 5 dígitos |
| Partido do candidato | precisa existir em `Partidos.txt` |
| Zona e seção do voto | numéricas |

## Relatórios

- `eleitores.txt`: total de eleitores, de candidatos a prefeito e a vereador, e quantidade de eleitores por seção de cada zona.
- `partidos.txt`: total de partidos e quantos candidatos a prefeito e a vereador cada um tem.
- `urnas.txt`: votos válidos, brancos e nulos de cada urna, para prefeito e vereador.
- `resultado_geral.txt`: soma de todas as urnas, com o prefeito eleito e os 10 vereadores mais votados.
- `erros.txt`: todas as linhas rejeitadas, com a mensagem de erro, e a contagem de erros de validação por classe.
