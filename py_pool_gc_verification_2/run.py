#!coding:utf8
from diskpool import *
from  misc import normalDistributeCount
def writeDataWithSepcificDistribution(diskgroup,ckgm,ckgCount,dataMappingFunc=normalDistributeCount):
	"""
	:param diskgroup:
	:param ckgm:
	:param ckgCount:
	:param dataMappingFunc: 垃圾数据分配的映射函数
	:return:
	"""
	dataDistribute = dataMappingFunc(ckgCount)

	ckgm.ckgDistribuion = dataDistribute[:]
	garbagePercent = 0
	for i in dataDistribute:
		tmpGarbagePercent = garbagePercent /10.0
		for j in range(i):
			# print tmpGarbagePercent
			status, ckg = writeNewDatatoCKG(diskgroup, ckgm, garbagePercent = tmpGarbagePercent)
			if not status:
				print "allocate ckg failed", "garbage percent",garbagePercent
				return False
		garbagePercent += 1
	return True

if __name__ == "__main__":
	ckCountPerDisk = 50
	diskgroup = []
	# 1: 创建DISK GROUP
	for i in range(6):
		diskgroup.append(Disk(i, ckCount=ckCountPerDisk))

	# 2: 创建CKG管理对象
	ckgm = ckgManager(diskgroup)

	# 3: 分配ckg, 分配80%的ckg
	ckgCount = int(ckCountPerDisk*0.8)

	# 4: 向80%的ckg 写入特定垃圾分布的数据到ckg
	writeDataWithSepcificDistribution(diskgroup, ckgm, ckgCount)

	# 查看当前分配ckg的使用情况
	# ckgm.showUsedCkg()
	# ckgm.showAllCkgDataInfo(diskgroup)
	ckgm.showGarbageDistribution()

	# 5: 实现修改写
	while True:
		if ckgm.allocateCkg(diskgroup): #分配ckg空间成功(修改写ckg使用到总空间的87%时,就分配不到ckg空间,13%是op空间)
			ckg = ckgm.getLatestCkgInfo()
			#随机将其它ckg置为invalid
			#新的ckg全置为valid状态
		else: #ckg分配失败
			pass
			#基于指定的算法做垃圾回收操作， 垃圾回收需要有一个空间存放搬移的有效数据
			# 1：进行gc操作，读取满足回收条件ckg内部的效数据到memory（仅统计有效数据的个数）
			# 2: 释放掉回收的ckg,基于上面统计的有效数据的个数 (op空间如何利用的问题)
			# 3: 从op空间分配一个有效ckg出来





