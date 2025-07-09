
# 📡 Cisco Packet Tracer Topology Documentation

## 📝 Topology Overview

This network topology represents a multi-router hierarchical design, connecting different network segments through various routers and switches. It includes multiple PCs grouped by network sections (A, B, C, D), interconnected via Cisco 2911 Routers and 2960 Switches.

---

## 🖼️ Topology Diagram

<img width="1174" height="479" alt="Image" src="https://github.com/user-attachments/assets/a81497d9-97b3-41cf-9f34-ccefd87a41f5" />

## 🖧 Network Devices

### Routers
- **Router0**: Connects to Switch0 and Router1
- **Router1**: Central router, connected to Router0, Switch3, and Router2
- **Router2**: Connects to Switch1 and Switch2, and Router1

### Switches
- **Switch0 (2960-24TT)**: Connects to PCA-1 and PCA-2
- **Switch1 (2960-24TT)**: Connects to PCB-1 and PCB-2
- **Switch2 (2960-24TT)**: Connects to PCC-1, PCC-1(1), and PCC-1(2)
- **Switch3 (2960-24TT)**: Connects to PCD-1

---

## 🖥️ End Devices

### Group A
- **PC A-1**
- **PC A-2**

### Group B
- **PC B-1**
- **PC B-2**

### Group C
- **PC C-1**
- **PC C-1(1)**
- **PC C-1(2)**

### Group D
- **PC D-1**

---

## 🌐 IP Addressing Scheme

| Network | Devices             | Subnet           | Gateway IP       |
|---------|---------------------|------------------|------------------|
| Net A   | PC A-1, A-2         | 192.168.1.0/24   | 192.168.1.1      |
| Net D   | PC D-1              | 192.168.4.0/24   | 192.168.4.1      |
| Net B   | PC B-1, B-2         | 192.168.2.0/24   | 192.168.2.1      |
| Net C   | PC C-1, C-1(1), C-1(2) | 192.168.3.0/24 | 192.168.3.1      |

| Inter-router Links | Subnet         |
|--------------------|----------------|
| Router0–Router1    | 10.0.0.0/30    |
| Router1–Router2    | 10.0.0.4/30    |

---

## 🔁 Interconnection Summary

| Device        | Connected To              |
|---------------|---------------------------|
| PC A-1, A-2    | Switch0                   |
| Switch0        | Router0                   |
| Router0        | Router1                   |
| PC D-1         | Switch3                   |
| Switch3        | Router1                   |
| Router1        | Router2                   |
| PC B-1, B-2    | Switch1                   |
| Switch1        | Router2                   |
| PC C-1, C-1(1), C-1(2) | Switch2          |
| Switch2        | Router2                   |

---

## 🔧 Router Configurations

### 🚦 Router0

```bash
enable
conf t

hostname Router0

interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown

exit

ip route 192.168.2.0 255.255.255.0 10.0.0.2
ip route 192.168.3.0 255.255.255.0 10.0.0.2
ip route 192.168.4.0 255.255.255.0 10.0.0.2

end
````

---

### 🚦 Router1

```bash
enable
conf t

hostname Router1

interface GigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 ip address 10.0.0.5 255.255.255.252
 no shutdown

interface GigabitEthernet0/2
 ip address 192.168.4.1 255.255.255.0
 no shutdown

exit

ip route 192.168.1.0 255.255.255.0 10.0.0.1
ip route 192.168.2.0 255.255.255.0 10.0.0.6
ip route 192.168.3.0 255.255.255.0 10.0.0.6

end
```

---

### 🚦 Router2

```bash
enable
conf terminal

hostname Router2

interface GigabitEthernet0/0
 ip address 10.0.0.6 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown

interface GigabitEthernet0/2
 ip address 192.168.3.1 255.255.255.0
 no shutdown

exit

ip route 192.168.1.0 255.255.255.0 10.0.0.5
ip route 192.168.4.0 255.255.255.0 10.0.0.5

end
```

---

## ✅ Testing & Verification

* **IP Addressing**: Assign IPs to PCs in the correct subnet.
* **Default Gateway**: Set each PC’s gateway to the router IP of the corresponding subnet.
* **Ping Test**: Between all PCs to ensure end-to-end communication.
* **Traceroute**: To verify the routing path.
* **Simulation Mode**: Check packet flow using simulation mode in Packet Tracer.

---


