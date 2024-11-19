import tkinter as tk
from tkinter import messagebox, filedialog
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import os
import pandas as pd

# 启用自动转换pandas DataFrame到R数据框
pandas2ri.activate()

# 导入所需的R包
cmplot = importr('CMplot')

def generate_cmplot(data_path, x=1e-5, y=2.806096e-8, filename="out", out_path="."):
    if not os.path.exists(data_path):
        messagebox.showerror("Error", "Data file not found!")
        return
    
    # 使用pandas读取数据文件
    data = pd.read_csv(data_path)

    # 将pandas DataFrame转换为R数据框
    data_r = pandas2ri.py2rpy(data)

    # 创建输入基本向量
    # 颜色部分
    threshold_col = robjects.vectors.StrVector(["black", "grey"])
    chr_den_col = robjects.vectors.StrVector(["darkgreen", "yellow", "red"])
    signal_col = robjects.vectors.StrVector(["red", "green"])
    # 设定值部分
    threshold_lty = robjects.vectors.IntVector([1, 2])
    threshold_lwd = robjects.vectors.IntVector([1, 1])
    signal_cex = robjects.vectors.IntVector([1, 1])
    signal_pch = robjects.vectors.IntVector([19, 19])

    # 调用CMplot函数
    try:

        print(data)

        cmplot.CMplot(data, 
                      plot_type=["m", "q"],  # 同时输出曼哈顿图和QQ图
                      LOG10=True, 
                      threshold=[x, y],  # 设置标准线 x 和 y
                      threshold_lty=threshold_lty,
                      threshold_lwd=threshold_lwd, 
                      threshold_col=threshold_col,  # 确保颜色值是有效的字符串
                      amplify=False,
                      bin_size=1e6,
                      chr_den_col=chr_den_col,
                      signal_col=signal_col,
                      signal_cex=signal_cex,
                      signal_pch=signal_pch,
                      file="jpg",  # 输出图片的格式
                      file_name=f"{filename}",
                      dpi=2000,  # 输出图片的大小
                      file_output=True,
                      verbose=True)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def run_plot():
    data_path = entry_data_path.get()
    x = float(entry_x.get())
    y = float(entry_y.get())
    filename = entry_filename.get()
    out_path = entry_out_path.get()
    
    # 如果 out_path 为空，则设置为当前工作路径
    if not out_path:
        out_path = os.getcwd()
    
    # 设置工作路径
    os.chdir(out_path)

    generate_cmplot(data_path, x, y, filename, out_path)
    messagebox.showinfo("Success", "Plot generated successfully!")

def exit_program():
    root.destroy()

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_data_path.delete(0, tk.END)
        entry_data_path.insert(0, file_path)

# 创建主窗口
root = tk.Tk()
root.title("CMplot Generator")

# 设置窗口大小和位置
window_width = 900
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 创建输入框和标签
label_data_path = tk.Label(root, text="输入文件:")
label_data_path.grid(row=0, column=0, padx=10, pady=5)
entry_data_path = tk.Entry(root, width=75)
entry_data_path.insert(0, "/path/to/your/data.csv")
entry_data_path.grid(row=0, column=1, padx=10, pady=5)

button_browse = tk.Button(root, text="浏览", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=5)

label_x = tk.Label(root, text="下分界线值:")
label_x.grid(row=1, column=0, padx=10, pady=5)
entry_x = tk.Entry(root, width=75)
entry_x.insert(0, "1e-5")
entry_x.grid(row=1, column=1, padx=10, pady=5)

label_y = tk.Label(root, text="上分界线值:")
label_y.grid(row=2, column=0, padx=10, pady=5)
entry_y = tk.Entry(root, width=75)
entry_y.insert(0, "2.806096e-8")
entry_y.grid(row=2, column=1, padx=10, pady=5)

label_filename = tk.Label(root, text="输出文件名:")
label_filename.grid(row=3, column=0, padx=10, pady=5)
entry_filename = tk.Entry(root, width=75)
entry_filename.insert(0, "out")
entry_filename.grid(row=3, column=1, padx=10, pady=5)

label_out_path = tk.Label(root, text="输出文件路径:")
label_out_path.grid(row=4, column=0, padx=10, pady=5)
entry_out_path = tk.Entry(root, width=75)
entry_out_path.insert(0, "")
entry_out_path.grid(row=4, column=1, padx=10, pady=5)

# 创建按钮
button_run = tk.Button(root, text="绘图", command=run_plot)
button_exit = tk.Button(root, text="退出", command=exit_program)

button_run.grid(row=5, column=1, sticky="w", padx=10, pady=20)
button_exit.grid(row=5, column=1, sticky="e", padx=10, pady=20)

# 运行主循环
root.mainloop()