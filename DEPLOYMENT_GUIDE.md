# ShadowStrike OSRS Bot - Remote Deployment Guide

## 🚀 Overview

This guide will help you deploy the ShadowStrike OSRS Bot system with a VPS server and client EXE for remote control.

## 📋 System Architecture

```
[Client PC] ←→ [VPS Server] ←→ [OSRS Game Client]
     ↓              ↓              ↓
[EXE Controller] [Bot Server] [Automated Bot]
```

## 🖥️ VPS Server Setup

### 1. VPS Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 10GB minimum
- **Network**: Public IP with port 9999 open

### 2. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install python3 python3-pip git -y

# Install required packages
pip3 install -r requirements.txt
```

### 3. Deploy Bot Server
```bash
# Create bot directory
mkdir -p ~/shadowstrike_bot
cd ~/shadowstrike_bot

# Download bot files
wget https://your-server.com/ShadowStrike_OSRS_Bot.py
wget https://your-server.com/VPS_Bot_Server.py
wget https://your-server.com/requirements.txt

# Set permissions
chmod +x VPS_Bot_Server.py
```

### 4. Configure Firewall
```bash
# Allow port 9999
sudo ufw allow 9999
sudo ufw enable
```

### 5. Create System Service
```bash
# Create service file
sudo nano /etc/systemd/system/shadowstrike-bot.service
```

Add this content:
```ini
[Unit]
Description=ShadowStrike OSRS Bot Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/shadowstrike_bot
ExecStart=/usr/bin/python3 VPS_Bot_Server.py --host 0.0.0.0 --port 9999
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6. Start Service
```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable shadowstrike-bot
sudo systemctl start shadowstrike-bot

# Check status
sudo systemctl status shadowstrike-bot
```

## 💻 Client EXE Setup

### 1. Build Client EXE
```bash
# Run the build script
python build_client_exe.py
```

### 2. Configure Client
1. Edit `deployment/config.txt`
2. Set your VPS IP address
3. Adjust port if needed

### 3. Distribute Client
- Copy the entire `deployment/` folder
- Send to users who need bot control access

## 🎮 Usage Instructions

### For VPS Administrators

1. **Start the Server:**
   ```bash
   sudo systemctl start shadowstrike-bot
   ```

2. **Check Status:**
   ```bash
   sudo systemctl status shadowstrike-bot
   ```

3. **View Logs:**
   ```bash
   sudo journalctl -u shadowstrike-bot -f
   ```

4. **Stop Server:**
   ```bash
   sudo systemctl stop shadowstrike-bot
   ```

### For Client Users

1. **Run Client EXE:**
   - Double-click `ShadowStrike_Bot_Controller.exe`
   - Enter VPS IP and port
   - Click "Connect"

2. **Control Bot:**
   - Click "Start Bot" to begin automation
   - Monitor status in real-time
   - View logs for progress updates
   - Use "Stop Bot" to halt automation

## 🔧 Configuration Options

### VPS Server Configuration
Edit `VPS_Bot_Server.py`:
```python
# Change these settings
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999       # Change if needed
MAX_CLIENTS = 10  # Maximum concurrent clients
```

### Client Configuration
Edit `Client_Bot_Controller.py`:
```python
# Default VPS settings
self.vps_host = "YOUR_VPS_IP_HERE"
self.vps_port = 9999
```

## 🛡️ Security Considerations

### 1. Firewall Rules
```bash
# Only allow specific IPs (optional)
sudo ufw allow from YOUR_IP to any port 9999
```

### 2. Authentication (Optional)
Add authentication to the server:
```python
# In VPS_Bot_Server.py
AUTH_TOKEN = "your_secret_token"
```

### 3. Rate Limiting
The server includes built-in rate limiting to prevent abuse.

## 📊 Monitoring and Logs

### Server Logs
- **Location**: `~/shadowstrike_bot/vps_bot_server.log`
- **View**: `tail -f vps_bot_server.log`

### Bot Logs
- **Location**: `~/shadowstrike_bot/shadowstrike_bot.log`
- **View**: `tail -f shadowstrike_bot.log`

### System Logs
- **View**: `sudo journalctl -u shadowstrike-bot -f`

## 🔄 Updates and Maintenance

### Update Bot Code
```bash
cd ~/shadowstrike_bot
# Download new files
wget https://your-server.com/ShadowStrike_OSRS_Bot.py
# Restart service
sudo systemctl restart shadowstrike-bot
```

### Update Client EXE
1. Run `python build_client_exe.py`
2. Distribute new EXE to users

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused:**
   - Check VPS IP and port
   - Verify firewall settings
   - Ensure service is running

2. **Bot Won't Start:**
   - Check Python dependencies
   - Verify bot files are present
   - Check logs for errors

3. **Client Can't Connect:**
   - Verify network connectivity
   - Check VPS is accessible
   - Try different port

### Debug Commands
```bash
# Check service status
sudo systemctl status shadowstrike-bot

# View recent logs
sudo journalctl -u shadowstrike-bot --since "1 hour ago"

# Test port connectivity
telnet YOUR_VPS_IP 9999

# Check if port is listening
sudo netstat -tlnp | grep 9999
```

## 📈 Performance Optimization

### VPS Optimization
- Use SSD storage for better I/O
- Allocate sufficient RAM (4GB+)
- Monitor CPU usage during bot operation

### Network Optimization
- Use VPS close to game servers
- Consider dedicated IP for stability
- Monitor bandwidth usage

## 🔐 Backup and Recovery

### Backup Bot State
```bash
# Create backup
tar -czf bot_backup_$(date +%Y%m%d).tar.gz ~/shadowstrike_bot/

# Restore backup
tar -xzf bot_backup_YYYYMMDD.tar.gz -C ~/
```

### Disaster Recovery
1. Restore VPS from backup
2. Reinstall bot server
3. Restore bot state files
4. Restart service

## 📞 Support

For issues or questions:
1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Contact support

## 🎯 Advanced Features

### Multiple Bot Instances
Run multiple bots on the same VPS:
```bash
# Start additional instances
python VPS_Bot_Server.py --port 9998
python VPS_Bot_Server.py --port 9997
```

### Load Balancing
Use a load balancer to distribute client connections across multiple bot servers.

### Monitoring Dashboard
Create a web dashboard to monitor all bot instances and their status.

---

**⚠️ Important Notes:**
- Always follow game terms of service
- Use bots responsibly
- Monitor for bans and adjust behavior
- Keep backups of important data
- Update regularly for security
