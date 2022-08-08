import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import switch_execute,getSoup

class PageUnlockAcc(PageBase):
	def __init__(self,driver):
		# 账户解锁 页面
		super().__init__(driver)
		self.confirm=(By.XPATH,"//a[contains(text(),'确定') or contains(text(),'Ok')]")
		self.inputCardid=(By.XPATH,"//input[contains(@placeholder,'证件号码') or contains(@placeholder,'Reserved ID')]")
		self.next=(By.XPATH,"//*[contains(text(),'下一步') or contains(text(),'Next')]/../..")
		self.inputSmscode=(By.XPATH,"//input[contains(@placeholder,'验证码') or contains(@placeholder,'verification code')]")
		self.unlock=(By.XPATH,"//*[contains(text(),'立即解锁') or contains(text(),'Unlock account now')]/../..")
		self.done=(By.XPATH,"//*[contains(text(),'完成') or contains(text(),'Complete')]/../..")


	def click_confirm(self):
		logging.info('点击 确定')
		self.findElement(self.confirm).click()

	def input_cardid(self,cardid):
		logging.info(f'输入证件号码 {cardid}')
		self.findElement(self.inputCardid).send_keys(cardid)

	def click_next(self):
		logging.info('点击 下一步')
		self.findElement(self.next).click()

	def input_smscode(self,smscode):
		logging.info(f'输入验证码 {smscode}')
		self.findElement(self.inputSmscode).send_keys(smscode)

	def click_unlock(self):
		logging.info('点击 立即解锁')
		self.findElement(self.unlock).click()

	def click_done(self):
		logging.info('点击 完成')
		self.findElement(self.done).click()