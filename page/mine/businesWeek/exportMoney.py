import logging
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageExportMoney(PageBase):
	def __init__(self,driver):
		# '资金提取' 页面
		super().__init__(driver)
		# 第一步页面 选择币种
		self.curr=(By.CLASS_NAME,'currency-item')

		#第二步页面 选择银行

		#第三步页面 填写信息
		self.keyboard=(By.ID,'myKeyboardNodot')
		self.btnConfirm=(By.XPATH,"//*[text()='确定']")
		self.btnIknow=(By.XPATH,"//*[text()='知道了' or text()='Understood']")
		self.btnSubmit=(By.XPATH,"//*[@class='submit']/*[text()='确认' or text()='Confirm']")

		#第四步页面 查看提交状态
		self.eleStatus=(By.XPATH,"//*[@class='right']/div[1]")
		self.btnDone=(By.XPATH,"//*[text()='完成' or text()='Done']")

	# 第一步
	def clickCurr(self,curr='HKD'):
		curNdic={'HKD':0,'USD':1,'CNY':2}
		nDic={0:'港元',1:'美元',2:'人民币'}
		logging.info(f'点击 {nDic[curNdic[curr]]}')
		self.findElements(self.curr)[curNdic[curr]].click()

	# #第三步
	# def clickConfirm(self):
	# 	logging.info('点击确定')
	# 	self.findElement(self.btnConfirm).click()

	def clickKeyboard(self):
		logging.info('点击出现键盘')
		self.findElement(self.keyboard).click()

	def getAmount(self):
		return self.findElement(self.keyboard).text

	def clickSubmit(self):
		logging.info('点击 确认')
		self.findElement(self.btnSubmit).click()

	# 第四步
	def textStatus(self):
		return self.isEleExists(self.eleStatus)

	def clickIknow(self):
		logging.info('点击 知道了')
		try:
			self.findElement(self.btnIknow,screen=0).click()
		except:
			pass

	def clickDone(self):
		logging.info('点击 完成')
		self.findElement(self.btnDone).click()