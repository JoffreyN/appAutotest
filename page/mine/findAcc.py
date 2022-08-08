import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.seleniumError import SCEENVE


class PageFindAcc(PageBase):
	def __init__(self,driver):
		super().__init__(driver)
		self.input_cardid=(By.XPATH,"//*[@class='input-area']/input")
		self.next=(By.XPATH,"//*[text()='下一步' or text()='Next']/../..")

		self.input_smscode=(By.XPATH,"//*[contains(@class,'query-code')]/input")
		self.yes=(By.XPATH,"//*[@class='md-button-content']/../..")

		self.accinfo=(By.XPATH,"//*[@class='text query-text']/p")
		self.goToLogin=(By.XPATH,"//*[text()='去登录' or text()='Go to login']/../..")

	def inputCardId(self,cardID):
		logging.info(f'输入证件id {cardID}')
		self.findElement(self.input_cardid).send_keys(cardID)

	def click_next(self):
		logging.info('点击 下一步')
		self.findElement(self.next).click()

	def inputSmscode(self,code):
		logging.info(f'输入验证码 {code}')
		self.findElement(self.input_smscode).send_keys(code)

	def click_yes(self):
		logging.info('点击 确认')
		self.findElement(self.yes).click()

	def getAccInfo(self):
		return self.findElement(self.accinfo).text

	def click_goToLogin(self):
		logging.info('点击 去登录')
		self.findElement(self.goToLogin).click()
