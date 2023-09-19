import tkinter as tk
import pyperclip
import json

# 设置窗口大小和位置
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
# 屏幕左上方为原点
DISPLAY_X = 1000
DISPLAY_Y = 50


# 读取JSON文件
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("找不到指定的JSON文件")
        return {}


# 复制指定的value值到剪贴板
def copy_to_clipboard(value):
    pyperclip.copy(value)


# 创建按钮来显示所有key值，每行显示两个按钮
def create_buttons(data):
    # 清除框架中的子部件
    for widget in frame.winfo_children():
        widget.destroy()

    row = 0
    col = 0

    for key, value in data.items():
        if isinstance(value, dict):
            # 如果value是一个JSON对象，创建一个进入下一级的按钮
            button = tk.Button(frame, text=key, command=lambda v=value: create_buttons(v), width=20, height=2)
        else:
            # 如果value是一个字符串，创建一个复制到剪贴板的按钮
            button = tk.Button(frame, text=key, command=lambda v=value: copy_to_clipboard(v), width=20, height=2)

        button.grid(row=row, column=col, padx=10, pady=10)
        col += 1

        if col == 2:
            col = 0
            row += 1

    # 添加返回上一级的按钮
    if row > 0 or col > 0:
        back_button = tk.Button(frame, text="返回上一级", command=lambda: create_buttons(resume_data), width=20,
                                height=2)
        back_button.grid(row=row, column=col, padx=10, pady=10)


# 创建主窗口
root = tk.Tk()
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{DISPLAY_X}+{DISPLAY_Y}")
# root.geometry("400x800+1250+50")  # 设置窗口大小和位置
root.title("填简历辅助工具")
# 设置窗口始终置顶
root.wm_attributes('-topmost', 1)

# 读取JSON文件
json_file_path = "resume.json"
resume_data = read_json_file(json_file_path)

# 创建Canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建垂直滚动条
scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# 创建框架来容纳按钮
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

# 初始状态，显示顶层JSON对象的按钮
create_buttons(resume_data)

# 进入主循环
root.mainloop()
