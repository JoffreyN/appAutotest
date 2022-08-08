import logging,re,time
from selenium.webdriver.common.by import By
from page.base import PageBase

try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By

class PageLogined(PageBase):
	def __init__(self,driver):
		# 输完登录密码点击确认后可能会出现的页面
		super().__init__(driver)
		self.wayDic={
			'Android':'id',
			'iOS':'ios_predicate'
		}
		self.btnSMS={
			'Android':(By.XPATH,"//*[contains(@text,'手机短信') or contains(@text,'SMS verification')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '手机短信' or name contains 'SMS verification'")
		}#手机短信认证，当用证券号登录可能会出现

		self.btnlingpai={
			'Android':(By.XPATH,"//*[contains(@text,'令牌验证')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '令牌验证'")
		}
		self.openLPapp={
			'Android':(By.XPATH,"//*[contains(@text,'打开招银令牌')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '打开招银令牌'")
		}

		# self.elePhone={
		# 	'Android':(By.ID,'com.cmbi.zytx:id/phone_number_view'),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='   '")
		# }
		self.inputLP={
			'Android':(By.ID,'com.cmbi.zytx:id/input_trade_lp'),
			'iOS':(AppiumBy.IOS_PREDICATE,"")
		}

		self.editSMS={
			'Android':(By.ID,'com.cmbi.zytx:id/sms_code_input'),
			'iOS':(AppiumBy.IOS_PREDICATE,"value contains '输入验证码' or value contains 'verification code'")
			# 'iOS':(AppiumBy.ID,"smsCode")
		}#短信验证码输入框
		self.btnConfirm={
			'Android':(By.XPATH,"//*[contains(@text,'确定') or contains(@text,'确认') or contains(@text,'Confirm') or contains(@text,'OK') or contains(@text,'Ok')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='确认' or name=='确定' or name=='Confirm' or name=='OK' or name=='Ok'")
		}

		self.eleMsg={
			'Android':(By.ID,'com.cmbi.zytx:id/message_view'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='使用手机号登录更便捷' or name contains 'more convenient'")
		}#登录完成后的引导页面标题元素
		self.btnIknow={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_i_know'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='我知道了' or name contains 'OK' or name contains 'I see'")
		}#引导页面上的 我知道了 按钮

		self.eleErrToast=(By.XPATH,"//*[contains(@text,'口令不正确')]")

	def clickLingpai(self):
		logging.info('点击 令牌验证 按钮')
		self.findElement(self.btnlingpai[self.PFN],False).click()
		self.findElement(self.btnConfirm[self.PFN],False).click()

	def clickOpenLPapp(self):
		logging.info('点击 打开招银令牌 按钮')
		self.findElement(self.openLPapp[self.PFN],False).click()

	def inputlingpai(self,token):
		logging.info(f'输入 令牌口令 {token}')
		self.findElement(self.inputLP[self.PFN]).set_value(token)

	def textSMS(self):
		return self.findElement(self.btnSMS[self.PFN],False).text

	def clickSMS(self):
		logging.info('点击 手机短信认证 按钮')
		self.findElement(self.btnSMS[self.PFN],False).click()
		time.sleep(1)
		self.findElement(self.btnConfirm[self.PFN],False).click()

	# def textPhone(self):
	# 	text=self.findElement(self.elePhone[self.PFN]).text
	# 	return re.findall(r'\d+',text)[0][2:]

	def inputSMS(self,smsCode):
		logging.info(f'输入 短信验证码 {smsCode}')
		# self.findElement(self.editSMS[self.PFN]).clear()
		logging.info(f"debug: {str(self.editSMS[self.PFN])}\n\n")
		ele=self.findElements(self.editSMS[self.PFN])
		logging.info(f"debug2: {len(ele)}\n\n")
		ele[0].send_keys(str(smsCode))

	def clickConfirm(self,ignoreError=0):
		logging.info('点击 确定 按钮')
		try:
			self.findElement(self.btnConfirm[self.PFN]).click()
		except Exception as err:
			if ignoreError:pass
			else:raise Exception

	def errToastExists(self):
		if self.PFN!='iOS':
			return 1 if self.isEleExists(self.eleErrToast) else 0
		else:
			return 0

	# def textEleMsg(self):
	# 	# self.findElement(self.eleMsg[self.PFN]).text
	# 	return self.waitTo(way=self.wayDic[self.PFN],name=self.eleMsg[self.PFN][1],operate='getText')

	def clickIknow(self):
		logging.info('点击 我知道了 按钮')
		try:
			self.findElement(self.btnIknow[self.PFN]).click()
		except:
			pass