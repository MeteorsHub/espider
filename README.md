# Espider
A simply constructed web crawling and scrabing framework that is easy to use  

![](https://github.com/MeteorKepler/espider/raw/master/artworks/spider-web.jpg)  

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
if you cannot install lxml on your computer, you can download it from [www.lfd.uci.edu/~gohlke/pythonlibs/#lxml](www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)
(an unofficial python packages download website). Or download from references of my project catalogue. Then use`pip install lxml-3.6.1-cp35-cp35m-win_amd64.whl`
to install lxml(make sure you have *wheel* installing tool in your computer)  
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
    ```
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
    ```
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
* 
