# Import the necessary libraries
from Crypto.Cipher import AES  # Import the AES encryption algorithm from the Crypto library
from Crypto.Util.Padding import pad, unpad  # Import the padding and unpadding functions for AES encryption
from Crypto.Random import get_random_bytes  # Import the function to generate random bytes for keys and IVs
import numpy as np  # Import the NumPy library for numerical computations
from PIL import Image  # Import the PIL library for image processing
import matplotlib.pyplot as plt  # Import the Matplotlib library for displaying images

# Define a function to perform CBC encryption
def cbc_encrypt(key, plaintext, iv):
    # Create a new AES cipher object in CBC mode with the given key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Encrypt the plaintext using the cipher object and pad the result to the AES block size
    return cipher.encrypt(pad(plaintext, AES.block_size))

# Define a function to perform CBC decryption
def cbc_decrypt(key, ciphertext, iv):
    # Create a new AES cipher object in CBC mode with the given key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt the ciphertext using the cipher object and unpad the result
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

# Define a function to perform OFB encryption
def ofb_encrypt(key, plaintext, iv):
    # Create a new AES cipher object in OFB mode with the given key and IV
    cipher = AES.new(key, AES.MODE_OFB, iv)
    # Encrypt the plaintext using the cipher object
    return cipher.encrypt(plaintext)

# Define a function to perform OFB decryption
def ofb_decrypt(key, ciphertext, iv):
    # Create a new AES cipher object in OFB mode with the given key and IV
    cipher = AES.new(key, AES.MODE_OFB, iv)
    # Decrypt the ciphertext using the cipher object
    return cipher.decrypt(ciphertext)

# Define a function to perform CTR encryption
def ctr_encrypt(key, plaintext, nonce):
    # Create a new AES cipher object in CTR mode with the given key and nonce
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    # Encrypt the plaintext using the cipher object
    return cipher.encrypt(plaintext)

# Define a function to perform CTR decryption
def ctr_decrypt(key, ciphertext, nonce):
    # Create a new AES cipher object in CTR mode with the given key and nonce
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    # Decrypt the ciphertext using the cipher object
    return cipher.decrypt(ciphertext)

# Define a function to encrypt an image using a given mode and key
def encrypt_image(image_path, key, mode, iv_or_nonce):
    # Open the image file using PIL
    image = Image.open(image_path)
    # Convert the image to a NumPy array
    data = np.array(image)
    # Flatten the array to a 1D array
    flattened_data = data.flatten()

    # Convert the flattened array to bytes
    plaintext = flattened_data.tobytes()

    # Perform the encryption based on the given mode
    if mode == 'cbc':
        # Use CBC encryption
        encrypted_data = cbc_encrypt(key, plaintext, iv_or_nonce)
    elif mode == 'ofb':
        # Use OFB encryption
        encrypted_data = ofb_encrypt(key, plaintext, iv_or_nonce)
    elif mode == 'ctr':
        # Use CTR encryption
        encrypted_data = ctr_encrypt(key, plaintext, iv_or_nonce)

    # Convert the encrypted data back to a NumPy array of integers
    encrypted_data = np.frombuffer(encrypted_data, dtype=np.uint8)

    # Reshape the array to the original image shape
    encrypted_data = encrypted_data[:data.size].reshape(data.shape)
    # Create a new PIL image from the encrypted data
    encrypted_image = Image.fromarray(encrypted_data)
    # Save the encrypted image to a file
    encrypted_image.save(f'encrypted_{mode}.png')

# Example usage
key = get_random_bytes(16)  # Generate a random 16-byte key
iv = get_random_bytes(16)  # Generate a random 16-byte IV
nonce = get_random_bytes(8)  # Generate a random 8-byte nonce for CTR mode
encrypt_image('image1.png', key, 'cbc', iv)  # Encrypt an image using CBC mode
encrypt_image('image1.png', key, 'ofb', iv)  # Encrypt an image using OFB mode
encrypt_image('image1.png', key, 'ctr', nonce)  # Encrypt an image using CTR mode

# Define a function to display the raw data of a list of images
# Define a function to display the raw data of a list of images
def display_raw_data(images):
    # Iterate over each image in the list
    for image in images:
        # Open the image file using PIL
        img = Image.open(image)
        # Convert the image to a NumPy array
        data = np.array(img)
        # Display the image data using Matplotlib with a grayscale colormap
        plt.imshow(data, cmap='gray')
        # Set the title of the plot to the image filename
        plt.title(image)
        # Show the plot
        plt.show()

# Call the function to display the raw data of the original and encrypted images
display_raw_data(['image1.png', 'encrypted_cbc.png', 'encrypted_ofb.png', 'encrypted_ctr.png'])