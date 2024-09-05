import re


def validate_cpf(cpf):
    cpf = re.sub('[^0-9]', '', cpf)

    if len(cpf) != 11:
        return False

    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    rest = total % 11
    if rest < 2:
        first_digit = 0
    else:
        first_digit = 11 - rest

    if int(cpf[9]) != first_digit:
        return False

    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    rest = total % 11
    if rest < 2:
        second_digit = 0
    else:
        second_digit = 11 - rest

    if int(cpf[10]) != second_digit:
        return False

    return True


def validate_cnpj(cnpj):
    cnpj = re.sub('[^0-9]', '', cnpj)

    if len(cnpj) != 14:
        return False

    def calculate_digit(cnpj, weight):
        total = 0
        for i in range(len(cnpj)):
            total += int(cnpj[i]) * weight[i]
        rest = total % 11
        if rest < 2:
            return 0
        else:
            return 11 - rest

    first_weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    first_digit = calculate_digit(cnpj[:12], first_weight)
    second_digit = calculate_digit(cnpj[:13], second_weight)

    if int(cnpj[12]) != first_digit or int(cnpj[13]) != second_digit:
        return False

    return True

