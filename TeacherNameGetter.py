# coding=UTF-8
import os
import re
import requests

from lxml import etree


def get_name(film_number):
    result = ""
    url = r"https://www.javbus.com/" + film_number
    try:
        response = requests.get(url)
    except:
        print("Unable to connect to website", end="")
        return ''
    html = response.text
    selector = etree.HTML(html)
    person = selector.xpath('/html/body/div[5]/div[1]/div[2]/p/span/a/text()')
    no_name = selector.xpath('/html/body/div[5]/div[1]/div[2]/text()')
    for string in no_name:
        if string.find('暫無出演者資訊') != -1:
            return '无名'
    if len(person) == 0:
        return ''
    flag = 0
    for index in range(len(person)):
        if person[index] == '單體作品':
            flag = 1
            result = person[len(person) - 1]
            break
    if flag != 1:
        result = '多人'
    return result


def regex(name, n):
    match = re.search(r'.*?.com', name)
    if match is not None:
        name = name[match.end(0):len(name)]
    match = re.search('[0-9]{6}_[0-9]{3}-1pon|FC2-PPV-[0-9]{7}|FC2PPV-[0-9]{7}|heyzo-[0-9]{4}', name, re.IGNORECASE)
    if match is None:
        match = re.search(r'([A-Za-z]{2,' + str(n) + r'})-([0-9]{3})', name, re.IGNORECASE)
        if match is None:
            match = re.search(r'(<first>[A-Za-z]{3,4})(<second>[0-9]{3})', name, re.IGNORECASE)
            if match is None:
                return '', -1
            else:
                return (match.group(1) + '-' + match.group(2)), 0
        else:
            return match.group(0), 0
    else:
        return match.group(0), 1


def re_name(old_name, new_name):
    try:
        os.rename(old_name, new_name)
    except WindowsError:
        new_name = new_name[0:len(new_name) - 4] + '-2.mp4'
        try:
            os.rename(old_name, new_name)
        except:
            print("Unable to rename file:")


def main():
    src = input("Please enter the folder path, press Enter to set to the current folder:")
    if src == "":
        src = os.path.dirname(os.path.realpath(__file__))
        src = src.replace('\\', '/')
        print(src)
    try:
        f_list = os.listdir(src)
    except WindowsError:
        print("Wrong path.")
        return 0
    for name in f_list:
        new_name = ""
        new_file_name = ""
        old_name = name
        old_file_name = src + "/" + old_name
        actor_name = ""
        for numberLength in range(3, 6):
            reg_result = regex(name, numberLength)
            new_name = reg_result[0].upper()
            new_file_name = src + "/" + new_name + ".mp4"
            if reg_result[1] == 0:
                actor_name = get_name(new_name)
                if actor_name == "":
                    continue
                else:
                    new_file_name = src + "/" + actor_name + '_' + new_name + ".mp4"
            elif reg_result[1] == -1:
                actor_name = "unable to regex"
                new_file_name = old_file_name
                break
            elif reg_result[1] == 1:
                actor_name = "Infantry"
                break
        print(new_name + " ", end="")
        print(actor_name)
        re_name(old_file_name, new_file_name)


main()
