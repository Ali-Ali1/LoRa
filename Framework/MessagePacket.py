class MessagePacket:
    def __init__(self, message_as_packet):
        self.message_as_packet = message_as_packet
        self.payload_size = len(message_as_packet)