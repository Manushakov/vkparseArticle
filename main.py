import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


PAUSE_TIME = 3
PATH = 'geckodriver.exe'
opt = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path=PATH, options=opt)


class Parse:
    """ Класс для работы с парсингом статей ВКонтакте
    Реализуется через Selenium
    ---------
    Методы
    _login - метод для авторизации
    _get_articles - метод для получения списка статей
    _get_information - метод для получения, обработки и добавления полученной информации в csv файл
    """

    def _login(self):  # функция для авторизации
        """
        Функция с помощью веб драйвера производит авторизацию, в случае неправильной пары пароль/логин выдает ошибку
        TimeoutException
        """
        username = input("Введите логин от вк ")
        password = input("Введите пароль от вк ")
        driver.get("https://vk.com/login")
        login_button = driver.find_element_by_id("email")
        login_button.send_keys(username)
        password_button = driver.find_element_by_id("pass")
        password_button.send_keys(password)
        submit_button = driver.find_element_by_id("login_button")
        submit_button.click()

        # Ожидает появление элемента, иначе выдает ошибку
        try:
            myelem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'page_avatar_wrap')))

        except TimeoutException:
            print("Ошибка выполнения, проверьте входные данные")

        else:
            print("Авторизация прошла успешно")

    def _get_articles(self):  # Функция для получения ссылок на все статьи
        """Функция выводит список всех статей"""
        links_dict = []
        driver.get("https://vk.com/@yvkurse")
        # Получает высоту документа
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Скроллит до низу
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Ожидает прогрузку страницы
            time.sleep(PAUSE_TIME)

            # Сравнивает новую длину и максимальную, в случае чего цикл повторяется
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        result = driver.find_elements_by_css_selector(".author_page_block a")
        for i in result:
            links_dict.append(i.get_attribute("href"))
        return links_dict[0]  # Возвращает список с ссылками на все статьи


    def _get_information(self, url_list):
        """Функция принимает список статей и выводит сгрупированную информацию каждой из них"""
        img_list = []
        text_list = []
        driver.get(url_list)
        end = driver.find_element_by_class_name('article_layer_misc')
        # Плавная прокрутка для корректного отображения изображений
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth' });", end)
        time.sleep(PAUSE_TIME)
        response = driver.page_source
        info = BeautifulSoup(response, "lxml")
        block = info.find("div", {"class": ["article ", "article_view"]})
        # получение заголовка
        header = block.find("h1", {"class": ["article_decoration_first", "article_decoration_last"]}).text
        text_containers = block.find_all("p", {"class": ["article_decoration_first", "article_decoration_last"]})
        for i in text_containers:
            text_list.append(i.text)
        images = block.find_all('img')
        for image in images:
            img_list.append(image.attrs['src'])
        return header, text_list, img_list


if __name__ == '__main__':
    try:
        a = Parse()
        print(a._get_information("https://vk.com/@yvkurse-muzeinyi-kompleks-tolbuhino"))
    finally:
        driver.quit()
        print("Программа закрыта")
