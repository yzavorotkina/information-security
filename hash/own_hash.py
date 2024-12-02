def tea_encrypt_block(v, key):
    delta = 0x9E3779B9
    sum_ = 0
    v0, v1 = v[0], v[1]
    for _ in range(32):  # 32 раунда
        sum_ = (sum_ + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_ + key[sum_ & 3])) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_ + key[(sum_ >> 11) & 3])) & 0xFFFFFFFF
    return v0, v1


def simple_hash(data):
    hash_value = (0xABCD1234, 0x1234ABCD)
    key = [0x0F1571C9, 0x47D9E859, 0x0F1571C9, 0x47D9E859]

    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        if len(block) < 8:
            block += b'\x00' * (8 - len(block))
        v0 = int.from_bytes(block[:4], 'big')
        v1 = int.from_bytes(block[4:], 'big')
        v0 ^= hash_value[0]
        v1 ^= hash_value[1]
        hash_value = tea_encrypt_block((v0, v1), key)

    return (hash_value[0] << 32) | hash_value[1]


if __name__ == "__main__":
    data = input("Введите данные для хеширования: ").encode('utf-8')
    hash_result = simple_hash(data)
    print("Хеш значение:", hex(hash_result))