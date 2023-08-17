class KeyManager:
    armstrong_numbers = [153,370,371,407]
    base_table = [1234,1243,1324,1342,1423,1432,2134,2143,2314, 2341, 2413, 2431, 3124, 3142, 3214, 3241,3412, 3421, 4123, 4132, 4213, 4231, 4312, 4321]

    def __init__(self, remark):
        sum = self.__ascii_sum__(remark)
        permutation = KeyManager.base_table[sum % len(KeyManager.base_table)]
        portionA = self.__buildPortionA__(remark, permutation)
        self.xorkey = str(portionA) + str(sum)

    def get_xor_key(self):
        return self.xorkey

    def __ascii_sum__(self, remark):
        sum = 0
        for i in remark:
            sum+= ord(i)
        return sum

    def __buildPortionA__(self, remark, permutation):
        portionA = ''
        while permutation > 0:
            portionA = str(KeyManager.armstrong_numbers[permutation % 10 -1]) + portionA
            permutation = permutation//10
        return portionA


class Encryptor:

    def __init__(self, remark):
        self.km = KeyManager(remark)

    def level1(self, data):
        enc_data = ''
        xor_key =self.km.get_xor_key()
        kl = len(xor_key)
        indx = 0
        for x in data:
            enc_data += chr(ord(x) ^ int(xor_key[indx]))
            indx = (indx + 1) % kl

        return enc_data

    def level2(self, enc_data):
        enc_enc_data = ''
        color = ColorManager.getColor(self.km.get_xor_key())
        r = 0
        c = 0
        number = 0
        i =0
        cl = len(color)

        for x in enc_data:
            r,c = self.__splitByte__(ord(x))
            number = (color[i] + r * 16 + c)%256
            i = (i+1)%cl
            enc_enc_data += chr(number)

        return enc_enc_data

    def __splitByte__(self, x):
        nibble1 = x >> 4
        nibble2 = x & 15
        return nibble1, nibble2

class Decryptor:

    def __init__(self, remark):
        self.km = KeyManager(remark)

    def level1(self, enc_data):
        data = ''
        xor_key =self.km.get_xor_key()
        kl = len(xor_key)
        indx = 0
        for x in enc_data:
            data += chr(ord(x) ^ int(xor_key[indx]))
            indx = (indx + 1) % kl

        return data

    def level2(self, enc_enc_data):
        dec_dec_data = ''
        color = ColorManager.getColor(self.km.get_xor_key())

        r = 0
        c = 0
        temp = 0
        i =0
        cl = len(color)

        for x in enc_enc_data:
            temp = (ord(x) - color[i] + 256)%256
            i = (i+1)%cl
            r = temp //16
            c = temp % 16
            dec_dec_data += chr(self.__mergeBits__(r,c))

        return dec_dec_data

    def __mergeBits__(self, r, c):
        return (r << 4) | c

class ColorManager:
    @classmethod
    def getColor(cls, xor_key):
        r = (int(xor_key[0:4]) + int(xor_key[12:])) %256
        g = (int(xor_key[4:8]) + int(xor_key[12:])) %256
        b = (int(xor_key[8:12]) + int(xor_key[12:])) %256
        return r,g,b