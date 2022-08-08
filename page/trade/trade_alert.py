import logging,re,traceback
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import myAddScreen

class PageTradeAlert(PageBase):
	def __init__(self,driver):
		# 新版交易点击 买入/卖出 后出现的确认窗口页面
		super().__init__(driver)
		self.btnConfirm=(By.CSS_SELECTOR,".van-dialog__confirm")
		self.btnCancel=(By.CLASS_NAME,"van-dialog__cancel")
		self.failedFlag=(By.XPATH,'//p[contains(text(),"价位范围内")]')
		self.iknow=(By.XPATH,'//*[contains(text(),"我知道了") or contains(text(),"I see")]/../..')

	def getPrice(self):
		priceTxt=self.findElement(self.failedFlag).text
		logging.info(f"获取单价 {priceTxt}")
		try:
			price=float(re.findall(r'\d.+\d',priceTxt)[0].split('-')[0])+0.4
			return round(price,3)
		except:
			logging.info(f'获取单价失败')
			return 15

	def clickIknow(self):
		logging.info("点击 确认")
		self.findElement(self.iknow).click()

	def failedFlagExists(self):
		return self.isEleExists(self.failedFlag)

	def clickConfirm(self):
		logging.info("点击 确认")
		try:
			self.findElement(self.btnConfirm).click()
		except Exception as err:
			myAddScreen(self,traceback.format_exc())
			raise err

	def clickCancel(self):
		logging.info("点击 取消")
		self.findElement(self.btnCancel).click()

	def flagExists(self):
		return self.isEleExists(self.btnConfirm)
