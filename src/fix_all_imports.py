import os
import re

def fix_imports_recursive(root_dir):
    """递归修复所有 Python 文件的导入路径"""
    
    fixed_files = []
    skipped_files = []
    
    # 遍历所有 Python 文件
    for root, dirs, files in os.walk(root_dir):
        # 跳过 venv 和 __pycache__
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.venv']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 导入替换规则
                replacements = [
                    # 修复 agents 导入
                    (r'from agents\.agent import', 'from src.agents.agent import'),
                    (r'from agents\.', 'from src.agents.'),
                    
                    # 修复 tools 导入
                    (r'from tools\.', 'from src.tools.'),
                    
                    # 修复 storage 导入
                    (r'from storage\.', 'from src.storage.'),
                    (r'from storage\.memory import', 'from src.storage.memory import'),
                    
                    # 修复 api 导入
                    (r'from api\.', 'from src.api.'),
                    (r'from api\.routes import', 'from src.api.routes import'),
                    
                    # 修复 utils 导入
                    (r'from utils\.', 'from src.utils.'),
                ]
                
                # 应用所有替换
                for pattern, replacement in replacements:
                    content = re.sub(pattern, replacement, content)
                
                # 如果内容有变化，保存文件
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # 计算相对路径
                    rel_path = os.path.relpath(file_path, root_dir)
                    fixed_files.append(rel_path)
                    print(f"✅ 修复: {rel_path}")
                else:
                    skipped_files.append(file_path)
    
    return fixed_files

if __name__ == "__main__":
    print("=" * 60)
    print("  批量修复 Python 导入路径")
    print("=" * 60)
    print()
    
    # 获取项目根目录
    root_dir = os.getcwd()
    print(f"项目目录: {root_dir}")
    print()
    
    print("开始修复...")
    print()
    
    fixed = fix_imports_recursive(root_dir)
    
    print()
    print("=" * 60)
    print(f"修复完成！共修复 {len(fixed)} 个文件")
    print("=" * 60)
    
    if fixed:
        print()
        print("已修复的文件:")
        for file in fixed:
            print(f"  - {file}")