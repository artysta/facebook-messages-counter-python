import json
import os

def get_percent(number, total_number):
    return round(number / total_number * 100, 2)

def count_messages(phrase):
    if not isinstance(phrase, str):
        print('Musisz podać wartość String!')
        return

    names_to_messages = { 'Messages Count': 0 }

    for file_name in os.listdir('./'):
        if '.json' not in file_name:
            continue
        
        file = open(file_name, 'r')
        data_json = json.load(file)
        messages = data_json['messages']

        for message in messages:
            sender_name = message['sender_name']

            if sender_name in names_to_messages:
                if (phrase == '') or (phrase != '' and 'content' in message and phrase in message['content'].lower()):
                    names_to_messages['Messages Count'] += 1
                    names_to_messages[sender_name] = names_to_messages[sender_name] + 1
            else:
                names_to_messages['Messages Count'] += 1
                names_to_messages[sender_name] = 1

    file.close()

    return names_to_messages

def print_result(dictionary):
    print(f'Całkowita liczba wiadomości {dictionary["Messages Count"]}.')

    for k, v in dictionary.items():
        print(f'{k} napisał {v} ({get_percent(v, dictionary["Messages Count"])}%) wiadomości.')

result = count_messages('')
print_result(result)