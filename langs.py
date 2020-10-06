# -*- coding: UTF-8 -*-
# Author: github.com/Young-Lord
# Time: 2020/10/6 17:30
import codecs


def get_text(line):
    return line[line.find('=') + 1:line.find('\t')]


def line_process(en_line, zh_line):
    global zhen_lines
    if en_line[0] == '#' or en_line[0] == '\r' or en_line.find("menu.copyright") != -1:
        zhen_lines.append(en_line)
        return
    zhen_line = en_line[:en_line.find("=") + 1]
    zhen_line += get_text(zh_line)
    zhen_line += '|'
    zhen_line += get_text(en_line)
    zhen_line += en_line[en_line.find('\t'):]
    zhen_lines.append(zhen_line)


en = codecs.open(r"en_US.lang", encoding='utf-8')
zh = codecs.open(r"zh_CN.lang", encoding='utf-8')
en_lines = en.readlines()
zh_lines = zh.readlines()
zhen_lines = list()

# print(en_lines[11])
# print(zh_lines[11])


# Main program
for enline, zhline in zip(en_lines, zh_lines):
    line_process(enline, zhline)

# After this, zhen_lines should save zhen file content(end with \r\n)

zhen = codecs.open(r"zh&en.lang", 'w', encoding='utf-8')
for zhen_line in zhen_lines:
    print(zhen_line, end="")
    zhen.write(zhen_line)

en.close()
zh.close()
zhen.close()