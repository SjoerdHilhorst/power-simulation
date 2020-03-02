from datetime import datetime

# Battery Data:


battery_id = "GREENER_001"    # str     config
soc = 0                       # float   dep
active_power_in = 0           # float   in
reactive_power_in = 0         # float   in
current_l1_in = 0             # float   dep
current_l2_in = 0             # float   dep
current_l3_in = 0             # float   dep
voltage_l1_l2_in = 0          # float   semi
voltage_l2_l3_in = 0          # float   semi
voltage_l3_l1_in = 0          # float   semi
frequency_in = 0              # float   semi
active_power_out = 0          # float   in
reactive_power_out = 0        # float   in
current_l1_out = 0            # float   dep
current_l2_out = 0            # float   dep
current_l3_out = 0            # float   dep
voltage_l1_l2_out = 0         # float   semi
voltage_l2_l3_out = 0         # float   semi
voltage_l3_l1_out = 0         # float   semi
frequency_out = 0             # float   semi
active_power_converter = 0    # float   dep
reactive_power_converter = 0  # float   dep


# Battery State

time = datetime.now()
system_status = 0             # int    const
system_mode = 0               # int    const
accept_values = 0             # bool   const
converter_started = 0         # bool   in
input_connected = 0           # bool   in
system_on_backup_battery = 0  # bool   in

# Enumerations

off = 0
on = 1
busy = 2
wait_for_reset = 3
suspended = 4
reset_busy = 5
starting_up = 6

statuses = {"OFF": off,
            "ON": on,
            "BUSY": busy,
            "WAIT FOR RESET": wait_for_reset,
            "SUSPENDED": suspended,
            "RESET BUSY": reset_busy,
            "STARTING UP": starting_up}

standby = 0
P_Q = 1
Pf = 2
Pf_QU = 3
Pf_QU_and_P_Q = 4
peakshaving = 5
gen_micro_grid = 6

modes = {"Standby": standby,
         "P/Q": P_Q,
         "P(f)": Pf,
         "P(f)/Q(U)": Pf_QU,
         "P(f)/Q(U) & PQ": Pf_QU_and_P_Q,
         "Peakshaving": peakshaving,
         "Generic micro-grid": gen_micro_grid}