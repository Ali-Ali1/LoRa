import simpy
from math import sqrt
from Framework import PropagationModel
from Framework.AirInterface import AirInterface
from Framework.EnergyProfile import EnergyProfile
from Framework.Gateway import Gateway
from Framework.MessagePacket import MessagePacket
from Framework.LoRaParameters import LoRaParameters
from Framework.Node import Node
from Framework.SNRModel import SNRModel
from Simulations.GlobalConfig import *
from Framework.Router import Router




tx_power_mW = {2: 91.8, 5: 95.9, 8: 101.6, 11: 120.8, 14: 146.5}
rx_measurements = {'pre_mW': 8.2, 'pre_ms': 3.4, 'rx_lna_on_mW': 39,
                   'rx_lna_off_mW': 34,
                   'post_mW': 8.3, 'post_ms': 10.7}


def run_helper(args):
    return run(*args)


def run(message_packet, locs, p_size, sigma, sim_time, gateway_location, num_nodes, num_routers,transmission_rate, confirmed_messages, adr):
    sim_env = simpy.Environment()
    gateway = Gateway(sim_env, gateway_location, max_snr_adr=True, avg_snr_adr=False)
    nodes = []
    routers = []
    node_coordinates = {}
    router_coordinates = {}
    # {router_A: [6,12]}
    air_interface = AirInterface(gateway, PropagationModel.LogShadow(std=sigma), SNRModel(), sim_env)


    # for router_id in range(num_routers):
    #     energy_profile = EnergyProfile(5.7e-3, 15, tx_power_mW,
    #                                    rx_power=rx_measurements)
    #
    #
    #     _sf = np.random.choice(LoRaParameters.SPREADING_FACTORS)
    #     if start_with_fixed_sf:
    #         _sf = start_sf
    #     lora_param = LoRaParameters(freq=np.random.choice(LoRaParameters.DEFAULT_CHANNELS),
    #                                 sf=_sf,
    #                                 bw=125, cr=5, crc_enabled=1, de_enabled=0, header_implicit_mode=0, tp=14)
    #     router = Router(message_packet, router_id, energy_profile, lora_param, sleep_time=(8 * p_size / transmission_rate),
    #                 processs_time=5,
    #                 adr=adr,
    #                 location=locs[router_id],
    #                 base_station=gateway, env=sim_env, payload_size= p_size, coordinates=[0, 0], air_interface=air_interface,
    #                 confirmed_messages=confirmed_messages)
    #     routers.append(router)
    #     router_coordinates[router_id] = router.coordinates
    #     sim_env.process(router.run())


    for node_id in range(10):
        energy_profile = EnergyProfile(5.7e-3, 15, tx_power_mW,
                                       rx_power=rx_measurements)


        _sf = np.random.choice(LoRaParameters.SPREADING_FACTORS)
        if start_with_fixed_sf:
            _sf = start_sf
        lora_param = LoRaParameters(freq=np.random.choice(LoRaParameters.DEFAULT_CHANNELS),
                                    sf=_sf,
                                    bw=125, cr=5, crc_enabled=1, de_enabled=0, header_implicit_mode=0, tp=14)
        node = Node(message_packet, node_id, energy_profile, lora_param, sleep_time=(8 * p_size / transmission_rate),
                    process_time=5,
                    adr=adr,
                    location=locs[node_id],
                    base_station=gateway, env=sim_env, payload_size= p_size, coordinates=[0, 0], air_interface=air_interface,
                    confirmed_messages=confirmed_messages)
        nodes.append(node)
        node_coordinates[node_id] = node.coordinates
        sim_env.process(node.run())

        # def closest_router():
        #     distances = []
        #
        #     for key, value in router_coordinates.items():
        #         dist = sqrt((router_coordinates[key][0] - node.coordinates[0])**2 + (router_coordinates[key][1] - node.coordinates[1])**2)
        #         distances.append(dist)
        #     distances.sort()
        #     node.base_station = 0
        # closest_router()

    sim_env.run(until=sim_time)

    # Simulation is done.
    # process data

    mean_energy_per_bit_list = list()
    for n in nodes:
        mean_energy_per_bit_list.append(n.energy_per_bit())

    data_mean_nodes = Node.get_mean_simulation_data_frame(nodes, name=sigma) / (
        num_nodes)

    data_gateway = gateway.get_simulation_data(name=sigma) / num_nodes
    data_air_interface = air_interface.get_simulation_data(name=sigma) / (
        num_nodes)

    # eff_en = data_mean_nodes['TotalEnergy'][sigma] / (p_size*data_mean_nodes['UniquePackets'][sigma])
    # print('Eb {} for Size:{} and Sigma:{}'.format(eff_en, p_size, sigma))

    return {
        'message_as_packet': MessagePacket.message_packets,
        'Custom Payload': MessagePacket.packets,
        'mean_nodes': data_mean_nodes,
        'gateway': data_gateway,
        'air_interface': data_air_interface,
        'path_loss_std': sigma,
        'payload_size': p_size,
        'mean_energy_all_nodes': mean_energy_per_bit_list

    }
