import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import switch_execute,scrollByXpath
from common.seleniumError import SCEENVE
from random import choice

class PageEditInfo(PageBase):
	def __init__(self,driver):
		# 修改资料 页面
		super().__init__(driver)
		#第一步
		self.phon_address=(By.XPATH,"//*[text()='联系方式及地址信息']")

		self.cardInfo=(By.XPATH,"//*[text()='证件信息维护']")
		self.workMoney=(By.XPATH,"//*[text()='职业背景及财务信息维护']")
		self.moneyInfo=(By.XPATH,"//*[text()='财务状况']")
		self.workInfo=(By.XPATH,"//*[text()='雇佣信息']")
		self.statement=(By.XPATH,"//*[text()='相关声明维护']")

		self.uploadfront={
			'Android':(By.ID,"front"),#点击上传证件图片 # webview
			'iOS':(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeButton[`label == "选取文件"`]') #原生
		}
		self.uploadAddressImg={
			'Android':(By.ID,"address_image"),#点击上传地址图片
			'iOS':(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeButton[`label == "选取文件"`]') #原生
		}


		self.btnPhone=(By.XPATH,"//*[text()='联系号码']")
		self.btnEmail=(By.XPATH,"//*[text()='电子邮箱']")
		self.btnEdit=(By.XPATH,"//*[text()='编辑']")
		self.btnDel=(By.XPATH,"//*[text()='删除']")
		self.yesDel=(By.CSS_SELECTOR,'.md-dialog-btn')#第1个
		self.withdraw=(By.XPATH,"//*[text()='撤回']")

		self.houseDesc=(By.ID,'residential_details')#财务状况 住房描述
		self.company=(By.NAME,'com_name')#财务状况 雇佣信息
		self.source_note={
			'Android':(By.XPATH,"//*[@text='资金来源']"),#财务状况 来源说明
			'iOS':(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeOther[`label == "资金来源"`]'),

		}
		self.source_note_list=["收入累积","薪金","佣金/生意收入","退休金/储备"]

		self.btn_statement=(By.CLASS_NAME,'md-check-icon')#相关声明维护 最后一个选项

		# 第二步
		self.reload={
			'iOS':(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeButton[`label == "reload"`]'),
			'Android':(By.ID,'com.cmbi.zytx:id/reload_btn')
		}
		self.input=(By.TAG_NAME,'input')
		self.editOldTel=(By.XPATH,'//XCUIElementTypeOther[@name="修改联系方式"]/XCUIElementTypeOther[1]/XCUIElementTypeTextField')#ios专用，需切换至原生
		self.editNewTel=(By.NAME,"mobile")
		self.editNewEmail=(By.NAME,"email")
		self.btnNextTel=(By.XPATH,"//*[text()='下一步']/../..")
		self.btnNextEmail=(By.XPATH,"//*[@onclick='sendEmailCode()']")
		self.ios_delete=(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeKey[`label == "删除"`]') #ios专用，需切换至原生
		self.ios_8=(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeKey[`label == "8"`]') #ios专用，需切换至原生
		self.ios_done=(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeButton[`label == "完成"`]') #ios专用，需切换至原生

		#第三步
		# self.inputCode=(By.TAG_NAME,"li")
		self.inputCode={
			'iOS':(By.IOS_CLASS_CHAIN,'**/XCUIElementTypeOther[`label == "修改联系方式"`]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]'),
			'Android':(By.XPATH,'*//android.widget.ListView/android.view.View[1]')
		}
		self.btnCheckTel=(By.XPATH,"//*[text()='验证手机号码']")
		self.btnCheckEmail=(By.XPATH,"//*[text()='验证电子邮箱']")

		#第四步
		self.eleMsg=(By.XPATH,"//*[contains(text(),'成功')]")
		self.btnBack=(By.XPATH,"//*[text()='完成']/../..")
		self.save=(By.XPATH,"//*[text()='保存']/../..")
		
	#第一步
	def clickphon_address(self):
		logging.info('点击 联系方式及地址信息')
		self.findElement(self.phon_address).click()

	# def click_address(self):
	# 	logging.info('点击 地址信息维护')
	# 	self.findElement(self.address).click()

	def clickCardInfo(self):
		logging.info('点击 证件信息维护')
		self.findElement(self.cardInfo).click()

	@switch_execute
	def clickUploadfront_ios(self):
		self.findElement(self.uploadfront[self.PFN]).click()

	def clickUploadfront(self):
		logging.info('点击 上传证件图片')
		if self.PFN=='Android':
			self.findElement(self.uploadfront[self.PFN]).click()
		else:
			self.clickUploadfront_ios()

	@switch_execute
	def clickUploadAddressImg_ios(self):
		self.findElement(self.uploadAddressImg[self.PFN]).click()

	def clickUploadAddressImg(self):
		logging.info('点击 上传地址图片')
		if self.PFN=='Android':
			self.findElement(self.uploadAddressImg[self.PFN]).click()
		else:
			self.clickUploadAddressImg_ios()

	def click_workMoney(self):
		logging.info('点击 职业背景及财务信息维护')
		self.findElement(self.workMoney).click()

	def click_moneyInfo(self):
		logging.info('点击 财务状况')
		self.findElement(self.moneyInfo).click()

	@switch_execute
	def inputsource_note(self):
		logging.info(f'资金来源说明')
		self.findElement(self.source_note[self.PFN]).click()
		if self.PFN=='Android':
			self.findElement((By.XPATH,f"//*[contains(@text,'{choice(self.source_note_list)}')]")).click()
		else:
			self.findElement((By.IOS_CLASS_CHAIN,f'**/XCUIElementTypeStaticText[`label contains "{choice(self.source_note_list)}"`]')).click()

	def click_workInfo(self):
		logging.info('点击 雇佣信息')
		self.findElement(self.workInfo).click()

	def click_statement(self):
		logging.info('点击 相关声明维护')
		self.findElement(self.statement).click()

	def clickPhone(self):
		logging.info('点击 联系号码')
		self.findElement(self.btnPhone).click()

	def clickEmail(self):
		logging.info('点击 电子邮箱')
		self.findElement(self.btnEmail).click()

	def clickbtn_statement(self):
		logging.info('点击 最后一个选项')
		self.clickByScript(self.findElements(self.btn_statement)[-1])

	def clickEdit(self,types=None):
		if types:
			# types in ['联系号码','电子邮箱','地址信息']
			xpath=f"//*[text()='{types}']/../../..//*[contains(text(),'编辑')]"
		else:
			xpath=self.btnEdit[1]
		for i in range(30):
			try:
				if types=='地址信息':scrollByXpath(self.driver,xpath)
				break
			except Exception as e:
				if i==29:raise e
				else:time.sleep(1)
		logging.info(f'点击 编辑{types}')
		self.findElement((By.XPATH,xpath)).click()

	def inputHouseDesc(self):
		# msg=time.strftime('%Y-%m-%d %X')
		logging.info(f'输入住房描述')
		ele=self.findElement(self.houseDesc)
		ele.clear()
		ele.send_keys('a')

	def inputCompanyname(self):
		# msg=time.strftime('%Y-%m-%d %X')
		logging.info(f'输入公司名称')
		ele=self.findElement(self.company)
		ele.clear()
		ele.send_keys('a')


	def isDelExists(self,types):
		xpath=f"//*[text()='{types}']/../../..//*[contains(text(),'删除')]"
		return self.isEleExists((By.XPATH,xpath))

	def clickDel(self,types):
		logging.info(f'点击 删除{types}')
		xpath=f"//*[text()='{types}']/../../..//*[contains(text(),'删除')]"
		self.findElement((By.XPATH,xpath)).click()

	def clickWithdraw(self):
		logging.info('点击 撤回')
		self.findElement(self.withdraw).click()

	def withdrawExists(self):
		time.sleep(1)
		return 1 if self.isEleExists(self.withdraw) else 0

	def clickYesDel(self):
		logging.info('点击 确认')
		self.findElements(self.yesDel,until='located')[1].click()
		time.sleep(5)

	# 第二步
	def textOldTel(self):
		return self.findElement(self.input,until='located').get_attribute('value').split()[-1]

	def textOldEmail(self):
		return self.findElement(self.input,until='located').get_attribute('value')

	@switch_execute
	def clickReload(self):
		logging.info(f'点击reload')
		self.findElement(self.reload[self.PFN]).click()

	def openKeybord(self):
		if self.PFN=='iOS':
			logging.info(f'点击打开键盘')
			# self.findElement(self.editNewTel).click()
			ele=self.findElement(self.editOldTel)
			x,y=ele.location.values()
			h,w=ele.size.values()
			self.driver.tap([(int(x+w),int(y+h/2))])
			time.sleep(2)

	def delOldTel(self):
		logging.info(f'删除旧手机号')
		if self.PFN=='iOS':
			ele=self.findElement(self.ios_delete)
			for i in range(15):ele.click()
			self.findElement(self.ios_done).click()
		else:
			for i in range(15):self.driver.press_keycode(112)

	def inputNewTel(self,tel):
		logging.info(f'输入新手机号 {tel}')
		self.findElement(self.editNewTel).send_keys(tel)

	def inputNewEmail(self,email):
		logging.info(f'输入新邮箱 {email}')
		self.findElement(self.editNewEmail).send_keys(email)

	def clickNextTel(self):
		logging.info('点击 下一步')
		self.findElement(self.btnNextTel).click()

	def clickNextEmail(self):
		logging.info('点击 下一步')
		self.findElement(self.btnNextEmail).click()

	#第三步
	# @switch_execute
	def clickInput(self):
		time.sleep(5)
		logging.info(f'点击出现验证码键盘')
		ele=self.findElement(self.inputCode[self.PFN],until='located')
		self.clickByEleXY(ele)
		# self.driver.execute_script(f'document.getElementsByClassName("realbox{box}")[0].value="{smsCode}";')

	# @switch_execute
	def inputSMScode(self,smsCode):
		time.sleep(5)
		logging.info(f'输入验证码 {smsCode}')
		if self.PFN=='iOS':
			ele=self.findElement(self.ios_8)
			for i in range(4):ele.click()
		if self.PFN=='Android':
			for i in range(4):self.driver.press_keycode(15)

	def clickCheckTel(self):
		logging.info('点击 验证手机号码')
		self.driver.execute_script(f'document.getElementsByTagName("button")[0].click();')
		# self.findElement(self.btnCheckTel).click()

	def clickCheckEmail(self):
		logging.info('点击 验证电子邮箱')
		self.driver.execute_script(f'document.getElementsByTagName("button")[0].click();')
		# self.findElement(self.btnCheckEmail).click()

	#第四步
	def msgExists(self):
		time.sleep(1)
		return 1 if self.isEleExists(self.eleMsg) else 0

	def clickBack(self):
		logging.info('点击 完成')
		try:
			self.findElement(self.btnBack,until='click').click()
		except SCEENVE:
			pass

	def clickSave(self):
		logging.info('点击 保存')
		self.findElement(self.save,until='located').click()
		