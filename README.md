# sp_licitacoesPy

## Simples wrapper, em desenvolvimento, para [API de licitações da Prefeitura de São Paulo](https://apilib.prefeitura.sp.gov.br/store/)

Este pacote foi feito para que não seja mais nescessário montar uma requisição manual (usando urrlib ou requests, por exemplo) para API. Agora basta algumas linhas de código:

```python
from sp_licitacoesPy import licitacoes
token = '------------' # Seu token aqui!

# Retorna uma lista com 35 licitações do ano de 2009.
dados = licitacoes.obter_dados(token, ano = 2009, quantidade = 35)
```

## Instalação e Uso

Para instalar, basta usar o [PyPi](https://pypi.org/):

```console
você@máquina:$ pip install sp_licitacoesPy
```

Agora, é nescessário criar uma conta na [Vitrine de APIs da Cidade de São Paulo](https://apilib.prefeitura.sp.gov.br/store/). É preciso se inscrever na API ***Licitacoes - v1***, e então gerar um token dentro de ***Applications*** na ***Default Application*** na aba ***Production Keys***, onde aparecerá um botão de gerar um ***Access Token***. 

Este token é necessário na verificação da solicitação para a API. Sem ele o pacote não funciona :/

*** Note *** que o ***Access Token*** gerado tem um tempo limite de 3600 segundos!
