from copy import deepcopy
from random import randint, choice
import toffee_test, toffee

from ..utils import WayLookupModel, EntryData, GpfData, UpdateData
from ..env import WayLookupEnv

from .waylookup_fixture import waylookup_env

entry_data1 = EntryData()
entry_data1.vSetIdx_0 = 11
entry_data1.waymask_0 = 5
entry_data1.ptag_0 = 11
entry_data2 = EntryData()
entry_data2.vSetIdx_1 = 13
entry_data2.waymask_1 = 2
entry_data2.ptag_1 = 22

gpf_data = GpfData()
gpf_data.gpaddr = 123
gpf_data.isForVSnonLeafPTE = 1
entry_data_gpf = EntryData()
entry_data_gpf.itlb_exception_0 = 2
entry_data_gpf.vSetIdx_0 = 25

update_data_hit = UpdateData()
update_data_hit.vSetIdx = entry_data1.vSetIdx_0
update_data_hit.blkPaddr = entry_data1.ptag_0 << 6
update_data_hit.waymask = entry_data1.waymask_0+1
update_data_hit.corrupt = 0

update_data_not_hit = UpdateData()
update_data_not_hit.vSetIdx = entry_data1.vSetIdx_0
update_data_not_hit.blkPaddr = entry_data1.ptag_0+222
update_data_not_hit.waymask = entry_data1.waymask_0
update_data_not_hit.corrupt = 0

update_data_none = UpdateData()
update_data_none.vSetIdx = 7
update_data_none.blkPaddr = 0
update_data_none.waymask = 2
update_data_none.corrupt = 0

# 读写相关
@toffee_test.testcase
async def test_read_write_normal(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.write(deepcopy(entry_data1), GpfData())
    await agent.read()

@toffee_test.testcase
async def test_read_empty(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.read()

@toffee_test.testcase
async def test_read_bypass(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.bypass(deepcopy(entry_data2), deepcopy(gpf_data))

@toffee_test.testcase
async def test_write_full(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    for _ in range(32):
        await agent.write(deepcopy(entry_data2), GpfData())
    await agent.write(deepcopy(entry_data1), GpfData())

@toffee_test.testcase
async def test_write_gpf_valid(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.write(deepcopy(entry_data_gpf), deepcopy(gpf_data))
    await agent.write(deepcopy(entry_data1), GpfData())

@toffee_test.testcase
async def test_write_gpf_bypass(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.bypass(deepcopy(entry_data_gpf), deepcopy(gpf_data))

@toffee_test.testcase
async def test_read_write_gpf_not_bypass(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.write(deepcopy(entry_data_gpf), deepcopy(gpf_data))
    await agent.read()


# 指针回环
@toffee_test.testcase
async def test_ptr_roll(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    for _ in range(32 + 3):
        await agent.write(deepcopy(entry_data2), GpfData())
        await agent.read()

# 更新
@toffee_test.testcase
async def test_update_hit(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.write(deepcopy(entry_data1), GpfData())
    await agent.update(update_data_hit)
    await agent.read()

@toffee_test.testcase
async def test_update_miss(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.write(deepcopy(entry_data1), GpfData())
    await agent.update(update_data_not_hit)
    await agent.read()

@toffee_test.testcase
async def test_update_no(waylookup_env: WayLookupEnv):
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    await agent.write(deepcopy(entry_data1), GpfData())
    await agent.update(update_data_none)
    await agent.read()

# 随机数据生成函数
def random_data():
    data = EntryData()
    data.vSetIdx_0 = randint(0, 255)
    data.vSetIdx_1 = randint(0, 255)
    data.waymask_0 = randint(0, 15)
    data.waymask_1 = randint(0, 15)
    data.ptag_0 = randint(0, 68719476735)
    data.ptag_1 = randint(0, 68719476735)
    data.itlb_pbmt_0 = randint(0, 3)
    data.itlb_pbmt_1 = randint(0, 3)
    data.meta_codes_0 = randint(0, 1)
    data.meta_codes_1 = randint(0, 1)
    # 随机出现gpf
    random_gpf_number = randint(1, 100)
    if random_gpf_number == 1:
        data.itlb_exception_0 = 2
    elif random_gpf_number == 2:
        data.itlb_exception_1 = 2
    else:
        data.itlb_exception_0 = randint(0, 1)
        data.itlb_exception_1 = randint(0, 1)
    gpf = GpfData()
    gpf.gpaddr = randint(1, 1000)
    gpf.isForVSnonLeafPTE = randint(0, 1)
    return data, gpf
def random_update_data(model: WayLookupModel):
    a = randint(1, 5)
    entry = choice(model.entries)
    data = UpdateData()
    # 命中
    if a==1:
        data.blkPaddr = entry.ptag_0 << 6
        data.vSetIdx = entry.vSetIdx_0
        data.waymask = randint(0, 15)
        data.corrupt = randint(0, 1)
    elif a==2:
        data.blkPaddr = entry.ptag_1 << 6
        data.vSetIdx = entry.vSetIdx_1
        data.waymask = randint(0, 15)
        data.corrupt = randint(0, 1)
    # waymask命中
    elif a==3:
        data.blkPaddr = randint(0, 68719476735) << 6
        data.vSetIdx = entry.vSetIdx_0
        data.waymask = entry.waymask_0
        data.corrupt = randint(0, 1)
    elif a==4:
        data.blkPaddr = randint(0, 68719476735) << 6
        data.vSetIdx = entry.vSetIdx_1
        data.waymask = entry.waymask_1
        data.corrupt = randint(0, 1)
    # 纯随机
    else:
        data.blkPaddr = randint(100, 500) << 6
        data.vSetIdx = randint(0, 255)
        data.waymask = randint(0, 15)
        data.corrupt = randint(0, 1)
    return data

    

@toffee_test.testcase
async def test_random(waylookup_env: WayLookupEnv):
    toffee.info("start")
    model = WayLookupModel()
    agent = waylookup_env.agent
    await agent.reset()
    await agent.flush()
    # 随机执行10k次
    data_num = 0
    for i in range(10000):
        random_number = randint(1, 10000)

        # 写入数据
        if random_number <= 3100:
            data, gpf = random_data()
            s = await agent.write(deepcopy(data), deepcopy(gpf))
            model.write(deepcopy(data), deepcopy(gpf))
            if s:
                data_num += 1
            toffee.info(f"[{i}] Write (num={data_num})")

        # 读取数据
        elif random_number <= 6000:
            # 检查下是不是empty，如果是则有可能bypass读
            if model.empty:
                if randint(0, 1):
                    data, gpf = random_data()
                    toffee.info(f"[{i}] Bypass read, num={data_num}")
                    await agent.bypass(deepcopy(data), deepcopy(gpf))
                    model.bypass(deepcopy(data), deepcopy(gpf))
                else:
                    toffee.info(f"[{i}] Fail read, num={data_num}")
                    await agent.read()
                    model.read()
            else:
                data_num -= 1
                toffee.info(f"[{i}] Read, num={data_num}")
                await agent.read()
                model.read()
        
        # 更新数据
        elif random_number <= 9995:
            data = random_update_data(model)
            await agent.update(deepcopy(data))
            model.update(deepcopy(data))
            toffee.info(f"[{i}] Update")

        else:
            if randint(1, 5) != 1:
                await agent.flush()
                model.flush()
                toffee.info(f"[{i}] Flush")
                data_num = 0
            else:
                await agent.reset()
                model.reset()
                toffee.info(f"[{i}] Reset")
                data_num = 0
