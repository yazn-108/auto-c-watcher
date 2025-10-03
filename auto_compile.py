import os
import time
import subprocess
from pathlib import Path
os.system("chcp 65001 > nul") 
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
print("✅ Auto-compile ready to monitor changes...")
try:
    PROJECT_PATH = str(Path(__file__).resolve().parent)
except NameError:
    PROJECT_PATH = os.getcwd()
OUTPUT_FILE = "main.exe"
files_last_modified = {}
def get_c_files(path):
    return [f for f in os.listdir(path) if f.endswith(".c")]
def update_last_modified():
    for f in get_c_files(PROJECT_PATH):
        full_path = os.path.join(PROJECT_PATH, f)
        files_last_modified[f] = os.path.getmtime(full_path)
def files_changed():
    for f in get_c_files(PROJECT_PATH):
        full_path = os.path.join(PROJECT_PATH, f)
        if f not in files_last_modified or os.path.getmtime(full_path) != files_last_modified[f]:
            return True
    return False
def compile_and_run():
    c_files = [os.path.join(PROJECT_PATH, f) for f in get_c_files(PROJECT_PATH)]
    if not c_files:
        print("⚠️ No C files found in the project.")
        return
    compile_cmd = ["gcc", *c_files, "-o", os.path.join(PROJECT_PATH, OUTPUT_FILE)]
    try:
        env = os.environ.copy()
        env["LANG"] = "C"  # Force gcc messages to English
        result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env
        )
        if result.returncode != 0:
            print("❌ Compilation failed:\n")
            print(result.stderr)
            return
        clear_console()
        exe_path = os.path.join(PROJECT_PATH, OUTPUT_FILE)
        print("✅ Compilation successful! Running program:\n")
        proc = subprocess.Popen(exe_path)
        proc.wait()
        print() 
    except FileNotFoundError:
        print("❌ GCC not found. Please make sure it is installed and added to PATH.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
update_last_modified()
while True:
    try:
        if files_changed():
            compile_and_run()
            update_last_modified()
        time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopped by user.")
        break
