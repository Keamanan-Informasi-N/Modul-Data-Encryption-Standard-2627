import argparse
import const as c

def split(bits):
    mid = len(bits) // 2
    return bits[:mid], bits[mid:]

def rotate_left(bits, nth):
    return bits[nth:] + bits[:nth]

def hex_to_bin(string):
    return bin(int(string, 16))[2:].zfill(len(string) * 4).upper()

def bin_to_hex(bits):
    return hex(int(bits, 2))[2:].zfill(len(bits) // 4).upper()

def xor(bits1, bits2):
    res = ''
    for b1, b2 in zip(bits1, bits2):
        res += '1' if b1 != b2 else '0'
    return res

def s_box_substitution(bits):
    res = ''
    for i in range(8):
        block = bits[i*6:(i+1)*6]
        
        row = int(block[0] + block[5], 2)
        column = int(block[1:5], 2)
        
        index = row * 16 + column
        apply_s_box = c.S_BOX[i][index]
        
        res += format(apply_s_box, '04b')
    
    return res

def add_padding(bits):
    if len(bits)%8 != 0:
        raise ValueError("Input must be byte aligned")
    
    data_len = len(bits) // 8
    pad_len = 8 - (data_len % 8)
    
    padding = format(pad_len, '08b') * pad_len
    return bits + padding

def remove_padding(bits):
    pad_len = int(bits[-8:], 2)
    
    if pad_len < 1 or pad_len > c.BLOCK_SIZE // 8:
        raise ValueError("Invalid padding length")
    
    padding = format(pad_len, '08b') * pad_len
    
    if bits[-len(padding):] != padding:
        raise ValueError("Invalid padding")
    
    return bits[:-len(padding)]
    
def gen_subkeys(key):
    key = permute(key, c.PC_1)
    left, right = split(key)
    subkeys = []
    for i in range(16):
        left = rotate_left(left, c.SHIFT_SCHEDULE[i])
        right = rotate_left(right, c.SHIFT_SCHEDULE[i])
        subkey = permute(left + right, c.PC_2)
        subkeys.append(subkey)
    return subkeys

def des_block(bits, subkeys):
    bits = permute(bits, c.INITIAL_PERMUTATION)
    
    left, right = split(bits)
    
    for subkey in subkeys:
        left, right = round(left, right, subkey)
    
    bits = right + left
    return permute(bits, c.INVERSE_INITIAL_PERMUTATION)

def round(left, right, subkey):
    expanded = permute(right, c.EXPANSION_PERMUTATION)
    
    xored = xor(expanded, subkey)
    substituted = s_box_substitution(xored)
    
    permuted = permute(substituted, c.P_BOX)
    
    new_right = xor(left, permuted)
    new_left = right
    return new_left, new_right

def permute(bits, table):
    permuted = ''
    for i in range(len(table)):
        permuted += bits[table[i] - 1]
    return permuted

def crypt(mode, method, key, input_pt, output_ct, iv=None):
    subkeys = gen_subkeys(hex_to_bin(key.read().strip()))
    bin_ct = ''
    bin_pt = hex_to_bin(input_pt.read().strip())
    
    if method == 'dec':
        subkeys = subkeys[::-1]
    
    if method == 'enc':
        bin_pt = add_padding(bin_pt)
    
    if mode == 'ecb':
        for i in range(0, len(bin_pt), c.BLOCK_SIZE):
            block = bin_pt[i:i+c.BLOCK_SIZE]
            bin_ct += des_block(block, subkeys)
    else:
        if iv is None:
            raise ValueError("Intial vector is required")
        last_block = hex_to_bin(iv.read().strip())
        
        for i in range(0, len(bin_pt), c.BLOCK_SIZE):
            block = bin_pt[i:i+c.BLOCK_SIZE]
            if method == 'enc':
                block = xor(block, last_block)
                encrypted = des_block(block, subkeys)
                last_block = encrypted
                bin_ct += last_block
            else:
                decrypted_block = des_block(block, subkeys)
                bin_ct += xor(decrypted_block, last_block)
                last_block = block
    if method == 'dec':
        bin_ct = remove_padding(bin_ct)
    return output_ct.write(bin_to_hex(bin_ct))

def add_common_arguments(parser):
    encrypt_group = parser.add_mutually_exclusive_group(required=True)
    encrypt_group.add_argument('--enc', action='store_const', dest='method', const='enc', help='Encryption method')
    encrypt_group.add_argument('--dec', action='store_const', dest='method', const='dec', help='Decryption method')
    
    parser.add_argument('key', type=argparse.FileType('r'), help='File contain the key')
    parser.add_argument('input', type=argparse.FileType('r'), help='File contain the input plaintext')
    parser.add_argument('output', type=argparse.FileType('w'), help='File to write the output cipher')
    
    return parser

def main():
    parser = argparse.ArgumentParser(description='DES Encryption')
    mode_parser = parser.add_subparsers(dest='mode', help='Mode of operation')
    
    cbc_parser = add_common_arguments(mode_parser.add_parser('cbc', help='Cipher Block Chaining'))
    ecb_parser = add_common_arguments(mode_parser.add_parser('ecb', help='Electronic Codebook'))
    cbc_parser.add_argument('--iv', required=True, type=argparse.FileType('r'), help='Initial vector file')
    
    args = parser.parse_args()

    crypt(args.mode, args.method, args.key, args.input, args.output, getattr(args, 'iv', None))
    
if __name__ == '__main__':
    main()