#!/usr/bin/env python3
"""
Simple test to isolate the string formatting issue
"""

def test_format():
    """Test the exact format call"""
    try:
        # Simulate the variables
        bomb_names = ["quantum", "plasma"]
        webhook_url = "https://discord.com/api/webhooks/test"
        selected_bombs = ["quantum", "plasma"]
        bomb_configs = {"quantum": {"name": "Test"}}
        
        # Test the template
        template = '''Bombs: {bomb_names_str}
Webhook: {webhook_url_str}
Selected: {selected_bombs_str}
Configs: {bomb_configs_str}'''
        
        result = template.format(
            bomb_names_str=', '.join(bomb_names),
            webhook_url_str=webhook_url,
            selected_bombs_str=selected_bombs,
            bomb_configs_str=bomb_configs
        )
        
        print("✅ Format test successful!")
        print(result)
        return True
        
    except Exception as e:
        print(f"❌ Format test failed: {e}")
        return False

if __name__ == "__main__":
    test_format()
