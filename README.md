# Modul DES (Data Encryption Standard)

DES (Data Encryption Standard) is a symmetric-key block cipher developed from IBM's Lucifer cipher in the early 1970s and later standardized for use as a federal encryption standard.

By "symmetric", DES uses the same secret key for both encryption and decryption. By "block cipher", DES processes data in fixed-size blocks rather than encrypting individual bits independently.

- It is a block cipher that processes data in 64-bit blocks.
- It takes a 64-bit plaintext block and generates a corresponding 64-bit ciphertext block.
- The key is 64 bits long, consisting of 56 effective key bits and 8 parity bits.
- The 8 parity bits are discarded during the key permutation process.
- It encrypts the plaintext through 16 rounds, where each round uses a different 48-bit subkey.
- The 16 subkeys are generated from the 56-bit effective key through permutation, splitting, and left circular shifts.
- The same DES structure is used for both encryption and decryption, with the subkeys applied in reverse order during decryption.

---

## DES Scheme

![DES Scheme](https://media.geeksforgeeks.org/wp-content/uploads/20250416155622491215/DES-Encryption-Algorithm.webp)

DES is based on the principles of the **Feistel cipher**, where the input block is divided into two halves and processed through multiple rounds.

DES also applies the concepts of **confusion and diffusion** through substitution and permutation operations. Each of the 16 rounds performs several operations using a 48-bit subkey generated from the main key.

---

## Initial Permutation

The 64-bit plaintext is first processed using the **Initial Permutation (IP)** table.

The permutation rearranges the positions of all 64 bits according to a predefined table.

```text
64-bit Plaintext
       |
       v
Initial Permutation
       |
       v
64-bit Permuted Block
       |
    +-----+
    |     |
    v     v
   L0     R0
  32-bit 32-bit
```

The resulting 64-bit block is divided into two 32-bit halves:

- `L0` = left half
- `R0` = right half

---

## Key Generation

The original DES key is 64 bits long. However, only 56 bits are used for encryption because every eighth bit is used as a parity bit.

The key generation process consists of three main stages:

```text
64-bit Key
    |
    v
Permuted Choice 1 (PC-1)
    |
    v
56-bit Key
    |
   +---+
   |   |
   v   v
  C0   D0
 28-bit 28-bit
   |     |
   +-----+
       |
  Left Circular Shift
       |
       v
    Ci + Di
     56-bit
       |
       v
Permuted Choice 2 (PC-2)
       |
       v
48-bit Subkey
```

This process is repeated for all 16 rounds to generate:

```text
K1, K2, K3, ..., K16
```

Each subkey is 48 bits long.

### Permuted Choice 1 (PC-1)

PC-1 transforms the original 64-bit key into a 56-bit key by rearranging its bits and removing the 8 parity bits.

```text
64-bit Key
    |
    v
   PC-1
    |
    v
56-bit Key
```

The 56-bit result is then divided into two 28-bit halves:

```text
56-bit Key
    |
 +--+--+
 |     |
 v     v
 C0    D0
28-bit 28-bit
```

### Left Circular Shift

For each round, both `C` and `D` are circularly shifted to the left.

The shift schedule used by DES is:

```text
Round:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
Shift:  1  1  2  2  2  2  2  2  1  2  2  2  2  2  2  1
```

### Permuted Choice 2 (PC-2)

After shifting, the 28-bit halves are combined into a 56-bit value.

PC-2 then selects and rearranges 48 bits from the 56-bit value to create the round subkey.

```text
Ci + Di
  |
  v
PC-2
  |
  v
Ki (48-bit)
```

This process produces 16 subkeys:

```text
K1 → Round 1
K2 → Round 2
...
K16 → Round 16
```

---

## DES Round Function

After the Initial Permutation, the block is processed through 16 Feistel rounds.

Each round receives:

- 32-bit left half
- 32-bit right half
- 48-bit round subkey

The basic structure of a round is:

```text
                 Ri-1
                   |
                   v
             Expansion (E)
                   |
                48-bit
                   |
                   XOR <----- Ki
                   |
                48-bit
                   |
                   v
                S-Boxes
                   |
                32-bit
                   |
                   v
                P-Box
                   |
                32-bit
                   |
                   XOR <----- Li-1
                   |
                   v
                  Ri

Li = Ri-1
```

The mathematical representation is:

```text
Li = Ri-1

Ri = Li-1 XOR F(Ri-1, Ki)
```

where `F` is the DES round function.

---

## Expansion Permutation

The right half of the block contains 32 bits. Before it is combined with the 48-bit subkey, it is expanded to 48 bits using the **Expansion Permutation** table.

```text
32-bit Ri-1
     |
     v
Expansion Permutation
     |
     v
48-bit Expanded R
```

Some bits are duplicated during this process.

The purpose of this expansion is to make the right half compatible with the 48-bit subkey.

---

## XOR with the Round Subkey

The 48-bit expanded right half is XORed with the corresponding 48-bit subkey.

```text
48-bit Expanded R
        XOR
48-bit Subkey Ki
        |
        v
48-bit Result
```

For each bit:

```text
0 XOR 0 = 0
0 XOR 1 = 1
1 XOR 0 = 1
1 XOR 1 = 0
```

---

## S-Box Substitution

The 48-bit XOR result is divided into eight groups of 6 bits.

```text
48-bit Input
    |
    +---- 6 bits ----> S1
    +---- 6 bits ----> S2
    +---- 6 bits ----> S3
    +---- 6 bits ----> S4
    +---- 6 bits ----> S5
    +---- 6 bits ----> S6
    +---- 6 bits ----> S7
    +---- 6 bits ----> S8
```

Each S-Box converts a 6-bit input into a 4-bit output.

```text
6-bit Input
    |
    v
 S-Box
    |
    v
4-bit Output
```

As a result:

```text
8 × 6 bits = 48 bits

8 × 4 bits = 32 bits
```

The first and sixth bits of each 6-bit input determine the row, while the middle four bits determine the column.

```text
b1 b2 b3 b4 b5 b6
|              |
+------ Row ----+

   b2 b3 b4 b5
       |
     Column
```

---

## P-Box Permutation

The 32-bit output of the S-Boxes is then rearranged using the **P-Box Permutation**.

```text
32-bit S-Box Output
        |
        v
       P-Box
        |
        v
32-bit Permuted Output
```

This permutation contributes to the diffusion property of DES.

---

## Feistel XOR and Swap

The result of the P-Box is XORed with the previous left half:

```text
Ri = Li-1 XOR F(Ri-1, Ki)
```

The previous right half becomes the new left half:

```text
Li = Ri-1
```

Therefore, after each round:

```text
       Li-1             Ri-1
         |                |
         |                v
         |              F()
         |                |
         +------ XOR <----+
                |
                v
               Ri

        Li = Ri-1
```

This process is repeated for all 16 rounds.

---

## Final Swap

After Round 16, the left and right halves are swapped before the final permutation.

```text
L16 | R16
   |
   v
R16 | L16
```

This produces the 64-bit block that will be processed by the final permutation.

---

## Inverse Initial Permutation

The swapped 64-bit block is processed using the **Inverse Initial Permutation (IP⁻¹)**.

```text
64-bit Block
     |
     v
Inverse Initial Permutation
     |
     v
64-bit Ciphertext
```

The final result is the encrypted 64-bit ciphertext block.

---

## 11. Complete DES Encryption Process

The complete DES encryption process can be summarized as:

```text
64-bit Plaintext
       |
       v
Initial Permutation
       |
       v
     L0, R0
       |
       v
   16 Feistel Rounds
       |
       +--> Expansion
       |
       +--> XOR with Subkey
       |
       +--> S-Box Substitution
       |
       +--> P-Box Permutation
       |
       +--> XOR with Left Half
       |
       v
   Final Swap
       |
       v
Inverse Initial Permutation
       |
       v
64-bit Ciphertext
```

---

## 12. DES Decryption

DES decryption uses the same Feistel structure as encryption. The main difference is the order of the subkeys.

Encryption:

```text
K1 → K2 → K3 → ... → K16
```

Decryption:

```text
K16 → K15 → K14 → ... → K1
```

Therefore, the same `des_block()` logic can be reused for both encryption and decryption by providing the subkeys in the appropriate order.

---

## Block Cipher Modes

DES operates on fixed 64-bit blocks. When the plaintext consists of multiple blocks, a **block cipher mode of operation** determines how those blocks are processed.

### Electronic Codebook (ECB)
![ECB Scheme](https://media.geeksforgeeks.org/wp-content/uploads/20241216150427964834/1.webp)
Each plaintext block is encrypted independently.

```text
P1 → DES → C1
P2 → DES → C2
P3 → DES → C3
```

### Cipher Block Chaining (CBC)
![CBC Scheme](https://media.geeksforgeeks.org/wp-content/uploads/20241216150551381074/2.webp)
Each plaintext block is XORed with the previous ciphertext block before encryption.

For the first block, an Initialization Vector (IV) is used.

```text
C1 = DES(P1 XOR IV)

C2 = DES(P2 XOR C1)

C3 = DES(P3 XOR C2)
```

For decryption:

```text
P1 = DES⁻¹(C1) XOR IV

P2 = DES⁻¹(C2) XOR C1

P3 = DES⁻¹(C3) XOR C2
```

---

## Padding

Since DES processes data in 64-bit blocks, plaintext must be aligned to an 8-byte block boundary.

This implementation uses padding so that the input length becomes a multiple of 8 bytes.

For example, if the plaintext contains 5 bytes:

```text
Plaintext:
[5 bytes]

Padding:
03 03 03

Padded plaintext:
[5 bytes] 03 03 03
```

The final byte indicates the number of padding bytes added.

During decryption, the padding is validated and removed to recover the original plaintext.

---
## Sources
https://www.geeksforgeeks.org/ethical-hacking/block-cipher-modes-of-operation/

https://www.geeksforgeeks.org/computer-networks/data-encryption-standard-des-set-1/

https://www.geeksforgeeks.org/computer-networks/difference-between-confusion-and-diffusion/

https://www.geeksforgeeks.org/python/feistel-cipher/

https://desaction.org/des-timeline/