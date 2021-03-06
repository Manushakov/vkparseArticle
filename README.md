[English version](README.en.md)
```
Основной задачей проекта являлось получение подробной информации из каждой статьи найденной по ссылке.
Так как ВК не располагает методами API для работы со статьями и поиск по стене не выдавал необходимое кол-во статей, я решил использовать Selenium.
Основной его задачей является динамическая прогрузка списка статей, которая требует авторизации.
Также я использовал метод плавного скролла, так как без него фотографии парсятся в ненадлежащем качестве. 
Библиотеку lxml я использовал для ускорения парсинга bs4. Pandas мне понадобился для реализации csv таблиц.
Selenoid – это сервер, запускающий изолированные браузеры в Docker контейнерах.
Вся функциональность описана в классе, для запуска парсинга существует метод класса start_parse.
```
**Необходимо наличие DOCKER для дальнейшей установки Selenoid\
Используется Python 3.7**

**Установка Selenoid для LINUX и MAC**\
`curl -s https://aerokube.com/cm/bash | bash`

**Установка и запуск браузера**

`./cm selenoid start —browsers 'chrome:71.0;`

**Установка Selenoid для Windows в PowerShell**

`Invoke-Expression (New-Object System.Net.WebClient).DownloadString("https://aerokube.com/cm/posh")`

**Запуск браузера**

`.\cm_windows_amd64.exe selenoid start —browsers 'chrome:71.0;'`

**копирование программы к себе с помощью git**

`git clone https://github.com/Manushakov/vkparseArticle.git`

**установка зависимостей**\
`pip install -r requirements`

**запуск программы**\
`python main.py`

**result.csv - итоговый результат работы программы.**
