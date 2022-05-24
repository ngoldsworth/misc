
as_bin = "000001011110110010100010000000111110101001010100100100101000000000110000111010101010010111101110000000110100101010101101000000010110101001101100111100011100000000101010111001100010111010000000011110110010100010000000111000100000101011101111000000100110101010110110"
as_bin_lst = list(as_bin)

as_let  = "The quick brown fox jumps over the lazy dog"
as_let_list = list(as_let)

for j, c in enumerate(as_let):
    let = c
    code = as_bin[6*j:6*(j+1)]
    print(c, code, int(code, 2))

def solution(s):
    captilize_escape = "000001"
    map_char_to_int = {
        ' ': 0, 'a':32, 'b':48, 'c':36,
        'd':38, 'e':34, 'f':52, 'g':54,
        'h':50, 'i':20, 'j':22, 'k':40,
        'l':56, 'm':44, 'n':46, 'o':42,
        'p':60, 'q':62, 'r':58, 's':28,
        't':30, 'u':41, 'v':57, 'w':23,
        'x':45, 'y':47, 'z':43,
    }
    as_braille = ''
    for c in s:
        tmp = c
        if 65 <= ord(c) and ord(c) <= 90:
            as_braille += captilize_escape
            tmp = tmp.lower()

        as_braille += '{0:06b}'.format(map_char_to_int[tmp])
    
    return as_braille

if __name__ == "__main__":
    print(solution(as_let))
    print(solution(as_let) == as_bin)