#!/usr/bin/env python3
"""
VexityBot Core Test Suite
Tests for core functionality without GUI dependencies
"""

import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestVexityBotCore(unittest.TestCase):
    """Test cases for VexityBot core functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_imports(self):
        """Test that core modules can be imported"""
        try:
            # Test networking module
            from VexityBotNetworking_Simple import NetworkEndpoint, ProtocolType
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import networking module: {e}")
    
    def test_network_endpoint_creation(self):
        """Test network endpoint creation"""
        try:
            from VexityBotNetworking_Simple import NetworkEndpoint, ProtocolType
            
            endpoint = NetworkEndpoint(
                host="127.0.0.1",
                port=8080,
                protocol=ProtocolType.TCP
            )
            
            self.assertEqual(endpoint.host, "127.0.0.1")
            self.assertEqual(endpoint.port, 8080)
            self.assertEqual(endpoint.protocol, ProtocolType.TCP)
        except Exception as e:
            self.fail(f"Network endpoint creation failed: {e}")
    
    def test_protocol_types(self):
        """Test protocol type enum"""
        try:
            from VexityBotNetworking_Simple import ProtocolType
            
            # Test that all expected protocol types exist
            expected_protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'WEBSOCKET', 'CUSTOM']
            for protocol in expected_protocols:
                self.assertTrue(hasattr(ProtocolType, protocol))
        except Exception as e:
            self.fail(f"Protocol type test failed: {e}")
    
    def test_bot_data_structure(self):
        """Test bot data structure"""
        # This would test the bot data structure
        # Implementation depends on your bot data format
        self.assertTrue(True)
    
    def test_config_files_exist(self):
        """Test that configuration files exist"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        
        if os.path.exists(config_dir):
            config_files = os.listdir(config_dir)
            self.assertGreater(len(config_files), 0, "No configuration files found")
        else:
            self.skipTest("Config directory not found")
    
    def test_requirements_file(self):
        """Test that requirements.txt exists and is readable"""
        requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt')
        
        self.assertTrue(os.path.exists(requirements_path), "requirements.txt not found")
        
        with open(requirements_path, 'r') as f:
            content = f.read()
            self.assertGreater(len(content), 0, "requirements.txt is empty")

if __name__ == "__main__":
    unittest.main()
