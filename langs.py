# -*- coding: UTF-8 -*-
# Author: github.com/Young-Lord
# Time: 2020/10/6 17:30
import codecs

fix_zhen_lines = {
    "map.position.agent": "Agent 位置：|Agent Pos: %s, %s, %s",
    "map.position": "位置：|Position:%s, %s, %s",
    "options.builddate.format": "创建日期：|Build Date: %s",
    "options.protocolversion.format": "协议版本：|Protocol Version: %1%s"
}


# add wrong translators here


def get_text(line):
    return line[line.find('=') + 1:line.find('\t')]


def line_process(en_line, zh_line):
    global zhen_lines
    
    # special lines process
    if en_line[0] == '#' or en_line[0] == '\r' or en_line[0] == '\n' or en_line.find("=") == -1:
        zhen_lines.append(en_line)
        return
    
    g_zh = get_text(zh_line)
    g_en = get_text(en_line)
    if g_zh == g_en:
        zhen_lines.append(en_line)
        return

    for keyword, correct_text in fix_zhen_lines.items():
        if en_line[:en_line.find("=")] == keyword:
            zhen_lines.append(keyword + "=" + correct_text + "\r\n")
            return

    if g_zh.count("%s") != 0:
        for iterator in range(1, g_zh.count("%s")+1):
            g_zh = g_zh.replace("%s", "%" + str(iterator) + "$s")
            g_en = g_en.replace("%s", "%" + str(iterator) + "$s")
    # special lines process end

    zhen_line = en_line[:en_line.find("=") + 1]
    zhen_line += g_zh
    zhen_line += '|'
    zhen_line += g_en
    zhen_line += en_line[en_line.find('\t'):]
    if zhen_line[0] == '|':
        return
    zhen_lines.append(zhen_line)


# __main__
en = codecs.open(r"en_US.lang", encoding='utf-8')
zh = codecs.open(r"zh_CN.lang", encoding='utf-8')
en_lines = en.readlines()
zh_lines = zh.readlines()
zhen_lines = list()  # it means zh&en

for enline, zhline in zip(en_lines, zh_lines):
    line_process(enline, zhline)

# After this, zhen_lines should save zhen file content(end with \r\n)

zhen = codecs.open(r"zh&en.lang", 'w', encoding='utf-8')
for zhen_line in zhen_lines:
    #    print(zhen_line, end="")
    zhen.write(zhen_line)

en.close()
zh.close()
zhen.close()
