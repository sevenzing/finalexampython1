
from os import walk
import os
import json

def normalize(word):
    l = [',', ';', '.']
    for i in l:
        word = word.replace(i, '')
    return word

def is_country(word):
    return len(word.split()) == 1

def save_to_file(dir_name, file_name, text):
    # если нет такой папки то надо создать
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    full_path = dir_name + file_name
    # пишем в файл
    with open(full_path, 'w') as _file:
        _file.write(text)

def get_countries(content):
    countries = []
    for author in content['metadata']['authors']:
        if 'location' not in author['affiliation']:
            continue
        elif 'country' not in author['affiliation']['location']:
            continue
        countries.append(author['affiliation']['location']['country'])
    return countries

path = 'sample/'
files = []
for dirpath, dirnames, filenames in walk(path):
    for filename in filenames: 
        files.append(dirpath + filename)

jsons = []
for file_name in files:
    with open(file_name, 'r') as _file:
        jsons.append((file_name[7:][:-5], json.load(_file)))

# создание опорного списка
allowed_list = set()
for file_name, content in jsons:
    countries = get_countries(content)
    for country in countries:
        if is_country(country):
            allowed_list.add(normalize(country))

for file_name, content in jsons:
    title = content['metadata']['title']
    paragraphs = []
    for paragraph in content['body_text']:
        paragraphs.append(paragraph['text'])
    
    full_text = title + 3 * '\n' + '\n\n'.join(paragraphs)
    
    countries = get_countries(content)
    true_country = 'undefined'
    for country in countries:
        if normalize(country) in allowed_list:
            true_country = normalize(country)
            break
    
    save_to_file('by_country/' + true_country + '/', file_name + '.txt', full_text)
