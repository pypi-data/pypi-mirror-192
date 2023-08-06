# Copyright 2021-2023 Datum Technology Corporation
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
########################################################################################################################


from mio import cache
from mio import common
from mio import cfg
from mio import cov
from mio import dox
from mio import results
from mio import sim

import os


def main(ip_str, deep_clean):
    vendor, name = common.parse_dep(ip_str)
    if vendor == "":
        ip = cache.get_anon_ip(name, True)
    else:
        ip = cache.get_ip(vendor, name, True)
    if deep_clean:
        common.banner(f"Deep cleaning IP '{ip.vendor}/{ip.name}'")
        for dep in ip.dependencies:
            dep_ip = cache.get_ip(dep.vendor, dep.target_ip)
            if dep_ip == None:
                common.dbg(f"Cannot find Dependency IP '{dep.vendor}/{dep.target_ip}'")
            else:
                clean_ip(dep_ip)
    else:
        common.banner(f"Cleaning IP '{ip.vendor}/{ip.name}'")
    clean_ip(ip)
    
    if ip.has_dut:
        if ip.dut_ip_type == "fsoc":
            core = cache.get_core(ip.dut_fsoc_full_name)
            if core == None:
                common.fatal(f"Cannot find DUT FuseSoC Core '{ip.dut_fsoc_full_name}'")
            clean_core(core)
        else:
            dut_ip = cache.get_ip(ip.dut.vendor, ip.dut.target_ip)
            if dut_ip == None:
                common.fatal(f"Cannot find DUT IP '{ip.dut.vendor}/{ip.dut.target_ip}'")
            clean_ip(dut_ip)


def clean_core(core):
    common.info(f"Deleting code and compiled code objects for FuseSoC core '{core.sname}'")
    common.remove_dir(cfg.sim_output_dir + '/viv/sim_wd/@fsoc__' + core.sname)
    common.remove_dir(cfg.sim_output_dir + '/vcs/sim_wd/@fsoc__' + core.sname)
    common.remove_dir(cfg.sim_output_dir + '/xcl/sim_wd/@fsoc__' + core.sname)
    common.remove_dir(cfg.sim_output_dir + '/qst/sim_wd/@fsoc__' + core.sname)
    common.remove_dir(cfg.sim_output_dir + '/riv/sim_wd/@fsoc__' + core.sname)
    common.remove_dir(cfg.fsoc_dir + "/" + core.sname)
    core.is_installed = False


def clean_ip(ip, no_infos=False):
    if ip.name == "uvm":
        return
    
    ip_str = f"{ip.vendor}/{ip.name}"
    ip_dir_name = f"{ip.vendor}__{ip.name}"
    
    common.remove_dir(cfg.sim_output_dir + '/viv/sim_wd')
    common.remove_dir(cfg.sim_output_dir + '/vcs/sim_wd')
    common.remove_dir(cfg.sim_output_dir + '/xcl/sim_wd')
    common.remove_dir(cfg.sim_output_dir + '/qst/sim_wd')
    common.remove_dir(cfg.sim_output_dir + '/riv/sim_wd')
    
    common.remove_dir(cfg.sim_output_dir + '/viv/cmp_out/' + ip_dir_name)
    common.remove_dir(cfg.sim_output_dir + '/vcs/cmp_out/' + ip_dir_name)
    common.remove_dir(cfg.sim_output_dir + '/xcl/cmp_out/' + ip_dir_name)
    common.remove_dir(cfg.sim_output_dir + '/qst/cmp_out/' + ip_dir_name)
    
    #common.remove_dir(cfg.sim_output_dir + '/viv/regr_wd/' + ip_dir_name)
    #common.remove_dir(cfg.sim_output_dir + '/mdc/regr_wd/' + ip_dir_name)
    #common.remove_dir(cfg.sim_output_dir + '/vcs/regr_wd/' + ip_dir_name)
    #common.remove_dir(cfg.sim_output_dir + '/xcl/regr_wd/' + ip_dir_name)
    #common.remove_dir(cfg.sim_output_dir + '/qst/regr_wd/' + ip_dir_name)
    
    if ip.is_local:
        if no_infos:
            common.dbg(f"Deleting compiled code objects for local IP '{ip_str}'")
        else:
            common.info(f"Deleting compiled code objects for local IP '{ip_str}'")
    else:
        if no_infos:
            common.dbg(f"Deleting compiled code objects for external IP '{ip_str}'")
        else:
            common.info(f"Deleting compiled code objects for external IP '{ip_str}'")
    ip.is_compiled  [common.simulators_enum.VIVADO ] = False
    ip.is_compiled  [common.simulators_enum.METRICS] = False
    ip.is_compiled  [common.simulators_enum.VCS    ] = False
    ip.is_compiled  [common.simulators_enum.XCELIUM] = False
    ip.is_compiled  [common.simulators_enum.QUESTA ] = False
    ip.is_compiled  [common.simulators_enum.RIVIERA] = False
    ip.is_elaborated[common.simulators_enum.VIVADO ] = False
    ip.is_elaborated[common.simulators_enum.METRICS] = False
    ip.is_elaborated[common.simulators_enum.VCS    ] = False
    ip.is_elaborated[common.simulators_enum.XCELIUM] = False
    ip.is_elaborated[common.simulators_enum.QUESTA ] = False
    ip.is_elaborated[common.simulators_enum.RIVIERA] = False
    
