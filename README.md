# Intelligent-task-offloading-in-private-5G-networks
Private 5G network using Open5GS and srsRAN with COTS devices (5G smartphones, laptops). Implements an Intelligent Task Offloading framework to dynamically route computation between UE, MEC, and Cloud for low-latency, high-throughput applications.

---

## 1. Introduction
In the rapidly evolving digital landscape, next-generation mobile networks are expected to support latency-sensitive and compute-intensive applications such as natural disaster response, autonomous vehicles, and industrial IoT systems like drones. Traditional cloud-based computing models often fail to meet these stringent real-time requirements due to latency from distant data centers and network congestion. To address these challenges, Intelligent Task Offloading has emerged as a pivotal approach, enabling dynamic and adaptive distribution of computational tasks across edge and cloud resources based on real-time conditions.

This work implements a real-world 5G-enabled intelligent task offloading system that autonomously decides whether to process data locally at the edge or remotely in the cloud. The system architecture leverages an Open5GS-based 5G core and srsRAN radio access stack, deployed on an edge server, with a USRP B210 software-defined radio acting as the base station. A mobile device connects to this private 5G network and offloads data depending on computational context. Central to this system is an AI-driven LSTM model that predicts future CPU usage on the edge node, enabling proactive decisions. When the predicted load surpasses a predefined threshold, tasks are seamlessly redirected to a cloud server hosted on an OpenStack virtual machine.

This intelligent approach ensures low latency and high availability. The system integrates real-time monitoring, predictive analytics, and virtualization to optimize task allocation based on factors like CPU load, memory, and disk utilization. This report details the design and implementation of the Smart Task Offloading system, emphasizing the role of AI in load prediction, orchestration across heterogeneous infrastructures, and performance metrics. The proposed solution presents a scalable, adaptive framework to meet the demands of modern mobile networks while maintaining optimal Quality of Service (QoS) and resource utilization.

---

## 2. Problem Statement

**  To develop an intelligent data offloading in edge computing environments to optimize resource allocation, reduce latency. **

Edge devices often face resource constraints and high latency due to inefficient task handling. Traditional offloading methods are not adaptive to changing network and resource conditions, leading to poor performance in real-time and latency-sensitive applications. To address this, there is a need for an intelligent task offloading system that can dynamically optimize resource allocation and reduce latency, ensuring efficient execution and improved quality of service in edge computing environments.

### 2.1 Objectives of Proposed Work
- Set up a private 5G network using Open5GS and srsRAN.
- Set up edge and cloud environments using Kubernetes and OpenStack respectively.
- Design an intelligent task offloading algorithm that dynamically allocates tasks between edge and cloud nodes based on real-time results and predicted resource utilization.
- Evaluate the model.

## 2.2 2.3 Hardware Minimum Requirements
- RAM: 32 GB
- Storage: 100 GB SSD or higher
- Processor: Multi-core CPU (Intel i7 or equivalent recommended)
- Base Station Hardware: USRP B210 Software Defined Radio

🫣 If you want you own private the cloud core then another device of same requirements is needed. We had used the servers for this purpose you can also opt to go with public cloud system but costs are applicable if not in free tier.

> 📒 More Detail refer our report (link of report).
---

## 3. System Design

<p align="center">
  <img src="./images/systemDesign.png" alt="image">
</p>

- User Equipment (UE) Layer: This layer consists of mobile devices (UEs) connected wirelessly via a 5G network. Communication is facilitated by a USRP B210 software-defined radio acting as the base station, which forms the Radio Access Network (RAN). These devices offload computation-intensive tasks to the network for processing.


## Total Work Flow
1. User connects Private 5G network
2. User request to schedular `10.45.0.1:5001/predict` endpoint at the edge core (Kubernetes).
3. Schedular forword request to one of the selected node
    - Schedular for every 30 seconds requests the metrics such as CPU,MEMORY Utilization from the edge nodes
    - It predicts the future load of each node and select a best node that is below threshold value we had set during deployment.
    - If no edge node is availble below threshold value it forwards the request to cloud core (Openstack) deployed in remote server.
4. The Edge core or cloud core process the image and return the results to the user and send the processed data to the storage node in cloud core for future use.

<p align="center">
  <img src="./images/workFlow.png" alt="image">
</p>
