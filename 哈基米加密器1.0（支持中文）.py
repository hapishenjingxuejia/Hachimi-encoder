# 定义字符集
charset = ["哈", "基", "米", "南", "北", "绿", "豆", "曼", "波"]

def encrypt(plaintext, key):
    """
    加密函数（支持中英文字符）
    :param plaintext: 明文字符串（可含中文）
    :param key: 密钥，数字字符串，如"123"
    :return: 密文字符串
    """
    ciphertext = []
    key_digits = [int(k) for k in key]  # 将密钥转换为数字列表
    key_length = len(key_digits)
    key_ptr = 0
    
    # 将明文转换为UTF-8字节序列
    byte_data = plaintext.encode('utf-8')
    
    for byte in byte_data:
        k = key_digits[key_ptr]
        key_ptr = (key_ptr + 1) % key_length  # 循环使用密钥
        
        # 拆分高4位和低4位
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
        
        # 获取对应的密文字符
        cipher_char1 = charset[a - 1]
        cipher_char2 = charset[b - 1]
        cipher_char3 = charset[c - 1]
        cipher_char4 = charset[d - 1]
        
        ciphertext.extend([cipher_char1, cipher_char2, cipher_char3, cipher_char4])
    
    return ''.join(ciphertext)

def decrypt(ciphertext, key):
    """
    解密函数（支持中英文字符）
    :param ciphertext: 密文字符串
    :param key: 密钥，数字字符串，如"123"
    :return: 明文字符串
    """
    plaintext_bytes = bytearray()
    key_digits = [int(k) for k in key]  # 将密钥转换为数字列表
    key_length = len(key_digits)
    key_ptr = 0
    
    # 检查密文长度是否为4的倍数
    if len(ciphertext) % 4 != 0:
        raise ValueError("密文长度必须是4的倍数")
    
    for i in range(0, len(ciphertext), 4):
        cipher_part = ciphertext[i:i+4]
        
        # 解密高4位
        a = charset.index(cipher_part[0]) + 1
        b = charset.index(cipher_part[1]) + 1
        s_high = (a - 1) * 9 + b
        high = s_high - key_digits[key_ptr]
        
        # 解密低4位
        c = charset.index(cipher_part[2]) + 1
        d = charset.index(cipher_part[3]) + 1
        s_low = (c - 1) * 9 + d
        low = s_low - key_digits[key_ptr]
        
        key_ptr = (key_ptr + 1) % key_length  # 循环使用密钥
        
        # 组合高4位和低4位
        byte = (high << 4) | low
        
        # 检查字节是否有效（0-255）
        if byte < 0 or byte > 255:
            raise ValueError(f"解密后得到无效的字节: {byte}")
        
        plaintext_bytes.append(byte)
    
    # 将字节序列解码为字符串
    try:
        return plaintext_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("解密后的字节序列不是有效的UTF-8编码")

def main():
    print("欢迎使用哈基米加密工具（支持中英文）！")
    print("=" * 40)
    
    while True:
        print("\n请选择功能：")
        print("1. 加密明文")
        print("2. 解密密文")
        print("3. 退出")
        
        choice = input("请输入选项（1/2/3）: ").strip()
        
        if choice == "1":
            # 加密功能
            plaintext = input("请输入明文（可含中文）: ").strip()
            key = input("请输入密钥（数字串，如123）: ").strip()
            
            if not plaintext:
                print("错误：明文不能为空！")
                continue
            
            if not key.isdigit():
                print("错误：密钥必须为数字！")
                continue
            
            try:
                ciphertext = encrypt(plaintext, key)
                print(f"\n加密结果: {ciphertext}")
            except Exception as e:
                print(f"加密失败: {e}")
        
        elif choice == "2":
            # 解密功能
            ciphertext = input("请输入密文: ").strip()
            key = input("请输入密钥（数字串，如123）: ").strip()
            
            if not ciphertext:
                print("错误：密文不能为空！")
                continue
            
            if not key.isdigit():
                print("错误：密钥必须为数字！")
                continue
            
            try:
                plaintext = decrypt(ciphertext, key)
                print(f"\n解密结果: {plaintext}")
            except ValueError as e:
                print(f"解密失败: {e}")
        
        elif choice == "3":
            print("感谢使用，再见！")
            break
        
        else:
            print("无效选项，请重新输入！")

if __name__ == "__main__":
    main()