import os

def count_file_lines(file_path):
    code, blank, comment = 0, 0, 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    blank += 1
                elif stripped.startswith(('#', '//', '"""', '<!--')):
                    comment += 1
                else:
                    code += 1
    except Exception as e:
        print(f"Skipped {file_path} due to error: {e}")
    return code, blank, comment

def count_directory(path, extensions={'.py', '.js', '.vue', '.ts', '.html'}):
    total_code, total_blank, total_comment = 0, 0, 0
    for root, _, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] in extensions:
                c, b, cm = count_file_lines(os.path.join(root, file))
                total_code += c
                total_blank += b
                total_comment += cm
    return total_code, total_blank, total_comment

if __name__ == '__main__':
    paths = [
        r'C:\Data\Python\Projects\daily\Big_homework\Big_Homework\一阶段',
        r'C:\Data\Python\Projects\daily\Big_homework\Big_Homework\二阶段\backend',
        r'C:\Data\Python\Projects\daily\Big_homework\Big_Homework\二阶段\frontend\App\src\views',
        r'C:\Data\Python\Projects\daily\Big_homework\Big_Homework\二阶段\frontend\App\src\App.vue'
    ]

    total_code, total_blank, total_comment = 0, 0, 0
    for path in paths:
        if os.path.isfile(path):
            c, b, cm = count_file_lines(path)
        else:
            c, b, cm = count_directory(path)
        total_code += c
        total_blank += b
        total_comment += cm

    print("合计：")
    print(f"代码行数: {total_code}")
    print(f"空行数: {total_blank}")
    print(f"注释行数: {total_comment}")
    print(f"总行数: {total_code + total_blank + total_comment}")
