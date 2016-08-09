# Espider Installing Help

* Open your terminal and change the directory to this folder.  
* Type in and run `python setup.py install`  
* Espider will be installed into you python environment. Typically `python/Lib/site-packages/espider/`  

## If you want to use additional functions

>Necessary if you use specific function below. But if not, you can ignore this.  

Espider uses some open sourse lib, you should install them before using.
* pymysql:   
    Espider.parser will use pymysql to save data to mysql.  
    Try to install with pip:  
    ```
    pip install pymysql
    ```  

* selenium:  
    Espider can use selenium and PhantomJS to load web pages dynamicly. If need to load web page that is computed by JavaScript, this tool is best for you. For official desciption, please view [phantomjs](http://phantomjs.org/)
    - First, you should install phantomjs by downloading from [phantomjs](http://phantomjs.org/) (or download from references 
    in my project catalogue)  
    - Then, copy *phantomjs.exe* (`phantomjs-2.1.1-windows/bin/phantomjs.exe`) to system path (typicaly `python/Scripts`).  
    - Finally, install selenium package. Try to use:  
        ```
        pip install selenium
        ```  
    - Additionally, because selenium designs its phantomjs webdriver without configurable proxy, I modified its code to surport proxy. You just need to change `selenium/webdriver/phantomjs/webdriver.py` like this:  

        *From original file:*  

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

        *To file like this:*    

        ```python
        def __init__(self, executable_path="phantomjs",
                    port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,
                    service_args=None, service_log_path=None, proxy=None):  
        ... 
        ... 
            try:
                    RemoteWebDriver.__init__(
                        self,
                        command_executor=self.service.service_url,
                        desired_capabilities=desired_capabilities,
                        proxy=proxy)
        ```  

        Which means add `proxy=None` to __init__()'s parameter of webdriver and `proxy=proxy` to RemoteWebDriver.__init__()'s parameter.  

* lxml:  
    Espider support parse web data with xsml. If you want to use xsml rule in your project,  lxml is required  
    Try to install with  
    ```
    pip install lxml
    ```  

    If you cannot install lxml directly via pip on your computer, you can download it from [www.lfd.uci.edu/~gohlke/pythonlibs/#lxml](www.lfd.uci.edu/~gohlke/pythonlibs/#lxml) (an unofficial python packages download website). Or download from references of my project catalogue. Then use`pip install lxml-3.6.1-cp35-cp35m-win_amd64.whl` to install lxml(make sure you have *wheel* installing tool in your computer)  