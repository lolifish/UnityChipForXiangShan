from typing import Optional, Tuple
from toffee.model import Model, driver_hook
from copy import deepcopy

from .data_model import *

def get_41_6(data):  
    return (data >> 6) & ((1 << 36) - 1)

# Waylookup的功能模型
class WayLookupModel(Model):
    def __init__(self, depth=32):
        super().__init__()
        self.depth = depth
        self.flush()
    
    @driver_hook(agent_name="agent")
    def flush(self):
        """刷新"""
        # 指针信息
        self.read_ptr = PtrData()
        self.write_ptr = PtrData()
        self.gpf_ptr = PtrData()
        # Entries 环形队列
        self.entries = [EntryData() for _ in range(self.depth)]
        # 队列空/满
        self.empty
        self.full
        # gpf数据
        self.gpf_data = GpfData()
        self._gpf_valid = False
        self.gpf_hit
    
    @driver_hook(agent_name="agent")
    def reset(self):
        """reset，直接和flush一样"""
        self.flush()

    @driver_hook(agent_name="agent")
    def read(self) -> Tuple[bool, Optional[EntryData], bool, Optional[GpfData]]:
        """Waylookup读入数据
        bool: 读是否成功
        EntryData: 读到的数据
        bool: 是否gpf_hit
        GpfData: GPF数据
        """
        # 无法在不Bypass的情况下读取空队列
        if self.empty :
            return False, None, False, None
        # 读数据
        data: EntryData = self.entries[self.read_ptr.value]
        # 是否GPF_hit
        gpf_hit = self.gpf_hit
        if gpf_hit:
            gpf_data = self.gpf_data
            self._gpf_valid = False
        else:
            gpf_data = None
        # 更新读指针
        self.read_ptr.value += 1
        if (self.read_ptr.value == self.depth):
            self.read_ptr.value = 0
            self.read_ptr.flag ^= 1
        # 返回数据
        return True, data, gpf_hit, gpf_data
        
    @driver_hook(agent_name="agent")
    def write(self, data: EntryData, gpf_data: GpfData) -> bool:
        """Waylookup写入数据"""
        # 如果队列满了则拒绝写
        if self.full:
            return False
        # 如果GPF_Valid有效则拒绝写
        if self._gpf_valid:
            return False
        # 写数据
        self.entries[self.write_ptr.value] = data
        # 检查gpf
        if (data.itlb_exception_0==2 or data.itlb_exception_1==2):
            self._gpf_valid = True
            self.gpf_data = gpf_data
            self.gpf_ptr = deepcopy(self.write_ptr)
        # 更新写指针
        self.write_ptr.value += 1
        if (self.write_ptr.value == self.depth):
            self.write_ptr.value = 0
            self.write_ptr.flag ^= 1
        return True
    
    @driver_hook(agent_name="agent")
    def bypass(self, entry_data: EntryData, gpf_data: GpfData) -> Tuple[bool, Optional[EntryData], bool, Optional[GpfData]]:
        """Bypass读的特殊情况"""
        # 是否满足Bypass读的条件
        if not self.empty:
            raise IndexError("Can't bypass read while pipeline is not empty.")
        # 写入entries
        self.entries[self.write_ptr.value] = entry_data
        # 更新读写指针
        self.read_ptr.value += 1
        if (self.read_ptr.value == self.depth):
            self.read_ptr.value = 0
            self.read_ptr.flag ^= 1
        self.write_ptr.value += 1
        if (self.write_ptr.value == self.depth):
            self.write_ptr.value = 0
            self.write_ptr.flag ^= 1
        # 如果Bypass存在gpf信息，不使能gpf_valid
        have_gpf = entry_data.itlb_exception_0==2 or entry_data.itlb_exception_1==2
        if not have_gpf:
            gpf_data_r = None
        else:
            gpf_data_r = deepcopy(gpf_data)
        # 直接返回数据
        return True, entry_data, have_gpf, gpf_data_r
    
    @driver_hook(agent_name="agent")
    def update(self, update_data: UpdateData):
        hit = False
        for i in range(self.depth):
            data = self.entries[i]
            # 对第0行
            vset_same = (data.vSetIdx_0 == update_data.vSetIdx) and (not update_data.corrupt)
            ptag_same = data.ptag_0 == get_41_6(update_data.blkPaddr)
            way_same = data.waymask_0 == update_data.waymask
            # 命中更新
            if (vset_same and ptag_same):
                data.waymask_0 = update_data.waymask
                data.meta_codes_0 = bin(data.ptag_0).count("1") % 2
                hit = True
            # 非命中更新
            elif (vset_same and way_same):
                data.waymask_0 = 0
                hit = True

            # 对第1行
            vset_same = (data.vSetIdx_1 == update_data.vSetIdx) and (not update_data.corrupt) 
            ptag_same = data.ptag_1 == get_41_6(update_data.blkPaddr)
            way_same = data.waymask_1 == update_data.waymask
            # 命中更新
            if (vset_same and ptag_same):
                data.waymask_1 = update_data.waymask
                data.meta_codes_1 = bin(data.ptag_1).count("1") % 2
                hit = True
            # 非命中更新
            elif (vset_same and way_same):
                data.waymask_1 = 0
                hit = True
            
    @property
    def empty(self) -> bool:
        """队列是否空"""
        return (self.read_ptr == self.write_ptr)
    @property
    def full(self) -> bool:
        """队列是否满"""
        return (self.read_ptr.value == self.write_ptr.value and self.read_ptr.flag != self.write_ptr.flag)
    @property
    def gpf_hit(self) -> bool:
        """读取是否包含gpf信息"""
        return ((self.read_ptr == self.gpf_ptr) and self._gpf_valid)
    
