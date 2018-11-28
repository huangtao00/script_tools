#!coding:utf8
from misc import *
class Su:
    def __init__(self, su_id):
        self.su_id = su_id
        self.status = "empty" #empty valid invalid
        self.ckg_id = -1
    def set_status(self, status):
        self.status = status
    def get_status(self):
        return self.status
    def get_ckg_id(self):
        return self.ckg_id
    def set_ckg_id(self,ckg_id):
        self.ckg_id = ckg_id

class Disk:
    """
        disk_size:单盘存储空间 4GB
        ck_size :单个ck的存储空间 4MB
        su_size : su存储空间   16KB
        单盘容量必须为su容量的整数倍 su_count = 2**18个
        后面chunk的size设置为4MB
        disk_id = 0, disk_size = 4*2**30, ck_size = 4*2**20, su_size = 16*2**10
    """
    def __init__(self, disk_id = 0, disk_size = 4*2**30, ck_size = 4*2**20, su_size = 16*2**10):
        self.disk_id = disk_id
        self.total_ck_count = disk_size / ck_size
        self.total_su_count = disk_size / su_size
        self.su_count_per_ck = ck_size / su_size
        # print self.su_count_per_ck
        self.available_su_count = self.total_su_count
        self.su_array=[]
        for i in range(self.total_su_count):
            self.su_array.append(Su(i))
    def get_available_space_by_percent(self):
        print ("can create %d chunk" % (self.available_su_count*self.total_ck_count /float(self.total_su_count)))
        return self.available_su_count /float(self.total_su_count)
    def decrease_su(self):
        self.available_su_count -= 1
    def show_all_su_status(self):
        for su in self.su_array:
            print su.get_status()
    def stat_available_su(self):
        print "disk[%d]:" % self.disk_id
        print self.available_su_count
        return self.available_su_count
    def stat_all_su_status(self):
        empty_su_count = 0
        valid_su_count = 0
        invalid_su_count = 0
        print "disk[%d]:" % self.disk_id
        for su in self.su_array:
            su_status = su.get_status()
            if su_status == "empty":
                empty_su_count += 1
            if su_status == "valid":
                valid_su_count += 1
            if su_status == "invalid":
                invalid_su_count += 1
        print "%-18s = %-10d" % ("empty_su_count",empty_su_count)
        print "%-18s = %-10d" % ("valid_su_count",valid_su_count)
        print "%-18s = %-10d" % ("invalid_su_count",invalid_su_count)
        print "%-18s = %-10d" %  ("available_su_count",self.available_su_count)
        print "\n"
        return [empty_su_count, valid_su_count, invalid_su_count ,self.available_su_count]

    def check_create_ck_availabce(self):
        """
        检查剩下的su是否足够创建一个ck
        :return: True　空间足够
        """
        if self.available_su_count < self.su_count_per_ck:
            print "sorry! su count is not enough in disk %d " % self.disk_id
            return False
        return True
    def create_a_ck(self, ckg_id):
        su_for_ck = []
        added_su = 0
        for su in self.su_array:
            if su.get_ckg_id() == -1:
                su.set_ckg_id(ckg_id)
                su_for_ck.append(su.su_id)
                self.decrease_su()
                added_su +=1
                if added_su == self.su_count_per_ck:
                    return su_for_ck
        print "never come here"
        return False

class DiskPool:
    def __init__(self,disk_count = 7):
        self.disk_count = disk_count
        self.disk_array = []
        for disk_id in range(self.disk_count):
            self.disk_array.append(Disk(disk_id,disk_size = 4*2**30, ck_size = 4*2**20, su_size = 1*2**20/2))
        self.total_ck_count = self.disk_array[0].total_ck_count

