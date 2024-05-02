from __future__ import annotations

import numpy as np
import core as core
from typing import Final

fs_valid: Final[tuple[str, ...]] = ('A', 'B', 'C', 'CD', 'D', 'E', 'EF', 'F', 'FG',
                                    'G', 'H', 'JS', 'J', 'K', 'M', 'N', 'P', 'R', 'S',
                                    'T', 'U', 'V', 'X', 'Y', 'Z', 'ZA', 'ZB', 'ZC')

es_valid: Final[tuple[str, ...]] = ('a', 'b', 'c', 'cd', 'd', 'e', 'ef', 'f', 'fg',
                                    'g', 'h', 'js', 'j', 'k', 'm', 'n', 'p', 'r', 's',
                                    't', 'u', 'v', 'x', 'y', 'z', 'za', 'zb', 'zc')

it_valid: Final[tuple[str, ...]] = ('01', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                    '10', '11', '12', '13', '14', '15', '16', '17', '18')


class AsymmetricToleranceDimension:
    fit_type_interf: Final[str] = "Interferência"
    fit_type_gap: Final[str] = "Folga"
    fit_type_uncertain: Final[str] = "Incerto"

    def __init__(self, dim: float | int, upper_tol: float, lower_tol: float):
        self.dim = dim
        self.upper_tol = upper_tol
        self.lower_tol = lower_tol

    def calc_tolerance_field(self):
        return self.upper_tol - self.lower_tol

    def __str__(self):
        return str(self.dim) + ":^ " + str(self.upper_tol) + "    v " + str(self.lower_tol)

    def get_html_string(self):
        if np.abs(self.dim - int(self.dim)) > 1e-4:
            dimstr = f'{self.dim:.3f}'
        else:
            dimstr = f'{int(self.dim)}'

        htmlstr = f"""
                    <table>
                        <tr>
                            <td rowspan='2' style="vertical-align: middle;"><h1>{dimstr}</h1></td>
                            <td style="vertical-align: middle;"><h5>{self.upper_tol/1000:+.3f}</h5></td>
                        </tr>
                        <tr>
                            <td style="vertical-align: middle;"><h5>{self.lower_tol/1000:+.3f}</h5></td>
                        </tr>
                    </table>
                  """
        return htmlstr

    @property
    def maxdim(self):
        return self.dim + self.upper_tol/1e3

    @property
    def mindim(self):
        return self.dim + self.lower_tol/1e3

    @classmethod
    def calc_fit_type(cls, hole: AsymmetricToleranceDimension, axle: AsymmetricToleranceDimension) -> str:
        if not hole.dim == axle.dim:
            raise ValueError('Furo e eixo devem possuir a mesma dimensão nominal no ajuste.')

        if hole.upper_tol <= axle.lower_tol:
            return cls.fit_type_interf
        elif hole.lower_tol >= axle.upper_tol:
            return cls.fit_type_gap
        else:
            return cls.fit_type_uncertain

    @classmethod
    def calc_clearance_limits(cls, hole: AsymmetricToleranceDimension, axle: AsymmetricToleranceDimension) \
            -> tuple[float, float]:

        if not (AsymmetricToleranceDimension.calc_fit_type(hole, axle) == AsymmetricToleranceDimension.fit_type_gap):
            raise ValueError('Esta montagem não é com folga.')

        #      Mínima folga                     Máxima folga
        return hole.lower_tol - axle.upper_tol, hole.upper_tol - axle.lower_tol

    @classmethod
    def calc_interference_limits(cls, hole: AsymmetricToleranceDimension, axle: AsymmetricToleranceDimension) \
            -> tuple[float, float]:

        if not (AsymmetricToleranceDimension.calc_fit_type(hole, axle) == AsymmetricToleranceDimension.fit_type_interf):
            raise ValueError('Esta montagem não é com interferência.')

        #      Mínima Interferência             Máxima Interferência
        return axle.lower_tol - hole.upper_tol, axle.upper_tol - hole.lower_tol

    @classmethod
    def calc_uncertain_limits(cls, hole: AsymmetricToleranceDimension, axle: AsymmetricToleranceDimension) \
            -> tuple[float, float]:

        if not (AsymmetricToleranceDimension.calc_fit_type(hole, axle) ==
                AsymmetricToleranceDimension.fit_type_uncertain):
            raise ValueError('Esta montagem não é com ajuste incerto.')

        #      Interferência                    Folga
        return hole.lower_tol - axle.upper_tol, hole.upper_tol - axle.lower_tol


