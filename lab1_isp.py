import statistics
import constant


def abrrev_checking(word, posit):
    value = False

    if word[posit] == "." and (word[posit - 1].islower() or word[posit - 1].isnumeric()):
        value = True

    return value


def clean_word(old_word):
    old_word = old_word.lower()
    length = len(old_word)
    end_sent = False
    symb_pos = 0

    for i in old_word:
        if i in constant.CHECK_LIST:
            if i in constant.END_LIST:
                end_sent = True

            length -= 1
            old_word = old_word[:symb_pos] + old_word[symb_pos + 1:]

        elif abrrev_checking(old_word, symb_pos):
            length -= 1
            old_word = old_word[:symb_pos] + old_word[symb_pos + 1:]
            end_sent = True

        else:
            symb_pos += 1

    return old_word, end_sent


def clean_text(old_list):
    s = 0
    num_list = []
    start_list = []

    for i in old_list:
        proto_word, end_sent = clean_word(i)

        if end_sent:
            num_list.append(s + 1)
            s = 0
        else:
            s += 1

        if proto_word != "":
            start_list.append(proto_word)

    return start_list, num_list


def word_count(raw_dict):
    own_dict = {}

    for i in raw_dict:
        if i in own_dict.keys():
            own_dict[i] += 1
        else:
            own_dict[i] = 1

    return own_dict


def symb_count(n_symb, spec_dict):
    n_dict = {}

    for i in spec_dict.keys():

        if len(i) >= n_symb:
            k = i
            n = 0
            m = n_symb
            for z in range(len(i) - n_symb + 1):
                proto = k[n:m]
                if proto in n_dict.keys():
                    n_dict[proto] += spec_dict[i]
                else:
                    n_dict[proto] = spec_dict[i]
                n += 1
                m += 1

    return n_dict


def print_result(word_list, sent_list, symb_list, m_symb):
    print(f"Arithmetic mean of words in sentences: {int(sum(sent_list) / len(sent_list))}\n")
    print(f"Median value of words in sentences: {statistics.median(sent_list)}\n\n")
    print("\nWORD RATING:\n")

    for key, value in word_list.items():
        print(key, '-->', value)

    print("\nSYMBOL RATING:\n")
    sorted_tuples = sorted(symb_list.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    i = 0

    for key in sorted_dict:
        if i < m_symb:
            print(f"\t{key}--|--{sorted_dict[key]}")
            i += 1


def start_analysis(n_symb, m_symb):
    if not n_symb:
        n_symb = constant.N_SYMB
    if not m_symb:
        m_symb = constant.M_SYMB

    file = open("testText", "r")
    str1 = file.read()

    for key in constant.REPLACE_DICT:
        str1 = str1.replace(key, constant.REPLACE_DICT[key])

    raw_list = str1.split(" ")
    new_list, sent_list = clean_text(raw_list)
    word_count_dict = word_count(new_list)
    symb_count_dict = symb_count(n_symb, word_count_dict)
    print_result(word_count_dict, sent_list, symb_count_dict, m_symb)


def start_data():
    print("Input N in n-grams for counting: ")
    n_symb = int(input())
    print("Input M in top-m for counting: ")
    m_symb = int(input())
    start_analysis(n_symb, m_symb)


if __name__ == "__main__":
    start_data()
