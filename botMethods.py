import selenium
import pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



class bot():

    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        #option.add_argument('no-sandbox')
        #option.add_argument('disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver',options=option)
        self.driver.get("https://www.rakutentrade.my/login/")

        
    def login(self , usr  , pw):
        WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.ID, "loginName")))
        loginBar = self.driver.find_element_by_xpath('//*[@id="loginName"]')
        passwordBar = self.driver.find_element_by_xpath('//*[@id="password"]')
        loginBar.send_keys(usr)
        passwordBar.send_keys(pw)
        passwordBar.send_keys(Keys.ENTER)

    def search_symbol(self , symbol):
        self.wait_find_element('xpath' ,'//*[@id="scene_home"]/div[1]/div[2]/div[2]/div/div[2]/input' , action = f"send_keys('{symbol}')")
        self.wait_find_element('xpath' ,'//*[@id="scene_home"]/div[1]/div[2]/div[2]/div/div[4]/div/div[1]/ul/li')
        
    def buy_stock(self , symbol , qty , tpin , otype , limit = False , valid = "day" , lprice = 0):
        self.search_symbol(symbol)
        self.wait_find_element('xpath' , '//*[@id="scene_stock_info"]/div[2]/div[1]/div[4]/div[2]/div[1]/button[1]')
        self.fill_order( qty , tpin , otype , valid = valid , limit = limit  , lprice = lprice)

    def sell_stock(self , symbol , qty , tpin , otype , limit = False , valid = "day" , lprice = 0):
        self.search_symbol(symbol)
        self.wait_find_element('xpath' , '//*[@id="scene_stock_info"]/div[2]/div[1]/div[4]/div[2]/div[1]/button[2]')
        self.fill_order( qty , tpin , otype , valid = valid , limit = limit  , lprice = lprice)
    
    def fill_order(self , qty , tpin , otype , valid = "day" , limit = False , lprice = 0):
        self.wait_find_element('xpath' ,'//*[@id="order-type-code"]')
        if limit is True:
            self.driver.find_element_by_tag_name('option[value="limit"]').click()
            self.wait_find_element('xpath' , '//*[@id="price_idx"]' , action = f'send_keys({lprice})')
        else:
            self.driver.find_element_by_tag_name('option[value="market"]').click()
        
        self.driver.find_element_by_xpath('//*[@id="order_pad"]/div[2]/div/div[4]/div[1]/div[5]/div[1]/input').send_keys(qty)
        self.driver.find_element_by_xpath('//*[@id="order-validity"]')
        if valid == 'day':
            self.driver.find_element_by_tag_name('option[value="DAY"]').click()
        else:
            self.driver.find_element_by_tag_name('option[value="GTD"]').click()   
        self.driver.find_element_by_xpath('//*[@id="order_pad"]/div[2]/div/div[4]/div[1]/div[5]/div[3]/input').send_keys(tpin)
        self.driver.find_element_by_xpath('//*[@id="order_pad"]/div[2]/div/div[4]/div[3]/div[1]/div[1]').click()
        self.driver.find_element_by_xpath('//*[@id="order-data-confirm"]').click()

    def wait_find_element(self , ftype , val , action = 'click()' , time = 30):
        if not (action is None or action == ""):
            action = f".{action}"
        elif action is None:
            action = ""
        if ftype.lower() == "xpath":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.XPATH, val)))
            return eval(f"self.driver.find_element_by_xpath('{val}'){action}")
        elif ftype.lower() == "id":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.ID, val)))
            return eval(f"self.driver.find_element_by_id('{val}'){action}")
        elif ftype.lower() == "name":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.NAME, val)))
            return eval(f"self.driver.find_element_by_name('{val}'){action}")
        elif ftype.lower() == "hyperlink1":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.LINK_TEXT, val)))
            return eval(f"self.driver.find_element_by_link_text('{val}'){action}")
        elif ftype.lower() == "hyperlink2":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, val)))
            return eval(f"self.driver.find_element_by_partial_link_text('{val}'){action}")
        elif ftype.lower() == "tagname":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.TAG_NAME, val)))
            return eval(f"self.driver.find_element_by_tag_name('{val}'){action}")
        elif ftype.lower() == "classname":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.CLASS_NAME, val)))
            return eval(f"self.driver.find_element_by_class_name('{val}').{action}")
        elif ftype.lower() == "css":
            WebDriverWait(self.driver , time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, val)))
            return eval(f"self.driver.find_element_by_css_selector('{val}'){action}")
        else:
            raise ValueError("Find type is does not exist")
    
    def check_status(self):
        self.wait_find_element('xpath', '//*[@id="ui-id-23"]')
        stocks = {}
        key = ["Code" , "Stock" , "Number of Shares" , "Total Market Value" , "Avg Acquisition Price" , "Current Price"]
        i = 1
        table = self.wait_find_element('xpath', '//*[@id="cash_portfolio_wrapper"]/div/div[2]' , action = None , time = 30)
        while True:
            datalist = []
            for x in range(8):
                data = table.find_elements_by_xpath(f"//*[@id='cash_portfolio']/tbody/tr[{i}]/td[{x}]")
                #datalist.append(len(data))
                for z in data:
                    datalist.append(z.text)
            stock = {}
            i += 2
            datalist[5]
            break
        print(datalist)
    
    def off(self):
        self.driver.quit()
