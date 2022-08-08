import logging,time,os,faker,string,sys
from random import sample,choice
from common.tools import getWebDriver,saveFile,out
from testData.data import regInfo,regURL_ttl
from page.register.register_web import PageRegisterWeb
from common.system_boss import getSMScode

def regWeb(args):
	if args.location=='zh_HK':
		fake=faker.Faker('zh_CN')
	else:
		fake=faker.Faker(args.location)
	fakeEn=faker.Faker('en')
	regTypeDic={0:'一般投资者',1:'专业投资者'}

	if not args.tel:
		if args.location=='zh_HK':
			args.tel=f"{choice([9,6])}{''.join(str(i) for i in sample(range(0,9),7))}"
		else:
			args.tel=fake.phone_number()
	if not args.email:args.email=f"{''.join(sample(string.ascii_lowercase+string.digits,20))}@{''.join(sample(string.ascii_lowercase+string.digits,15))}.com"

	args.cnName=fake.name()
	args.enName=f"{args.env}{fakeEn.name()}".replace('.','')
	args.cardID=fake.ssn()
	birthPlace=fake.address()
	contactPlace='香港'
	# contactPlace=fake.address()[:2]
	company=fake.company()

	driverWeb=getWebDriver(headless=args.headless)
	_s='TTL-' if args.ttl else ''
	saveFile(f"-----{_s}{args.env.upper()}环境 {regTypeDic[args.pi]} {time.strftime('%Y-%m-%d %X')} -----")
	_url=regURL_ttl[args.env]
	driverWeb.get(_url)
	pageRegisterWeb=PageRegisterWeb(driverWeb)
	#第一步
	if args.location=='zh_HK':
		pageRegisterWeb.clickSwitchArea()
		pageRegisterWeb.clickAreacode(args.location)

	pageRegisterWeb.inputPhone(args.tel)
	saveFile(f'手机号： {args.tel}')
	pageRegisterWeb.clickGetcode()
	time.sleep(3)
	code=getSMScode(args.tel,env=args.env,n=4)
	pageRegisterWeb.inputSMScode(code)
	pageRegisterWeb.clickNext()
	#第二步
	if args.pi:pageRegisterWeb.clickPI()
	if args.margin:
		pageRegisterWeb.clickAccMargin()
		saveFile(f"已勾选保证金账户")
	pageRegisterWeb.selectCardType()
	pageRegisterWeb.clickReadme()
	#ttl 填写推荐号 655
	if args.ttl:pageRegisterWeb.inputAecode('655')
	pageRegisterWeb.clickNext1()
	pageRegisterWeb.clickConfirm(1)
	# 第三步
	pageRegisterWeb.flag('20')
	pageRegisterWeb.inputCardPic(regInfo['pic1'])
	pageRegisterWeb.inputRealName(args.cnName)
	saveFile(f'中文名: {args.cnName}')
	pageRegisterWeb.inputREnName(args.enName)
	saveFile(f'英文名: {args.enName}')
	pageRegisterWeb.inputCardId(args.cardID)
	saveFile(f'证件ID: {args.cardID}')
	pageRegisterWeb.inputBirthPlace(birthPlace)
	saveFile(f'出生地址: {birthPlace}')
	pageRegisterWeb.clickBirthDay()
	pageRegisterWeb.clickBirthDayOK()
	saveFile('出生日期： 1984-06-01')
	pageRegisterWeb.inputAddress(contactPlace)
	saveFile(f'联系地址: {contactPlace}')
	pageRegisterWeb.clickCardExpire()
	pageRegisterWeb.inputAddressPic(regInfo['pic2'])
	# import os
	# os.system('pause')
	pageRegisterWeb.clickNext2()
	# 第四步
	pageRegisterWeb.inputHomeTel(regInfo['homeTel'])
	pageRegisterWeb.inputEmail(args.email)
	saveFile(f'邮箱号： {args.email}')
	pageRegisterWeb.selectJobStatus()
	pageRegisterWeb.selectJob()
	pageRegisterWeb.selectIndustry()
	pageRegisterWeb.inputCompanyName(company)
	saveFile(f'公司名称: {company}')
	pageRegisterWeb.clickNext3()
	pageRegisterWeb.clickCardBtnOk()
	# 第五步
	if args.pi:pageRegisterWeb.inputPiPic(regInfo['pic3'])
	pageRegisterWeb.clickBackgroundInfo()
	pageRegisterWeb.clickMarketChoose()

	#衍生品问卷
	pageRegisterWeb.derTest()
	pageRegisterWeb.clickderTest()

	#简易投资问卷
	pageRegisterWeb.investmentTest()
	pageRegisterWeb.clickNext1()

	if args.pi:
		# 风险取向测评
		pageRegisterWeb.riskTest()
		pageRegisterWeb.selectYears()
		pageRegisterWeb.selectTimes()
		pageRegisterWeb.clickRpqTest()
		pageRegisterWeb.clickAccountMarket()
	pageRegisterWeb.clickNext4()
	pageRegisterWeb.clickNext5()
	#第六步
	pageRegisterWeb.clickAddHkNext()
	if args.pi:
		pageRegisterWeb.chooseSignType()
		pageRegisterWeb.inputF2Fpic(regInfo['pic4'])
		pageRegisterWeb.clickNext6()
	#第七步
	pageRegisterWeb.clickAgreeSign()
	# while 1:
	# 	flag=eval(open('flag.txt','r',encoding='utf-8').read())
	# 	if flag:
	# 		break
	# 	else:
	# 		now=time.strftime('%Y-%m-%d %X')
	# 		out(f'{now} 暂停中...')
	# 		time.sleep(1)
	pageRegisterWeb.clickSignTable()
	#第八步
	# pageRegisterWeb.flag('95')
	pageRegisterWeb.sign()
	pageRegisterWeb.clickPaperDone()
	if '提交成功' in pageRegisterWeb.textMsg():
		time.sleep(1)
		driverWeb.quit()
		return args