def input_parser(instr: str, dim_precision=1e-4) -> tuple[float | int, str, str, str, str]:
    """
    Função que recebe a string de entrada no padrão de ajuste furo-eixo e retorna os parâmetros em separado. A string
    deve estar no formato:
    #(.#)A(A)#(#)a(a)#(#)
    -> tudo o que estiver entre parênteses é opcional
    -> # é uma quantidade qualquer de dígitos de 0 a 9
    -> . é o delimitador de casas decimais, caso haja
    -> A é uma quantidade qualquer de caracteres maiúsculos de 'A' a 'Z'
    -> a é uma quantidade qualquer de caracteres minúsculos de 'a' a 'Z'
    :param instr: String de entrada
    :param dim_precision: Tolerância da dimensão principal. Se o valor da tolerância principal estiver tão ou mais
    próximo de um inteiro quanto este valor, ele será arredondado.
    :return: Tupla no formato: (dimensão(numérico),
                                Especificação do Furo (string),
                                padrão IT do furo (string),
                                especificação do eixo (string),
                                padrão IT do eixo (string))
    """
    if dim_precision < 0:
        raise ValueError('A precisão da dimensão nominal deve ser positiva ou nula.')

    if instr == '':
        raise ValueError('A entrada está vazia.')

    dim: float | int
    furo_spec: str
    furo_it: str
    eixo_spec: str
    eixo_it: str

    instr = instr.strip()

    auxstr = ''
    auxind = 0

    while (auxind < len(instr)) and (instr[auxind].isdigit() or instr[auxind] == '.'):
        auxstr += instr[auxind]
        auxind += 1

    if auxind >= len(instr):
        raise ValueError('A notação do ajuste furo-eixo está incompleta.')

    try:
        dim = float(auxstr)
        dim_aux = round(dim, 0)
        if np.abs(dim - dim_aux) <= dim_precision:
            dim = int(dim)
    except Exception as ex:
        raise ValueError('O valor da dimensão nominal não está na formatação correta.')

    if not instr[auxind].isalpha():
        raise ValueError('O valor da dimensão nominal não está na formatação correta.')

    auxstr = ''
    while (auxind < len(instr)) and instr[auxind].isalpha() and instr[auxind].isupper():
        auxstr += instr[auxind]
        auxind += 1

    if auxind >= len(instr):
        raise ValueError('A notação do ajuste furo-eixo está incompleta')

    furo_spec = auxstr

    if not instr[auxind].isdigit():
        raise ValueError('A especificação do padrão do furo (letra) não está na formatação correta')

    auxstr = ''
    while (auxind < len(instr)) and instr[auxind].isdigit():
        auxstr += instr[auxind]
        auxind += 1

    if auxind >= len(instr):
        raise ValueError('A notação do ajuste furo-eixo está incompleta')

    furo_it = auxstr

    if instr[auxind] in ('-', '\\', '/'):
        auxind += 1

    if not instr[auxind].isalpha():
        raise ValueError('O valor do padrão IT do eixo não está na formatação correta')

    auxstr = ''
    while (auxind < len(instr)) and instr[auxind].isalpha() and instr[auxind].islower():
        auxstr += instr[auxind]
        auxind += 1

    if auxind >= len(instr):
        raise ValueError('A notação do ajuste furo-eixo está incompleta')

    eixo_spec = auxstr

    if not instr[auxind].isdigit():
        raise ValueError('A especificação do padrão do furo (letra) não está na formatação correta')

    auxstr = ''
    while (auxind < len(instr)) and instr[auxind].isdigit():
        auxstr += instr[auxind]
        auxind += 1

    eixo_it = auxstr

    if not (auxind == len(instr)):
        raise ValueError('A formatação do ajuste furo-eixo não está correta')

    return dim, furo_spec, furo_it, eixo_spec, eixo_it


def input_validator(parsed_input: tuple[float | int, str, str, str, str]) -> None:
    """
    :param parsed_input: entrada já interpretada pela função input_parser(...). É uma tupla no seguinte formato:

                    (dimensão(numérico),
                    Especificação do Furo (string),
                    padrão IT do furo (string),
                    especificação do eixo (string),
                    padrão IT do eixo (string))

    :return: Apenas levantará exceção caso a entrada seja inválida (fora da norma)
    """
    dim, furo_spec, furo_it, eixo_spec, eixo_it = parsed_input

    if dim <= 0:
        raise ValueError('A dimensão nominal deve ser positiva')

    if dim > 3150:
        raise ValueError('A dimensão nominal está acima da especificada pela norma.')

    if furo_spec not in fs_valid:
        raise ValueError('A especificação do furo não está na norma.')

    if eixo_spec not in es_valid:
        raise ValueError('A especificação do eixo não está na norma.')

    if furo_it not in it_valid:
        raise ValueError('O padrão IT do furo não está dentro do especificado pela norma')

    if eixo_it not in it_valid:
        raise ValueError('O padrão IT do eixo não está dentro do especificado pela norma')


def calculate_asymmetric_tol_dimension_axle(parsed_input: tuple[int | float, str, str, str, str]) \
        -> AsymmetricToleranceDimension:
    dim, _, _, eixo_spec, eixo_it = parsed_input
    upper_tol, lower_tol = core.calcula_afastamentos_eixo(dim, eixo_spec, eixo_it)

    return AsymmetricToleranceDimension(dim, upper_tol, lower_tol)


def calculate_asymmetric_tol_dimension_hole(parsed_input: tuple[int | float, str, str, str, str]) \
        -> AsymmetricToleranceDimension:
    dim, furo_spec, furo_it, _, _ = parsed_input
    upper_tol, lower_tol = core.calcula_afastamentos_furo(dim, furo_spec, furo_it)

    return AsymmetricToleranceDimension(dim, upper_tol, lower_tol)
