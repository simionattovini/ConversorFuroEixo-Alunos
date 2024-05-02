import tables as tb
import numpy as np


def calcula_afastamentos_eixo(dim: float | int, spec: str, it: str) -> tuple[float, float]:
    """
    Função que calcula os afastamentos superior e inferior de um eixo, dados os dados a seguir
    :param dim: dimensão nominal
    :param spec: especificação do eixo: 'a', 'b', 'c', 'cd', 'd', ..., 'zc'
    :param it: padrão IT: '01', '0', '1', ..., '18'
    :return: tupla no formato (af. sup., af. inf.) em mm
    """
    # IMPLEMENTAR
    pass


def calcula_afastamentos_furo(dim: float | int, spec: str, it: str) -> tuple[float, float]:
    """
    Função que calcula os afastamentos superior e inferior de um furo, dados os dados a seguir
    :param dim: dimensão nominal
    :param spec: especificação do furo: 'A', 'B', 'C', 'CD', 'D', ..., 'ZC'
    :param it: padrão IT: '01', '0', '1', ..., '18'
    :return: tupla no formato (af. sup., af. inf.) em mm
    """
    # IMPLEMENTAR
    pass
