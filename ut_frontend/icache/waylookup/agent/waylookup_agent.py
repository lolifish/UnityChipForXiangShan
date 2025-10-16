import sys
sys.path.append("./")

from toffee.agent import driver_method, Agent

from ..bundle import WayLookupBundle
from ..utils import EntryData, GpfData, UpdateData
from dut.WayLookup import DUTWayLookup
import toffee

from typing import Tuple, Optional

class WayLookupAgent(Agent):
    def __init__(self, bundle: WayLookupBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle

    @driver_method()
    async def flush(self):
        # 拉低所有握手端口
        self.bundle.read_ready.value = 0
        self.bundle.write_valid.value = 0
        self.bundle.update_valid.value = 0
        # flush
        self.bundle.flush.value = 1
        await self.bundle.step()
        self.bundle.flush.value = 0
        await self.bundle.step()
    
    @driver_method()
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()

    @driver_method()
    async def read(self) -> Tuple[bool, Optional[EntryData], bool, Optional[GpfData]]:
        # 读取信号
        await self.bundle.step()
        entry_data = EntryData()
        entry_data.vSetIdx_0 = self.bundle.read_vSetIdx_0.value
        entry_data.vSetIdx_1 = self.bundle.read_vSetIdx_1.value
        entry_data.waymask_0 = self.bundle.read_waymask_0.value
        entry_data.waymask_1 = self.bundle.read_waymask_1.value
        entry_data.ptag_0 = self.bundle.read_ptag_0.value
        entry_data.ptag_1 = self.bundle.read_ptag_1.value
        entry_data.itlb_exception_0 = self.bundle.read_itlb_exception_0.value
        entry_data.itlb_exception_1 = self.bundle.read_itlb_exception_1.value
        entry_data.itlb_pbmt_0 = self.bundle.read_itlb_pbmt_0.value
        entry_data.itlb_pbmt_1 = self.bundle.read_itlb_pbmt_1.value
        entry_data.meta_codes_0 = self.bundle.read_meta_codes_0.value
        entry_data.meta_codes_1 = self.bundle.read_meta_codes_1.value
        # GPF数据
        has_gpf = self.bundle.read_itlb_exception_0.value == 2 or self.bundle.read_itlb_exception_1.value == 2
        if has_gpf:
            gpf_data = GpfData()
            gpf_data.gpaddr = self.bundle.read_gpf_gpaddr.value
            gpf_data.isForVSnonLeafPTE = self.bundle.read_gpf_isForVSnonLeafPTE.value
        else:
            gpf_data = None
        # 执行真正的读操作
        self.bundle.read_ready.value = 1
        await self.bundle.step()
        # 尝试等待valid
        _wait_cnt = 0
        success = False
        while _wait_cnt < 5:
            if (self.bundle.read_valid.value):
                success = True
                break
            _wait_cnt += 1
            await self.bundle.step()
        # 读失败不返回数据
        self.bundle.read_ready.value = 0
        await self.bundle.step()
        if not success: return False, None, False, None
        return True, entry_data, has_gpf, gpf_data
    
    @driver_method()
    async def write(self, data: EntryData, gpf_data: GpfData) -> bool:
        # 写入信号
        self.bundle.write_valid.value = 1
        self.bundle.write_vSetIdx_0.value = data.vSetIdx_0
        self.bundle.write_vSetIdx_1.value = data.vSetIdx_1
        self.bundle.write_waymask_0.value = data.waymask_0
        self.bundle.write_waymask_1.value = data.waymask_1
        self.bundle.write_ptag_0.value = data.ptag_0
        self.bundle.write_ptag_1.value = data.ptag_1
        self.bundle.write_itlb_exception_0.value = data.itlb_exception_0
        self.bundle.write_itlb_exception_1.value = data.itlb_exception_1
        self.bundle.write_itlb_pbmt_0.value = data.itlb_pbmt_0
        self.bundle.write_itlb_pbmt_1.value = data.itlb_pbmt_1
        self.bundle.write_meta_codes_0.value = data.meta_codes_0
        self.bundle.write_meta_codes_1.value = data.meta_codes_1
        self.bundle.write_gpf_gpaddr.value = gpf_data.gpaddr
        self.bundle.write_gpf_isForVSnonLeafPTE.value = gpf_data.isForVSnonLeafPTE
        await self.bundle.step()
        # 尝试等待ready
        _wait_cnt = 0
        success = False
        while _wait_cnt < 5:
            if (self.bundle.write_ready.value):
                success = True
                break
            _wait_cnt += 1
            await self.bundle.step()
        self.bundle.write_valid.value = 0
        await self.bundle.step(5)
        # 返回是否成功
        if not success: return False
        else: return True

    @driver_method()
    async def update(self, update_data: UpdateData):
        self.bundle.blkPaddr.value = update_data.blkPaddr
        self.bundle.corrupt.value = update_data.corrupt
        self.bundle.vSetIdx.value = update_data.vSetIdx
        self.bundle.waymask.value = update_data.waymask
        self.bundle.update_valid.value = 1
        await self.bundle.step()
        self.bundle.update_valid.value = 0
        await self.bundle.step()
    
    @driver_method()
    async def bypass(self, data: EntryData, gpf_data: GpfData) -> Tuple[bool, Optional[EntryData], bool, Optional[GpfData]]:
        # 写入信号
        self.bundle.write_valid.value = 1
        self.bundle.write_vSetIdx_0.value = data.vSetIdx_0
        self.bundle.write_vSetIdx_1.value = data.vSetIdx_1
        self.bundle.write_waymask_0.value = data.waymask_0
        self.bundle.write_waymask_1.value = data.waymask_1
        self.bundle.write_ptag_0.value = data.ptag_0
        self.bundle.write_ptag_1.value = data.ptag_1
        self.bundle.write_itlb_exception_0.value = data.itlb_exception_0
        self.bundle.write_itlb_exception_1.value = data.itlb_exception_1
        self.bundle.write_itlb_pbmt_0.value = data.itlb_pbmt_0
        self.bundle.write_itlb_pbmt_1.value = data.itlb_pbmt_1
        self.bundle.write_meta_codes_0.value = data.meta_codes_0
        self.bundle.write_meta_codes_1.value = data.meta_codes_1
        self.bundle.write_gpf_gpaddr.value = gpf_data.gpaddr
        self.bundle.write_gpf_isForVSnonLeafPTE.value = gpf_data.isForVSnonLeafPTE
        # 读使能进入bypass
        self.bundle.read_ready.value = 1
        await self.bundle.step()
        self.bundle.read_ready.value = 0
        self.bundle.write_valid.value = 0
        # 读取信号
        entry_data = EntryData()
        entry_data.vSetIdx_0 = self.bundle.read_vSetIdx_0.value
        entry_data.vSetIdx_1 = self.bundle.read_vSetIdx_1.value
        entry_data.waymask_0 = self.bundle.read_waymask_0.value
        entry_data.waymask_1 = self.bundle.read_waymask_1.value
        entry_data.ptag_0 = self.bundle.read_ptag_0.value
        entry_data.ptag_1 = self.bundle.read_ptag_1.value
        entry_data.itlb_exception_0 = self.bundle.read_itlb_exception_0.value
        entry_data.itlb_exception_1 = self.bundle.read_itlb_exception_1.value
        entry_data.itlb_pbmt_0 = self.bundle.read_itlb_pbmt_0.value
        entry_data.itlb_pbmt_1 = self.bundle.read_itlb_pbmt_1.value
        entry_data.meta_codes_0 = self.bundle.read_meta_codes_0.value
        entry_data.meta_codes_1 = self.bundle.read_meta_codes_1.value
        # 读取GPF
        has_gpf = self.bundle.read_itlb_exception_0.value == 2 or self.bundle.read_itlb_exception_1.value == 2
        if has_gpf:
            gpf_data = GpfData()
            gpf_data.gpaddr = self.bundle.read_gpf_gpaddr.value
            gpf_data.isForVSnonLeafPTE = self.bundle.read_gpf_isForVSnonLeafPTE.value
        else:
            gpf_data = None
        await self.bundle.step()
        return True, entry_data, has_gpf, gpf_data


