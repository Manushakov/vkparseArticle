from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

SCROLL_PAUSE_TIME = 3
path = 'geckodriver.exe'
opt = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path=path, options=opt)


def login():  # функция для авторизации
    username = input("Введите логин от вк ")
    password = input("Введите пароль от вк ")
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


def get_articles():  # Функция для получения ссылок на все статьи
    links_dict = []
    driver.get("https://vk.com/@yvkurse")
    # Получает высоту документа
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Скроллит до низу
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Ожидает прогрузку страницы
        time.sleep(SCROLL_PAUSE_TIME)

        # Сравнивает новую длину и максимальную, в случае чего цикл повторяется
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    result = driver.find_elements_by_css_selector(".author_page_block a")
    for i in result:
        links_dict.append(i.get_attribute("href"))
    return links_dict  # Возвращает список с ссылками на все статьи
