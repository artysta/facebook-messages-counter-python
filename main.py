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
    if total_number == 0:
        return 0.00
    return round(number / total_number * 100, 2)

def count_messages(phrase):
    if not isinstance(phrase, str):
        return {'error': 'You must provide a string value!'}

    sender_message_counts = {'Messages Count': 0}

    if not os.path.exists('./'):
        return {'error': 'Current directory not found.'}

    json_files_found = False
    for file_name in os.listdir('./'):
        if not file_name.endswith('.json'):
            continue
        json_files_found = True

        encodings = ['utf-8-sig', 'utf-16', 'utf-8', 'cp1250', 'iso-8859-2']
        data_json = None
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

        if data_json:
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
    
    if not json_files_found:
        return {'error': 'No JSON files found in the current directory.'}

    return sender_message_counts

last_result = {}

def count_and_display():
    global last_result
    phrase = phrase_entry.get().strip().lower()
    
    result_box.configure(state='normal')
    result_box.delete('1.0', tk.END)
    result_box.insert(tk.END, "Processing data... please wait.\n")
    result_box.configure(state='disabled')
    window.update_idletasks()

    result = count_messages(phrase)
    last_result = result

    result_box.configure(state='normal')
    result_box.delete('1.0', tk.END)

    if 'error' in result:
        result_box.insert(tk.END, result['error'])
        messagebox.showerror("Error", result['error'])
    else:
        total = result['Messages Count']
        if total == 0:
            output = "No messages to analyze or no messages containing the specified phrase."
        else:
            output = f"Total number of messages: {total}\n\n"
            sorted_senders = sorted(
                ((name, count) for name, count in result.items() if name != 'Messages Count'),
                key=lambda x: x[1],
                reverse=True
            )
            for name, count in sorted_senders:
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

    filtered_items = [(name, count) for name, count in last_result.items() if name != 'Messages Count' and count > 0]
    
    if not filtered_items:
        messagebox.showinfo("Info", "No sender data to display charts.")
        return

    sorted_items = sorted(
        filtered_items,
        key=lambda x: x[1],
        reverse=True
    )

    names = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    phrase = phrase_entry.get().strip()
    title_suffix = f"(phrase: '{phrase}')" if phrase else "(all messages)"
    title = f"Number of Messages by Sender {title_suffix}"

    plt.figure(figsize=(12, 7), facecolor='#2e2e2e')
    
    plt.rc('axes', edgecolor='#A0A0A0', labelcolor='#ffffff')
    plt.rc('xtick', color='#ffffff')
    plt.rc('ytick', color='#ffffff')
    plt.rc('text', color='#ffffff')
    plt.rc('font', size=10)
    plt.rc('figure', autolayout=True)

    if chart_type == "bar":
        plt.bar(names, counts, color='#4CAF50')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Sender', labelpad=10)
        plt.ylabel('Number of messages', labelpad=10)
        plt.grid(axis='y', linestyle='--', alpha=0.6, color='#505050')
    elif chart_type == "pie":
        colors = plt.cm.viridis(counts / max(counts))
        plt.pie(counts, labels=names, autopct='%1.1f%%', startangle=140, colors=colors,
                textprops={'color': '#ffffff'})
        plt.axis('equal')
    
    plt.title(title, fontsize=14, pad=20, color='#ffffff')
    plt.tight_layout()
    plt.show()

window = tk.Tk()
window.title("Facebook Message Analyzer")
window.geometry("1200x600")
window.minsize(900, 500)
window.configure(bg="#1E1E1E")

style = ttk.Style()
style.theme_use("clam")

dark_bg = "#1E1E1E"
dark_panel = "#2B2B2B"
light_text = "#E0E0E0"
accent_color = "#4CAF50"
button_hover = "#5CB85C"
button_active = "#3D8E40"
border_color = "#404040"

style.configure("TFrame", background=dark_bg)
style.configure("TLabel", background=dark_bg, foreground=light_text, font=("Segoe UI", 11))

style.configure("TEntry", 
                fieldbackground=dark_panel, 
                foreground=light_text, 
                font=("Segoe UI", 11), 
                borderwidth=1, 
                relief="solid",
                bordercolor=border_color,
                insertbackground=light_text)

style.configure("TButton", 
                background=accent_color, 
                foreground=light_text, 
                font=("Segoe UI", 11, "bold"), 
                borderwidth=0, 
                relief="flat", 
                padding=(15, 7),
                focuscolor=accent_color)

style.map("TButton", 
          background=[("active", button_hover), ("pressed", button_active)],
          foreground=[("active", light_text)])

main_frame = ttk.Frame(window, padding=(30, 20, 30, 30))
main_frame.pack(fill=tk.BOTH, expand=True)

control_frame = ttk.Frame(main_frame)
control_frame.grid(row=0, column=0, columnspan=5, pady=(0, 25), sticky="ew")
main_frame.grid_columnconfigure(0, weight=1) 

phrase_label = ttk.Label(control_frame, text="Enter a phrase to search (optional):")
phrase_label.pack(side=tk.LEFT, padx=(0, 15))

phrase_entry = ttk.Entry(control_frame, width=35)
phrase_entry.pack(side=tk.LEFT, padx=(0, 25), ipady=3)

chart_buttons_frame = ttk.Frame(control_frame)
chart_buttons_frame.pack(side=tk.LEFT)

count_button = ttk.Button(chart_buttons_frame, text="Analyze", command=count_and_display)
count_button.pack(side=tk.LEFT, padx=(0, 10))

bar_chart_button = ttk.Button(chart_buttons_frame, text="Bar Chart", command=show_bar_chart)
bar_chart_button.pack(side=tk.LEFT, padx=(0, 10))

pie_chart_button = ttk.Button(chart_buttons_frame, text="Pie Chart", command=show_pie_chart)
pie_chart_button.pack(side=tk.LEFT)

result_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=90, height=20, font=("Consolas", 10),
                                       bg=dark_panel, fg=light_text, insertbackground=light_text,
                                       borderwidth=2, relief="solid", highlightbackground=accent_color, highlightcolor=accent_color)
result_box.grid(row=1, column=0, columnspan=5, pady=(0, 0), sticky="nsew") 
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

result_box.configure(state='disabled')

window.mainloop()