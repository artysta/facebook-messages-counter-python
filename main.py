import tkinter as tk
from tkinter import ttk
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

    result_box.configure(state='normal')
    result_box.delete('1.0', tk.END)

    if 'error' in result:
        result_box.insert(tk.END, result['error'])
    else:
        total = result['Messages Count']
        output = f"Total number of messages: {total}\n\n"
        for name, count in result.items():
            if name != 'Messages Count':
                output += f"{name}: {count} messages ({get_percent(count, total)}%)\n"
        result_box.insert(tk.END, output)

    result_box.configure(state='disabled')

window = tk.Tk()
window.title("Facebook Message Analyzer (Dark Mode)")
window.geometry("720x500")
window.configure(bg="#2e2e2e")

style = ttk.Style()
style.theme_use("clam")

dark_bg = "#2e2e2e"
dark_panel = "#3a3a3a"
light_text = "#ffffff"
accent_color = "#4caf50"

style.configure("TFrame", background=dark_bg)
style.configure("TLabel", background=dark_bg, foreground=light_text, font=("Segoe UI", 12))
style.configure("TEntry", fieldbackground=dark_panel, foreground=light_text, font=("Segoe UI", 12))
style.configure("TButton", background=accent_color, foreground=light_text, font=("Segoe UI", 12, "bold"))
style.map("TButton", background=[("active", "#45a049")])

main_frame = ttk.Frame(window, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

phrase_label = ttk.Label(main_frame, text="Enter a phrase to search (optional):")
phrase_label.grid(row=0, column=0, sticky=tk.W)

phrase_entry = ttk.Entry(main_frame, width=40)
phrase_entry.grid(row=0, column=1, padx=10, pady=5)

count_button = ttk.Button(main_frame, text="Count", command=count_and_display)
count_button.grid(row=0, column=2, padx=10)

result_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=20, font=("Courier New", 10),
                                       bg=dark_panel, fg=light_text, insertbackground=light_text)
result_box.grid(row=1, column=0, columnspan=3, pady=20)
result_box.configure(state='disabled')

window.mainloop()
