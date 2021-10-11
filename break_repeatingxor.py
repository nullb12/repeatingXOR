import base64
import singlexor


def deci_to_binary(decimal, bin_length=4):
    bin_shell = b''
    while decimal > 0:
        dec_bit = bytes(str((decimal % 2)), 'ascii')
        decimal = decimal // 2
        bin_shell += dec_bit
    while len(bin_shell) < bin_length:
        bin_shell += bytes(str(0), 'ascii')

# calculates the number of differing bits between two equal bytestrings
def hamming_dist(h_block1, h_block2):
    dist = 0
    for byte1, byte2 in zip(h_block1, h_block2):
        binary1, binary2 = deci_to_binary(byte1), deci_to_binary(byte2)
        for bit1, bit2 in zip(binary1, binary2):
            if bit1 != bit2:
                dist += 1
    return dist

# Finds most probable keysizes for the XOR key
def find_keys(ciphertext, min_keysize, max_keysize):
    hamming_dict = {}
    for keysize in range(min_keysize, max_keysize):
        n = 1
        distances = []
        # iterates through adjacent chunks of ciphertext, keysize chars apart 
        # (ex) ciphertext = abcdefghijk, keysize=2: ab|cd, cd|ef, ef|gh ...        
        while n * max_keysize <= len(ciphertext):
            chunk1, chunk2 = ciphertext[(n - 1) * keysize:n * keysize], ciphertext[n * keysize:(n + 1) * keysize]
            n += 1
             # normalize each hamming distance
            distances.append(hamming_dist(chunk1, chunk2) / keysize)
        # finds the average normalized hamming distance for the keysize
        hamming_dict[keysize] = (sum(distances) / len(distances))
    # sorts keysizes by ascending normalized hamming distance
    sorted_keys = sorted(hamming_dict.items(), key=lambda kv: kv[1])
    return sorted_keys


def break_txt(ciphertxt, keysize):
    blocklist = [ciphertxt[i:i + keysize] for i in range(0, len(ciphertxt), keysize)]
    return blocklist

def transpose_block(blocks):
    transposed_blocks = []
    for i in range(len(blocks[0])):
        transpose = b''
        for block in blocks:
            ith_byte = block[i:i + 1]
            transpose += ith_byte
        transposed_blocks.append(transpose)

    return transposed_blocks

# Decodes a chunk of the ciphertext with a single-byte XOR
def single_char_xor(ciphertext):
    plaintexts = []
    #Iterates through all printable ASCII characters
    for i in range(128):
        output_bytes = bytes([(i ^ byte) for byte in ciphertext])
        plaintexts.append(output_bytes)
    return plaintexts


def solve_block(blocklist):
    xor_key_bytes = []
    for block in blocklist:
        # decodes XOR, finds the plaintexts with the highest frequencies of common english letters
        xor_byte = []
        transpose_xor = single_char_xor(block)
        best = cryptopals3prime.grade_plaintexts3(transpose_xor)
        for i in list(best):
            x = chr(transpose_xor.index(i))
            xor_byte.append(x)
        xor_key_bytes.append(xor_byte)
    return xor_key_bytes

# joins key bytes as a single string
def key_combinations(key_bytes):
    output = ''
    for key_byte in key_bytes:
        for char in key_byte:
            output += char
    return output

def main():
    in_file = input('Please input your encoded XORd file (with extension): ')
    fh = open(in_file, 'r')
    decoded_ciphertext = base64.b64decode(fh.read().encode())
    key_sizes = []
    keysize = find_keys(decoded_ciphertext, 2, 20)[0][0]
    chunks = break_txt(decoded_ciphertext, keysize)
    t = transpose_block(chunks)
    possible_key = solve_block(t)
    print('broken text', chunks)
    print('transposes', t)
    print()
    print('Possible key:', key_combinations(possible_key))
    fh.close()
    
if __name__ == '__main__':
    main()
    
