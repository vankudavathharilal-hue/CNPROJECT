# Network Connectivity & Latency Monitor

Computer Networks project for monitoring:

- Ping / network reachability
- Latency
- DNS resolution
- TCP port connectivity
- Latency history graph

## Requirements

- Python 3.10+
- VS Code recommended
- Internet connection

## Windows setup

Open the project folder in VS Code Terminal.

### 1. Create virtual environment

```powershell
python -m venv venv
```

### 2. Activate it

```powershell
venv\Scripts\activate
```

### 3. Install packages

```powershell
pip install -r requirements.txt
```

### 4. Test the networking functions

```powershell
python test_network.py
```

### 5. Start the web application

```powershell
python app.py
```

### 6. Open the dashboard

Open:

http://127.0.0.1:5000

## Project architecture

Browser -> Flask API -> Ping / DNS / TCP -> Network

## Next planned modules

1. Packet-loss calculation
2. Multiple-host monitoring
3. Automatic monitoring
4. SQLite database
5. Historical reports
6. Traceroute
7. Alerts
8. Final project documentation and PPT
