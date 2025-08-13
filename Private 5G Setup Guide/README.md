# Private-5g
Setting up a real time 5g network using **Open5gs** as core and **srsRAN** as RAN which is connected to real 5G COTS Devices (**5G Mobiles**) using **USRP B210** as BASE Satation


📡 Private 5G Network Setup
This repository documents the end-to-end setup of a real-time 5G network using:

Open5GS as the 5G Core

srsRAN as the Radio Access Network (RAN)

USRP B210 as the base station hardware

Connected to Commercial Off-The-Shelf (COTS) 5G devices (smartphones)

✅ Fully tested with Samsung S23 and OPPO Reno 5G using OpenCell SIM cards.




## Reqiurements
```
- ubuntu 22.04 LTS 
- USRP B210
- Opencell SIM
- COTS UE (Samsung s23, OPPO Reno 5G used in our setup)
```

#### Tip: USE UBUNTU IN HOST WITHOUT CREATING VM. (Ex: USE DUAL BOOT) 

## The steps are mentioned in above [/Steps-1-7 ](https://github.com/ManojPandekamat/Private-5g-setup-with-Open5gs-and-srsRAN-and-B210/tree/main/Steps-1-7) folder
## Go through the following steps for complete set-up
```
  1. Open5gs setup.
  2. uhd drivers installation for connecting B210 with the srsRAN.
  3. srsRAN setup.
  4. Creating User in Open5gs from Open5gs webUI
  5. Writing the sim (Opencells SIM card).
  6. Configuring COTS UE (5G Mobile Phone).
  7. Checking connectivity. 
```
