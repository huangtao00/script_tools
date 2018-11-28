#!coding:utf8
import random
def reorder_data(data):
	index = [i for i in range(len(data))]
	result = []
	for i in range(len(index)):
		pos = random.choice(index)
		result.append(data[pos])
		index.remove(pos)
	return result

def normalDistributeCount(ckgCount):
	"""
	:param ckgCount: 所有可用的ckg数量，需要决定 垃圾量为0%	 10%  ... 100%的数据 占ckg的数量
	:return: [0 ,2 ,3, 4 ,5 , 12	  5		  4		  3		  2		  0]   表示垃圾量为0的数据分配0个ckg，垃圾量占90%的数据分配2个ckg
	"""
	totalSum = 0
	upFactor = []
	for i in range(0,11):
		tmp = function_one(i)
		upFactor.append(tmp)
		totalSum += tmp
	result = []
	for i in upFactor:
		result.append(int(i/totalSum*ckgCount))
	left = ckgCount - sum(result)
	result[5] += left
	# print sum(result)
	return result
def function_one(x):
	f=1.1-(0.2*x -1)**2
	return f

if __name__ == "__main__":
	# data = ['valid', 'valid', 'valid', 'valid', 'valid', 'invalid']
	# print reorderStripRandom(data)
	# for	 i	in range (4000):
	# 	print normalDistributeCount(i)
	new = []
	old = [i for i in range(10)]
	new.append(old.pop(0))
	print new
	print old
	new.append(old.pop(0))
	print new
	print old