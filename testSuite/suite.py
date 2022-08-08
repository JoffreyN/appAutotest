import unittest
from common.parameter import ParameTestCase
from common.tools import getDriver

from testCase.testLogin import TestLogin
from testCase.testTrade import TestTrade
from testCase.testTradeFund import TestTradeFund
from testCase.testBusineManage import TestBusineManage
from testCase.testBusineManage_prod import TestBusineManage_prod
from testCase.testMy import TestMy
from testCase.testRegister import TestRegister
from testCase.testHomeNews import TestHomeNews
from testCase.testMarket import TestMarket
# from testCase.testCurrExchange import TestCurrExchange
from testCase.testAccUIview import TestAccUIview

def loadSuite(driver,args):
	testCasesDic={
		'login':TestLogin,
		'tradeFund':TestTradeFund,
		'more':TestBusineManage,
		'trade':TestTrade,
		# 'currExchange':TestCurrExchange,
		'my':TestMy,
		'register':TestRegister,
		# 'homeNews':TestHomeNews,
		'accUIview':TestAccUIview,
		'market':TestMarket,
	}
	if args.env=='prod':testCasesDic['more']=TestBusineManage_prod
	testSuite=unittest.TestSuite()
	for sName in args.suite.split():
		if sName=='all':
			for suiteName,testClass in testCasesDic.items():
				# if suiteName=='currExchange':continue
				__testClass=testCasesDic[suiteName]
				__testClass.args=args
				__testClass.driver=driver
				testSuite.addTest(ParameTestCase.paramed(__testClass,driver=driver,args=args))
		else:
			try:
				__testClass=testCasesDic[sName]
				__testClass.args=args
				__testClass.driver=driver
				testSuite.addTest(ParameTestCase.paramed(__testClass,driver=driver,args=args))
			except KeyError:
				raise Exception(f'未知的测试用例集: {sName}')
	return testSuite

if __name__=='__main__':
	desired_caps={
		'platformName':'Android',
		'deviceName':'VBJDU19510007442',
		'platformVersion':'9',
		'appPackage':'com.cmbi.zytx',
		"appActivity": '.module.AppStartEmptyActivity',
		'autoGrantPermissions':True,
		'unicodeKeyboard': True,
		'resetKeyboard': True,
		'noReset': True,
		'automationName':'uiautomator2',
	}
	driver=getDriver(desired_caps)
	runner=unittest.TextTestRunner(verbosity=2)
	runner.run(loadSuite(driver,args))