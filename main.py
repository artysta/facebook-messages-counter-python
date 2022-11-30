import json
import os

def get_percent(number, total_number):
    return round(number / total_number * 100, 2)

def count_all_messages():
    names_to_messages = {}
    total_number_of_messages = 0

    for filename in os.listdir('./'):
        if '.json' not in filename:
            continue
        
        file = open(filename, 'r')
        data_json = json.load(file)
        messages = data_json['messages']

        for message in messages:
            sender_name = message['sender_name']
            total_number_of_messages += 1

            if sender_name in names_to_messages:
                names_to_messages[sender_name] = names_to_messages[sender_name] + 1
            else:
                names_to_messages[sender_name] = 0
        
    print(f'Całkowita liczba wiadomości {total_number_of_messages}.')

    for k, v in names_to_messages.items():
        print(f'{k} napisał {v} ({get_percent(v, total_number_of_messages)}%) wiadomości.')

count_all_messages()