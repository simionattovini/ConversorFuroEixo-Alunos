import pandas as pd
import numpy as np

# Carregamento das tabelas

tab_it1a18 = pd.read_csv('Resources/Tabela 1 - IT1 a IT18.csv',
                         encoding='utf-8',
                         sep=';',
                         header=[0, 1])

tab_it0e01 = pd.read_csv('Resources/Tabela 5 - IT0 e IT01.csv',
                         encoding='utf-8',
                         sep=';',
                         header=[0, 1])

tab_eixos = pd.read_csv('Resources/Tabela 2 - Eixos.csv',
                        encoding='utf-8',
                        sep=';',
                        header=[0, 1, 2, 3])

tab_furos = pd.read_csv('Resources/Tabela 3 - Furos.csv',
                        encoding='utf-8',
                        sep=';',
                        header=[0, 1, 2, 3])


def consulta_tabela_eixo_afast(dim: int | float, spec: str, it: str) -> float:
    """
    Função que consulta a tabela de afastamentos de eixo e retorna o valor encontrado em micrômetros
    :param dim: Dimensão nominal, em mm
    :param spec: especificação do eixo ('a', 'b', 'c', 'cd, 'd', ..., 'zc')
    :param it: especificação da tolerância padrão IT ('01', '0', '1', ..., '18')
    :return: afastamento em micrômetros
    """
    lsvalid = [str(el) for el in range(0, 19)]
    lsvalid.insert(0, '01')

    if it not in lsvalid:
        raise ValueError('Especificação IT não está entre 01, 0, 1 e 18')

    c1 = tab_eixos.columns[0]
    c2 = tab_eixos.columns[1]

    row: pd.DataFrame
    val: pd.DataFrame

    if dim <= 3:
        row = tab_eixos.loc[tab_eixos.index == 0]
    else:
        row = tab_eixos.loc[(tab_eixos[c1] < dim) & (tab_eixos[c2] >= dim)]

    val = row.loc[:, row.columns.get_level_values(3) == spec]

    if val.size == 0:
        raise ValueError('Valor não encontrado na tabela')

    if spec == 'j':
        if it in ('5', '6'):
            val = val.loc[:, val.columns == val.columns[0]]
        elif it == '7':
            val = val.loc[:, val.columns == val.columns[1]]
        elif it == '8':
            val = val.loc[:, val.columns == val.columns[2]]
        else:
            raise ValueError('Valor não encontrado na tabela')

    if spec == 'k':
        if it in ('4', '5', '6', '7'):
            val = val.loc[:, val.columns == val.columns[0]]
        else:
            val = val.loc[:, val.columns == val.columns[1]]

    if val.size == 0:
        raise ValueError('Valor não encontrado na tabela')

    if val.size > 1:
        raise ValueError('Consulta ambígua: mais de um valor foi encontrado')

    if np.isnan(val.iat[0, 0]):
        raise ValueError('Valor não encontrado na tabela')

    return val.iat[0, 0]


def consulta_tabela_furo_afast(dim: int | float, spec: str, it: str) -> float:
    """
    Função que consulta a tabela de afastamentos de furo e retorna o valor encontrado em micrômetros.
    IMPORTANTE: Nas células onde há a marcação "+ Delta" o valor de Delta é ignorado. Ex: na célula em que consta
    "20 + Delta" a tabela conterá apenas o valor 20, independente do valor de Delta.
    :param dim: Dimensão nominal, em mm
    :param spec: especificação do furo ('A', 'B', 'C', 'CD, 'D', ..., 'ZC')
    :param it: especificação da tolerância padrão IT ('01', '0', '1', ..., '18')
    :return: afastamento em micrômetros
    """
    lsvalid = [str(el) for el in range(0, 19)]
    lsvalid.insert(0, '01')

    if it not in lsvalid:
        raise ValueError('Especificação IT não está entre 01, 0, 1 e 18')

    c1 = tab_furos.columns[0]
    c2 = tab_furos.columns[1]

    row: pd.DataFrame
    val: pd.DataFrame

    if dim <= 3:
        row = tab_furos.loc[tab_furos.index == 0]
    else:
        row = tab_furos.loc[(tab_furos[c1] < dim) & (tab_furos[c2] >= dim)]

    val = row.loc[:, row.columns.get_level_values(3) == spec]

    if val.size == 0:
        raise ValueError('Valor não encontrado na tabela')

    if spec == 'J':
        val = val.loc[:, val.columns.get_level_values(1) == ('IT' + it)]

    if spec in ('K', 'M', 'N'):
        lsvalid_leq8 = filter(lambda x: int(x) <= 8, lsvalid)
        if it in lsvalid_leq8:
            val = val.loc[:, val.columns == val.columns[0]]
        else:
            val = val.loc[:, val.columns == val.columns[1]]

    if val.size == 0:
        raise ValueError('Valor não encontrado na tabela')

    if val.size > 1:
        raise ValueError('Consulta ambígua: mais de um valor foi encontrado')

    if np.isnan(val.iat[0, 0]):
        raise ValueError('Valor não encontrado na tabela')

    return val.iat[0, 0]


