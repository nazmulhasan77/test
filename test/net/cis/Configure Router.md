# Cisco Router Initial Configuration - CISCO2911/K9

## Device Information
- **Model:** Cisco CISCO2911/K9 (revision 1.0)
- **Memory:** 491520K/32768K bytes
- **Processor Board ID:** FTX152400KS
- **Interfaces:** 3 Gigabit Ethernet
- **Non-Volatile Configuration Memory:** 255K bytes
- **System CompactFlash:** 249856K bytes

---

## Configuration Steps

### 1. Entering Privileged EXEC Mode
```shell
Router> enable
Router# configure terminal
```

### 2. Setting Hostname
```shell
Router(config)# hostname CSER1
```

### 3. Configuring Interface GigabitEthernet0/0
```shell
CSER1(config)# interface gigabitEthernet 0/0
CSER1(config-if)# ip address 192.168.5.1 255.255.255.0
CSER1(config-if)# no shutdown
CSER1(config-if)# exit
```

> ✅ **Status:**
> - Interface GigabitEthernet0/0 changed state to **up**
> - Line protocol on GigabitEthernet0/0 changed state to **up**

---

### 4. Configuring Interface GigabitEthernet0/1
```shell
CSER1(config)# interface gigabitEthernet 0/1
CSER1(config-if)# ip address 192.168.10.1 255.255.255.0
CSER1(config-if)# exit
```

> ✅ **Status:**
> - Interface GigabitEthernet0/1 changed state to **up**
> - Line protocol on GigabitEthernet0/1 changed state to **up**

---

## Notes
- Interfaces successfully activated and assigned IP addresses.

---

## Summary of Interfaces

| Interface              | IP Address      | Subnet Mask       | Status |
|------------------------|------------------|--------------------|--------|
| GigabitEthernet0/0     | 192.168.5.1       | 255.255.255.0      | up     |
| GigabitEthernet0/1     | 192.168.10.1      | 255.255.255.0      | up     |