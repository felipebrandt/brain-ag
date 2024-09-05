
def store_strings(string_list):
    string_dict = {}
    for string in string_list:
        if string_dict.get(string.lower()):
            string_dict[string.lower()] += 1
        else:
            string_dict[string.lower()] = 1
    return string_dict


if __name__ == '__main__':
    print(store_strings(["PaTiNeTe", "SKATE", "Patinete", "BicicletA"]))