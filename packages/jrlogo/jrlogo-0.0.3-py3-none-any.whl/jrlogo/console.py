from typing import Union, Tuple

sys_input = input  # 备份系统的input函数

_buf = ""  # 输入缓冲区

def _get_word_from_str(s: str) -> Tuple[str, str]:
    """从字符串s中获取一个单词，返回单词和剩余字符串"""
    s = s.lstrip()
    if s == "":
        return "", ""
    i = 0
    while i < len(s) and s[i] > ' ':
        i += 1
    return s[:i], s[i:]

def _read_word() -> Union[str, None]:
    """从输入缓冲区中读取一个单词，返回None时表示输入结束"""
    global _buf
    try:
        while True:
            if _buf == "":
                _buf = sys_input()
            word, _buf = _get_word_from_str(_buf)
            if word != "":
                return word
    except EOFError:
        return None

def read(type=None):
    """从输入缓冲区中读取一个词，根据type类型参数，返回不同类型的值"""
    word = _read_word()
    if word is None:
        return None
    if type == None:
        # 自动判断类型
        try:
            x = float(word)
            if x.is_integer():
                return int(x)
            return x
        except:
            return word
    elif type == int:
        return int(word)
    elif type == float:
        return float(word)
    else:
        return word
    
def readline() -> str:
    """从输入缓冲区中读取一行"""
    global _buf
    if _buf == "":
        buf = sys_input()
        _buf = ""
        return buf
    else:
        buf = _buf
        _buf = ""
    return buf

write = print  # 重命名系统的print函数

if __name__ == "__main__":
    while True:
        x = read()
        write(x, " | ")
        if x is None:
            break