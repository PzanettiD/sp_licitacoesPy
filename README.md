<center><h1>sp_licitacoesPy</h1></center>

## Simples wrapper, em desenvolvimento, para [API de licitações da Prefeitura de São Paulo](https://apilib.prefeitura.sp.gov.br/store/)

Este pacote foi feito para que não seja mais nescessário montar uma requisição manual (usando urrlib ou requests, por exemplo) para API. Agora basta algumas linhas de código.

```python
from sp_licitacoesPy import licitacoes
token = '------------' # Seu token aqui!

# Retorna uma lista com 35 licitações do ano de 2009.
dados = licitacoes.obter_dados(token, ano = 2009, quantidade = 35)
```

## Instalação e Uso

Para instalar, basta usar o [PyPi](https://pypi.org/):

```properties
você@máquina:$ pip install sp_licitacoesPy
```
