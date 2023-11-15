"""Este módulo contém funções utilitárias para trabalhar com datas e horas.

Functions:
- `get_str_date_hoje():`
    - Retorna a data de hoje no formato YYYY-mm-dd.

- `get_str_datetime_agora():`
    - Devolve a data e a hora actuais no formato YYYY-mm-dd HH:MM:SS.

- `get_str_date_timedelta(dias_delta):`
    - Retorna a data de hoje mais um certo número de dias no formato YYYY-mm-dd.

- `get_str_datetime_timedelta(dias_delta`):`
    - Retorna a data de hoje mais um determinado número de dias no formato YYYY-mm-dd HH:MM:SS.

"""
from datetime import datetime, date, timedelta


def get_str_date_hoje():
    """Retorna a data de hoje no formato YYYY-mm-dd.

    Returns:
        str: data de hoje no formato YYYY-mm-dd.
    """
    return date.today().strftime('%Y-%m-%d')


def get_str_date_invertido(data):
    """Retorna a data no formato YYYY-mm-dd.

    Args:
        data (str): data no formato dd.mm.YYYY.

    Returns:
        str: data no formato YYYY-mm-dd.
    """
    split_data = data.split('.')
    return split_data[2] + '-' + split_data[1] + '-' + split_data[0]

def get_str_datetime_agora():
    """Retorna a data e hora atual no formato YYYY-mm-dd HH:MM:SS.

    Returns:
        str: data e hora atual no formato YYYY-mm-dd HH:MM:SS.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
