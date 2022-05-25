import Huffman
import KMP


def search(files, keyword): 
    result = []
    for i in files:
        file = open(i, "r")
        result.append({"file": i, "num": KMP.count(file.read(), keyword)})
        file.close()

    def num(result):
        return result["num"]

    result.sort(key=num, reverse=True) 
    return result


def cal_words_freq(files, reverse=True): 
    result = {}
    for i in files:
        file = open(i, "r")
        content = file.read()
        for j in ',.:?"!\()0123456789\'':
                content = content.replace(j, "")
                content = content.replace("<br />"," ")
        word=""
        for j in range(len(content)):
            if content[j]!=" ":
                word+=content[j].lower()
            else:
                if word=='':
                    pass
                else:
                    if word not in result.keys():
                        result[word] = KMP.count(content.lower(), word)
                    word=""
        file.close()
    result2 = []
    for key in result.keys():
        result2.append({"word": key, "num": result[key]})

    def num(result):
        return result["num"]

    result2.sort(key=num, reverse=reverse)
    return result2


def cal_words_positions(files): 
    result = {}
    for i in files:
        file = open(i, "r")
        content = file.read()
        for j in ',.:?"!\()0123456789\'':
                content = content.replace(j, "")
                content = content.replace("<br />"," ")
        word=""
        for j in range(len(content)):
            if content[j]!=" ":
                word+=content[j].lower()
            else:
                if word=='':
                    pass
                else:
                    if word not in result.keys():
                        result[word] = KMP.positions(content.lower(), word)
                    word=""
        file.close()
    result2 = []
    for key in result.keys():
        result2.append({"word": key, "pos": result[key]})
    return result2


class File(object):
    def __init__(self, file_pos): 
        self.pos = file_pos
        self.chars_freqs = None
        self.Huffman_codes = None

    def get_content(self): 
        file = open(self.pos, "r")
        content = file.read()
        for j in ',.:?"!\()0123456789\'':
                content = content.replace(j, " ")
        content = content.replace("<br />"," ")
        file.close()
        return content

    def set_content(self, content): 
        file = open(self.pos, "w")
        file.write(content)
        file.close()

    def get_apperance_num(self, word): 
        return KMP.count(self.get_content(), word)

    def get_huffman_codes(self): 
        codes = []
        words = []
        if not self.chars_freqs:
            self.chars_freqs = Huffman.cal_count_freq(self.get_content())
        if not self.Huffman_codes:
            self.Huffman_codes = Huffman.cal_Huffman_codes(self.chars_freqs)
        for char in self.get_content():
            i = 0
            for item in self.chars_freqs:
                if char == item[0] and char not in words:
                    codes.append((char, self.Huffman_codes[i]))
                    words.append(char)
                i += 1
        return codes

    def get_encodeStr(self): 
        if not self.chars_freqs:
            self.chars_freqs = Huffman.cal_count_freq(self.get_content())
        if not self.Huffman_codes:
            self.Huffman_codes = Huffman.cal_Huffman_codes(self.chars_freqs)
        huffmanStr = ''
        for char in self.get_content():
            i = 0
            for item in self.chars_freqs:
                if char == item[0]:
                    huffmanStr += self.Huffman_codes[i]
                i += 1
        return huffmanStr

    def get_decodeStr(self, huffmanStr): 
        if not self.chars_freqs:
            self.chars_freqs = Huffman.cal_count_freq(self.get_content())
        if not self.Huffman_codes:
            self.Huffman_codes = Huffman.cal_Huffman_codes(self.chars_freqs)
        orignStr = ''
        while huffmanStr != '':
            i = 0
            for item in self.Huffman_codes:
                if item in huffmanStr:
                    if huffmanStr.index(item) == 0:
                        orignStr += self.chars_freqs[i][0]
                        huffmanStr = huffmanStr[len(item):]
                i += 1
        return orignStr

