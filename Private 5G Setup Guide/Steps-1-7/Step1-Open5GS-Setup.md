# 📡 Step 1 – Open5GS Setup

This step covers the installation and configuration **Open5GS** for a private 5G setup.

---

## 1️⃣ Installing MongoDB
```bash
sudo apt update
sudo apt install gnupg
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```


## 2️⃣ Installing Open5GS
```bash
sudo add-apt-repository ppa:open5gs/latest
sudo apt update
sudo apt install open5gs
```



## 3️⃣ Installing Node.js (for WebUI)
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# Create deb repository
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list

# Install Node.js
sudo apt update
sudo apt install nodejs -y
```


## 4️⃣ Installing Open5GS WebUI
```bash
curl -fsSL https://open5gs.org/open5gs/assets/webui/install | sudo -E bash -
```



## ⚙️ Configuration for srsRAN Compatibility
### 💡 TIP
- **Single Node Setup** (srsGNB and Open5gs on the same PC)  
  No change in IP address required — just change the **MCC** and **MNC** code.
- **Multi-Node Setup** (srsGNB and Open5gs on different PCs)  
  Change the IP address where highlighted in image to IP address of Machine (where you have installed the open5Gs) and **MCC** and **MNC** code.