class CkgManager:
    def __init__(self, DiskPool):
        self.disk_pool = DiskPool
        self.used_ckg_id_array = []
        self.vblock_available_ckg_id_array =[i for i in range(DiskPool.disk_array[0].total_ck_count*2)]
        self.used_ckgs_su_set = {}
        self.status_table = {"empty":"e","valid":"v","invalid":"i"}
    def get_vblock_available_ckg_id_array(self):
        return self.vblock_available_ckg_id_array
    def get_used_ckg_id(self):
        return self.used_ckg_id_array
    def get_used_ckgs_su_set(self):
        return  self.used_ckgs_su_set
    def create_ckg(self):
        for disk in self.disk_pool.disk_array:
            if not disk.check_create_ck_availabce(): #如果有一个disk空间不足，不能分配ck空间
                print "no room to create ck for disk %d" % disk.disk_id
                return -1
        #创建ckg
        ckg_id = self.vblock_available_ckg_id_array.pop(0) #分配一个ckg_id
        self.used_ckg_id_array.append(ckg_id)
        ckg_su_set = []
        for disk in self.disk_pool.disk_array:
            ckg_su_set.append(disk.create_a_ck(ckg_id))
        self.used_ckgs_su_set[ckg_id] = ckg_su_set #用这个字典变量 建立ckg_id与所有su_id的关联
        # print ckg_su_set
        return ckg_id #返回ckg_id
    def generate_stripe_data(self,garbage_percent):
        """
        :param garbage_percent: 垃圾量占比1 0.9 0.8 ... 0
        :return:
        """
        disk_count = self.disk_pool.disk_count
        invalid_count = int(disk_count * garbage_percent)
        valid_count  = disk_count - invalid_count
        stripeData = "valid " * valid_count + "invalid " * invalid_count #组成一个分条的数据分布情况
        stripeData = stripeData.split() #变成list
        # reorderStripeData = reorderStripRandom(stripeData) #打乱顺序
        return stripeData
    def write_data_to_ckg(self, ckg_id, data):
        #按分条写data
        #遍历ckg的分条
        ckg_su_id = self.used_ckgs_su_set[ckg_id] #[[suid,suid, suid] [] [] [] [] []] 内部对应每个disk的 su id
        su_count = len(ckg_su_id[0])
        for i in range(su_count):
            redata = reorder_data(data)
            for disk_id in range(len(ckg_su_id)): #遍历一个分条
                su_id = ckg_su_id[disk_id][i] #取出su_id
                disk_pool.disk_array[disk_id].su_array[su_id].set_status(redata[disk_id])
    def write_data_to_multiple_ckg(self,percent,func=normalDistributeCount):
        """
        程序快速填满空间时会用该函数
        :param percent: 要写的ckg占所有ckg的比例 ， 如 0.8表示 写满总空间的80%
        :param func: 函数，产生垃圾分布情况 如 func(11)  返回 [ 2 3 1 1 1 1 1 1 1 1 1]  产生2个ckg,垃圾量为0，产生3个ckg,垃圾量为10%
        :return:
        """
        write_ckg_count = int(self.disk_pool.total_ck_count * percent)
        data_distribute = func(write_ckg_count)
        garbage_percent = 0
        for i in data_distribute:
            tmp = garbage_percent / 10.0
            for j in range(i):
                ckg_id = self.create_ckg()
                if ckg_id != -1: #分配 ckg_id成功
                    data = self.generate_stripe_data(tmp)  # 70% garbage data
                    self.write_data_to_ckg(ckg_id, data)
                else:
                    print "create ckg failed %f" %  garbage_percent
                    return False
            garbage_percent += 1
        return True

    def show_ckg_status(self,ckg_id):
        ckg_su_id = self.used_ckgs_su_set[ckg_id] #[[suid,suid, suid] [] [] [] [] []] 内部对应每个disk的 su id
        su_count = len(ckg_su_id[0])
        description = "e: empty v: valid i: invalid"
        print "*"*len(description)
        print description
        print "*"*len(description)
        for i in range(su_count):
            redata = reorder_data(data)
            for disk_id in range(len(ckg_su_id)): #遍历一个分条
                su_id = ckg_su_id[disk_id][i] #取出su_id
                key = disk_pool.disk_array[disk_id].su_array[su_id].get_status()
                print self.status_table[key],
            print "\n"

if __name__ == "__main__":
    disk_count = 6
    disk_pool = DiskPool(disk_count)
    # for i in range(6):
    #     disk_pool.disk_array[i].stat_all_su_status()
    # for i in range(disk_count):
    #      disk_pool.disk_array[i].stat_all_su_status()
    ckgm = CkgManager(disk_pool)

    # for i in range(1000):
    #     ckg_id = ckgm.create_ckg()
    #     data = ckgm.generate_stripe_data(0.7) #70% garbage data
    #     ckgm.write_data_to_ckg(ckg_id, data)

    for i in range(disk_count):
         print disk_pool.disk_array[i].get_available_space_by_percent()
    # ckgm.show_ckg_status(ckg_id)l
    ckgm.write_data_to_multiple_ckg(0.8, normalDistributeCount)

    for i in range(disk_count):
         print disk_pool.disk_array[i].get_available_space_by_percent()