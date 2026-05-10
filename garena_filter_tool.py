
import tkinter as tk
from tkinter import filedialog, messagebox
import os

selected_file = ""

def process_file(filepath):
    base_dir = os.path.dirname(filepath)
    output_file = os.path.join(base_dir, "garena_filtered.txt")

    results = []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if "garena" not in line.lower():
                continue

            parts = line.split(":")

            if len(parts) >= 3:
                username = parts[-2].strip()
                password = parts[-1].strip()

                if username and password:
                    results.append(f"{username}:{password}")

    with open(output_file, "w", encoding="utf-8") as out:
        for item in results:
            out.write(item + "\n")

    return output_file, len(results)

def choose_file():
    global selected_file

    filepath = filedialog.askopenfilename(
        title="Chọn file TXT",
        filetypes=[("Text Files", "*.txt")]
    )

    if filepath:
        selected_file = filepath
        file_label.config(text=f"Đã chọn:\\n{os.path.basename(filepath)}")

def run_filter():
    global selected_file

    if not selected_file:
        messagebox.showwarning("Thiếu file", "Vui lòng chọn file TXT.")
        return

    status_label.config(text="Đang xử lý...")
    root.update()

    try:
        output_file, total = process_file(selected_file)

        status_label.config(text="Hoàn thành!")

        messagebox.showinfo(
            "Xong",
            f"Đã lọc {total} dòng.\\n\\nFile xuất:\\n{output_file}"
        )

    except Exception as e:
        status_label.config(text="Có lỗi")
        messagebox.showerror("Lỗi", str(e))

root = tk.Tk()
root.title("Garena Filter Tool")
root.geometry("520x300")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Tool Lọc URL Garena",
    font=("Arial", 16, "bold")
)
title.pack(pady=15)

desc = tk.Label(
    root,
    text="Lọc các dòng chứa 'garena' và xuất user:pass",
    wraplength=420
)
desc.pack(pady=5)

choose_btn = tk.Button(
    root,
    text="Chọn File TXT",
    command=choose_file,
    width=25,
    height=2
)
choose_btn.pack(pady=15)

file_label = tk.Label(root, text="Chưa chọn file")
file_label.pack(pady=5)

run_btn = tk.Button(
    root,
    text="Bắt Đầu Lọc",
    command=run_filter,
    width=25,
    height=2
)
run_btn.pack(pady=20)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
