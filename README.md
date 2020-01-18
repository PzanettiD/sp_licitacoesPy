# sp_licitacoesPy

## Simples wrapper, em desenvolvimento, para [API de licitações da Prefeitura de São Paulo](https://apilib.prefeitura.sp.gov.br/store/)

Este pacote foi feito para que não seja mais nescessário montar uma requisição manual (usando urrlib ou requests, por exemplo) para API. Agora basta algumas linhas de código:

```python
from sp_licitacoesPy import licitacoes
token = '------------' # Seu token aqui!

# Retorna uma lista com 35 licitações do ano de 2009.
dados = licitacoes.obter_dados(token, ano = 2009, quantidade = 35)
```

## Instalação

Para instalar, basta usar o [PyPi](https://pypi.org/):

```console
você@máquina:$ pip install sp_licitacoesPy
```

Agora, é nescessário criar uma conta na [Vitrine de APIs da Cidade de São Paulo](https://apilib.prefeitura.sp.gov.br/store/). É preciso se inscrever na API ***Licitacoes - v1***, e então gerar um token dentro de ***Applications*** na ***Default Application*** na aba ***Production Keys***, onde aparecerá um botão de gerar um ***Access Token***. 

> Este token é necessário na verificação da solicitação para a API. Sem ele o pacote não funciona :/

> **Note** que o ***Access Token*** gerado tem um tempo limite de 3600 segundos!

## Uso

Todas as funções nescessárias estão dentro de um único arquivo *licitacoes.py* dentro do pacote. São duas as funções mais importantes:

+ resposta_json()

   - Esta função constrói um URL para solicitação à API, e retorna a resposta JSON em um dicionário.

+ obter_dados()

   - Esta função que "limpa" a resposta JSON da API, e retorna uma lista de dicionários com as licitações.

#### Parâmetros para ambas as funções:

| token           | ano = 2008         | quantidade = 1| offset = 0 |
|:-------------:  |:------------------:|:-------------:|:----------:|
| **obrigatório** | *opcional*         | *opcional*    | *opcional* |
| *str*           | *int*              | *int*         | *int*      |
| deve ser válido | 2008<= ano <= 2019 | < 10.000      | < 10.000   |

> ***Note*** que o valor quatidade + offset também não pode ser superior ao de 10.000

+ **token**: é aquele gerado pela próptia Vitirine de APIs. Se este não for válido, resultará em um erro "Token_Invalido"

+ **ano**: o ano da(s) licitação(ões) desejada(s), este deve estar entre 2008 e 2019. O valor padrão é o ano de 2008.

+ **quantidade**: a quatidade de licitações desejadas, que não deve ultrapassar 10.000. O valor padrão é de 1 (uma licitação apenas).

+ **offset**: se refere a paginação da base de dados das licitações, este não deve ultrapassar o valor de 10.000. O valor padrão é de 0.
