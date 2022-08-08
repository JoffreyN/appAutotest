import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import scrollByXpath
from random import randint

class PageImportStock(PageBase):
	def __init__(self,driver):
		# '股票存入' 页面
		super().__init__(driver)
		self.inHKstock=(By.CLASS_NAME,"market-content")
		self.brokerList=(By.XPATH,"//*[text()='转出方信息' or text()='Transfer information']/../div[@class='flex-cell']")
		self.broker=(By.XPATH,"//*[text()='ALEXANDRA STOCK CO']")
		self.account=(By.XPATH,"//*[text()='账户号码' or text()='Account number']/..//input")
		self.phone=(By.XPATH,"//*[text()='联系电话' or text()='Contact number']/..//input")
		self.next=(By.XPATH,"//*[text()='下一步' or text()='Next step']")

		self.addstock=(By.CLASS_NAME,"add")#添加股票信息
		self.stockName=(By.XPATH,"//*[text()='股票名称' or text()='Stock name']/..//input")
		self.resultOne=(By.CLASS_NAME,"stock-item")#第一条搜索结果
		self.stockNum=(By.XPATH,"//*[text()='股票数量' or text()='Quantity']/..//input")
		self.addStock=(By.XPATH,"//*[text()='添加' or text()='Add']")

		self.confirm=(By.XPATH,"//*[text()='确认提交' or text()='Confirm submission']")
		self.done=(By.XPATH,"//*[text()='已联系转出' or contains(text(),'Already contacted')]")
		self.successFlag=(By.XPATH,"//*[contains(text(),'待处理') or contains(text(),'Pending')]")

	def click_inHKstock(self):
		logging.info('点击 转入港股')
		self.findElement(self.inHKstock).click()

	def click_brokerList(self):
		logging.info('点击 打开转出方券商列表')
		self.findElement(self.brokerList).click()

	def click_broker(self):
		logging.info('点击 选择券商')
		self.findElement(self.broker).click()

	def input_account(self):
		acc=str(randint(100000,999999))
		logging.info(f'点击 输入账户号码 {acc}')
		self.findElement(self.account).send_keys(acc)

	def input_phone(self):
		tel=f"135{str(randint(10000000,99999999))}"
		logging.info(f'点击 输入手机号码 {tel}')
		self.findElement(self.phone).send_keys(tel)

	def click_next(self):
		logging.info('点击 下一步')
		scrollByXpath(self.driver,self.next[1])
		self.findElement(self.next).click()

	def click_addstock(self):
		logging.info('点击 添加股票信息')
		self.findElement(self.addstock).click()

	def input_stockName(self,stockCode='00700'):
		logging.info(f'点击 输入股票代码 {stockCode}')
		self.findElement(self.stockName).send_keys(stockCode)

	def click_resultOne(self):
		logging.info('点击 第一条搜索结果')
		self.findElement(self.resultOne).click()

	def input_stockNum(self,num='500'):
		logging.info(f'点击 股数 {num}')
		self.findElement(self.stockNum).send_keys(num)

	def click_addStock(self):
		logging.info('点击 添加')
		self.findElement(self.addStock).click()

	def click_confirm(self):
		logging.info('点击 确认提交')
		self.findElement(self.confirm).click()

	def click_done(self):
		logging.info('点击 已联系转出')
		self.findElement(self.done).click()

	def isSucess(self):
		return 1 if self.isEleExists(self.successFlag) else 0




