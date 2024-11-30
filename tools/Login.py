import random
import time
from gmssl import sm4
import hashlib
import base64
import requests
from Crypto.Util.Padding import pad, unpad
import json

SM4_BLOCK_SIZE = 16

class Login():
    def md5_encryption(data):
        md5 = hashlib.md5()  # 创建一个md5对象
        md5.update(data.encode('utf-8'))  # 使用utf-8编码数据
        return md5.hexdigest()  # 返回加密后的十六进制字符串
    def hex_to_bytes(hex_str):
        return bytes.fromhex(hex_str)
    def pkcs7_padding(data):
        return pad(data, SM4_BLOCK_SIZE)
    def pkcs7_unpadding(data):
        return unpad(data, SM4_BLOCK_SIZE)
    def sm4_encrypt(plaintext, key, iv=None, mode='ECB', padding='Pkcs7', output_format='Base64'):
        crypt_sm4 = sm4.CryptSM4()
        key = Login.hex_to_bytes(key)
        # 设置加密模式
        if mode == 'ECB':
            crypt_sm4.set_key(key, sm4.SM4_ENCRYPT)
        elif mode == 'CBC':
            iv = Login.hex_to_bytes(iv) if iv else None
            crypt_sm4.set_key(key, sm4.SM4_ENCRYPT, iv)
        # 数据填充
        if padding == 'Pkcs7':
            plaintext = Login.pkcs7_padding(plaintext.encode())
        # 加密操作
        if mode == 'ECB':
            ciphertext = crypt_sm4.crypt_ecb(plaintext)
        elif mode == 'CBC':
            ciphertext = crypt_sm4.crypt_cbc(plaintext)
        # 输出格式转换
        if output_format == 'Base64':
            return base64.b64encode(ciphertext).decode()
        elif output_format == 'Hex':
            return ciphertext.hex()
    def sm4_decrypt(ciphertext, key, iv=None, mode='ECB', padding='Pkcs7', input_format='Base64'):
        crypt_sm4 = sm4.CryptSM4()
        key = Login.hex_to_bytes(key)
        # 设置解密模式
        if mode == 'ECB':
            crypt_sm4.set_key(key, sm4.SM4_DECRYPT)
        elif mode == 'CBC':
            iv = Login.hex_to_bytes(iv) if iv else None
            crypt_sm4.set_key(key, sm4.SM4_DECRYPT, iv)
        # 输入格式转换
        if input_format == 'Base64':
            ciphertext = base64.b64decode(ciphertext)
        elif input_format == 'Hex':
            ciphertext = bytes.fromhex(ciphertext)
        # 解密操作
        if mode == 'ECB':
            plaintext = crypt_sm4.crypt_ecb(ciphertext)
        elif mode == 'CBC':
            plaintext = crypt_sm4.crypt_cbc(ciphertext)
        # 数据去填充
        #if padding == 'Pkcs7':
            #plaintext = pkcs7_unpadding(plaintext)
        return plaintext.decode()
    def main(username, password, my_uuid, DeviceName):
        utc = int(time.time())
        uuid= my_uuid   
        #md5签名结果用hex
        encryptData='''{"password":"'''+password+'''","schoolId":"100","userName":"'''+username+'''","type":"1"}'''
        #签名结果
        sign_data='platform=android&utc={}&uuid={}&appsecret=pie0hDSfMRINRXc7s1UIXfkE'.format(utc,uuid)
        sign=Login.md5_encryption(sign_data)
        key='e2c9e15e84f93b81ee01bbd299a31563'
        content=Login.sm4_encrypt(encryptData, key, mode='ECB', padding='Pkcs7', output_format='Base64')
        content=content[:-24]
        url = "http://210.45.246.53:8080/login/appLoginHGD"
        headers = {
            "token": "",
            "isApp": "app",
            "deviceId": uuid,
            "deviceName": DeviceName,
            "version": "3.4.5",
            "platform": "android",
            "uuid": uuid,
            "utc": str(utc),
            "sign": sign,
            "Content-Type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0"
        }
        # 请求体内容
        data = {
            "cipherKey": "BL+FHB2+eDL3gMtv1+2UljBFraZYQFOXkmyKrqyRAzcw1R4rsq1i8p1tEOXhZMHTlFWmR+i/mdf4DNi0hCUSoQ88JMTUSUIkgU0+mowqRlVc/n/qYGqXERFqyMqn+GANUvWU65+F6/RLhpAB3AiYSJOY/RplvXmRvQ==",
            "content": content
        }
        # 发送POST请求
        response = requests.post(url, headers=headers, json=data)
        # 打印响应内容
        result=response.text
        DecryptedData=json.loads(Login.sm4_decrypt(result,key, mode='ECB', padding='Pkcs7',input_format='Base64'))
        token=DecryptedData['data']['token']
        uuid = str(random.randint(1000000000000000, 9999999999999999))
        return token
