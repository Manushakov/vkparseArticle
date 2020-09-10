import time
import sys
import logging
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


capabilities = DesiredCapabilities.CHROME.copy()
PAUSE_TIME = 3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_handler.setFormatter(formatter)
logger.addHandler(logger_handler)

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=capabilities
)


class Parse:
    """ Класс для работы с парсингом статей ВКонтакте
    Реализуется через Selenium
    ---------
    Методы
    _login - метод для авторизации
    _get_articles - метод для получения списка статей
    _get_information - метод для получения, обработки и добавления полученной информации в csv файл
    _create_csv - собирает информацию, по итогу создает csv файл с результатами
    start_parse - запускает полный цикл работы парсера
    """

    @staticmethod
    def _login():  # метод для авторизации
        """
        метод с помощью веб драйвера производит авторизацию, в случае неправильной пары пароль/логин выдает ошибку
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
            logger.warning("Ошибка выполнения, проверьте входные данные")
            driver.close()
            sys.exit()
        else:
            logger.info("Авторизация прошла успешно")

    @staticmethod
    def _get_articles() -> list:
        """
        метод выводит список всех статей
        """
        link = input("Введите ссылку на список статей, например https://vk.com/@yvkurse:  ")
        links_dict = []
        driver.get(link)
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
        value = len(links_dict)
        logger.info(f"Список статей успешно получен. Количество {value}")
        return links_dict  # Возвращает список с ссылками на все статьи

    @staticmethod
    def _get_information(url) -> list:
        """метод принимает статью и выводит сгрупированную информацию про нее"""
        img_list = []
        text_list = ""
        driver.get(url)
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
            text_list += i.text + " "

        images = block.find_all('img')

        for image in images:
            img_list.append(image.attrs['src'])

        return [header, text_list, img_list]

    @staticmethod
    def _create_csv(urls_list):
        """метод принимает список ссылок и создает информацию с каждой из них"""
        count = 0
        frames = []
        for url in urls_list:
            count += 1
            logger.info(f"Анализировано {count} статей")
            content = Parse._get_information(url)
            data = [{
                "Заголовок": content[0],
                "Текст статьи": content[1],
                "img": content[2]

            }]

            frames.append(pd.DataFrame(data))
        result = pd.concat(frames)
        return result.to_csv('result.csv', index=False)

    def start_parse(self) -> None:
        """ Производит запуск всего цикла парсинга, результатом которого является csv файл"""
        try:
            self._login()
            links = self._get_articles()
            self._create_csv(links)
        finally:
            driver.quit()
            logger.info("Программа закрыта")
