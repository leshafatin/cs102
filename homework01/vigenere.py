def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    up_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for indx, ch in enumerate(plaintext):
        if ch.islower():
            ciphertext += alphabet[
                    (alphabet.index(ch) + alphabet.index(keyword[indx % len(keyword)])) % len(alphabet)]
        else:
            ciphertext += up_alphabet[
                    (up_alphabet.index(ch) + up_alphabet.index(keyword[indx % len(keyword)])) % len(up_alphabet)]

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    up_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for indx, ch in enumerate(ciphertext):
        if ch.islower():
            plaintext += alphabet[
                (alphabet.index(ch) - alphabet.index(keyword[indx % len(keyword)])) % len(alphabet)]
        else:
            plaintext += up_alphabet[
                (up_alphabet.index(ch) - up_alphabet.index(keyword[indx % len(keyword)])) % len(up_alphabet)]

    return plaintext
