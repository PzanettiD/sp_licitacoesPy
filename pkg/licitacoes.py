# Dependência (https://requests.readthedocs.io/pt_BR/latest/user/quickstart.html)
import requests

# Exceção personalizada:
class Token_Invalido(Exception):

    '''
    Essa exceção deve ser levantada quando
    se há problemas relacionados ao token.
    O token pode ser invalido por:
        1. Não ser da forma str.
        2. Não ser válido pela API.
    '''

    err_message = "Parece que o seu Token não é valido, para gerar outro vá para https://apilib.prefeitura.sp.gov.br/"
    err_message2 = "Parece que o seu token não é do tipo STR."


# Função que constroi um URL para solicitação e 
# envia-o para a API, indexando a resposta JSON
# em um dicionário.
def resposta_json(token, ano = 2008, quantidade = 1, offset = 0):
    
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
    
    # Cria um dicionário que oferecerá os parâmetros pré definidos (do header) pela API para os requests,
    # confere se o token é do tipo str, e o concatena a o segundo parâmetro do cabeçalho.
    if type(token) != str:
        raise Token_Invalido(Token_Invalido.err_message2)
    cabeca = {'accept': 'application/json', 'Authorization': 'Bearer ' + token, 'content-type': 'application/json;charset=utf-8'}

    # Confere se o ano está dentro do disponível na base de dados e se é do tipo integer.
    if type(ano) != int or ano > 2019 or ano < 2005:
        raise ValueError('O ano deve estar entre 2005 e 2019. E precisa ser do tipo integer (int)!')
    
    # Concatena o ano à própria url, já que o parâmetro ano é dificilmente acessado pelo GET to HTTP.
    base_url = 'https://gateway.apilib.prefeitura.sp.gov.br/sg/licitacoes/v1/' + str(ano)
    
    # Confere se a quantidade está dentro do disponível na base de dados, 
    # caso for maior, o request retorna o código 404, pois não há mais conteúdo JSON,
    # acho que é um bug da API.
    if type(quantidade) != int or quantidade > 10000 or quantidade <= 0:
        raise ValueError('A quantidade deve estar entre 1 e 10000. E precisa ser do tipo integer (int)!')
   
    # Confere se a offset está dentro do suportado pela API, igual ao anterior.
    if type(offset) != int or offset > 10000 or offset < 0:
        raise ValueError('O valor offset deve estar entre 0 e 10000. E precisa ser do tipo integer (int)!')
    
    # Endereça os valores finais à um dicionário, requerido para fazer a solicitação.
    parametros = {'limite': quantidade, 'offset': offset} 
   
    # Faz um request prévio para checar por erro nos parâmetros solicitados.
    prev_erro = requests.get(base_url, headers=cabeca, params={'limite': 1, 'offset': 0})
    
    # Avalia caso o token seja inválido, normalmente neste caso a API
    # retorna o código 401 e uma JSON com mensagem de erro.
    if prev_erro.status_code == 401:
        raise Token_Invalido(Token_Invalido.err_message)
    
    # Valida os parâmetros 'offset' e 'quantidade' para evitar o erro no parser de JSON 
    # quando passamos do número limite de licitações disponíveis.
    count_licitacoes = prev_erro.json()['total']
    if offset + quantidade > count_licitacoes or offset + quantidade > 10000:
        quantidade = count_licitacoes
        offset = 0
       
    # Faz o pedido através do 'requests' usando o cabeçalho (header) criado e os
    # parâmetros necessários.
    resposta = requests.get(base_url, headers=cabeca, params=parametros)
   
    # Cria um dicionário a partir do parser de JSON integrado ao 'requests'.
    resposta_dict = resposta.json() 
    
    # Retorna o dicionário, que possui dois itens:
    # resposta_dict['total'] = total de licitações do ano
    # resposta_dict['data'] = uma lista de licitações (a quantidade é especificada pelo usuário no request).
    return resposta_dict


# Função que a partir da resposta_json, "limpa" os dados obtidos, para
# melhor visualização e compreensão e retorna uma lista de dicionários limpa,
# contendo apenas os dados.
def obter_dados(token, ano = 2008, quantidade = 1, offset = 0):

    '''
    
    Esta função foi criada, pois a resposta json original não é muito bem formatada,
    existem varios erros nas chaves do dicionário, e nos próprios dados. Os erros 
    principais eram os espaços brancos, bem como alguns parâmetros duplicados.

    Essencialmente, os parâmetros desta função são iguais ao da resposta_json.

    '''
    
    # Faz uma solicitação inicial para obter os dados 'crús' da resposta json da API.
    resposta_crua = resposta_json(token, ano, quantidade, offset)

    # Seleciona apenas os dados da resposta_crua (que é o que estamos interessados),
    # em forma de lista de dicionários.
    impr_info = resposta_crua['data']

    # Cria uma lista de dicionários vazia que será preenchida pelas licitações solicitadas.
    licit_list = []

    # Confere os dicionários dentro da lista inicial não formatada (impr_info)
    for licit in impr_info:
        
        # Cria um novo dicionário vazio que irá conter os dados da licitação já formatados.
        new_licit = {}
        
        # Procura por erros dentro das chaves dos dicionários.
        for k, v in licit.items():

            # Existem licitações que contém o parâmetro 'Orgão' e outras,
            # 'Órgão', então aqui se universaliza os dados para 'Órgão', e
            # adiciona ao dicionário vazio.
            if k == 'Orgão':
                new_licit['Órgão'] = licit[k]

            # Existem licitações que contém o parâmetro 'objeto' e outras, 
            # 'Objeto', então aqui se universaliza os dados para 'Objeto', e
            # adiciona ao dicionário vazio.
            if k == 'objeto':
                new_licit['Objeto'] = licit[k]

            # Em último caso, apaga os espaços em branco que continham nas chaves do dicionário,
            # e adiciona ao dicionário vazio.
            else:
                new_licit[" ".join(k.split())] = licit[k]
        
        # Procura por erros dentro dos valores do dicionário com as chaves já 'limpas'.
        for j, l in new_licit.items():

            # Apaga os espaços em branco.
            if type(l) == str:
                new_licit[j] = " ".join(l.split())

            # Formata os valores da chave 'Valor Contrato'.
            if j == 'Valor Contrato':
                
                # Confere se o valor é uma str vazia e coloca como 0.
                if new_licit[j] == '':
                    new_licit[j] = 0
                
                # Se não, coloca os valore como tipo float, que é melhor
                # para a comparação na análise dos dados.
                else:
                    new_licit[j] = float(l.replace('.', '').replace(',', '.'))
        
        # Ao final, adiciona o dicionário já formatado a lista de dicionários.
        licit_list.append(new_licit)
    
    # Retorna a lista de dicionários já limpa.
    return licit_list
