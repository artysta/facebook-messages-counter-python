import tkinter as tk
from tkinter import scrolledtext
import json
import os

def get_percent(number, total_number):
    return round(number / total_number * 100, 2)

def count_messages(phrase):
    if not isinstance(phrase, str):
        return {'error': 'You must provide a string value!'}

    sender_message_counts = { 'Messages Count': 0 }

    for file_name in os.listdir('./'):
        if not file_name.endswith('.json'):
            continue

        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data_json = json.load(file)
                messages = data_json.get('messages', [])

                for message in messages:
                    sender_name = message.get('sender_name')
                    if not sender_name:
                        continue

                    content = message.get('content', '').lower()

                    if sender_name in sender_message_counts:
                        if phrase == '' or phrase in content:
                            sender_message_counts['Messages Count'] += 1
                            sender_message_counts[sender_name] += 1
                    else:
                        if phrase == '' or phrase in content:
                            sender_message_counts['Messages Count'] += 1
                            sender_message_counts[sender_name] = 1
        except Exception as e:
            print(f'Error while processing {file_name}: {e}')

    return sender_message_counts

def count_and_display():
    phrase = phrase_entry.get().strip().lower()
    result = count_messages(phrase)

    if 'error' in result:
        result_box.delete('1.0', tk.END)
        result_box.insert(tk.END, result['error'])
        return

    total = result['Messages Count']
    output = f"Total number of messages: {total}\n\n"
    for name, count in result.items():
        if name != 'Messages Count':
            output += f"{name}: {count} messages ({get_percent(count, total)}%)\n"

    result_box.delete('1.0', tk.END)
    result_box.insert(tk.END, output)

window = tk.Tk()
window.title("Facebook Message Analyzer")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
width = screen_width // 2
height = screen_height // 2
x = screen_width // 4
y = screen_height // 4
window.geometry(f"{width}x{height}+{x}+{y}")

phrase_label = tk.Label(window, text="Enter a phrase (optional):", font=("Arial", 14))
phrase_label.pack(pady=5)

phrase_entry = tk.Entry(window, font=("Arial", 14), width=40)
phrase_entry.pack(pady=5)

count_button = tk.Button(window, text="Count", font=("Arial", 16), command=count_and_display)
count_button.pack(pady=10)

result_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=15, font=("Courier New", 12))
result_box.pack(pady=10)

window.mainloop()
