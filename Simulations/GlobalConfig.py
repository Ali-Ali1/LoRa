import numpy as np
from Framework.MessagePacket import MessagePacket
############### SIMULATION SPECIFIC PARAMETERS ###############
start_with_fixed_sf = False
start_sf = 7

scaling_factor = 0.1
transmission_rate_id = str(scaling_factor)
transmission_rate_bit_per_ms = scaling_factor*(12*8)/(60*60*1000)  # 12*8 bits per hour (1 typical packet per hour)
simulation_time = 24 * 60 * 60 * 1000 * 30/scaling_factor # 30 days
cell_size = 1
adr = True
confirmed_messages = True
messages = MessagePacket.message_packets
messages_num = MessagePacket.packets # Num of custom messages/Packets
#payload_sizes = range(0, messages_num, 1) # Payload Size set to num of custom messages, can also pick a random range
payload_sizes = range(5, 55, 5) # Random payload size
path_loss_variances = [7.9]  # [0, 5, 7.8, 15, 20]

MAC_IMPROVEMENT = False
num_locations = 10
num_of_simulations = 1
locations_file = "locations/"+"{}_locations_{}_sim.pkl".format(num_locations, num_of_simulations)
results_file = "results/{}_{}_{}_cnst_num_bytes.p".format(adr, confirmed_messages, transmission_rate_id)

############### SIMULATION SPECIFIC PARAMETERS ###############

############### DEFAULT PARAMETERS ###############
LOG_ENABLED = True
MAX_DELAY_BEFORE_SLEEP_MS = 500
PRINT_ENABLED = True
MAX_DELAY_START_PER_NODE_MS = np.round(simulation_time / 10)
track_changes = True
middle = np.round(cell_size / 2)
load_prev_simulation_results = True

############### DEFAULT PARAMETERS ###############
