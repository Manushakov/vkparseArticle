```
The main task of this project was getting an information from vk articles.
Since VK does not have API methods for working with articles and the search on the vk wall didn't return the required number of articles, I decided to use Selenium.
Selenium dynamically load a list of articles, this process requires a authorisation.
Also, I used a smooth scrolling, images withoit him was parsed in bad quality. 
I used the lxml to speed up the parsing of bs4. I needed Pandas to implement csv tables.
```
**You have to install docker for Selenoid working\
Python 3.7**

**Installation Selenoid for LINUX и MAC**\
`curl -s https://aerokube.com/cm/bash | bash`

**Installation and browser running**

`./cm selenoid start —browsers 'chrome:71.0;`

**Installation Selenoid for Windows in PowerShell**

`Invoke-Expression (New-Object System.Net.WebClient).DownloadString("https://aerokube.com/cm/posh")`

**Installation and browser running**

`.\cm_windows_amd64.exe selenoid start —browsers 'chrome:71.0;'`

**git clone**

`git clone https://github.com/Manushakov/vkparseArticle.git`

**install dependencies**\
`pip install -r requirements`

**run program**\
`python main.py`

**result.csv - result of program.**