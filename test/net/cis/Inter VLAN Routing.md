# Inter-VLAN Routing (Cisco Packet Tracer Project)

This project demonstrates the setup and configuration of Inter-VLAN Routing using a Layer 3 router or a Layer 3 switch in **Cisco Packet Tracer**. It allows different VLANs to communicate with each other through proper interface configuration and IP addressing.

## 📁 Project File

- File: `Inter VLAN Routing.pkt`
- Software: Cisco Packet Tracer

## 🎯 Objectives

- Create multiple VLANs and assign ports accordingly.
- Configure VLAN interfaces and assign IP addresses.
- Enable Inter-VLAN communication using:
  - Router-on-a-Stick (if using a router)
  - Switch Virtual Interfaces (SVIs) (if using a Layer 3 switch)
- Verify connectivity between VLANs via ping tests.

## 🛠️ Requirements

- Cisco Packet Tracer (version 7.0 or above recommended)
- Basic knowledge of VLANs and subnetting
- Devices used:
  - One or more switches
  - One router or Layer 3 switch
  - Multiple end devices (PCs)
- Appropriate IP addressing scheme for each VLAN

## 🧑‍💻 Configuration Steps

1. **Create VLANs:**
   ```bash
   Switch> enable
   Switch# configure terminal
   Switch(config)# vlan 10
   Switch(config-vlan)# name vlan-A
   Switch(config)# vlan 20
   Switch(config-vlan)# name vlan-B
   Switch(config)# vlan 30
   Switch(config-vlan)# name vlan-C
   ```

2. **Assign VLANs to ports:**
   ```bash
   Switch(config)# interface fastethernet 0/1
   Switch(config-if)# switchport mode access
   Switch(config-if)# switchport access vlan 10
   ```

3. **Configure Router-on-a-Stick or SVIs:**
   - For Router-on-a-Stick:
     ```bash
     Router(config)# interface fastethernet 0/0.10
     Router(config-subif)# encapsulation dot1Q 10
     Router(config-subif)# ip address 192.168.10.1 255.255.255.0
     ```
   - For SVI on Layer 3 Switch:
     ```bash
     Switch(config)# interface vlan 10
     Switch(config-if)# ip address 192.168.10.1 255.255.255.0
     Switch(config-if)# no shutdown
     ```

4. **Assign IP addresses to PCs and set default gateways.**

5. **Test connectivity using `ping` across VLANs.**

## ✅ Verification

Use the following commands to verify configuration:

- `show vlan brief`
- `show ip interface brief`
- `ping <destination-ip>`

## 📸 Screenshots 

![Image](https://github.com/user-attachments/assets/c8d3726b-8695-402e-b6eb-2bde29a54f49)


## 🧠 Author / Credits

Prepared by: Md. Nazmul Hasan <br>
Institution: University of Rajshahi <br>
Course: Computer Networks Lab
