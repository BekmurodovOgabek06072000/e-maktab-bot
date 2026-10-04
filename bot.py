import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ACCOUNTS = [
    {"login": "umedjonnarzuloyev", "password": "umedjon111"},
    {"login": "xalilovbobojon", "password": "xalilov11"},
    {"login": "uchqunqilichov", "password": "uchqun11"},
    {"login": "baqoyevalisher", "password": "baqoyeva11"},
    {"login": "ganisherbaqoyev", "password": "ganisher11"},
    {"login": "jalolxudoyorov", "password": "jalol11"},
    {"login": "muxaramshodmonova", "password": "muxaram11"},
    {"login": "shavkat.roziyev09198", "password": "shavkat111"},
    {"login": "askarsanoyev", "password": "askar11"},
    {"login": "qudratov.quvonch", "password": "qudratov11"},
    {"login": "baqoyev.mehriddin", "password": "baqoyev11"},
    {"login": "umid.shodmonov041219", "password": "umid11"},
    {"login": "sherzodismoilov07198", "password": "sherzod11"},
    {"login": "boltayevrazzoq", "password": "boltayev11"},
    {"login": "rahmatshamsiyev", "password": "rahmat11"},
    {"login": "rustam.boltayev01198", "password": "rustam11"},
    {"login": "rizomatazimov", "password": "rizomat11"},
    {"login": "ismoilov_golib", "password": "ismoilov11"},
    {"login": "idiyevaliyor", "password": "idiyev11"},
    {"login": "rustam.qurbonov28071", "password": "rustam11"},
    {"login": "husan.murodov0105198", "password": "husan11"},
    {"login": "boronovtolib", "password": "boronov11"},
    {"login": "boronovtolib", "password": "boronov11"},
    {"login": "umid.shukurov1705198", "password": "shukurov11"}
]

def click_submit_button(driver, wait):
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        try:
            btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", btn)
    except Exception:
        active_elem = driver.switch_to.active_element
        active_elem.send_keys(Keys.ENTER)

def is_login_failed(driver):
    """
    Tizimda 'Login yoki parol noto'g'ri' degan xatolik xabari chiqganini tekshiradi.
    """
    try:
        error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'noto‘g‘ri') or contains(text(), 'notogri') or contains(text(), 'xato')]")
        return len(error_elements) > 0
    except Exception:
        return False

def process_account(driver, account):
    max_attempts = 2  # Ko'pi bilan 2 marta urinish
    
    for attempt in range(1, max_attempts + 1):
        try:
            driver.get("https://login.emaktab.uz/")
            wait = WebDriverWait(driver, 10)
            
            print(f"\n==========================================")
            print(f"[{account['login']}] Kirish boshlandi (Urinish {attempt}/{max_attempts})...")
            
            # Login va Parolni kiritish
            login_input = wait.until(EC.element_to_be_clickable((By.NAME, "login")))
            password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            
            login_input.clear()
            login_input.send_keys(account["login"])
            
            password_input.clear()
            password_input.send_keys(account["password"])
            
            # Kirish tugmasini bosish
            click_submit_button(driver, wait)
            time.sleep(2.5)
            
            # 1. Login yoki Parol noto'g'riligini tekshirish
            if is_login_failed(driver):
                print(f"[{account['login']}] XABAR: Login yoki parol noto'g'ri!")
                if attempt < max_attempts:
                    print(f"[{account['login']}] Qayta urinib ko'rilmoqda...")
                    time.sleep(1.5)
                    continue
                else:
                    print(f"[{account['login']}] 2 marta noto'g'ri kiritildi. Keyingi akkauntga o'tilmoqda.")
                    break

            # 2. CAPTCHA rasmi borligini tekshirish
            captcha_imgs = driver.find_elements(By.XPATH, "//img[contains(@class, 'captcha')]")
            
            if captcha_imgs:
                print(f"[{account['login']}] CAPTCHA talab qilindi.")
                try:
                    captcha_input = wait.until(EC.element_to_be_clickable((By.NAME, "captcha")))
                    captcha_input.click()
                    print(">>> Kursor CAPTCHA katagiga qo'yildi. Sonlarni yozib Enter tugmasini bosing!")
                except Exception:
                    pass

                # Tizimga kirib ketishini yoki login xatosi chiqishini kutamiz
                while "login" in driver.current_url.lower():
                    if is_login_failed(driver):
                        break
                    time.sleep(0.5)

                # Agar CAPTCHA kiritilgandan keyin ham login/parol noto'g'ri desa
                if is_login_failed(driver):
                    print(f"[{account['login']}] XABAR: Login yoki parol noto'g'ri!")
                    if attempt < max_attempts:
                        print(f"[{account['login']}] Qayta urinib ko'rilmoqda...")
                        time.sleep(1.5)
                        continue
                    else:
                        print(f"[{account['login']}] 2 marta noto'g'ri kiritildi. Keyingi akkauntga o'tilmoqda.")
                        break

            # Agar URL'da 'login' qolmagan bo'lsa — muvaffaqiyatli kirildi
            if "login" not in driver.current_url.lower():
                print(f"[{account['login']}] Muvaffaqiyatli kirildi!")
                print(f"[{account['login']}] 2 soniyadan so'ng keyingi akkauntga o'tiladi...")
                time.sleep(2)
                break

        except Exception as err:
            print(f"[{account['login']}] Xatolik yuz berdi:", err)
            break

    driver.delete_all_cookies()

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    
    driver_path = r"C:\Users\bekmu\Desktop\eMaktab_Bot\chromedriver.exe"
    if os.path.exists(driver_path):
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    try:
        for acc in ACCOUNTS:
            process_account(driver, acc)
        print("\nBarcha akkauntlar bo'yicha ish yakunlandi!")
    finally:
        pass

if __name__ == "__main__":
    main()