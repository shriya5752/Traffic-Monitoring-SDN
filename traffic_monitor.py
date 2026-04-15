from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class TrafficMonitor(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        log.info("Packet in from %s", packet.src)

        # Learn MAC
        self.mac_to_port[packet.src] = in_port

        # Decide output port
        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
        else:
            out_port = of.OFPP_FLOOD

        # Install flow rule (THIS FIXES SPAM)
        if out_port != of.OFPP_FLOOD:
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.actions.append(of.ofp_action_output(port=out_port))
            self.connection.send(msg)

        # Send packet
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)

    def _handle_ConnectionUp(self, event):
        log.info("Switch connected")

        # Request stats periodically
        import threading, time

        def stats_loop():
            while True:
                for conn in core.openflow.connections:
                    conn.send(of.ofp_stats_request(
                        body=of.ofp_flow_stats_request()))
                time.sleep(5)

        thread = threading.Thread(target=stats_loop)
        thread.daemon = True
        thread.start()

    def _handle_FlowStatsReceived(self, event):
        log.info("Flow Stats Received:")
        for stat in event.stats:
            log.info("Packets=%s Bytes=%s",
                     stat.packet_count,
                     stat.byte_count)


def launch():
    def start_switch(event):
        TrafficMonitor(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
