set serialnumber [lindex $::argv 0]
set devicename  [lindex $::argv 1]
set configurationfile [lindex $::argv 2]
set initializationpdi [lindex $::argv 3]

# Connect to the device
open_hw_manager
connect_hw_server -url localhost:3121 -allow_non_jtag
current_hw_target [get_hw_targets */xilinx_tcf/Xilinx/${serialnumber}]
set_property PARAM.FREQUENCY 15000000 [get_hw_targets */xilinx_tcf/Xilinx/${serialnumber}]
open_hw_target
current_hw_device [get_hw_devices ${devicename}]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices ${devicename}] 0]

# Configure FPT flash
create_hw_cfgmem -hw_device [lindex [get_hw_devices ${devicename}] 0] [lindex [get_cfgmem_parts {cfgmem-2048-ospi-x8-single}] 0]
set_property PROGRAM.BLANK_CHECK  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.ERASE  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.CFG_PROGRAM  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.VERIFY  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.CHECKSUM  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
refresh_hw_device [lindex [get_hw_devices ${devicename}] 0]

# Write Configuration file to flash
set_property PROGRAM.ADDRESS_RANGE  {entire_device} [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.FILES [list "/opt/amd/aved/amd_v80_gen5x8_24.1_xbtest_stress_20241002/flash_setup/fpt_setup_amd_v80_gen5x8_24.1_20241002.pdi" ] [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]

# Write Initialization PDI
set_property PROGRAM.FILE {/opt/amd/aved/amd_v80_gen5x8_24.1_xbtest_stress_20241002/flash_setup/v80_initialization.pdi} [get_hw_devices ${devicename}]
set_property PROGRAM.BLANK_CHECK  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.ERASE  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.CFG_PROGRAM  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.VERIFY  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
set_property PROGRAM.CHECKSUM  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]

startgroup
 program_hw_devices [lindex [get_hw_devices ${devicename}] 0]
 refresh_hw_device [lindex [get_hw_devices ${devicename}] 0]
 program_hw_cfgmem -hw_cfgmem [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${devicename}] 0]]
endgroup
