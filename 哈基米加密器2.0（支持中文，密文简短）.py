import zlib
import base64
from itertools import cycle

# 定义字符集
charset = ["哈", "基", "米", "南", "北", "绿", "豆", "曼", "波"]

def compress_data(data):
    """压缩数据并返回Base64编码"""
    compressed = zlib.compress(data.encode('utf-8'))
    return base64.b64encode(compressed).decode('ascii')

def decompress_data(compressed_data):
    """解压Base64编码的数据"""
    compressed = base64.b64decode(compressed_data.encode('ascii'))
    return zlib.decompress(compressed).decode('utf-8')

def encrypt(plaintext, key):
    """
    优化后的加密函数
    :param plaintext: 明文字符串
    :param key: 密钥字符串
    :return: 密文字符串
    """
    # 先压缩数据
    compressed = compress_data(plaintext)
    
    ciphertext = []
    key_cycle = cycle(int(k) for k in key)
    
    for byte in compressed.encode('ascii'):
        k = next(key_cycle)
        
        # 拆分高低4位
        high = byte >> 4
        low = byte & 0x0F
        
        # 加密高4位
        s_high = high + k
        a = ((s_high - 1) // 9) + 1
        b = ((s_high - 1) % 9) + 1
        
        # 加密低4位
        s_low = low + k
        c = ((s_low - 1) // 9) + 1
        d = ((s_low - 1) % 9) + 1
        
        ciphertext.extend([
            charset[a - 1],
            charset[b - 1],
            charset[c - 1],
            charset[d - 1]
        ])
    
    return ''.join(ciphertext)

def decrypt(ciphertext, key):
    """
    优化后的解密函数
    :param ciphertext: 密文字符串
    :param key: 密钥字符串
    :return: 明文字符串
    """
    if len(ciphertext) % 4 != 0:
        raise ValueError("密文长度必须是4的倍数")
    
    compressed_bytes = bytearray()
    key_cycle = cycle(int(k) for k in key)
    
    for i in range(0, len(ciphertext), 4):
        part = ciphertext[i:i+4]
        
        # 解密高4位
        a = charset.index(part[0]) + 1
        b = charset.index(part[1]) + 1
        s_high = (a - 1) * 9 + b
        high = s_high - next(key_cycle)
        
        # 解密低4位
        c = charset.index(part[2]) + 1
        d = charset.index(part[3]) + 1
        s_low = (c - 1) * 9 + d
        low = s_low - next(key_cycle)
        
        byte = (high << 4) | low
        if byte < 0 or byte > 255:
            raise ValueError("无效的字节值")
        
        compressed_bytes.append(byte)
    
    # 解压数据
    try:
        compressed_data = compressed_bytes.decode('ascii')
        return decompress_data(compressed_data)
    except Exception as e:
        raise ValueError(f"解密失败: {str(e)}")

def main():
    print("优化版哈基米加密工具（支持中英文，压缩优化）")
    print("=" * 50)
    
    while True:
        print("\n请选择功能：")
        print("1. 加密明文")
        print("2. 解密密文")
        print("3. 退出")
        
        choice = input("请输入选项（1/2/3）: ").strip()
        
        if choice == "1":
            plaintext = input("请输入明文（可含中文）: ").strip()
            if not plaintext:
                print("错误：明文不能为空！")
                continue
            
            key = input("请输入密钥（数字串）: ").strip()
            if not key.isdigit():
                print("错误：密钥必须为数字！")
                continue
            
            try:
                ciphertext = encrypt(plaintext, key)
                print(f"\n加密结果（长度：{len(ciphertext)}）:")
                print(ciphertext)
            except Exception as e:
                print(f"加密失败: {e}")
        
        elif choice == "2":
            ciphertext = input("请输入密文: ").strip()
            if not ciphertext:
                print("错误：密文不能为空！")
                continue
            
            key = input("请输入密钥: ").strip()
            if not key.isdigit():
                print("错误：密钥必须为数字！")
                continue
            
            try:
                plaintext = decrypt(ciphertext, key)
                print(f"\n解密结果: {plaintext}")
            except Exception as e:
                print(f"解密失败: {e}")
        
        elif choice == "3":
            print("感谢使用，再见！")
            break
        
        else:
            print("无效选项，请重新输入！")

if __name__ == "__main__":
    main()