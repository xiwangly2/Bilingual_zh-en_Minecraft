# -*- coding: UTF-8 -*-
# Author: github.com/Young-Lord
# Time: 2020/10/6 17:30
import codecs
import os,sys
print("If you got a luan4 ma3 , please give me a issue")

fix_zhen_lines = {
    "map.position.agent": "Agent 位置：|Agent Pos: %s, %s, %s",
    "map.position": "位置：|Position:%s, %s, %s",
    "options.builddate.format": "创建日期：|Build Date: %s",
    "options.protocolversion.format": "协议版本：|Protocol Version: %1%s",
    "xbox.profile.realName": "在 Xbox 应用程序中管理用于共享您的实际姓名的隐私设置。  |  Manage your privacy settings for sharing your real name in the Xbox app."
}# add wrong translators here


def get_text(line):
    if line.find('\t')!=-1:
        return line[line.find('=') + 1:line.find('\t')]
    elif line.find('\r')!=-1:
        return line[line.find('=') + 1:line.find('\r')]
    else:
        return line[line.find('=') + 1:line.find('\n')]

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
        #print(en_line)
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

def info(zh,en=""):
    print("[INFO]"+zh,end="")
    if en!='':
        print("|",end="")
    print(en)

def error(zh,en=""):
    print("[ERROR]"+zh,end="")
    if en!='':
        print("|",end="")
    print(en)
    exit()
# __main__
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
try:
    en = codecs.open(r"en_US.lang", encoding='utf-8')
    zh = codecs.open(r"zh_CN.lang", encoding='utf-8')
    load_from="local"
except FileNotFoundError:
    en.close()
    zh.close()
    info("请将MCBE的语言文件（en_US.lang和zh_CN.lang）复制到程序目录下")
    info("一般情况下，他们位于（win10）"+r"C:\Program Files\WindowsApps\Microsoft.MinecraftUWP_"+"[当前版本号]"+r"_x64__8wekyb3d8bbwe\data\resource_packs\vanilla\texts"+"目录下")
    info("个人建议用Everything搜索这两个文件")
    error("寻找待合成的文件失败！")

en_lines = en.readlines()
zh_lines = zh.readlines()
zhen_lines = list()  # it means zh&en

for enline, zhline in zip(en_lines, zh_lines):
    line_process(enline, zhline)

# After this, zhen_lines should save zhen file content(end with \r\n)
choice_fonts=input("[ASK]是否使用字体修复（可以让文字显示更清晰，但是会替换掉纯中文的语言选项）\n是-默认(y) 否(n):")
if choice_fonts=='y' or choice_fonts=='是' or choice_fonts=='yes' or choice_fonts=='Y' or choice_fonts=='':
    zhen = codecs.open(r"./texts/zh_CN.lang", 'w', encoding='utf-8')
    config_file=open("./texts/languages.json")
    content=config_file.read()
    config_file.close()
    if content.find("zh&en") != -1:
        content=content.replace('  "zh&en",',"")
        content=content.replace("\n\n","\n")
        content=content.replace("\n\n","\n")
    config_file=open("./texts/languages.json","w")
    config_file.write(content)
    config_file.close()
    config_file=codecs.open("./texts/language_names.json", 'r', encoding='utf-8')
    content=config_file.read()
    config_file.close()
    if content.find('[ "zh&en", "中英双语" ],')!=-1:
        content=content.replace('[ "zh_CN", "简体中文 (中国)" ],[ "zh&en", "中英双语" ],','[ "zh_CN", "中英双语" ],')
    config_file=codecs.open("./texts/language_names.json", 'w', encoding='utf-8')
    config_file.write(content)
    config_file.close()
    
else:
    try:
       os.remove("./texts/zh_CN.lang")
    except:
        pass
    zhen = codecs.open(r"./texts/zh&en.lang", 'w', encoding='utf-8')
    config_file=open("./texts/languages.json")
    content=config_file.read()
    config_file.close()
    if content.find("zh&en") == -1:
        content=content[:2]+'  "zh&en",\r\n'+content[2:]
        content=content.replace("\n\n","\n")
        content=content.replace("\n\n","\n")
    config_file=open("./texts/languages.json","w")
    config_file.write(content)
    config_file.close()
    config_file=codecs.open("./texts/language_names.json", 'r', encoding='utf-8')
    content=config_file.read()
    config_file.close()
    if content.find('[ "zh_CN", "中英双语" ],')!=-1:
        content=content.replace('[ "zh_CN", "中英双语" ],','[ "zh_CN", "简体中文 (中国)" ],[ "zh&en", "中英双语" ],')
    config_file=codecs.open("./texts/language_names.json", 'w', encoding='utf-8')
    config_file.write(content)
    config_file.close()

for zhen_line in zhen_lines:
    #    print(zhen_line, end="")
    zhen.write(zhen_line)

en.close()
zh.close()
zhen.close()
