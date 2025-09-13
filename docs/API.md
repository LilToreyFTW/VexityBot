# VexityBot API Documentation

## Core Classes

### VexityBotGUI
Main GUI application class.

```python
from main_gui import VexityBotGUI
import tkinter as tk

root = tk.Tk()
app = VexityBotGUI(root)
root.mainloop()
```

### BotManager
Manages individual bot instances.

```python
from VexityBotCore import BotManager

manager = BotManager()
manager.start_all_bots()
manager.stop_all_bots()
```

### NetworkManager
Handles network communication.

```python
from VexityBotNetworking import VexityBotNetworkManager

network = VexityBotNetworkManager(endpoint, bot_id)
await network.start()
```

## Configuration

### Bot Configuration
```python
bot_config = {
    "name": "AlphaBot",
    "specialty": "Nuclear Warfare",
    "port": 8081,
    "status": "Online"
}
```

### Network Configuration
```python
endpoint = NetworkEndpoint(
    host="191.96.152.162",
    port=8080,
    protocol=ProtocolType.TCP,
    ssl_enabled=True
)
```

## Examples

See the `examples/` directory for complete usage examples.
