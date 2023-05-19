import statistics

import pandas as pd
from typing import List
from sanitizer_random.lib.sanitizer_random import SanitizerRandom
from vertex_ch_encoder.lib.vertex_ch_encoder import EncoderSTL, DecoderSTL, base2, base3
import numpy as np
import matplotlib.pyplot as plt
from facet_ch_encoder.lib.facet_ch_encoder import EncoderSTL as FacetEncoderSTL, DecoderSTL as FacetDecoderSTL
import csv

byte_len_base3 = 6

SECRET_SIZE_BITS_BASE_2 = 4 * 8  # size of any secret = 4 bytes
SECRET_SIZE_BITS_BASE_3 = 4 * 6  # size of any secret = 4 bytes


def all_substrings(string):
    n = len(string)
    return {string[i:j + 1] for i in range(n) for j in range(i, n)}


def LongestSubstream(s1: str, s2: str):
    return max(all_substrings(s1) & all_substrings(s2), key=len)


def SecretBytesListToBinary(b: list[int]) -> str:
    bit_mask: int = 0x80
    res = ""
    for byte_value in b:
        # res += ''.join('{:08b}'.format(b) for b in str_byte.encode('utf8'))
        # print(''.join('{:08b}'.format(b) for b in str_byte.encode('utf8')))
        byte_res = ""
        for i in range(0, 8):
            if byte_value & bit_mask:
                byte_res += "1"
            else:
                byte_res += "0"
            bit_mask = bit_mask >> 1
        res += byte_res
        print(byte_res)
        bit_mask = 0x80
    return res


def SecretBytesListToBinaryNoPrint(b: list[int]) -> str:
    bit_mask: int = 0x80
    res = ""
    for byte_value in b:
        # res += ''.join('{:08b}'.format(b) for b in str_byte.encode('utf8'))
        # print(''.join('{:08b}'.format(b) for b in str_byte.encode('utf8')))
        byte_res = ""
        for i in range(0, 8):
            if byte_value & bit_mask:
                byte_res += "1"
            else:
                byte_res += "0"
            bit_mask = bit_mask >> 1
        res += byte_res
        print(byte_res)
        bit_mask = 0x80
    return res


def SecretBytesToTernary(b: list[int]):
    res = ""
    for byte_value in b:
        ternary = np.base_repr(byte_value, base=3)
        diff_len = byte_len_base3 - len(ternary)
        for i in range(0, diff_len):
            ternary = "0" + ternary
        res += ternary
        print(ternary)
    return res


def unicode_to_str(lst: list[int]) -> str:
    list_of_strings = [chr(x) for x in lst]

    result = ''.join(list_of_strings)
    return result


def WriteUnicodeToFile(b: list[int], filename: str):
    f = open(filename, "w", encoding="utf-8")

    print("unicode string")
    print(unicode_to_str(b))
    f.write(unicode_to_str(b))

    f.close()


