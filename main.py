from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


path = 'geckodriver.exe'
opt = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path=path, options=opt)


def login():  # функция для авторизации
    username = input("Введите логин от вк ")
    password = input("Введите пароль от вк")
    driver.get("https://vk.com/login")
    login_button = driver.find_element_by_id("email")
    login_button.send_keys(username)
    password_button = driver.find_element_by_id("pass")
    password_button.send_keys(password)
    submit_button = driver.find_element_by_id("login_button")
    submit_button.click()
    try:  # Ожидает появление элемента, иначе выдает ошибку
        myelem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'page_avatar_wrap')))
    except TimeoutException:
        print("Ошибка выполнения, проверьте входные данные")
    else:
        print("Авторизация прошла успешно")
