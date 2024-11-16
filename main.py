from gost_hash import get_gost_hash


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result


def mod_inverse(e, phi):
    t, new_t = 0, 1
    r, new_r = phi, e

    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r

    if r > 1:
        raise ValueError("e не обратим к phi!")
    if t < 0:
        t += phi
    return t


def initialize_rsa():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17

    while gcd(e, phi) != 1:
        e += 1

    d = mod_inverse(e, phi)

    return p, q, n, phi, e, d


def rsa_sign(hash_value, d, n):
    return mod_pow(hash_value, d, n)


def rsa_verify(signature, hash_value, e, n):
    decrypted_hash = mod_pow(signature, e, n)
    return decrypted_hash == hash_value


def main():
    # Инициализация RSA
    p, q, n, phi, e, d = initialize_rsa()

    # Ввод сообщения
    message = input("Введите сообщение для подписи: ")

    # Вычисление ГОСТ Стрибог хэша
    hash_digest = get_gost_hash(message)
    print(f"Хэш (ГОСТ Стрибог): {hash_digest}")

    # Преобразуем первые 8 символов хэша в десятичное число
    hash_substr = hash_digest[:8]
    decimal_hash = int(hash_substr, 16)
    print(f"ГОСТ Стрибог хэш в десятичном формате: {decimal_hash}")

    # Подписание хэша
    signature = rsa_sign(decimal_hash % n, d, n)
    print(f"Подпись: {signature}")

    # Проверка подписи
    is_valid = rsa_verify(signature, decimal_hash % n, e, n)
    if is_valid:
        print("Подпись верна.")
    else:
        print("Подпись неверна.")


if __name__ == "__main__":
    main()