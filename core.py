import requests

def fazer_url(pars, token):
    cabeca = {'accept': 'application/json', 'Authorization': 'Bearer ' + token, 'content-type': 'application/json;charset=utf-8'}
    ano = pars['ano']
    limite = 100
    offset = 0

    if ano > 2019 or ano < 2005:
        raise ValueError('O ano deve estar entre 2005 e 2019.')
    base_url = 'https://gateway.apilib.prefeitura.sp.gov.br/sg/licitacoes/v1/' + str(ano)
    
    if pars['limite']:
        limite = pars['limite']
        if limite > 10000 or limite <= 0:
            raise ValueError('O valor limite deve estar entre 1 e 10000')
   
    if pars['offset']:
        offset = pars['offset']
        if offset > 10000 or offset < 0:
            raise ValueError('O valor offset deve estar entre 0 e 10000')
    
    parametros = {'limite': limite, 'offset': offset} 
    response = requests.get(base_url, headers=cabeca, params=parametros)
    return response