def consulta_tabela_it0e01(dim: int | float, it: str) -> float:
    """
    Função que consulta a tabela de tolerâncias IT0 e IT01 e retorna a tolerância encontrada em micrômetros.
    :param dim: Dimensão nominal, em mm
    :param it: especificação da tolerância padrão IT ('01', '0', '1', ..., '18')
    :return: tolerância, em micrômetros
    """
    if it not in ('0', '01'):
        raise ValueError('Especificação IT diferente de 0 ou 01')

    c1 = tab_it0e01.columns[0]
    c2 = tab_it0e01.columns[1]

    row: pd.DataFrame

    if dim <= 3:
        row = tab_it0e01.loc[tab_it0e01.index == 0]
    else:
        row = tab_it0e01.loc[(tab_it0e01[c1] < dim) & (tab_it0e01[c2] >= dim)]

    val = row.loc[:, row.columns.get_level_values(0) == ('IT' + it)]

    if val.size == 0:
        raise ValueError('Valor não encontrado na tabela')

    return val.iat[0, 0]


def consulta_tabela_it1a18(dim: int | float, it: str) -> float:
    """
    Função que consulta a tabela de tolerâncias IT1 a IT18 e retorna o valor da tolerância em micrômetros
    :param dim: Dimensão nominal, em mm
    :param it: especificação da tolerância padrão IT ('01', '0', '1', ..., '18')
    :return: tolerância, em micrômetros
    """
    if it not in tuple([str(el) for el in range(1, 19)]):
        raise ValueError('Especificação IT não está entre 1 e 18')

    c1 = tab_it1a18.columns[0]
    c2 = tab_it1a18.columns[1]

    row: pd.DataFrame

    if dim <= 3:
        row = tab_it1a18.loc[tab_it1a18.index == 0]
    else:
        row = tab_it1a18.loc[(tab_it1a18[c1] < dim) & (tab_it1a18[c2] >= dim)]

    val = row.loc[:, row.columns.get_level_values(0) == ('IT' + it)]

    if val.size == 0:
        raise ValueError('Valor não encontrado na tabela')

    aux = val.iat[0, 0]

    if it in [str(el) for el in range(12, 19)]:
        aux = aux * 1000

    return aux


def consulta_tabela_delta_furo(dim: int | float, it: str) -> float:
    """
    Função que consulta as colunas do Delta da tabela de furo.
    IMPORTANTE: esta é a única função de consulta que, ao não encontrar um valor de Delta, retorna 0.0 no lugar de
    levantar uma exceção. Isso acontece devido à interpretação da própria tabela.
    :param dim: Dimensão nominal, em mm
    :param it: especificação da tolerância padrão IT ('01', '0', '1', ..., '18')
    :return: valor do delta em micrômetros
    """
    if it not in tuple([str(el) for el in range(3, 9)]):
        raise ValueError('Especificação IT não está entre 3 e 8, portanto não há especificação para o Delta')

    c1 = tab_furos.columns[0]
    c2 = tab_furos.columns[1]

    row: pd.DataFrame
    val: pd.DataFrame

    if dim <= 3:
        row = tab_furos.loc[tab_furos.index == 0]
    else:
        row = tab_furos.loc[(tab_furos[c1] < dim) & (tab_furos[c2] >= dim)]

    val = row.loc[:, row.columns.get_level_values(3) == ('IT' + it)]

    if val.size == 0:
        raise ValueError('Valor não encontrado na tabela')

    if val.size > 1:
        raise ValueError('Consulta ambígua: mais de um valor foi encontrado')

    if np.isnan(val.iat[0, 0]):
        return 0

    return val.iat[0, 0]
