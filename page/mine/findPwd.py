import logging,time
from selenium.webdriver.common.by import By
from common.tools import switch_execute
from page.base import PageBase
from common.seleniumError import SCEENVE


class PageFindPwd(PageBase):
	def __init__(self,driver):
		# 找回密码 页面
		super().__init__(driver)
		self.btnNext_satrt=(By.XPATH,"//*[text()='下一步' or text()='Next']")
		self.btnNext_postResetApply=(By.XPATH,"//a[@onclick='postResetApply()']")
		self.btnYes_postResetVerify=(By.XPATH,"//a[@onclick='postResetVerify()']")
		self.btnNext_mail=(By.XPATH,"//div[contains(@class,'reset-user-field')]/a")
		self.btnNext=(By.XPATH,"//*[text()='下一步' or text()='Next']/../..")
		self.editSMScode=(By.CLASS_NAME,"android.widget.EditText")#输入手机验证码
		self.btnSubmit=(By.XPATH,"//*[text()='确认' or text()='Confirm']")
		self.btnSubmit_ttl=(By.XPATH,"//*[text()='确认' or text()='Confirm']/../..")
		self.editPassword=(By.ID,"password")
		self.editPassword2=(By.ID,"confirm-password")
		self.btnSubmit2=(By.XPATH,"//*[text()='完成设置' or text()='Complete']")
		self.eleMsg=(By.ID,"com.cmbi.zytx:id/btn_determine2")
		self.btnDone=(By.XPATH,"//*[text()='完成' or text()='Complete']")
		self.btnDone_ttl=(By.XPATH,"//*[text()='完成' or text()='Complete']/../..")
		#新页面
		# self.forget_accpwd=(By.XPATH,"//*[contains(text(),'证券账户的交易密码')]/../..")
		# self.forget_telpwd=(By.XPATH,"//*[contains(text(),'手机号码对应的')]/../..")
		self.accountid=(By.ID,'accountid')
		self.card_id=(By.ID,'card_id')
		self.user=(By.ID,'user')

		self.input_ttl=(By.TAG_NAME,'input')
		
		self.alert_msg=(By.XPATH,"//div[contains(text(),'证件号码错误') or contains(text(),'Wrong reserved')]")
		self.alert_yes=(By.XPATH,"//a[contains(text(),'确认') or contains(text(),'Ok')]")

	def alertMsgExists(self):
		return self.isEleExists(self.alert_msg)	

	def click_alertYes(self):
		logging.info('点击 弹窗确认')
		self.findElement(self.alert_yes).click()

	# def clickforget_accpwd(self):
	# 	logging.info('点击 忘记证券账户密码')
	# 	self.findElement(self.forget_accpwd).click()

	# def clickforget_telpwd(self):
	# 	logging.info('点击 忘记手机账户密码')
	# 	self.findElement(self.forget_telpwd).click()

	def inputaccountid(self,keyword,ttl=0):
		logging.info(f'输入账户号: {keyword}')
		if ttl:
			self.findElements(self.input_ttl)[0].send_keys(keyword)
		else:
			self.findElement(self.accountid).send_keys(keyword)

	def inputcard_id(self,keyword,ttl=0):
		logging.info(f'输入证件ID: {keyword}')
		if ttl:
			ele=self.findElements(self.input_ttl)[1]
			ele.clear()
			ele.send_keys(keyword)
		else:
			self.findElement(self.card_id).send_keys(keyword)

	def inputuser(self,keyword,ttl=0):
		logging.info(f'输入手机号: {keyword}')
		if ttl:
			self.findElement(self.input_ttl).send_keys(keyword)
		else:
			self.findElement(self.user).send_keys(keyword)

	def clickNext_start(self,ttl=0):
		logging.info('点击 下一步')
		if ttl:
			self.findElement(self.btnNext,until='located').click()
		else:
			self.findElement(self.btnNext_satrt,until='located').click()

	def clickNext_mail(self):
		logging.info('点击 下一步')
		# for i in range(5):
		# 	try:
		self.findElement(self.btnNext_mail,until='located').click()
			# 	break
			# except Exception as e:
			# 	if i==4:raise e
			# 	else:time.sleep(1)

	def clickNext_postResetApply(self,n=0):
		logging.info('点击 下一步')
		self.findElements(self.btnNext_postResetApply,until='located')[n].click()

	def clickYes_postResetVerify(self,n=0):
		logging.info('点击 确认')
		self.findElements(self.btnYes_postResetVerify,until='located')[n].click()

	def clickNext(self,n=0):
		logging.info('点击 下一步')
		self.findElements(self.btnNext,until='located')[n].click()

	@switch_execute
	def inputSMScode_ttl(self,smsCode):
		if self.PFN=='iOS':
			for i in smsCode:
				xpath=(By.IOS_CLASS_CHAIN,f'**/XCUIElementTypeKey[`label == "{i}"`]')
				self.findElement(xpath,until='located').click()
				time.sleep(1)
		else:
			keyevent_dict={'0':7,'1':8,'2':9,'3':10,'4':11,'5':12,'6':13,'7':14,'8':15,'9':16,}
			for i in smsCode:
				# driver.press_keycode
				self.driver.keyevent(keyevent_dict[i])
				time.sleep(1)
				


	def inputSMScode(self,smsCode,ttl=0):
		time.sleep(5)
		logging.info(f'输入验证码 {smsCode}')
		if ttl:
			# self.driver.execute_script(f'document.getElementsByTagName("input")[0].click();')
			# self.inputSMScode_ttl(smsCode)
			self.findElements(self.input_ttl)[0].send_keys(smsCode)
		else:
			self.driver.execute_script(f'document.getElementById("realbox").value="{smsCode}";')

	def clickSubmit(self,ttl=0):
		logging.info('点击 确认')
		if ttl:
			self.findElement(self.btnSubmit_ttl).click()
		else:
			self.findElement(self.btnSubmit).click()

	def inputPassword(self,keyword,ttl=0):
		logging.info('输入旧密码')
		if ttl:
			self.findElements(self.input_ttl)[0].send_keys(keyword)
		else:
			self.findElement(self.editPassword).send_keys(keyword)

	def inputPassword2(self,keyword,ttl=0):
		logging.info('再次输入旧密码')
		if ttl:
			self.findElements(self.input_ttl)[1].send_keys(keyword)
		else:
			self.findElement(self.editPassword2).send_keys(keyword)

	def clickSubmit2(self,ttl=0):
		logging.info('点击 完成设置')
		if ttl:
			self.findElement(self.btnNext).click()
		else:
			self.findElement(self.btnSubmit2).click()

	def textMsg(self):
		return self.findElement(self.eleMsg).text

	def clickRelogin(self):
		logging.info('点击 重新登陆')
		self.findElement(self.eleMsg).click()

	def clickDone(self,ttl=1):
		logging.info('点击 完成')
		if ttl:
			self.findElement(self.btnDone_ttl).click()
		else:
			self.findElement(self.btnDone).click()