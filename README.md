# 🔄 ARP Spoofing Tool

This tool implements an ARP spoofing (man-in-the-middle) attack that allows you to intercept network traffic between two hosts on a local network.

## 📝 Description

This Python script uses the Scapy library to perform an ARP poisoning attack. The attack consists of falsifying ARP messages to trick two hosts into believing that the attacker's MAC address is that of the other host. This way, all traffic between the two hosts is redirected through the attacker's machine.

## ⚙️ Prerequisites

- Python 3.x
- Scapy library
- Root/administrator permissions
- iptables (for Linux systems)

## 🚀 Installation

```bash
pip install scapy
```

## 🛠️ Usage

1. Modify the `target1_host` and `target2_host` variables with the IP addresses of the hosts you want to intercept.
2. Run the script with root privileges:

```bash
sudo python arpPoisoning.py
```

## ✨ Main Features

- **get_mac(ip)**: Gets the MAC address associated with an IP address.
- **spoof(target_host, spoof_host)**: Sends spoofed ARP packets to deceive the target host.
- **clean_target_arp_table(destination_host, source_host)**: Restores original ARP tables when closing the program.

## 🔍 How It Works

1. The script enables IP forwarding (`ip_forward`) to allow intercepted traffic to continue flowing:
   ```
   echo 1 > /proc/sys/net/ipv4/ip_forward
   ```

2. It continuously sends falsified ARP packets to both target hosts.

3. When the user interrupts the script with Ctrl+C, the hosts' ARP tables are cleaned up.

## 🔧 iptables Configuration

For the attack to work properly and to manipulate traffic, you need to set up appropriate iptables rules. These rules aren't explicitly created in the script, so you'll need to configure them manually before running the tool:

### Basic iptables Setup for Traffic Interception

```bash
# Create a new chain for our intercepted traffic
iptables --flush
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
```

Remember to clear these rules after finishing your tests:

```bash
iptables --flush
```

## ⚠️ Important Note

**Warning**: This tool is provided for educational and testing purposes only. Using this script to intercept network traffic without explicit authorization from the owners of the target hosts may violate computer security and privacy laws. Use only in controlled test environments or with explicit permission.

## 📜 License

Distributed under the MIT License.
