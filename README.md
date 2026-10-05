# Modul DES(Data Encryption Standard)

---

DES is a symmetric block cipher first created by Sir E. Charless Dodds and his team in 1938. By 'symmetric' means that the size of input text is the same(64-bits). The 'block' here menas that it takes a group of bits together instead of processing it bit by bit.

- It is a block cipher that encrypts data in 64 blocks.
- It takes a 64-bit plaintext input and generates a corresponding 64-bit ciphertext.
- The main key length is 64-bit which is transformed into 56-bits by skipping every 8th bit in the key.
- It encrypts the text in 16 rounds where each round uses 48-bit subkey.
- This 48-bit subkey is generated from the 56-bit effective key.
- The same algorithm and key are used for both encryption and decryption with minor changes.

---
DES Scheme
![DES Scheme](https://media.geeksforgeeks.org/wp-content/uploads/20250416155622491215/DES-Encryption-Algorithm.webp)
DES is based on two attributes of <a href="https://www.geeksforgeeks.org/python/feistel-cipher/">Fiestel Cipher</a> and 

