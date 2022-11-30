import json

def get_percent(number, total_number):
    return round(number / total_number * 100, 2)

file = open('message_1.json', 'r')
data_json = json.load(file)
messages = data_json['messages']

name_to_messages = {}
total_number_of_messages = 0

for message in messages:
    sender_name = message['sender_name']
    total_number_of_messages += 1

    if sender_name in name_to_messages:
        name_to_messages[sender_name] = name_to_messages[sender_name] + 1
    else:
        name_to_messages[sender_name] = 0

print(f'Całkowita liczba wiadomości {total_number_of_messages}.')

for k, v in name_to_messages.items():
    print(f'{k} napisał {v} ({get_percent(v, total_number_of_messages)}%) wiadomości.') 