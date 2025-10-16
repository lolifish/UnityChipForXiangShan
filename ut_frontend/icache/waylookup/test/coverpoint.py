import toffee.funcov as fc

from ..bundle import WayLookupBundle

# Flush
def check_flush_read(bundle: WayLookupBundle) -> bool:
    return (bundle.readPtr_value.value == 0 and bundle.readPtr_flag.value == 0)
def check_flush_write(bundle: WayLookupBundle) -> bool:
    return (bundle.writePtr_value.value == 0 and bundle.writePtr_flag.value == 0)
def check_flush_gpf(bundle: WayLookupBundle) -> bool:
    return (bundle.gpf_bits.value == 0 and bundle.gpf_valid.value == 0)
def get_cover_group_flush(bundle: WayLookupBundle):
    group = fc.CovGroup("WayLookup_flush")
    group.add_cover_point(
        bundle, {
            "readPtr flush": check_flush_read,
            "writePtr flush": check_flush_write,
            "gpf flush": check_flush_gpf,
        }, name="flush", once=False
    )
    group.mark_function("flush", ["ut_frontend/icache/waylookup/test/waylookup_test.test_ptr_roll", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    return group



# Ptr update
read_value_r = 0
read_flag_r = 0
def check_ptr_read_inc(bundle: WayLookupBundle) -> bool:
    global read_value_r, read_flag_r
    if bundle.readPtr_value.value == read_value_r + 1:
        read_value_r = bundle.readPtr_value.value
        return True
    else:
        return False
def check_ptr_read_roll(bundle: WayLookupBundle) -> bool:
    global read_value_r, read_flag_r
    if (not bundle.flush.value) and read_flag_r!=bundle.readPtr_flag.value and read_value_r==31:
        read_value_r = 0
        read_flag_r ^= 1
        return True
    else:
        return False
    
write_value_r = 0
write_flag_r = 0
def check_ptr_write_inc(bundle: WayLookupBundle) -> bool:
    global write_value_r, write_flag_r
    if bundle.writePtr_value.value == write_value_r + 1:
        write_value_r = bundle.writePtr_value.value
        return True
    else:
        return False
def check_ptr_write_roll(bundle: WayLookupBundle) -> bool:
    global write_value_r, write_flag_r
    if (not bundle.flush.value) and write_flag_r!=bundle.writePtr_flag.value and write_value_r==31:
        write_value_r = 0
        write_flag_r ^= 1
        return True
    else:
        return False
    
def get_cover_group_ptr(bundle: WayLookupBundle):
    group = fc.CovGroup("WayLookup_ptr")
    group.add_cover_point(
        bundle, {
            "readPtr increment": check_ptr_read_inc,
            "readPtr roll over": check_ptr_read_roll,
        }, name="readPtr", once=False
    )
    group.add_cover_point(
        bundle, {
            "writePtr increment": check_ptr_write_inc,
            "writePtr roll over": check_ptr_write_roll,
        }, name="writePtr", once=False
    )
    group.mark_function("readPtr", ["ut_frontend/icache/waylookup/test/waylookup_test.test_ptr_roll", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    group.mark_function("writePtr", ["ut_frontend/icache/waylookup/test/waylookup_test.test_ptr_roll", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    return group


# Update 情况
_get_vset_same = lambda bundle: bundle.vset_same.value or bundle.vset_same_1.value or bundle.vset_same_2.value or bundle.vset_same_3.value or bundle.vset_same_4.value or bundle.vset_same_5.value or bundle.vset_same_6.value or bundle.vset_same_7.value or bundle.vset_same_8.value or bundle.vset_same_9.value or bundle.vset_same_10.value or bundle.vset_same_11.value or bundle.vset_same_12.value or bundle.vset_same_13.value or bundle.vset_same_14.value or bundle.vset_same_15.value or bundle.vset_same_16.value or bundle.vset_same_17.value or bundle.vset_same_18.value or bundle.vset_same_19.value or bundle.vset_same_20.value or bundle.vset_same_21.value or bundle.vset_same_22.value or bundle.vset_same_23.value or bundle.vset_same_24.value or bundle.vset_same_25.value or bundle.vset_same_26.value or bundle.vset_same_27.value or bundle.vset_same_28.value or bundle.vset_same_29.value or bundle.vset_same_30.value or bundle.vset_same_31.value or bundle.vset_same_32.value or bundle.vset_same_33.value or bundle.vset_same_34.value or bundle.vset_same_35.value or bundle.vset_same_36.value or bundle.vset_same_37.value or bundle.vset_same_38.value or bundle.vset_same_39.value or bundle.vset_same_40.value or bundle.vset_same_41.value or bundle.vset_same_42.value or bundle.vset_same_43.value or bundle.vset_same_44.value or bundle.vset_same_45.value or bundle.vset_same_46.value or bundle.vset_same_47.value or bundle.vset_same_48.value or bundle.vset_same_49.value or bundle.vset_same_50.value or bundle.vset_same_51.value or bundle.vset_same_52.value or bundle.vset_same_53.value or bundle.vset_same_54.value or bundle.vset_same_55.value or bundle.vset_same_56.value or bundle.vset_same_57.value or bundle.vset_same_58.value or bundle.vset_same_59.value or bundle.vset_same_60.value or bundle.vset_same_61.value or bundle.vset_same_62.value or bundle.vset_same_63.value
_get_ptag_same = lambda bundle: bundle.ptag_same.value or bundle.ptag_same_1.value or bundle.ptag_same_2.value or bundle.ptag_same_3.value or bundle.ptag_same_4.value or bundle.ptag_same_5.value or bundle.ptag_same_6.value or bundle.ptag_same_7.value or bundle.ptag_same_8.value or bundle.ptag_same_9.value or bundle.ptag_same_10.value or bundle.ptag_same_11.value or bundle.ptag_same_12.value or bundle.ptag_same_13.value or bundle.ptag_same_14.value or bundle.ptag_same_15.value or bundle.ptag_same_16.value or bundle.ptag_same_17.value or bundle.ptag_same_18.value or bundle.ptag_same_19.value or bundle.ptag_same_20.value or bundle.ptag_same_21.value or bundle.ptag_same_22.value or bundle.ptag_same_23.value or bundle.ptag_same_24.value or bundle.ptag_same_25.value or bundle.ptag_same_26.value or bundle.ptag_same_27.value or bundle.ptag_same_28.value or bundle.ptag_same_29.value or bundle.ptag_same_30.value or bundle.ptag_same_31.value or bundle.ptag_same_32.value or bundle.ptag_same_33.value or bundle.ptag_same_34.value or bundle.ptag_same_35.value or bundle.ptag_same_36.value or bundle.ptag_same_37.value or bundle.ptag_same_38.value or bundle.ptag_same_39.value or bundle.ptag_same_40.value or bundle.ptag_same_41.value or bundle.ptag_same_42.value or bundle.ptag_same_43.value or bundle.ptag_same_44.value or bundle.ptag_same_45.value or bundle.ptag_same_46.value or bundle.ptag_same_47.value or bundle.ptag_same_48.value or bundle.ptag_same_49.value or bundle.ptag_same_50.value or bundle.ptag_same_51.value or bundle.ptag_same_52.value or bundle.ptag_same_53.value or bundle.ptag_same_54.value or bundle.ptag_same_55.value or bundle.ptag_same_56.value or bundle.ptag_same_57.value or bundle.ptag_same_58.value or bundle.ptag_same_59.value or bundle.ptag_same_60.value or bundle.ptag_same_61.value or bundle.ptag_same_62.value or bundle.ptag_same_63.value
_get_waymask_same = lambda bundle: bundle.entries_0_waymask_0.value==bundle.waymask.value or bundle.entries_0_waymask_1.value==bundle.waymask.value or bundle.entries_1_waymask_0.value==bundle.waymask.value or bundle.entries_1_waymask_1.value==bundle.waymask.value or bundle.entries_2_waymask_0.value==bundle.waymask.value or bundle.entries_2_waymask_1.value==bundle.waymask.value or bundle.entries_3_waymask_0.value==bundle.waymask.value or bundle.entries_3_waymask_1.value==bundle.waymask.value or bundle.entries_4_waymask_0.value==bundle.waymask.value or bundle.entries_4_waymask_1.value==bundle.waymask.value or bundle.entries_5_waymask_0.value==bundle.waymask.value or bundle.entries_5_waymask_1.value==bundle.waymask.value or bundle.entries_6_waymask_0.value==bundle.waymask.value or bundle.entries_6_waymask_1.value==bundle.waymask.value or bundle.entries_7_waymask_0.value==bundle.waymask.value or bundle.entries_7_waymask_1.value==bundle.waymask.value or bundle.entries_8_waymask_0.value==bundle.waymask.value or bundle.entries_8_waymask_1.value==bundle.waymask.value or bundle.entries_9_waymask_0.value==bundle.waymask.value or bundle.entries_9_waymask_1.value==bundle.waymask.value or bundle.entries_10_waymask_0.value==bundle.waymask.value or bundle.entries_10_waymask_1.value==bundle.waymask.value or bundle.entries_11_waymask_0.value==bundle.waymask.value or bundle.entries_11_waymask_1.value==bundle.waymask.value or bundle.entries_12_waymask_0.value==bundle.waymask.value or bundle.entries_12_waymask_1.value==bundle.waymask.value or bundle.entries_13_waymask_0.value==bundle.waymask.value or bundle.entries_13_waymask_1.value==bundle.waymask.value or bundle.entries_14_waymask_0.value==bundle.waymask.value or bundle.entries_14_waymask_1.value==bundle.waymask.value or bundle.entries_15_waymask_0.value==bundle.waymask.value or bundle.entries_15_waymask_1.value==bundle.waymask.value or bundle.entries_16_waymask_0.value==bundle.waymask.value or bundle.entries_16_waymask_1.value==bundle.waymask.value or bundle.entries_17_waymask_0.value==bundle.waymask.value or bundle.entries_17_waymask_1.value==bundle.waymask.value or bundle.entries_18_waymask_0.value==bundle.waymask.value or bundle.entries_18_waymask_1.value==bundle.waymask.value or bundle.entries_19_waymask_0.value==bundle.waymask.value or bundle.entries_19_waymask_1.value==bundle.waymask.value or bundle.entries_20_waymask_0.value==bundle.waymask.value or bundle.entries_20_waymask_1.value==bundle.waymask.value or bundle.entries_21_waymask_0.value==bundle.waymask.value or bundle.entries_21_waymask_1.value==bundle.waymask.value or bundle.entries_22_waymask_0.value==bundle.waymask.value or bundle.entries_22_waymask_1.value==bundle.waymask.value or bundle.entries_23_waymask_0.value==bundle.waymask.value or bundle.entries_23_waymask_1.value==bundle.waymask.value or bundle.entries_24_waymask_0.value==bundle.waymask.value or bundle.entries_24_waymask_1.value==bundle.waymask.value or bundle.entries_25_waymask_0.value==bundle.waymask.value or bundle.entries_25_waymask_1.value==bundle.waymask.value or bundle.entries_26_waymask_0.value==bundle.waymask.value or bundle.entries_26_waymask_1.value==bundle.waymask.value or bundle.entries_27_waymask_0.value==bundle.waymask.value or bundle.entries_27_waymask_1.value==bundle.waymask.value or bundle.entries_28_waymask_0.value==bundle.waymask.value or bundle.entries_28_waymask_1.value==bundle.waymask.value or bundle.entries_29_waymask_0.value==bundle.waymask.value or bundle.entries_29_waymask_1.value==bundle.waymask.value or bundle.entries_30_waymask_0.value==bundle.waymask.value or bundle.entries_30_waymask_1.value==bundle.waymask.value or bundle.entries_31_waymask_0.value==bundle.waymask.value or bundle.entries_31_waymask_1.value==bundle.waymask.value

def check_update_hit(bundle: WayLookupBundle) -> bool:
    return bundle.update_valid and _get_vset_same(bundle) and _get_ptag_same (bundle)
def check_update_miss(bundle: WayLookupBundle) -> bool:
    return bundle.update_valid and _get_vset_same(bundle) and _get_waymask_same(bundle) and (not _get_ptag_same(bundle))
def check_update_no(bundle:WayLookupBundle) -> bool:
    return bundle.update_valid and (not _get_vset_same(bundle))

def get_cover_group_update(bundle):
    group = fc.CovGroup("WayLookup_update")
    group.add_cover_point(
        bundle, {
            "update hit": check_update_hit,
            "update miss": check_update_miss,
            "update -not update": check_update_no
        }, name="update", once=False
    )
    group.mark_function("update", ["ut_frontend/icache/waylookup/test/waylookup_test.test_update_hit", "ut_frontend/icache/waylookup/test/waylookup_test.test_update_miss", "ut_frontend/icache/waylookup/test/waylookup_test.test_update_no", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    return group

# 读
def _get_entries_empty(bundle: WayLookupBundle):
    return (bundle.readPtr_value.value == bundle.writePtr_value.value) and (bundle.readPtr_flag.value == bundle.writePtr_flag.value)
def _get_entries_full(bundle: WayLookupBundle):
    return (bundle.readPtr_value.value == bundle.writePtr_value.value) and (bundle.readPtr_flag.value != bundle.writePtr_flag.value)

def check_read_bypass(bundle: WayLookupBundle):
    return bundle.read_ready.value and _get_entries_empty(bundle) and bundle.write_valid.value
def check_read_normal(bundle: WayLookupBundle):
    return bundle.read_ready.value and (not _get_entries_empty(bundle))
def check_read_fail(bundle: WayLookupBundle):
    return bundle.read_ready.value and _get_entries_empty(bundle) and (not bundle.write_valid.value)

def check_read_gpf_hit(bundle: WayLookupBundle):
    return (not check_read_fail(bundle)) and bundle.gpf_hit.value
def check_read_gpf_not_hit(bundle: WayLookupBundle):
    return (not check_read_fail(bundle)) and (not bundle.gpf_hit.value)

def get_cover_group_read(bundle: WayLookupBundle):
    group = fc.CovGroup("WayLookup_read")
    group.add_cover_point(
        bundle, {
            "read normal": check_read_normal,
            "read bypass": check_read_bypass,
            "read fail": check_read_fail,
        }, "read info", once=False
    )
    group.add_cover_point(
        bundle, {
            "read gpf hit": check_read_gpf_hit,
            "read gpf not-hit": check_read_gpf_not_hit,
        }, "read gpf info", once=False
    )
    group.mark_function("read info", ["ut_frontend/icache/waylookup/test/waylookup_test.test_read_write_normal", "ut_frontend/icache/waylookup/test/waylookup_test.test_read_empty", "ut_frontend/icache/waylookup/test/waylookup_test.test_read_bypass", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    group.mark_function("read gpf info", ["ut_frontend/icache/waylookup/test/waylookup_test.test_read_write_gpf_not_bypass", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    return group

# 写
def check_write_gpf_stop(bundle: WayLookupBundle):
    return bundle.write_valid.value and bundle.gpf_valid.value
def check_write_normal(bundle: WayLookupBundle):
    return bundle.write_valid.value and (not _get_entries_full(bundle)) and (not bundle.gpf_valid.value)
def check_write_fail(bundle: WayLookupBundle):
    return bundle.write_valid.value and _get_entries_full(bundle) and (not bundle.gpf_valid.value)

def check_write_gpf_bypass(bundle: WayLookupBundle):
    return bundle.write_valid.value and (bundle.write_itlb_exception_0.value==2 or bundle.write_itlb_exception_1.value==2) and bundle.read_ready.value
def check_write_gpf_not_bypass(bundle: WayLookupBundle):
    return bundle.write_valid.value and (bundle.write_itlb_exception_0.value==2 or bundle.write_itlb_exception_1.value==2) and (not bundle.read_ready.value)

def get_cover_group_write(bundle: WayLookupBundle):
    group = fc.CovGroup("WayLookup_write")
    group.add_cover_point(
        bundle, {
            "write normal": check_write_normal,
            "write gpf-stop": check_write_gpf_stop,
            "write fail": check_write_fail,
        }, "write info", once=False
    )
    group.add_cover_point(
        bundle, {
            "write gpf bypass": check_write_gpf_bypass,
            "write gpf normal": check_write_gpf_not_bypass,
        }, "write gpf info", once=False
    )
    group.mark_function("write info", ["ut_frontend/icache/waylookup/test/waylookup_test.test_read_write_normal", "ut_frontend/icache/waylookup/test/waylookup_test.test_write_gpf_valid", "ut_frontend/icache/waylookup/test/waylookup_test.test_write_full", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    group.mark_function("write gpf info", ["ut_frontend/icache/waylookup/test/waylookup_test.test_write_gpf_bypass", "ut_frontend/icache/waylookup/test/waylookup_test.test_read_write_gpf_not_bypass", "ut_frontend/icache/waylookup/test/waylookup_test.test_random"])
    return group
