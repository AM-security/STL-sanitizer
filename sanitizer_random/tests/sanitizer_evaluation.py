import pytest
from sanitizer_random.lib.sanitizer_random import SanitizerRandom
from vertex_ch_encoder.lib.vertex_ch_encoder import EncoderSTL, DecoderSTL, base2, base3
import numpy as np
from facet_ch_encoder.lib.facet_ch_encoder import EncoderSTL as FacetEncoderSTL, DecoderSTL as FacetDecoderSTL

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
def experiment_random_text_base_2_vertex_how_many_bits_survive() -> str:
    # Decoding before sanitization


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

    secret_after_binary_str = SecretBytesListToBinaryNoPrint(secret_after)


    return secret_after_binary_str


def test_run_experiment_ten_times_count_prob_of_each_bit_to_survice():
    decoder_before = DecoderSTL("test_objects/vertex_channel/base2/random_text/encoded_bunny.STL",
                                False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL(base2)  # path to save the decoded carrier
    secret_before_binary_str = SecretBytesListToBinaryNoPrint(secret_before)

    number_of_experiments = 30
    idx = 0

    secrets_after = []
    while idx < number_of_experiments:
        secret_after = experiment_random_text_base_2_vertex_how_many_bits_survive()
        print("experiment number " + str(idx))

        secrets_after.append(secret_after)
        idx += 1

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


    for key in bit_pos_survival_prob:
        print(str(key) +": " + str(bit_pos_survival_prob[key]) + " %")
    # print(secret_before)