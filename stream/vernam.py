def vernam_cipher(text, key):
    text_codes = [ord(char) for char in text]
    key_codes = [ord(char) for char in key]

    cipher_codes = [t ^ k for t, k in zip(text_codes, key_codes)]
    return cipher_codes


def codes_to_text(codes):
    return ''.join(chr(code) for code in codes)


plain_text = input("Введите текст для шифрования: ")
key = input("Введите ключ (той же длины, что и текст): ")

if len(plain_text) != len(key):
    print("Ошибка: ключ должен быть той же длины, что и текст.")
else:
    encrypted_codes = vernam_cipher(plain_text, key)
    print("Зашифрованный текст (в виде кодов):", encrypted_codes)

    decrypted_codes = vernam_cipher(codes_to_text(encrypted_codes), key)
    decrypted_text = codes_to_text(decrypted_codes)
    print("Расшифрованный текст:", decrypted_text)