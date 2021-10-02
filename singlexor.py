frequent_chars = b'etaoinshrdlu'

# Uses XOR to decode a hex string with each printable ASCII character as a key
def single_byte_xor(encoded_string):
    plaintexts = []
    hex_to_ascii = bytes.fromhex(encoded_string)
    for byte in range(128):
        xor_result = b"".join([chr(byte ^ i).encode() for i in hex_to_ascii])
        plaintexts.append(xor_result)
    return plaintexts

# "Scores" each decoded plaintext by frequency of common english characters
def grade_plaintext(plaintxt):
    score = 0
    for i in range(len(plaintxt)):
        char = plaintxt[i:i + 1]
        if char in frequent_chars:
            score += 12 - frequent_chars.index(char)
    return score

# returns plaintexts with highest scores -> highest scored plaintext is likely the original message
def grade_plaintexts3(plaintxts):
    scores, best_indices, best_plaintexts = [], [], []
    for i in range(len(plaintxts)):
        plaintxt = plaintxts[i]
        scores.append(grade_plaintext(plaintxt))
    for i in range(len(scores)):
        if scores[i] == max(scores):
            best_indices.append(i)
    for i in best_indices:
        best_plaintexts.append(plaintxts[i])

    return best_plaintexts

def main():
    l = input('Enter a hex string that has been XOR\'d: ' )
    print(grade_plaintexts3(single_byte_xor(l)))
    
if __name__ == '__main__':
    main()
