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
    for indx, ch in enumerate(plaintext):
        if ch.isalpha():
            if ch.islower():
                ciphertext += alphabet[
                     (alphabet.index(ch) + alphabet.index(keyword[indx % len(keyword)].lower())) % len(alphabet)]
            else:
                ciphertext += alphabet[
                    (alphabet.index(ch.lower()) + alphabet.index(keyword[indx % len(keyword)].lower())) % len(alphabet)].upper()
        else:
            ciphertext += ch

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
    for indx, ch in enumerate(ciphertext):
        if ch.isalpha():
            if ch.islower():
                plaintext += alphabet[
                    (alphabet.index(ch) - alphabet.index(keyword[indx % len(keyword)].lower())) % len(alphabet)]
            else:
                plaintext += alphabet[
                    (alphabet.index(ch.lower()) - alphabet.index(keyword[indx % len(keyword)].lower())) % len(
                        alphabet)].upper()
        else:
            plaintext += ch
    return plaintext
