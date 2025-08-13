# 📡 Private 5G Network Setup

This repository documents the **end-to-end setup** of a real-time 5G network using:

- **Open5GS** as the 5G Core  
- **srsRAN** as the Radio Access Network (RAN)  
- **USRP B210** as the base station hardware  
- Connected to **Commercial Off-The-Shelf (COTS)** 5G devices (smartphones)  

✅ Fully tested with **Samsung S23** and **OPPO Reno 5G** using **OpenCell SIM cards**.


## 🛠 Requirements

| Component       | Purpose |
|-----------------|---------|
| **Ubuntu 22.04 LTS** | Operating system for running Open5GS & srsRAN |
| **USRP B210**   | Software-defined radio hardware acting as the 5G base station |
| **OpenCell SIM** | SIM cards for registering UEs with the 5G core |
| **COTS UE**     | 5G smartphones for testing connectivity |

💡 **Tip:** Install Ubuntu on bare metal (dual boot recommended) instead of using a virtual machine for better hardware performance and less probability of the errors.


## 🚀 Setup Guide

Follow the steps in the [`Steps-1-7`](./Steps-1-7) folder for a detailed walk-through.

### High-Level Process

1. **Open5GS Setup** – Install and configure the 5G Core network.
2. **UHD Drivers Installation** – Set up USRP B210 drivers for hardware communication.
3. **srsRAN Setup** – Configure the Radio Access Network.
4. **Open5GS WebUI User Creation** – Register UE subscribers in the 5G Core.
5. **SIM Writing** – Program OpenCell SIM cards with matching IMSI & keys.
6. **COTS UE Configuration** – Configure mobile phones for private 5G connection.
7. **Connectivity Test** – Verify registration, attach procedure, and data transfer.