# Infiltrated picture of elephant
def test_sanitize_vertex_ch_random_text_base_3():
    # Decoding before sanitization
    decoder_before = DecoderSTL(
        "test_objects/vertex_channel/base3/text/encoded_sphere.STL", False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL(base3)  # path to save the decoded carrier

    secret_before_binary_str = SecretBytesListToBinary(secret_before)

    print("Secret before:")
    print(secret_before)
    # secret's size is 90 bytes = 720 bits
    sanitizer = SanitizerRandom("test_objects/vertex_channel/base3/text/encoded_sphere.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS_BASE_3)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base3/text/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL(
        "test_objects/vertex_channel/base3/text/sanitized_sphere.STL", False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL(base3)  # path to save the decoded carrier
    print("Secret after:")
    print(secret_after)

    WriteUnicodeToFile(secret_after, "test_objects/vertex_channel/base3/text/secret_after.txt")


    secret_after_binary_str = SecretBytesToTernary(secret_after)

    print("Longest run:")
    print(LongestSubstream(secret_before_binary_str, secret_after_binary_str))

    assert secret_before != secret_after


# Infiltrated text
def test_sanitize_vertex_ch_random_text_base_2():
    # Decoding before sanitization
    decoder_before = DecoderSTL("test_objects/vertex_channel/base2/text/encoded_sphere.STL",
                                False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL(base2)  # path to save the decoded carrier
    secret_before_binary_str = SecretBytesListToBinary(secret_before)

    print("Secret before:")
    print(secret_before)

    sanitizer = SanitizerRandom("test_objects/vertex_channel/base2/text/encoded_sphere.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS_BASE_2)
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base2/text/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/vertex_channel/base2/text/sanitized_sphere.STL",
                               False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL(base2)  # path to save the decoded carrier

    # Decoding after sanitization
    decoder_after_1 = DecoderSTL("test_objects/vertex_channel/base2/text/sanitized_sphere.STL", False)  # carrier's with secret filepath
    decoder_after_1.DecodeFileFromSTL("test_objects/vertex_channel/base2/text/secret_after.txt", base2)  # path to save the decoded carrier

    print("Secret after:")
    print(secret_after)

    WriteUnicodeToFile(secret_after, "test_objects/vertex_channel/base3/text/secret_after.txt")

    secret_after_binary_str = SecretBytesListToBinary(secret_after)

    print("Longest run:")
    print(LongestSubstream(secret_before_binary_str, secret_after_binary_str))
    assert secret_before != secret_after



def test_sanitize_vertex_ch_random_text_base_3_from_base_3():
    # Decoding before sanitization
    decoder_before = DecoderSTL(
        "test_objects/vertex_channel/base3/text_from_base3/encoded_bunny.STL", False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL(base3)  # path to save the decoded carrier

    secret_before_binary_str = SecretBytesToTernary(secret_before)

    print("Secret before:")
    print(secret_before)
    # secret's size is 90 bytes = 720 bits
    sanitizer = SanitizerRandom("test_objects/vertex_channel/base3/text_from_base3/encoded_bunny.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS_BASE_3)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base3/text_from_base3/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL(
        "test_objects/vertex_channel/base3/text_from_base3/sanitized_bunny.STL", False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL(base3)  # path to save the decoded carrier
    print("Secret after:")
    print(secret_after)

    WriteUnicodeToFile(secret_after, "test_objects/vertex_channel/base3/text_from_base3/secret_after.txt")


    secret_after_binary_str = SecretBytesToTernary(secret_after)

    print("Longest run:")
    print(LongestSubstream(secret_before_binary_str, secret_after_binary_str))

    assert secret_before != secret_after


# FACETS
# Infiltrated text
def test_sanitize_facet_ch_random_text_base_2():
    # Decoding before sanitization
    decoder_before = FacetDecoderSTL("test_objects/facet_channel/text/encoded_sphere.STL", False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL()  # path to save the decoded carrier

    sanitizer = SanitizerRandom("test_objects/facet_channel/text/encoded_sphere.STL")  # carrier's filepath
    sanitizer.SanitizeFacetCh(SECRET_SIZE_BITS_BASE_2)
    sanitizer.SaveSanitizedFile(
        "test_objects/facet_channel/text/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = FacetDecoderSTL("test_objects/facet_channel/text/sanitized_sphere.STL", False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL()  # path to save the decoded carrier



    print("Secret before:")
    print(secret_before)
    secret_before_binary_str = SecretBytesListToBinary(secret_before)


    print("Secret after:")
    print(secret_after)

    secret_after_binary_str = SecretBytesListToBinary(secret_after)
    print("Longest run:")
    print(LongestSubstream(secret_before_binary_str, secret_after_binary_str))



    assert secret_before != secret_after




# Random text vertex channel sanitizer jebsmmsfzvvalkeiqwgctgsopjhyjnyjhfksznqrzarktcwxtudolvujizaylsef
def test_sanitize_vertex_ch_random_text_base_2():
    # Decoding before sanitization
    decoder_before = DecoderSTL("test_objects/vertex_channel/base2/text/encoded_sphere.STL",
                                False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL(base2)  # path to save the decoded carrier
    secret_before_binary_str = SecretBytesListToBinary(secret_before)

    print("Secret before:")
    print(secret_before)

    sanitizer = SanitizerRandom("test_objects/vertex_channel/base2/random_text/encoded_bunny.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS_BASE_2)
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base2/random_text/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/vertex_channel/base2/random_text/sanitized_bunny.STL",
                               False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL(base2)  # path to save the decoded carrier

    # Decoding after sanitization
    decoder_after_1 = DecoderSTL("test_objects/vertex_channel/base2/random_text/sanitized_bunny.STL", False)  # carrier's with secret filepath
    decoder_after_1.DecodeFileFromSTL("test_objects/vertex_channel/base2/random_text/secret_after.txt", base2)  # path to save the decoded carrier

    print("Secret after:")
    print(secret_after)

    WriteUnicodeToFile(secret_after, "test_objects/vertex_channel/base2/random_text/secret_after.txt")

    secret_after_binary_str = SecretBytesListToBinary(secret_after)

    print("Longest run:")
    print(LongestSubstream(secret_before_binary_str, secret_after_binary_str))
    assert secret_before != secret_after



###################################

# Random text vertex channel sanitizer jebsmmsfzvvalkeiqwgctgsopjhyjnyjhfksznqrzarktcwxtudolvujizaylsef
def sanitize_and_return_new_sequence_vertex_ch(encoded_stl:str, sanitized_stl_save:str) -> str:
    # Decoding before sanitization


    sanitizer = SanitizerRandom(encoded_stl)  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS_BASE_2)
    sanitizer.SaveSanitizedFile(
        sanitized_stl_save)  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL(sanitized_stl_save,
                               False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL(base2)  # path to save the decoded carrier

    secret_after_binary_str = SecretBytesListToBinaryNoPrint(secret_after)


    return secret_after_binary_str


def calculate_prob_and_variance_of_all_bits(secret_before: str, secrets_after: List[str]) -> List[int]:
    array_of_probabilities_of_survival_all_bits = []
    for secret_after in secrets_after:
        a = len(secret_before)
        b = len(secret_after)
        counter_matching = 0
        for i in range(len(secret_after)):
            if secret_after[i] == secret_before[i]:
                counter_matching += 1
        prob = int((100 * counter_matching) / len(secret_after))
        array_of_probabilities_of_survival_all_bits.append(prob)
    return array_of_probabilities_of_survival_all_bits

# n - number of experiments
def build_gistogram(array_of_probabilities_of_survival_all_bits: List[int]):
    # df = pd.DataFrame({'Survival of all bits': array_of_probabilities_of_survival_all_bits},
    # )
    probabilitites = pd.Series(array_of_probabilities_of_survival_all_bits)
    ax = probabilitites.hist(grid=True,bins=100, rwidth=0.9,color='#607c8e')
    plt.title('Probabilities of survival for 100 experiments')
    plt.ylabel('Counts')
    plt.xlabel('Probability of survival for all bits')
    plt.grid(axis='y', alpha=0.75)
    fig = ax.get_figure()
    fig.savefig('../experiment/original/histogram.png')
    #select unique values
    # unique_list = []
    # # traverse for all elements
    # for x in array_of_probabilities_of_survival_all_bits:
    #     # check if exists in unique_list or not
    #     if x not in unique_list:
    #         unique_list.append(x)
    #
    #
    # dict_prob_how_many_times_repeated = {}
    #
    # for i, in range(len(unique_list)):
    #     counter = 0
    #     for prob in array_of_probabilities_of_survival_all_bits:
    #         if prob == unique_list[i]:
    #             counter += 1
    #     dict_prob_how_many_times_repeated[unique_list[i]] = counter

def build_csv_file(secret_before: str, secrets_after: List[str],
                   array_of_probabilities_of_survival_all_bits: List[int],
                   array_of_probabilities_of_survival_individual_bits: List[int],
                   array_of_variances_of_individual_bits: List[int]):
    # field names
    fields_bits = []
    for i in range(len(secret_before)):
        fields_bits.append("bit_" + str(i+1))
    fields = ['-', 'Survival of all bits for each sequence, %']
    fields += fields_bits

    rows = []
    row_zero = {'-': 'Original sequence', 'Survival of all bits for each sequence, %': '    '}
    idx = 0
    for character in [*secret_before]:
        row_zero['bit_' +str(idx+1)] = character
        idx += 1
    # row_zero = ['Run #', 'Original sequence'] + [*secret_before]
    rows.append(row_zero)
    # data rows of csv file
    idx = 1
    for secret_after in secrets_after:
        current_row = {'-': 'Run #' + str(idx), 'Survival of all bits for each sequence, %': array_of_probabilities_of_survival_all_bits[idx-1]}
        ch_counter = 1
        for character in [*secret_after]:
            current_row['bit_' +str(ch_counter)] = character
            ch_counter += 1
        rows.append(current_row)
        idx += 1
    rows.append({})
    # variance and prob of survival after each bit
    indiv_prob_row = {'-': 'Survival probability of individual bits, %:', }
    idx = 1
    for i in range(len(array_of_probabilities_of_survival_individual_bits)):
        indiv_prob_row['bit_'+str(idx)] = array_of_probabilities_of_survival_individual_bits[i]
        idx += 1
    rows.append(indiv_prob_row)

    indiv_variance_row = {'-': 'Variance of individual bits:', }
    idx = 1
    for i in range(len(array_of_probabilities_of_survival_individual_bits)):
        indiv_variance_row['bit_'+str(idx)] = array_of_variances_of_individual_bits[i]
        idx += 1
    rows.append(indiv_variance_row)
    # name of csv file
    filename = "../experiment/original/evaluation.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(rows)

def run_experiment_ten_times_count_prob_of_each_bit_to_survice(stl_file_name: str, stl_sanitize_save_wihtout_ext: str):
    decoder_before = DecoderSTL(stl_file_name,
                                False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL(base2)  # path to save the decoded carrier
    secret_before_binary_str = SecretBytesListToBinaryNoPrint(secret_before)

    number_of_experiments = 3
    idx = 0

    secrets_after = []
    while idx < number_of_experiments:
        sanitized_stl_file_name: str = stl_sanitize_save_wihtout_ext + str(idx+1) + ".STL"
        secret_after = sanitize_and_return_new_sequence_vertex_ch(stl_file_name, sanitized_stl_file_name)
        print("experiment number " + str(idx))
        print(secret_after)
        secrets_after.append(secret_after)
        idx += 1

    # histogram and prob of all bits
    array_of_probabilities_of_survival_all_bits = calculate_prob_and_variance_of_all_bits(secret_before_binary_str, secrets_after)
    build_gistogram(array_of_probabilities_of_survival_all_bits)

    bit_pos_bit_states = {}
    for secret_after in secrets_after:
        for bit_pos, bit in enumerate(secret_after):

            new_sequence = ""
            if bool(bit_pos_bit_states):
                if bit_pos in bit_pos_bit_states:
                    prev_seq_of_bit_states = bit_pos_bit_states[bit_pos]
                    new_sequence += prev_seq_of_bit_states
            new_sequence += str(bit)
            bit_pos_bit_states[bit_pos] = new_sequence



    print("Secret before:")
    lenn = str(len(secret_before_binary_str))
    print(lenn)
    bit_pos_survival_prob = {}
    array_of_variances_of_individual_bits = []
    for bit_pos in bit_pos_bit_states:
        original_bit_value = secret_before_binary_str[bit_pos]

        number_of_ones = bit_pos_bit_states[bit_pos].count('1')
        number_of_zeros = bit_pos_bit_states[bit_pos].count('0')

        prob_of_staying_the_same = 0
        if original_bit_value == "1":
            prob_of_staying_the_same = (100 * number_of_ones) / len(bit_pos_bit_states[bit_pos])
        else:
            prob_of_staying_the_same = (100 * number_of_zeros) / len(bit_pos_bit_states[bit_pos])

        bit_pos_survival_prob[bit_pos] = prob_of_staying_the_same

        # calculate variance. we have strings for each bit position, we need to get ints
        int_array_bit_position = []
        for str_bit in bit_pos_bit_states[bit_pos]:
            int_array_bit_position.append(int(str_bit))
        array_of_variances_of_individual_bits.append(statistics.variance(int_array_bit_position))

    array_of_probalities_of_inidividual_bits = []
    for key in bit_pos_survival_prob:
        array_of_probalities_of_inidividual_bits.append(int(bit_pos_survival_prob[key]))
        print(str(key) +": " + str(bit_pos_survival_prob[key]) + " %")



    build_csv_file(secret_before_binary_str, secrets_after, array_of_probabilities_of_survival_all_bits,
                   array_of_probalities_of_inidividual_bits, array_of_variances_of_individual_bits)
    return
    #print(statistics.median(array_of_prob))
    # print(secret_before)




def test_final_experiment_vertex_channel():
    original_secret = "jebsmmsfzv" # 10 bytes =
    # original_stl = "../experiment/original/original_stl/bunny.STL"
    encoded_stl = "../experiment/original/encoded_stl/encoded_bunny.STL"
    stl_sanitize_save_without_ext = "../experiment/original/sanitized_stl/sanitized_bunny_"

    # encoder = EncoderSTL(original_stl, False)  # carrier's filepath
    # encoder.EncodeBytesInSTL(original_secret,  # secret's path
    #                          "../experiment/original/encoded_stl/encoded_bunny.STL",
    #                          base2)  # path to save the carrier with secret

    run_experiment_ten_times_count_prob_of_each_bit_to_survice(encoded_stl, stl_sanitize_save_without_ext)