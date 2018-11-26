#!coding:utf8
import sys
class SU:
	def __init__(self,suId):
		self.suId = suId
		self.status = "empty" #empty valid invalid
	def setStatus(self,status):
		self.status = satus
	def getStatus(self):
		return self.status

class Chunk:
	def __init__(self,ckId,chunkSize = 4*2**20 ,stripeUnitSize = 16*2**10):
		"""
		chunkSize 4M
		stripeUnitSize 16K 
		"""
		self.status = "unused" #used
		self.ckId = ckId
		self.chunkSize = chunkSize
		self.suSize = stripeUnitSize
		self.suCount = chunkSize / stripeUnitSize
		self.su_array = [] 
		for i in range(0,self.suCount):
			self.su_array.append(SU(i))
	def setstatus(self,status):
		self.status = status

	def showInfo(self):
		print "ckId=" + str(self.ckId)
		print "chunkSize=" + str(self.chunkSize)
		print "suSize=" + str(self.suSize)
		print "suCount=" + str(self.suCount)
class Disk:
	def __init__(self,diskId,ckCount = 10):
		"""
			100*4M 400M的 disk容量
		"""
		self.diskId = diskId
		self.ckCount = ckCount
		self.ck_array = []
		for i in range(self.ckCount):
			self.ck_array.append(Chunk(i))
	def __init__(self,diskId,ckCount = 14,chunkSize = 4*2**20 ,stripeUnitSize = 16*2**10):
		"""
			100*4M 400M的 disk容量
		"""
		self.diskId = diskId
		self.ckCount = ckCount
		self.ck_array = []
		for i in range(self.ckCount):
			self.ck_array.append(Chunk(i,chunkSize = 4*2**20 ,stripeUnitSize = 16*2**10))

class ckgManager:
	def __init__(self,diskgroup):
		self.CONST_GC_LEVEL = 0.8
		if len(diskgroup)<=0:
			print ("disk group initialized error,please check your parameter")
			sys.exit(1)
		self.diskCount = len(diskgroup)
		self.stripCount = diskgroup[0].ck_array[0].suCount
		self.totalCkgCount = len(diskgroup[0].ck_array)
		self.leftCkgCount = self.totalCkgCount
		self.usedCkgCount = self.totalCkgCount - self.leftCkgCount
		self.dangerLevelUsedCkgCount = int(self.totalCkgCount*self.CONST_GC_LEVEL)
		self.usedCkgInfo=[]
		self.usedCkgId=[]
	def allocateCkg(self,diskgroup):
		"""
			这个函数还有考虑如何将分条凑成ckg,进行分配的问题，后面再考虑
		"""
		if self.usedCkgCount >= self.dangerLevelUsedCkgCount:
			print ("no enough ckg capacity available ")
			#todo
		    #do gc algorithm
		if self.usedCkgCount >= self.dangerLevelUsedCkgCount:
			print ("sorry, gc algorithm did not work ")
			return False
		diskIdList = range(len(diskgroup))
		ckg=[]
		for diskID, disk in zip(diskIdList, diskgroup):
			chunkIdList = range(len(disk.ck_array))
			for chunkId, chunk in zip(chunkIdList, disk.ck_array):
				if (chunk.status == "unused"):
					chunk.setstatus("used")
					ckg.append({"diskId":diskID, "chunkId":chunkId})
					break;
		#上面是存在整个ckg没有使用的情况

		if (len(ckg) == len(diskgroup)):
			self.usedCkgInfo.append(ckg)
			self.usedCkgId.append(ckg[0]["chunkId"]) #存在可分配的ckg,所有chunk都是空的，不是用分条拼凑出来的
			self.usedCkgCount += 1
			self.leftCkgCount -= 1
			return True
		else:	#这里要做vblock分条的ckg的分配,然后再得到ckgId
			#todo
			pass  #
	def getCkgLBA(self,ckgId):
		"""
		:param ckgId:
		:return: 通过ckgId计算得到这个ckgId对应的LBA地址
		"""
		start  = ckgId*self.diskCount*self.stripCount
		end = start + self.diskCount*self.stripCount -1 #包括最后一个
		return (start,end)
	def showUsedCkg(self):
		count = 0
		for ckg in   self.usedCkgInfo:
			print "diskId", "chunkId","--->ckg[",count,"]"
			for ck in ckg:
				print ck["diskId"],"\t",ck["chunkId"]
			count += 1
def writeNewData(diskgroup,capacityPercent,type):
	"""
		diskgroup对象
		写满capacityPercent（百分比）的用户空间，
		type几种典型的垃圾分布场景
	"""

if __name__ == "__main__":
	# aCK = Chunk(0, 4*2**20, 16*2**10)
	# aCK.showInfo()
	# for i in aCK.su_array:
	# 	print i.suId
	# 	print i.status
	diskgroup = []
	stripeStat=[0,0,0] #e,v,invalid
	for i in range(6):
		diskgroup.append(Disk(i,ckCount=20))

	for disk in  diskgroup:
		for chunk in disk.ck_array:
			for stripe in chunk.su_array:
				if stripe.getStatus() == "empty":
					stripeStat[0]+=1
	print stripeStat[0]
	diskIdList = range(len(diskgroup))
	# ckg=[]
	# for diskID,disk in  zip(diskIdList,diskgroup):
	# 	chunkIdlist = range(len(disk.ck_array))
	# 	for chunkId,chunk in zip(chunkIdlist,disk.ck_array):
	# 		if (chunk.status == "unused"):
	# 			chunk.setstatus("used")
	# 			ckg.append((diskID,chunkId))
	# 			break;
	# print ckg
	#
	#
	# ckg1 = []
	# for diskID, disk in zip(diskIdList, diskgroup):
	# 	chunkIdlist = range(len(disk.ck_array))
	# 	for chunkId, chunk in zip(chunkIdlist, disk.ck_array):
	# 		if (chunk.status == "unused"):
	# 			chunk.setstatus("used")
	# 			ckg1.append((diskID, chunkId))
	# 			break;
	# print ckg1
	ckm=ckgManager(diskgroup)
	for i in range(14):
		ckm.allocateCkg(diskgroup)
		# ckm.showUsedCkg()
		print "total ckg count", ckm.totalCkgCount
		print "already used ckg count", ckm.usedCkgCount


	print "gc triger ckg count",ckm.dangerLevelUsedCkgCount
	print ckm.usedCkgId


