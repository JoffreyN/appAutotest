# 1. 每天跑一次test和uat环境个20~30个，随机
# 2. ABC账户占30%
# 3. 10%的不需要审核
# 4. 
from regWeb import main as regWeb_main
from common.system_openbo import loginBO
import random,HTMLReport,logging,traceback

class Args():
	def __init__(self):
		pass

def random_pick(some_list, probabilities):
	x=random.uniform(0,1)
	cumulative_probability=0.0
	for item, item_probability in zip(some_list, probabilities):
		cumulative_probability+=item_probability
		if x<cumulative_probability:
			break
	return item

loginBO('test')
loginBO('uat')
accNumbers=random.randint(20,30)
# accNumbers=1
for env in ['test','uat']:
	# print(f'{env} 开户,总计 {accNumbers} 个')
	for i in range(accNumbers):
		acc_type=random_pick(['abc','ttl'],[0.3,0.7])
		need_check=random_pick([0,1],[0.1,0.9])
		logging.info(f'{env} 开户,共 {accNumbers} 个  第 {i} 个,账户类型: {acc_type} ,需要审核: {need_check}')
		args=Args()
		args.regbyapi=True
		args.margin=True
		args.headless=True
		args.setPwd=False
		args.pi=False
		args.location='zh_CN'
		args.tel=None
		args.email=None
		args.env=env

		args.ttl=acc_type
		args.check=args.active=need_check
		try:
			args=regWeb_main(args)
		except Exception as err:
			logging.info(traceback.format_exc())
