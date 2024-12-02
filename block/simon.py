def left_rotate(x, shift, size=16):
    return ((x << shift) & ((1 << size) - 1)) | (x >> (size - shift))


def right_rotate(x, shift, size=16):
    return (x >> shift) | ((x << (size - shift)) & ((1 << size) - 1))


def simon_encrypt_block(block, key):
    """Шифрование одного блока данных алгоритмом SIMON."""
    z = 0b11111010001001010110000111001101111101000100101011000011100110
    rounds = 32
    k = [key & 0xFFFF, (key >> 16) & 0xFFFF]
    x, y = block & 0xFFFF, (block >> 16) & 0xFFFF

    for i in range(2, rounds):
        tmp = (~left_rotate(k[i - 1], shift=3, size=16)) ^ k[i - 2] ^ left_rotate(k[i - 1], shift=1, size=16) ^ (z & 1)
        z >>= 1
        k.append(tmp & 0xFFFF)

    for i in range(rounds):
        tmp = x
        x = y ^ (left_rotate(x, shift=1) & left_rotate(x, shift=8)) ^ left_rotate(x, shift=2) ^ k[i]
        y = tmp

    return (y << 16) | x


def simon_decrypt_block(block, key):
    z = 0b11111010001001010110000111001101111101000100101011000011100110
    rounds = 32
    k = [key & 0xFFFF, (key >> 16) & 0xFFFF]
    x, y = block & 0xFFFF, (block >> 16) & 0xFFFF

    for i in range(2, rounds):
        tmp = (~left_rotate(k[i - 1], shift=3, size=16)) ^ k[i - 2] ^ left_rotate(k[i - 1], shift=1, size=16) ^ (z & 1)
        z >>= 1
        k.append(tmp & 0xFFFF)

    for i in range(rounds - 1, -1, -1):
        tmp = y
        y = x ^ (left_rotate(y, shift=1) & left_rotate(y, shift=8)) ^ left_rotate(y, shift=2) ^ k[i]
        x = tmp

    return (y << 16) | x


def simon_encrypt(data, key):
    encrypted_data = bytearray()
    for i in range(0, len(data), 4):
        block = data[i:i + 4]
        if len(block) < 4:
            block += b'\x00' * (4 - len(block))
        block_int = int.from_bytes(block, byteorder='little')
        encrypted_block = simon_encrypt_block(block_int, key)
        encrypted_data += encrypted_block.to_bytes(4, byteorder='little')
    return encrypted_data


def simon_decrypt(data, key):
    decrypted_data = bytearray()
    for i in range(0, len(data), 4):
        block = data[i:i + 4]
        block_int = int.from_bytes(block, byteorder='little')
        decrypted_block = simon_decrypt_block(block_int, key)
        decrypted_data += decrypted_block.to_bytes(4, byteorder='little')
    return decrypted_data.rstrip(b'\x00')


if __name__ == "__main__":
    with open('plaintext.txt', 'rb') as f:
        plaintext = f.read()

    key = 0x1FE2548A

    ciphertext = simon_encrypt(plaintext, key)

    with open('ciphertext.bin', 'wb') as f:
        f.write(ciphertext)

    print("Шифрование завершено. Зашифрованные данные сохранены в 'ciphertext.bin'.")

    with open('ciphertext.bin', 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = simon_decrypt(encrypted_data, key)

    with open('decrypted.txt', 'wb') as f:
        f.write(decrypted_data)

    print("Расшифрование завершено. Расшифрованные данные сохранены в 'decrypted.txt'.")
