from dataclasses import dataclass

# 指针数据
@dataclass(eq=True)
class PtrData:
    value: int = 0
    flag: int = 0

# Entry数据
@dataclass(eq=True)
class EntryData:
    vSetIdx_0: int = 0
    vSetIdx_1: int = 0
    waymask_0: int = 0
    waymask_1: int = 0
    ptag_0: int = 0
    ptag_1: int = 0
    itlb_exception_0: int = 0
    itlb_exception_1: int = 0
    itlb_pbmt_0: int = 0
    itlb_pbmt_1: int = 0
    meta_codes_0: int = 0
    meta_codes_1: int = 0

# GPF数据
@dataclass(eq=True)
class GpfData:
    gpaddr: int = 0
    isForVSnonLeafPTE: int = 0

# Update数据
@dataclass()
class UpdateData:
    blkPaddr: int = 0
    vSetIdx: int = 0
    waymask: int = 0
    corrupt: int = 0

