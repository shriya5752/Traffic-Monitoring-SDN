# SDN Traffic Monitoring using POX and Mininet

A Software Defined Networking (SDN) based traffic monitoring system built with the POX controller and Mininet. Collects real-time flow statistics — packet count and byte count — via OpenFlow.

---

## Tech Stack

| Tool | Role |
|------|------|
| [Mininet](http://mininet.org/) | Network emulator |
| [POX Controller](https://github.com/noxrepo/pox) | SDN controller |
| OpenFlow | Controller-switch communication protocol |
| Python | Controller logic |

---

## Setup

### Prerequisites

- Linux (Ubuntu recommended)
- Mininet installed
- POX cloned locally

### 1. Start the POX Controller

```bash
python3 pox.py misc.traffic_monitor
```

### 2. Start Mininet Topology

In a separate terminal:

```bash
sudo mn --topo single,3 --controller remote
```

---

## Running the Experiment

Inside the Mininet CLI, run:

```bash
# Test connectivity
pingall

# Generate continuous traffic
h1 ping h2
```

Monitor the POX controller terminal for:
- `packet_in` events from switches
- Periodic flow statistics (packet count, byte count)

---

## Sample Output

```
[INFO] Flow stats received from switch
Packets=27  Bytes=2646
Packets=22  Bytes=2156
```

---

## Test Cases

**Test 1 — Normal Traffic**
- Host-to-host communication (`h1 → h2`) works without packet loss
- Ping packets are transmitted successfully

**Test 2 — Traffic Monitoring**
- Flow statistics are collected and logged by the controller
- Packet and byte counts increase proportionally with traffic

---

## Key Concepts Demonstrated

- SDN architecture and controller-switch separation
- OpenFlow protocol for flow rule installation
- Dynamic flow management based on packet-in events
- Real-time network monitoring via flow statistics

---

## Project Structure

```
.
├── pox/
│   └── misc/
│       └── traffic_monitor.py   # Custom POX component
└── README.md
```

---

## References

- [POX Documentation](https://noxrepo.github.io/pox-doc/html/)
- [Mininet Walkthrough](http://mininet.org/walkthrough/)
- [OpenFlow Spec](https://opennetworking.org/sdn-resources/openflow/)
