**Cisco Packet Tracer VLAN and Trunk Configuration**

### **1. Configure VLANs**

1. Enter global configuration mode:
   ```
   enable
   configure terminal
   ```
2. Set hostname:
   ```
   hostname Network_Lab
   ```
3. Create VLANs:
   ```
   vlan 10
   name Grpup-1
   exit

   vlan 20
   name Grpup-2
   exit
   ```

### **2. Assign Ports to VLANs**

- Assign **FastEthernet0/1** to VLAN 10:
  ```
  interface FastEthernet0/1
  switchport mode access
  switchport access vlan 10
  exit
  ```
- Assign **FastEthernet0/2** to VLAN 20:
  ```
  interface FastEthernet0/2
  switchport mode access
  switchport access vlan 20
  exit
  ```

### **3. Configure Trunk Port**

- Set **FastEthernet0/24** as trunk:
  ```
  interface FastEthernet0/24
  switchport mode trunk
  switchport trunk allowed vlan 10,20
  exit
  ```

### **4. Save Configuration**

- Save the configuration:
  ```
  copy running-config startup-config

  do write memory
  ```

### **5. Verify Configuration**

- Check VLAN assignments:
  ```
  show vlan brief
  ```
- Check trunk ports:
  ```
  show interfaces trunk
  ```

