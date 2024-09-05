
def is_possible_division(num, div):
    return num % div == 0


def in_range(num):
    return num in range(17)


def is_valid_number(raw_input):
    try:
        number = int(raw_input)
        return {'number': number,
                'is_valid': in_range(number)}
    except ValueError:
        return {'number': raw_input,
                'is_valid': False}


def question_6():
    response = {'number': -1,
                'is_valid': False}
    while not response.get('is_valid'):
        raw_input = input('Digite um Número entre 0 e 16:')
        response = is_valid_number(raw_input)
    number = response.get('number')
    if is_possible_division(number, 3):
        if is_possible_division(number, 5):
            return 'baz'
        return 'foo'
    elif is_possible_division(number, 5):
        return 'bar'
    else:
        return number


if __name__ == '__main__':
    while True:
        print(question_6())

