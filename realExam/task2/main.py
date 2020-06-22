import re
import csv

file_name = 'language.csv'

#считываем файл
content = []
with open(file_name) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    first = True
    for row in readCSV:
        if first:
            all_features = row[10:] 
        else:
            content.append(row)
        first = False

    features_counter = {name:0 for name in all_features}


# считаем сколько признаков встретилось
for features in content:
    for feature_name, i in zip(all_features, features):
        if i != '':
            features_counter[feature_name] += 1

n = len(content)
wellknown_features, specific_features, rare_features = [], [], []

# подготавливаем списки для записи в файл
for feature_name in features_counter:
    if features_counter[feature_name] / n >= 0.5:
        wellknown_features.append(feature_name)
    elif re.match(r'^[\w ]*in[\w -]*[lL]anguages$', feature_name) != None:
        specific_features.append(feature_name)
    else:
        rare_features.append(feature_name)
    
# запись в файлы 

with open('wellknown_features.txt', 'w') as _file:
    _file.write('\n'.join(wellknown_features))


with open('specific_features.txt', 'w') as _file:
    _file.write('\n'.join(specific_features))


with open('rare_features.txt', 'w') as _file:
    _file.write('\n'.join(rare_features))