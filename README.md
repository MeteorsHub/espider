# Espider
>A simply constructed web crawling and scrabing framework that is easy to use  

![](https://github.com/MeteorKepler/espider/raw/master/artworks/spider-web.jpg)  

## What can I do with espider?  
Espider can automaticly huge amount of scribe web sources with just a few lines of codes to design. It can use proxy and dynamic parsing method to handle ip restrict and anti-scribing issues.  
Espider have two procedures-- web spider and content parser. Web spider wil start with a starting url and then use rules that you define to analyse catalogue and download all the required web source to you hard disk. Content parser wil parse stored web source and extract needed infomation to file or mysql.
Surpportted web source type includes html, xml, json, images like jpg, bmp, tif, videos like avi, mp4, audios like mp3. For furthor infomation, please refer to *TODO*  

![](https://github.com/MeteorKepler/espider/raw/master/artworks/mainproc.jpg)  

## Environment  
Because of getting start with python not so familiarly and the project is just a begining, I have only tested the project in specific environment below. 
Some errors may occur running in different environment. Better capatibility will be modified in later version.
* os: windows 7-64bit
* python version: 3.5  

## Requirements  
Espider uses some open sourse lib, you should install them before using.
* pymysql:   
Espider.parser will use pymysql to save data to mysql.  
Try to install with pip:  
`
pip install pymysql
`
* lxml:   
Espider support parse web data with xsml. lxml is required  
Try to install with  
`
pip install lxml
`  
If you cannot install lxml on your computer, you can download it from [www.lfd.uci.edu/~gohlke/pythonlibs/#lxml](www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)
(an unofficial python packages download website). Or download from references of my project catalogue. Then use`pip install lxml-3.6.1-cp35-cp35m-win_amd64.whl`
to install lxml(make sure you have *wheel* installing tool in your computer)  
See also in *TODO*  
* selenium:  
Espider can use selenium and PhantomJS to load web pages dynamicly. If need to load web page that is computed by
JavaScript, this tool is best for you. For furthor desciption, please view [phantomjs](http://phantomjs.org/)
    * First, you should install phantomjs by downloading from [phantomjs](http://phantomjs.org/) (or download from references 
    in my project catalogue)  
    * Then, copy *phantomjs.exe* (`phantomjs-2.1.1-windows/bin/phantomjs.exe`) to system path (typicaly `python/Scripts`).  
    * Finally, install selenium package. Try to use:  
    `
    pip install selenium
    `  
    * Additionally, because selenium designs its phantomjs webdriver without configurable proxy, I modified its code 
    to surport proxy. You just need to change `selenium/webdriver/phantomjs/webdriver.py` like this:  
    from  
    ```python
    def __init__(self, executable_path="phantomjs",
                 port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,
                 service_args=None, service_log_path=None):  
    ...  
        try:
                RemoteWebDriver.__init__(
                    self,
                    command_executor=self.service.service_url,
                    desired_capabilities=desired_capabilities)
    ```  
    to  
    ```python
    def __init__(self, executable_path="phantomjs",
                 port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,
                 service_args=None, service_log_path=None, proxy=None):  
    ...  
        try:
                RemoteWebDriver.__init__(
                    self,
                    command_executor=self.service.service_url,
                    desired_capabilities=desired_capabilities,
                    proxy=proxy)
    ```  
    which means add one parameter to defination of webdriver.  

## Install  
Espider is easy to install with a *setup.py*. First, download espider project. Then, switch to `espider/espider` catalogue. Finally, use `python install  


## Get started  
There are several examples in `test/` folder you could refer to.  
Generally speaking, you should build a class that inherit `espider.spider.BaseSpider`. Then you should define parameter `espiderName`, `startUrl`  and function `getUrlList()` like the code below:  

```python
import re

from espider.spider import BaseSpider

class NationalGeo(BaseSpider):
    espiderName = 'nationalGeographicSpider'
    startUrl = 'http://ocean.nationalgeographic.com/ocean/photos/underwater-exploration-photos/'

    def getUrlList(self, response):
        data = response.read().decode('utf8')
        cataloguelist = re.findall('''<a href="(/ocean/.*?)" title=".*?">.*?</a>''', data)
        contentList = re.findall('''<a class="thumb" title=".*?" href='(.*?)'>''', data)
        return (cataloguelist, contentList)
```

Every Spider should have a espiderName to identify different spider. StartUrl is the entrance of your spider. getUrlList() use http response to extract urllist and contentlist. They are all list object, each element is an url like */ocean/underwater-exploration/*. Cataloguelist is catalogues that espider will automaticly track all the source catalogues through using DFS method. Contentlist is all the sources that you want to download- urllist of ocean pitures in this case.  
Next, just use 2 lines of code to start your espider.  

```python
#Limit scribing page amount just for demo

#from espider.config import configs
#configs.spider.catalogueLimit = 5
#configs.spider.contentLimit = 20

mySpider = NationalGeo()
mySpider.startEspider()
```

All the source will be saved to `pipeline/`. If you want to change related configurations, please refer to *TODO*  
Logging file and proxy file (if you use proxy) is in `resources/`. For more infomation, please refer to *TODO*  
You can also use different means to extract urllist, such as BeautifulSoup, lxml, re and etc. For more infomation, please refer to *TODO*  

## Parse content
In last section, we learned how to scribe content files from Internet. But what if you want specific data instead of data altogether?  
Espider provide a content parsing tool to help you parse content data. Now we have HtmlParser, XmlParser and JsonParser. Similar to spider, a parser need to define a class that inherit HtmlParser or other parsers. Then design parseContent() function which use plain text input to find useful data dict and return a list whose element is a dict-like object.  
By default, parsed data will be stored in files. You can also change the configs to stored in database. See into *TODO*