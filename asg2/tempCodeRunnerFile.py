from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import numpy as np
from PIL import Image


import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, AES.block_size))

def ecb_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

def cbc_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    prev_block = iv
    for i in range(0, len(plaintext), AES.block_size):
        block = plaintext[i:i + AES.block_size]
        block = bytes(a ^ b for a, b in zip(block, prev_block))
        encrypted_block = cipher.encrypt(block)
        ciphertext += encrypted_block
        prev_block = encrypted_block
    return ciphertext

def cbc_decrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    prev_block = iv
    for i in range(0, len(ciphertext), AES.block_size):
        block = ciphertext[i:i + AES.block_size]
        decrypted_block = cipher.decrypt(block)
        plaintext += bytes(a ^ b for a, b in zip(decrypted_block, prev_block))
        prev_block = block
    return plaintext

def ofb_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    key_stream = cipher.encrypt(iv)
    ciphertext = b''
    for i in range(0, len(plaintext), AES.block_size):
        block = plaintext[i:i + AES.block_size]
        ciphertext_block = bytes(a ^ b for a, b in zip(block, key_stream))
        ciphertext += ciphertext_block
        key_stream = cipher.encrypt(key_stream)
    return ciphertext

def ofb_decrypt(key, ciphertext, iv):
    return ofb_encrypt(key, ciphertext, iv)

def ctr_encrypt(key, plaintext, nonce):
    cipher = AES.new(key, AES.MODE_ECB)
    counter = nonce
    ciphertext = b''
    for i in range(0, len(plaintext), AES.block_size):
        block = plaintext[i:i + AES.block_size]
        key_stream = cipher.encrypt(counter)
        ciphertext_block = bytes(a ^ b for a, b in zip(block, key_stream))
        ciphertext += ciphertext_block
        counter = int.from_bytes(counter, 'big') + 1
        counter = counter.to_bytes(AES.block_size, 'big')
    return ciphertext

def ctr_decrypt(key, ciphertext, nonce):
    return ctr_encrypt(key, ciphertext, nonce)



def encrypt_image(image_path, key, mode, iv_or_nonce):
    image = Image.open(image_path)
    data = np.array(image)
    flattened_data = data.flatten()

    if mode == 'cbc':
        encrypted_data = cbc_encrypt(key, flattened_data, iv_or_nonce)
    elif mode == 'ofb':
        encrypted_data = ofb_encrypt(key, flattened_data, iv_or_nonce)
    elif mode == 'ctr':
        encrypted_data = ctr_encrypt(key, flattened_data, iv_or_nonce)

    encrypted_data = np.array(encrypted_data).reshape(data.shape)
    encrypted_image = Image.fromarray(encrypted_data)
    encrypted_image.save(f'encrypted_{mode}.png')

# Example usage
key = get_random_bytes(16)
iv = get_random_bytes(16)
nonce = get_random_bytes(16)
encrypt_image('image1.png', key, 'cbc', iv)
encrypt_image('image1.png', key, 'ofb', iv)
encrypt_image('image1.png', key, 'ctr', nonce)




def display_images(images):
    for image in images:
        img = mpimg.imread(image)
        imgplot = plt.imshow(img)
        plt.show()

display_images(['image1.png', 'encrypted_cbc.png', 'encrypted_ofb.png', 'encrypted_ctr.png'])