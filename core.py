# Dependência (https://requests.readthedocs.io/pt_BR/latest/user/quickstart.html)
import requests

# Exceção personalizada:
class Token_Invalido(Exception):

    '''
    Essa exceção deve ser levantada quando
    o token do usuário não é válido, ou seja
    a página retorna o código 401 (não autorizado).
    '''

    err_message = "Parece que o seu Token não é valido, para gerar outro vá para https://apilib.prefeitura.sp.gov.br/"


# Função que constroi um URL para solicitação e 
# envia-o para a API, indexando a resposta JSON
# em um dicionário.
def fazer_url(token, ano = 2008, quantidade = 1, offset = 0):
    
    '''
    Inicialmente a função formata uma solicitação para a API
    da prefeitura, incluindo os parâmetros desejados na busca.
    Depois, usando o 'requests', é possível obter o retorno JSON
    e assim endereça-lo à um dicionário.

    token -> (string) Token do usuário, este é único e pode ser gerado à 
    partir de uma inscrição em https://apilib.prefeitura.sp.gov.br/
    (o token tem tempo para expiração!).
    
    ano -> (integer) O ano de coleta dos dados, note que só estão disponíveis
    os anos de 2005 à 2009. VALOR PADRÃO = 2008.

    quantidade -> (integer) O número de licitações que vão ser retornadadas
    ao dicionário, sendo o máximo 10.000 (alguns anos possuem mais de
    10.000 licitações, porém a própria API não consegue alcançar estes
    dados). VALOR PADRÃO = 1.

    offset -> (integer) Utilizado para a paginação - Número do registro
    a partir do qual serão retornados os dados. VALOR PADRÃO = 0.

    '''
    
    # Cria um dicionário que oferecerá os parâmetros pré definidos pela API para os requests,
    # o token está já incluso aqui no segundo parâmetro.
    cabeca = {'accept': 'application/json', 'Authorization': 'Bearer ' + token, 'content-type': 'application/json;charset=utf-8'}
    
    # Confere se o ano está dentro do disponível na base de dados e se é do tipo integer.
    if ano > 2019 or ano < 2005 or type(ano) != int:
        raise ValueError('O ano deve estar entre 2005 e 2019.')
    
    # Concatena o ano à própria url, já que o parâmetro ano é dificilmente acessado pelo GET to HTTP.
    base_url = 'https://gateway.apilib.prefeitura.sp.gov.br/sg/licitacoes/v1/' + str(ano)
    
    # Confere se a quantidade está dentro do disponível na base de dados, 
    # caso for maior, o request retorna o código 404, pois não há mais conteúdo JSON,
    # acho que é um bug da API.
    if quantidade > 10000 or quantidade <= 0 or type(quantidade) != int:
        raise ValueError('A quantidade deve estar entre 1 e 10000')
   
    # Confere se a offset está dentro do suportado pela API, igual ao anterior.
    if offset > 10000 or offset < 0 or type(offset) != int:
        raise ValueError('O valor offset deve estar entre 0 e 10000')
    
    # Endereça os valores finais à um dicionário, requerido para fazer a solicitação.
    parametros = {'limite': quantidade, 'offset': offset} 
   
    # Faz o pedido através do 'requests' usando o cabeçalho (header) criado e os
    # parâmetros necessários.
    resposta = requests.get(base_url, headers=cabeca, params=parametros)
   
    # Avalia caso o token está inválido, normalmento neste caso a API retorna o código
    # 401 e uma JSON com mensagem de erro.
    if resposta.status_code == 401:
        raise Token_Invalido(Token_Invalido.err_message)
    
    # Cria um dicionário a partir do parser de JSON integrado ao 'requests'.
    resposta_dict = resposta.json() 
    
    # Retorna uma lista de dicionários (cada dicionário é uma licitação diferente, que possuem valores,
    # diferentes).
    return resposta_dict['data']

