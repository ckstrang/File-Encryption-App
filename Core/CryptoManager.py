import os
import struct
from time import sleep

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


class CryptoManager:
    """
    Handles encryption and decryption of files using AES-GCM.
    Includes attributes to modify encryption settings for future expansion, leave as default for AES-GCM.
    
    Attributes:
        key_length   (int): Length of the key to use for cipher.
        salt_length  (int): Length of the salt to use for cipher.
        nonce_length (int): Length of the nonce to use for cipher.
        buffer_size  (int): Size of buffer for reading of files.
        tag_size     (int): Size of tag for verification.
    """
    def __init__(self, key_length: int = 32, salt_length: int = 32, nonce_length: int = 12, buffer_size: int = 65536, tag_size: int = 16):
        """
        Initializes the CryptoManager.

        Parameters:
            key_length   (int): Length of the key to use for cipher.
            salt_length  (int): Length of the salt to use for cipher.
            nonce_length (int): Length of the nonce to use for cipher.
            buffer_size  (int): Size of buffer for reading of files.
            tag_size     (int): Size of tag for verification.
        """
        self.key_length = key_length
        self.salt_length = salt_length
        self.nonce_length = nonce_length
        self.ext_len = 3
        self.buffer_size = buffer_size
        self.tag_size = tag_size
        self.progress = 0.0

    def _derive_key(self, password: str, salt: bytes, iterations: int) -> bytes:
        """
        Derives key used for cipher using a password and a salt
        
        Parameters:
            password   (str): User password for key generation.
            salt       (str): Salt used for key generation.
            iterations (int): Number of iterations for key generation.

        Returns:
            bytes           : A byte string that can be used as a key.
        
        """
        return PBKDF2(password, salt, dkLen=self.key_length, count=iterations)
    
    def get_progress(self) -> float:
        """Returns the progress (float) of the current crypto operation"""
        return self.progress


    
    def encrypt(self, input_path: str, password: str, iterations: int, output_dir: str) -> None:
        """
        Encrypts a file using AES GCM.
            
        Parameters:
            input_path (str): Path to the file to be encrypted.
            password   (str): Password to use when deriving key used in cipher.

        Returns:
            None
            
        """
        salt:  bytes = get_random_bytes(self.salt_length)
        nonce: bytes = get_random_bytes(self.nonce_length)
        key:   bytes = self._derive_key(password, salt, iterations)
        
        cipher = AES.new(key, AES.MODE_GCM, nonce)

        if output_dir != '':
            output_path: str = output_dir + '/' + os.path.basename(input_path) + '.encrypted'
        else:
            output_path = input_path + '.encrypted'

        self._parse_files('encrypt', cipher, input_path, output_path, salt, nonce, iterations)


    def decrypt(self, input_path, password: str, output_dir: str) -> None:
        """
        Decrypts a file using AES GCM.

        Parameters:
            input_path (str): Path to the file to be decrypted.
            password   (str): Password to use when deriving key used in cipher.
            output_dir (str): Path to where the output file should be written.

        Returns:
            None          
        """
        with open(input_path, 'rb') as input_file:
            salt:  bytes = input_file.read(32)
            nonce: bytes = input_file.read(12)
            iterations = int.from_bytes(input_file.read(4), byteorder='big', signed=False)
            self.ext_len = int.from_bytes(input_file.read(1), 'big')
            file_ext = input_file.read(self.ext_len).decode('utf-8')
            check_ext = file_ext if file_ext.startswith('.') else '.' + file_ext
            if not input_path.lower().endswith(check_ext.lower()):
                if output_dir != '':
                    output_path = output_dir + '/' +  os.path.basename(input_path.replace('.encrypted', '')) + '_decrypted' + file_ext
                else:
                    output_path = input_path.replace('.encrypted', '_decrypted') + file_ext
            else:
                if output_dir != '':
                    output_path = output_dir + '/' + os.path.basename(input_path.replace('.encrypted', '_decrypted'))
                else:
                    output_path = input_path.replace('.encrypted', '_decrypted') + file_ext

        key: bytes = self._derive_key(password, salt, iterations)   
        cipher = AES.new(key, AES.MODE_GCM, nonce)

        self._parse_files('decrypt', cipher, input_path, output_path, salt, nonce, iterations)

    
    def _parse_files(self, mode: str, cipher, input_path: str, output_path: str, salt: bytes, nonce: bytes, iterations: int) -> None:
        """
        Peforms the reading and writing process of the encryption or decryption. 
        Parses the input file in self.buffer_size chunks, encrypting or decrypting them, and writing the result to an output file.

        Parameters:
            mode        (str): Encryption or Decryption mode
            input_path  (str): Path to the file being encrypted or decrypted.
            output_path (str): Path to the output file of encryption or decryption.
            salt      (bytes): Salt used in key derivation, to be written in encrypted file.
            nonce     (bytes): Nonce used in cipher creation, to be written in encrypted file.

        Returns:
            None

        """
        with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:
            if mode == 'encrypt':
                output_file.write(salt)
                output_file.write(nonce)
                output_file.write(iterations.to_bytes(4, byteorder="big", signed=False))
                
                file_ext = os.path.splitext(input_path)[1].encode('utf-8')
                ext_len = len(file_ext).to_bytes(1, 'big')
                output_file.write(ext_len)
                output_file.write(file_ext)

            input_file.seek(0, 2)
            total_size = input_file.tell()
            if mode == 'encrypt':
                input_file.seek(0, 0)
            if mode == 'decrypt': 
                total_size = total_size - self.salt_length - self.nonce_length - self.tag_size - 4 - 1 - self.ext_len
                input_file.seek(self.salt_length + self.nonce_length + 4 + 1 + self.ext_len)

            total_read = 0
            while True:
                to_read = min(self.buffer_size, total_size - total_read) if mode == 'decrypt' else self.buffer_size
                chunk = input_file.read(to_read)
                if not chunk:
                    break
                if mode == 'encrypt':
                    output_file.write(cipher.encrypt(chunk))
                elif mode == 'decrypt':
                    output_file.write(cipher.decrypt(chunk))
                total_read += len(chunk)
                self.progress = total_read / total_size
                sleep(0.01)

            if mode == 'encrypt':
                tag = cipher.digest()
                output_file.write(tag)
            elif mode == 'decrypt':
                tag = input_file.read(self.tag_size)
                cipher.verify(tag)
                print('decryption successful.')