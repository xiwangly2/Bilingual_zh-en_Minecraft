# -*- coding: UTF-8 -*-
# Author: github.com/Young-Lord
# Time(V1): 2020/10/6 17:30
# Time(V2): 2021/1/25 18:23
import codecs
import os,sys
print("If you got a luan4 ma3 , please give me a issue")




def has_content(line):
    if line[0] in ['#','\r','\n',' ']:
        return False
    if line.find('=')!=-1:
        return True
    info("line="+line)
    error("出bug了，请联系我并附带上两个.lang文件（位置：has_content）")

def get_name(line):
    if has_content(line):
        return line[:line.find("=")]
    else:
        return ''

def get_text(line):
    if has_content(line):
        if line.find('\t')!=-1:
            return line[line.find('=') + 1:line.find('\t')]
        elif line.find('\r')!=-1:
            return line[line.find('=') + 1:line.find('\r')]
        else:
            return line[line.find('=') + 1:line.find('\n')]
    else:
        return ''

def get_empty(line):
    if line.find('\t')!=-1:
        return line[line.find('\t'):line.find('#')]
    else:
        return ''

def get_comment(line):
    return (line.rstrip())[line.find("#")+1:]

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
    os._exit(3)


info("程序目录:"+os.path.abspath(os.path.dirname(sys.argv[0])))
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
f=codecs.open(r"错误翻译.py", encoding='utf-8')
contenttt=f.read().replace('\r','').replace('\n','')
contenttt=contenttt[contenttt.find("=")+1:]
f.close()
fix_zhen_lines = eval(contenttt)
try:
    en = codecs.open(r"en_US.lang", encoding='utf-8')
    zh = codecs.open(r"zh_CN.lang", encoding='utf-8')
    load_from="local"
except FileNotFoundError:
    try:
        en.close()
    except:
        pass
    try:
        zh.close()
    except:
        pass
    info("请将MCBE的语言文件（en_US.lang和zh_CN.lang）复制到程序目录下")
    info("一般情况下，他们位于（win10）"+r"C:\Program Files\WindowsApps\Microsoft.MinecraftUWP_"+"[当前版本号]"+r"_x64__8wekyb3d8bbwe\data\resource_packs\vanilla\texts"+"目录下")
    info("个人建议用Everything搜索这两个文件")
    error("寻找待合成的文件失败！")

en_lines = en.readlines()
en_lines[0] = en_lines[0].replace('\ufeff','')
zh_lines = zh.readlines()
zh_lines[0] = zh_lines[0].replace('\ufeff','')
en.close()
zh.close()
zhen = codecs.open("./texts/zh&en.lang", 'w', encoding='utf-8')

#MAIN PROGRESS
res_lines=list()
current_index=0
res_lines_index=dict()
for i in zh_lines:
    #print(i.strip())
    #if get_name(i)!='':
    #    print(get_name(i),end="=")
    #print("{}{}{}{}\r\n".format(get_text(i),get_empty(i),"#" if i.find("#")!=-1 else "",get_comment(i)))
    if not has_content(i):
        res_lines.append(i)
        current_index+=1
        continue
    res_lines_index[get_name(i)]=current_index
    res_lines.append({"name":get_name(i),"zh":get_text(i),"en":"","empty":get_empty(i),"comment":get_comment(i),"commented":(True if i.find("#")!=-1 else False)})
    current_index+=1
for i in en_lines:
    if not has_content(i):
        continue
    if get_name(i) not in res_lines_index.keys():
        res_lines.append({"name":get_name(i),"zh":"","en":get_text(i),"empty":get_empty(i),"comment":get_comment(i),"commented":(True if i.find("#")!=-1 else False)})
    else:
        res_lines[res_lines_index[get_name(i)]]["en"]=get_text(i)

for i in res_lines:
    if type(i)==str:
        zhen.write(i.rstrip()+"\r\n")
        continue
    if i["comment"]=="":
        i["empty"]=""
        i["commented"]=False
    if i["name"] in fix_zhen_lines.keys():
        zhen.write(i["name"]+"="+fix_zhen_lines[i["name"]]+"\r\n")
        continue
    if i["zh"]==i["en"]:
        zhen.write("{}={}{}{}{}\r\n".format(i["name"],i["zh"],i["empty"],"#" if i["commented"] else "",i["comment"]))
        continue
    if i["zh"].count("%s") > 0:
        for iterator in range(1, i["zh"].count("%s")+1):
            i["zh"] = i["zh"].replace("%s", "%" + str(iterator) + "$s",1)
            i["en"] = i["en"].replace("%s", "%" + str(iterator) + "$s",1)
    if i["zh"].count("%d") > 0:
        for iterator in range(1, i["zh"].count("%d")+1):
            i["zh"] = i["zh"].replace("%d", "%" + str(iterator) + "$d",1)
            i["en"] = i["en"].replace("%d", "%" + str(iterator) + "$d",1)
    zhen.write(i["name"]+"=")
    zhen.write(i["zh"].rstrip())
    if not(i["zh"]=='' or i["en"]=='' or (i["zh"]==i["en"])):
        zhen.write("|")
    if not (i["zh"]==i["en"]):
        zhen.write(i["en"].rstrip())
    zhen.write(i["empty"])
    if i["commented"]:
        zhen.write("#"+(i["comment"].rstrip()))
    zhen.write("\r\n")

zhen.close()
info("生成成功！")
os.system("pause")