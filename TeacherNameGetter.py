# coding=UTF-8
import os,re,requests
from lxml import etree
def getName(input):
    url = r'https://www.javbus.com/'+input 
    try:
        response = requests.get(url)
    except:
        print("Unable to connect to website",end="")
        return ''
    html = response.text
    selector = etree.HTML(html)
    person = selector.xpath('/html/body/div[5]/div[1]/div[2]/p/span/a/text()')
    noName = selector.xpath('/html/body/div[5]/div[1]/div[2]/text()')
    for string in noName:
        if string.find('暫無出演者資訊')!= -1:
            return '无名'
    if len(person)==0:
        #print("unvalid file name",end="")
        return ''
    flag = 0
    for index in range(len(person)):
        if person[index] =='單體作品':
            flag = 1
            result = person[len(person)-1]
            break
    if flag != 1:
        result = '多人'
    return (result)

def regex(name,n):
    match = re.search(r'.*?.com',name)
    if match != None:
        name = name[match.end(0):len(name)]
    match = re.search('[0-9]{6}_[0-9]{3}-1pon|FC2-PPV-[0-9]{7}|FC2PPV-[0-9]{7}|heyzo-[0-9]{4}',name,re.IGNORECASE)
    if match == None:
        match = re.search(r'([A-Za-z]{2,'+str(n)+r'})-([0-9]{3})',name,re.IGNORECASE)
        if match == None:
            match = re.search(r'(<first>[A-Za-z]{3,4})(<second>[0-9]{3})',name,re.IGNORECASE)
            if match == None:
                return '',-1
            else:
                return (match.group(1)+'-'+match.group(2)),0
        else:
            return match.group(0),0
    else:
        return match.group(0),1

def reName(oldName,newName):
    try:
        os.rename(oldName,newName)
    except WindowsError:
        newName = newName[0:len(newName)-4]+'-2.mp4'
        try:
            os.rename(oldName,newName)
        except:
            print("Unable to rename file:")

def main():
    src= input("Please enter the folder path, press Enter to set to the current folder:")
    if src == "":
        src = os.path.dirname(os.path.realpath(__file__))
        src = src.replace('\\','/')
        print (src)
    try:
        flist = os.listdir(src)
    except WindowsError:
        print("Wrong path.")
        return 0
    for name in flist:
        situation = ""
        oldName = name
        oldfileName = src+"/"+ oldName
        actorName = ""
        for numberLength in range(3,6):
            regResult = regex(name,numberLength)
            newName = regResult[0].upper()
            newfileName = src+"/"+newName+".mp4"
            if regResult[1] == 0:
                actorName = getName(newName)
                if actorName == "":
                    continue
                else:
                    newfileName = src+"/"+actorName+'_'+newName+".mp4"
            elif regResult[1] == -1:
                actorName = "unRegexable"
                newfileName = oldfileName
                break
            elif regResult[1] == 1:
                actorName = "Infantry"
                break
        print(newName+" ",end="")
        print (actorName)
        reName(oldfileName,newfileName)
main()