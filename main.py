import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext, messagebox
import json
import os
import matplotlib.pyplot as plt
import codecs

def fix_double_encoded(text):
    try:
        return codecs.decode(text.encode('latin1'), 'utf-8')
    except:
        return text

def get_percent(number, total_number):
    return round(number / total_number * 100, 2)

def count_messages(phrase):
    if not isinstance(phrase, str):
        return {'error': 'You must provide a string value!'}

    sender_message_counts = {'Messages Count': 0}

    for file_name in os.listdir('./'):
        if not file_name.endswith('.json'):
            continue

        encodings = ['utf-8-sig', 'utf-16', 'utf-8', 'cp1250', 'iso-8859-2']
        for enc in encodings:
            try:
                with open(file_name, 'r', encoding=enc) as file:
                    data_json = json.load(file)
                    break
            except Exception:
                continue
        else:
            print(f"Unable to read {file_name} with any known encoding.")
            continue

        messages = data_json.get('messages', [])
        for message in messages:
            sender_name = fix_double_encoded(message.get('sender_name', ''))
            if not sender_name:
                continue

            content = fix_double_encoded(message.get('content', '')).lower()

            if phrase == '' or phrase in content:
                sender_message_counts['Messages Count'] += 1
                if sender_name in sender_message_counts:
                    sender_message_counts[sender_name] += 1
                else:
                    sender_message_counts[sender_name] = 1

    return sender_message_counts

last_result = {}

def count_and_display():
    global last_result
    phrase = phrase_entry.get().strip().lower()
    result = count_messages(phrase)
    last_result = result

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

def show_bar_chart():
    show_chart(chart_type="bar")

def show_pie_chart():
    show_chart(chart_type="pie")

def show_chart(chart_type="bar"):
    if not last_result or 'Messages Count' not in last_result or last_result['Messages Count'] == 0:
        messagebox.showinfo("Info", "No data to display. Please run the count first.")
        return

    sorted_items = sorted(
        ((name, count) for name, count in last_result.items() if name != 'Messages Count'),
        key=lambda x: x[1],
        reverse=True
    )

    names = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    phrase = phrase_entry.get().strip()
    title_suffix = f"(phrase: '{phrase}')" if phrase else "(all messages)"
    title = f"Number of Messages by Sender {title_suffix}"

    plt.figure(figsize=(10, 6))
    if chart_type == "bar":
        plt.bar(names, counts, color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Sender')
        plt.ylabel('Number of messages')
    elif chart_type == "pie":
        plt.pie(counts, labels=names, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    plt.show()

window = tk.Tk()
window.title("Facebook Message Analyzer (Dark Mode)")
window.geometry("1200x600")
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

bar_chart_button = ttk.Button(main_frame, text="Show Bar Chart", command=show_bar_chart)
bar_chart_button.grid(row=0, column=3, padx=10)

pie_chart_button = ttk.Button(main_frame, text="Show Pie Chart", command=show_pie_chart)
pie_chart_button.grid(row=0, column=4, padx=10)

result_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=95, height=20, font=("Courier New", 10),
                                       bg=dark_panel, fg=light_text, insertbackground=light_text)
result_box.grid(row=1, column=0, columnspan=5, pady=20)
result_box.configure(state='disabled')

window.mainloop()
