
import tkinter as tk
from tkinter import filedialog, messagebox
import os

selected_file = ""

def split_file(filepath, parts):
    file_size = os.path.getsize(filepath)
    target_size = max(1, file_size // parts)

    base_dir = os.path.dirname(filepath)
    filename = os.path.splitext(os.path.basename(filepath))[0]

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        part_num = 1
        current_size = 0

        output_path = os.path.join(base_dir, f"{filename}_part_{part_num}.txt")
        out = open(output_path, "w", encoding="utf-8")

        for line in f:
            encoded = line.encode("utf-8")

            if current_size >= target_size and part_num < parts:
                out.close()
                part_num += 1
                current_size = 0
                output_path = os.path.join(base_dir, f"{filename}_part_{part_num}.txt")
                out = open(output_path, "w", encoding="utf-8")

            out.write(line)
            current_size += len(encoded)

        out.close()

    return base_dir

def choose_file():
    global selected_file

    filepath = filedialog.askopenfilename(
        title="Chọn file TXT",
        filetypes=[("Text Files", "*.txt")]
    )

    if filepath:
        selected_file = filepath
        file_label.config(text=f"Đã chọn:\n{os.path.basename(filepath)}")

def run_split():
    global selected_file

    if not selected_file:
        messagebox.showwarning("Thiếu file", "Vui lòng chọn file TXT.")
        return

    try:
        parts = int(parts_entry.get())

        if parts <= 0:
            raise ValueError

    except:
        messagebox.showerror("Lỗi", "Số lượng file phải là số nguyên > 0")
        return

    status_label.config(text="Đang xử lý...")
    root.update()

    try:
        output_dir = split_file(selected_file, parts)

        status_label.config(text="Hoàn thành!")

        messagebox.showinfo(
            "Xong",
            f"Đã tách thành {parts} file.\n\nThư mục:\n{output_dir}"
        )

    except Exception as e:
        status_label.config(text="Có lỗi xảy ra")
        messagebox.showerror("Lỗi", str(e))

root = tk.Tk()
root.title("TXT Splitter Pro")
root.geometry("500x320")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Tool Tách File TXT",
    font=("Arial", 16, "bold")
)
title.pack(pady=15)

desc = tk.Label(
    root,
    text="Chọn file TXT và nhập số lượng file muốn tách",
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
choose_btn.pack(pady=10)

file_label = tk.Label(root, text="Chưa chọn file")
file_label.pack(pady=5)

parts_frame = tk.Frame(root)
parts_frame.pack(pady=15)

parts_label = tk.Label(parts_frame, text="Số file cần tách:")
parts_label.pack(side="left", padx=5)

parts_entry = tk.Entry(parts_frame, width=10)
parts_entry.insert(0, "5")
parts_entry.pack(side="left")

run_btn = tk.Button(
    root,
    text="Bắt Đầu Tách",
    command=run_split,
    width=25,
    height=2
)
run_btn.pack(pady=15)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
