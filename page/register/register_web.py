import logging,time,os
from common.seleniumError import SCENSEE,SCEECIE,SCEENVE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from page.base import PageBase
from common.tools import switch_execute,swithToRightWeb
 
class PageRegisterWeb(PageBase):
	def __init__(self,driver):
		# web版 在线开户 页面
		super().__init__(driver)
		self.eleFlag=(By.CLASS_NAME,"progress-text")
		#第一步
		self.btnLoacltion=(By.ID,"login-mobcountry")
		self.editPhone=(By.NAME,"phone")
		self.btnGetcode=(By.XPATH,"//*[text()='获取验证码']")
		self.editSMScode=(By.NAME,"confirm_num")
		self.btnNext=(By.XPATH,"//*[text()='下一步']/../..")#下一步
		self.eleAlert=(By.XPATH,"//*[contains(text(),'过于频繁')]")#可能出现的 “短信验证码频繁”弹框
		self.eleAlertConf=(By.XPATH,"//*[contains(text(),'确认') or contains(text(),'确定')]")#确认弹框

		#第二步
		self.btnPI=(By.XPATH,"//*[contains(text(),'专业投资者')]/../../div[1]") 
		self.btnAccMargin=(By.XPATH,"//*[contains(text(),'保证金账户')]/../../div[1]")#保证金账户
		self.btnCardType=(By.XPATH,"//*[contains(text(),'开户证件')]/..")#证件类型
		self.passport=(By.XPATH,"//*[text()='护照']")#护照
		self.btnReadme=(By.XPATH,"//*[contains(text(),'已阅读')]/../../div[1]")
		# self.btnNext1=(By.XPATH,"//*[@onclick='startOpening()']")
		self.input=(By.XPATH,"//input")#客户推荐号


		# 第三步
		self.editCardPic={'Android':(By.NAME,"front"),}
		try:self.editCardPic['iOS']=(By.IOS_PREDICATE,"name=='选取文件'")
		except AttributeError:pass
		self.editRealName=(By.NAME,"name_cn")
		self.editREnName=(By.NAME,"name_en")
		self.editCardId=(By.NAME,"card_id")
		# self.editBirthPlace=(By.NAME,"birth_place")
		self.btnBirthDay=(By.XPATH,"//*[contains(text(),'出生日期')]/../div[1]")
		self.btnBirthDayOK=(By.XPATH,"//*[text()='选择出生日期']/../../div[3]")
		self.cardExpire1=(By.CSS_SELECTOR,".starttime")
		self.starttimeOK=(By.XPATH,"//*[text()='选择开始日期']/../../div[3]")
		self.cardExpire2=(By.CSS_SELECTOR,".endtime")
		self.endtimeOK=(By.XPATH,"//*[text()='选择结束日期']/../../div[3]")
		self.editAddress=(By.ID,"address")
		self.editAddressPic={'Android':(By.XPATH,"//input[@name='address_certify']"),}
		try:self.editAddressPic['iOS']=(By.IOS_PREDICATE,"name=='选取文件'")
		except AttributeError:pass
		self.btnNext2=(By.XPATH,"//*[text()='下一步，个人信息']/../..")

		# 第四步
		self.editHomeTel=(By.XPATH,"//*[text()='住宅电话']/..//input[1]")
		self.editEmail=(By.NAME,"email")
		self.btnJobStatus=(By.XPATH,"//*[text()='工作状况']/..//div[1]")#工作状况
		self.workStatus=(By.XPATH,"//*[text()='在职']")
		self.btnJob=(By.XPATH,"//*[text()='职位']/..//div[1]")#
		self.normalemp=(By.XPATH,"//*[contains(text(),'一般员工')]")
		self.btnIndustry=(By.XPATH,"//*[text()='所属行业']/..//div[1]")#
		self.industry1=(By.XPATH,"//*[contains(text(),'农业')]")
		self.editCompanyName=(By.NAME,"com_name")#公司名称

		self.loseFoucs=(By.XPATH,"//*[contains(text(),'雇佣信息')]")
		# self.btnNext3=(By.XPATH,"//*[@onclick='personalInfo()']")
		self.btnCardBtnOk=(By.XPATH,"//*[contains(text(),'已确认')]")

		#第五步
		self.editPiPic=(By.XPATH,"//input[@name='pi_certify']")
		self.btnBackgroundInfo=(By.XPATH,"//*[text()='下一步，开通市场']/../..")
		# self.btnMarketChoose=(By.XPATH,"//*[@onclick='marketChoose()']")
		self.startPlay=(By.XPATH,"//*[text()='开始播放']/../..")
		self.btnNext4=(By.XPATH,"//*[text()='确认，下一步']/../..")
		self.btnNext5=(By.XPATH,"//*[contains(text(),'您已阅读')]/../../div[2]/div[2]")

		#第六步
		self.signType=(By.XPATH,"//*[text()='客户经理面签']/../..//label[1]")
		# self.btnAddHkNext=(By.ID,"addHk-next")
		self.editF2Fpic=(By.XPATH,"//input[@name='face2face_certify']")
		# self.btnNext6=(By.XPATH,"//*[@onclick='setAccountMethod()']")

		#第七步
		self.btnAgreeSign=(By.XPATH,"//*[text()='本人同意签署']/../../div[1]")
		self.btnSignTable=(By.XPATH,"//*[text()='开始签署表格']/../..")
		
		#第八步
		self.canvas=(By.XPATH,'//*[@resource-id="ttcanvas"]')
		self.canvas_web=(By.ID,"ttcanvas")
		self.btnPaperDone=(By.XPATH,"//*[text()='完成']/../..")

		self.eleMsg=(By.XPATH,"//*[contains(text(),'提交成功')]")

		# 衍生品问卷
		self.derivateANS=[
			"//*[text()='是']/../../div[1]",
			"(//*[text()='上述各项皆是']/../../div[1])[1]",
			"(//*[text()='上述各项皆是']/../../div[1])[2]",
			"(//*[text()='上述各项皆是']/../../div[1])[3]",
			"//*[text()='杠杆']/../../div[1]",
		]
		self.btnderTest=(By.XPATH,"//*[text()='下一步']/../..")

		# 简易投资问卷
		self.investment_ANS=[
			"//*[contains(text(),'积极增长')]/../../div[1]",
			"//*[contains(text(),'超过5年')]/../../div[1]",
			"//*[text()='股票']/../../div[1]",
			"//*[text()='期货' or text()='期貨']/../../div[1]",
		]
		# self.investment_next=(By.XPATH,"//*[text()='下一步']/../..")

		# 风险取向测评
		self.riskANS=[
			"//*[contains(text(),'24 个月或')]/../../div[1]",
			"//*[contains(text(),'25%或')]/../../div[1]",
			"//*[text()='超过 5 年']/../../div[1]",
			"(//*[contains(text(),'50%或')]/../../div[1])[1]",
			"(//*[contains(text(),'50%或')]/../../div[1])[2]",
			"//*[contains(text(),'积极增长')]/../../div[1]",
			"//*[contains(text(),'非保本')]/../div[1]"
		]
		self.btnYears=(By.XPATH,"//*[@name='q28_5_1']/../div[2]")#经验年期 5-10年
		self.btnTimes=(By.XPATH,"//*[@name='q28_5_2']/../div[2]")#近三年交易次数  5次或以上
		self.btnRpqTest=(By.XPATH,"//*[text()='下一步，测评结果']/../..")
		self.btnAccountMarket=(By.XPATH,"//*[text()='下一步，风险披露']/../..")

		self.continue_kaihu=(By.XPATH,"//*[text()='继续开户']/../..")

	def flag(self,msg='20'):
		pass
		# for i in range(5):
		# 	try:
		# 		text=self.findElement(self.eleFlag,20).text
		# 		if f'{msg}%' in text:return
		# 	except SCESERE:
		# 		pass

	#第一步
	def clickSwitchArea(self):
		logging.info(f'点击切换区号')
		self.findElement(self.btnLoacltion).click()

	def clickAreacode(self,area):
		areaNameDic={'zh_CN':'中国大陆','zh_HK':'中国香港'}
		areaName=areaNameDic[area]
		logging.info(f'点击区号 {areaName}')
		_xpath=(By.XPATH,f"//*[text()='{areaName}']")
		self.findElement(_xpath).click()

	def inputPhone(self,phone):
		logging.info(f'输入手机号 {phone}')
		self.findElement(self.editPhone).send_keys(phone)

	def clickGetcode(self):
		logging.info('点击 获取验证码')
		try:
			self.findElement(self.btnGetcode).click()
		except AttributeError:
			pass

	def clickConfirm(self,n=0):
		logging.info('点击 确认/确定')
		self.findElements(self.eleAlertConf,until='located')[n].click()

	def acceptAlert(self):
		time.sleep(1)
		if self.isEleExists(self.eleAlert,timeout=3):
			try:
				logging.info(f'{self.findElement(self.eleAlert,screen=0).text} ,等待 5 秒后重试')
			except AttributeError:
				return 0
			time.sleep(5)
			self.findElement(self.eleAlertConf).click()
			time.sleep(1)
			return 1
		else:
			return 0

	def inputSMScode(self,code):
		logging.info(f'输入验证码 {code}')
		self.findElement(self.editSMScode).send_keys(code)

	def clickNext(self):
		logging.info('点击 下一步')
		from common.seleniumError import SCEECIE
		for i in range(3):
			try:
				time.sleep(2)
				self.findElement(self.btnNext).click()
				return
			except SCEECIE:
				pass

	#第二步
	def clickPI(self):
		logging.info('点击 专业投资者PI')
		self.findElement(self.btnPI).click()

	def clickAccMargin(self):
		logging.info('点击勾选 保证金账户')
		self.findElement(self.btnAccMargin).click()

	def selectCardType(self):
		logging.info('选择证件类型 护照')
		self.findElement(self.btnCardType).click()
		time.sleep(0.5)
		self.findElement(self.passport).click()
		# Select(self.findElement(self.btnCardType)).select_by_visible_text("护照")

	def clickReadme(self):
		logging.info('点击勾选已读')
		ele=self.findElement(self.btnReadme)
		self.driver.execute_script("arguments[0].scrollIntoView();",ele)
		for i in range(5):
			try:
				ele.click()
				break
			except SCEECIE:
				if i==4:raise SCEECIE
				time.sleep(1)

	def inputAecode(self,aecode):
		logging.info(f'输入aecode: {aecode}')
		self.findElement(self.input).send_keys(aecode)

	def clickNext1(self):
		logging.info('点击 下一步')
		self.findElement(self.btnNext).click()

	def clickContinue(self):
		logging.info('点击 继续开户')
		self.findElement(self.continue_kaihu).click()

	# 第三步
	@switch_execute
	def clickCardPic_IOS(self):
		self.findElement(self.editCardPic[self.PFN]).click()

	def clickCardPic(self):
		logging.info(f'点击上传证件图片')
		if self.PFN=='Android':
			self.findElement(self.editCardPic[self.PFN],until='located').click()
		else:
			self.clickCardPic_IOS()

	def inputCardPic(self,pathToPic):
		logging.info(f'上传证件图片')
		# print('debug:',pathToPic)
		self.waitTo(way='NAME',name=self.editCardPic[self.PFN][1],operate='send_keys',value=pathToPic)

	def inputRealName(self,realName):
		logging.info(f'输入 真实姓名 {realName}')
		self.findElement(self.editRealName).send_keys(realName)

	def inputREnName(self,enName):
		logging.info(f'输入 英文名 {enName}')
		self.findElement(self.editREnName).send_keys(enName)

	def inputCardId(self,cardID):
		logging.info(f'输入 证件号 {cardID}')
		self.findElement(self.editCardId).send_keys(cardID)

	def inputBirthPlace(self,birthPlace):
		pass
		# logging.info(f'输入 出生地 {birthPlace}')
		# self.findElement(self.editBirthPlace).send_keys(birthPlace)

	def clickBirthDay(self):
		logging.info(f'点击 出生日期 ')
		ele=self.findElement(self.btnBirthDay)
		self.driver.execute_script("arguments[0].scrollIntoView();",ele)
		time.sleep(0.5)
		ele.click()

	def clickBirthDayOK(self):
		logging.info(f'点击确定')
		self.waitTo(ignoreError=(SCENSEE,SCEECIE,SCEENVE),way='XPATH',name=self.btnBirthDayOK[1],operate='click')
		
	def clickCardExpire(self):
		logging.info('点击选择 证件有效期')
		self.clickByScript(self.findElement(self.cardExpire1))
		time.sleep(0.5)
		self.waitTo(ignoreError=(SCENSEE,SCEECIE,SCEENVE),way='XPATH',name=self.starttimeOK[1],operate='click')
		# self.findElement(self.starttimeOK).click()
		time.sleep(1)
		# self.waitTo(ignoreError=(SCENSEE,SCEECIE,SCEENVE),way='CSS_SELECTOR',name=self.cardExpire2[1],operate='click')
		self.clickByScript(self.findElement(self.cardExpire2))
		time.sleep(0.5)
		self.waitTo(ignoreError=(SCENSEE,SCEECIE,SCEENVE),way='XPATH',name=self.endtimeOK[1],operate='click')
		# self.findElement(self.endtimeOK).click()
		time.sleep(0.5)

	def inputAddress(self,address):
		logging.info(f'输入 居住地址 {address}')
		self.driver.execute_script(f'document.getElementById("{self.editAddress[1]}").scrollIntoView();')
		self.findElement(self.editAddress).send_keys(address)

	def clickAddressUp(self):
		logging.info('点击选择上传地址图片')
		if self.PFN=='Android':
			self.findElement(self.editAddressPic[self.PFN],until='located').click()
		else:
			self.clickAddressUp_IOS()
	@switch_execute
	def clickAddressUp_IOS(self):
		self.findElement(self.editAddressPic[self.PFN],until='located').click()

	def inputAddressPic(self,pathToPic):
		logging.info(f'上传居住地址图片')
		self.findElement(self.editAddressPic[self.PFN],until='located').send_keys(pathToPic)
		# self.waitTo(way='NAME',name=self.editAddressPic[self.PFN][1],operate='send_keys',value=pathToPic)

	def clickNext2(self):
		logging.info('点击 下一步，个人信息')
		self.waitTo(ignoreError=(SCENSEE,SCEECIE),way='XPATH',name=self.btnNext2[1],operate='click')

	# 第四步
	def inputHomeTel(self,homeTel):
		logging.info(f'输入 住宅电话 {homeTel}')
		self.findElement(self.editHomeTel).send_keys(homeTel)

	def inputEmail(self,email):
		logging.info(f'输入 邮箱 {email}')
		self.findElement(self.editEmail).send_keys(email)

	def selectJobStatus(self):
		logging.info('选择工作状况 在职')
		self.findElement(self.btnJobStatus).click()
		time.sleep(0.5)
		self.findElement(self.workStatus).click()
		# Select(self.findElement(self.btnJobStatus)).select_by_visible_text("在职")
	
	def selectJob(self):
		logging.info('选择职位 一般员工')
		# Select(self.findElement(self.btnJob)).select_by_visible_text("一般员工")
		self.findElement(self.btnJob).click()
		time.sleep(0.5)
		self.findElement(self.normalemp).click()

	def selectIndustry(self):
		logging.info('选择所属行业')
		# Select(self.findElement(self.btnIndustry)).select_by_visible_text("金融业")
		self.findElement(self.btnIndustry).click()
		time.sleep(0.5)
		self.findElement(self.industry1).click()	

	def inputCompanyName(self,company):
		logging.info(f'输入 公司名称 {company}')
		self.findElement(self.editCompanyName).send_keys(company)
		self.findElement(self.loseFoucs,until='located').click()

	def clickNext3(self):
		logging.info('点击 下一步，投资背景')
		self.findElement(self.btnNext).click()

	def clickCardBtnOk(self):
		logging.info('点击 已确认')
		self.findElement(self.btnCardBtnOk).click()

	# 第五步
	def clickPiPic(self):
		logging.info(f'点击上传资产证明图片')
		self.driver.execute_script(f'document.getElementById("pi_certify").scrollIntoView();')
		self.findElement(self.editPiPic,until='located').click()

	def inputPiPic(self,pathToPic):
		logging.info(f'上传资产证明图片')
		self.findElement(self.editPiPic,until='located').send_keys(pathToPic)
		# self.waitTo(way='NAME',name=self.editPiPic[1],operate='send_keys',value=pathToPic)

	def clickBackgroundInfo(self):
		logging.info('点击 下一步，开通市场')
		self.waitTo(way='xpath',name=self.btnBackgroundInfo[1],operate='click')
		# self.findElement(self.btnBackgroundInfo).click()

	def clickMarketChoose(self):
		logging.info('点击 下一步')
		for i in range(5):
			try:
				self.findElement(self.btnNext).click()
				break
			except SCEENVE:
				if i==4:raise SCEENVE(f'点击下一步失败')

	#衍生品问卷
	def derTest(self):
		for xpath in self.derivateANS:
			ele=self.findElement((By.XPATH,xpath))
			self.driver.execute_script("arguments[0].scrollIntoView();",ele)
			time.sleep(0.5)
			ele.click()

	def clickderTest(self):
		logging.info('衍生品问卷完成，点击 下一步')
		self.findElement(self.btnNext).click()

	# 简易投资问卷
	def investmentTest(self):
		logging.info('开始 简易投资问卷')
		for xpath in self.investment_ANS:
			ele=self.findElement((By.XPATH,xpath))
			self.driver.execute_script("arguments[0].scrollIntoView();",ele)
			time.sleep(0.5)
			ele.click()

	# 风险取向测评
	def riskTest(self):
		for xpath in self.riskANS:
			ele=self.findElement((By.XPATH,xpath))
			self.driver.execute_script("arguments[0].scrollIntoView();",ele)
			time.sleep(0.5)
			ele.click()

	def selectYears(self):
		logging.info('经验年期 5-10年')
		# Select(self.findElement(self.btnYears)).select_by_visible_text("5-10年")
		self.findElement(self.btnYears).click()
		self.driver.execute_script('document.querySelector(".md-selector-list").querySelectorAll(".md-cell-item")[4].click();')

	def selectTimes(self):
		logging.info('近三年交易次数 5次或以上')
		# Select(self.findElement(self.btnTimes)).select_by_visible_text("5次或以上")
		self.findElement(self.btnTimes).click()
		self.driver.execute_script('document.querySelectorAll(".md-selector-list")[1].querySelectorAll(".md-cell-item")[3].click();')

	def clickRpqTest(self):
		logging.info('点击 下一步，测评结果')
		self.findElement(self.btnRpqTest).click()

	def clickAccountMarket(self):
		logging.info('点击 下一步，风险披露')
		self.findElement(self.btnAccountMarket).click()


	def clickNext4(self):
		logging.info('点击 开始播放')
		self.findElement(self.startPlay).click()
		time.sleep(2)
		logging.info('点击 确认，下一步')
		self.findElement(self.btnNext4).click()

	def clickNext5(self):
		logging.info('点击 确认')
		try:
			self.findElement(self.btnNext5).click()
		except:
			pass

	#第六步
	def chooseSignType(self):
		logging.info(f'点击 客户经理面签')
		self.findElement(self.signType).click()
		self.driver.execute_script('document.querySelectorAll(".md-radio")[1].click();')

	def clickF2Fpic(self):
		logging.info(f'点击上传面签署凭证')
		self.findElement(self.editF2Fpic,until='located').click()

	def inputF2Fpic(self,pathToPic):
		logging.info(f'上传面签署凭证')
		self.findElement(self.editF2Fpic,until='located').send_keys(pathToPic)
		# self.waitTo(way='XPATH',name=self.editF2Fpic[1],operate='send_keys',value=pathToPic)
		time.sleep(0.5)
	
	def clickNext6(self):
		logging.info('点击 确认，下一步')
		time.sleep(0.5)
		self.waitTo(way='xpath',name=self.btnNext[1],operate='click')

	def clickAddHkNext(self):
		logging.info('点击 下一步，签署')
		self.waitTo(way='xpath',name=self.btnNext[1],operate='click')
		# self.waitTo(way='id',name=self.btnAddHkNext[1],operate='click')

	#第七步
	def clickAgreeSign(self):
		logging.info('勾选本人已同意')
		self.findElement(self.btnAgreeSign).click()

	def clickSignTable(self):
		logging.info('点击 点击开始签署表格')
		self.findElement(self.btnSignTable).click()

	#第八步
	def sign(self,device='web'):
		time.sleep(3)
		logging.info('自动签名')
		if device=='web':
			from selenium.webdriver.common.touch_actions import TouchActions
			canvas=self.findElement(self.canvas_web)
			a,b=canvas.location.values()
			w=int(canvas.get_attribute('width'))
			h=int(canvas.get_attribute('height'))
			c=a+w;d=b+h;x=55;y=300
			bounds=(
				# A
				(int((240/x)*a),int((500/y)*b),int((160/x)*a),int((710/y)*b)),
				(int((240/x)*a),int((500/y)*b),int((320/x)*a),int((710/y)*b)),
				(int((180/x)*a),int((630/y)*b),int((300/x)*a),int((630/y)*b)),
				# U
				(int((360/x)*a),int((510/y)*b),int((360/x)*a),int((710/y)*b)),
				(int((360/x)*a),int((710/y)*b),int((460/x)*a),int((710/y)*b)),
				(int((460/x)*a),int((510/y)*b),int((460/x)*a),int((710/y)*b)),
				# T
				(int((520/x)*a),int((520/y)*b),int((650/x)*a),int((520/y)*b)),
				(int((585/x)*a),int((520/y)*b),int((585/x)*a),int((720/y)*b)),
				# O
				(int((700/x)*a),int((520/y)*b),int((700/x)*a),int((700/y)*b)),
				(int((700/x)*a),int((700/y)*b),int((845/x)*a),int((700/y)*b)),
				(int((845/x)*a),int((700/y)*b),int((845/x)*a),int((520/y)*b)),
				(int((845/x)*a),int((520/y)*b),int((700/x)*a),int((520/y)*b)),
				# T
				(int((150/x)*a),int((780/y)*b),int((320/x)*a),int((780/y)*b)),
				(int((235/x)*a),int((780/y)*b),int((235/x)*a),int((1000/y)*b)),
				# E
				(int((350/x)*a),int((780/y)*b),int((350/x)*a),int((1000/y)*b)),
				(int((350/x)*a),int((780/y)*b),int((470/x)*a),int((780/y)*b)),
				(int((350/x)*a),int((880/y)*b),int((470/x)*a),int((880/y)*b)),
				(int((350/x)*a),int((1000/y)*b),int((470/x)*a),int((1000/y)*b)),
				# S
				(int((680/x)*a),int((780/y)*b),int((550/x)*a),int((780/y)*b)),
				(int((550/x)*a),int((780/y)*b),int((550/x)*a),int((880/y)*b)),
				(int((550/x)*a),int((880/y)*b),int((680/x)*a),int((880/y)*b)),
				(int((680/x)*a),int((880/y)*b),int((680/x)*a),int((1000/y)*b)),
				(int((680/x)*a),int((1000/y)*b),int((540/x)*a),int((1000/y)*b)),
				# T
				(int((730/x)*a),int((780/y)*b),int((900/x)*a),int((780/y)*b)),
				(int((810/x)*a),int((780/y)*b),int((810/x)*a),int((1000/y)*b)),
				# -
				# (a+2,int((b+d)/2),c,int((b+d)/2))
			)
			actions=TouchActions(self.driver)
			for coords in bounds:
				actions.tap_and_hold(*coords[:2])
				actions.move(*coords[-2:])
				actions.release(*coords[-2:])
			actions.perform()
		else:# 在Android端切换到webview后获取的canvas元素坐标不准确
			swithToRightWeb(self.driver,0)
			canvas=self.findElement(self.canvas)
			x1,y1=canvas.location.values()
			h,w=canvas.size.values()
			x2,y2=x1+w,y1+h
			self.driver.swipe(x1+100,y1+100,x2-100,y2-100,200)
			swithToRightWeb(self.driver,'/form/handwrite')

	def clickPaperDone(self):
		logging.info('点击 完成')
		self.findElement(self.btnPaperDone).click()

	def textMsg(self):
		return self.findElement(self.eleMsg).text.strip()
