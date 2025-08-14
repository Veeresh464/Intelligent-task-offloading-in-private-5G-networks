# Intelligent-task-offloading-in-private-5G-networks
Private 5G network using Open5GS and srsRAN with COTS devices (5G smartphones, laptops). Implements an Intelligent Task Offloading framework to dynamically route computation between UE, MEC, and Cloud for low-latency, high-throughput applications.

---
**Total Work Flow**
1. User connects Private 5G network
2. User request to schedular `10.45.0.1:5001/predict` endpoint at the edge core (Kubernetes).
3. Schedular forword request to one of the selected node
    - Schedular for every 30 seconds requests the metrics such as CPU,MEMORY Utilization from the edge nodes
    - It predicts the future load of each node and select a best node that is below threshold value we had set during deployment.
    - If no edge node is availble below threshold value it forwards the request to cloud core (Openstack) deployed in remote server.
4. The Edge core or cloud core process the image and return the results to the user and send the processed data to the storage node in cloud core for future use.
