#!/usr/bin/env python3
"""
Black Screen Takeover Module
Makes the user's entire screen go completely black and dark
"""

import tkinter as tk
import threading
import time
import sys
import os
from typing import Optional

class BlackScreenTakeover:
    """Black Screen Takeover - Complete screen blackout functionality"""
    
    def __init__(self):
        self.black_window = None
        self.is_active = False
        self.thread = None
        self.duration = 0  # 0 = infinite
        self.start_time = 0
        
    def activate_black_screen(self, duration: int = 0, fade_speed: float = 0.1):
        """
        Activate black screen takeover
        
        Args:
            duration: How long to keep screen black (0 = infinite)
            fade_speed: Speed of fade to black (0.1 = fast, 1.0 = slow)
        """
        if self.is_active:
            return False
            
        self.duration = duration
        self.start_time = time.time()
        self.is_active = True
        
        # Start black screen in separate thread
        self.thread = threading.Thread(target=self._create_black_screen, args=(fade_speed,), daemon=True)
        self.thread.start()
        
        return True
    
    def deactivate_black_screen(self):
        """Deactivate black screen takeover"""
        if not self.is_active:
            return False
            
        self.is_active = False
        
        if self.black_window:
            try:
                self.black_window.destroy()
            except:
                pass
            self.black_window = None
            
        return True
    
    def _create_black_screen(self, fade_speed: float):
        """Create the black screen overlay"""
        try:
            # Create fullscreen black window
            self.black_window = tk.Tk()
            self.black_window.title("")
            self.black_window.configure(bg='black')
            
            # Make it fullscreen and always on top
            self.black_window.attributes('-fullscreen', True)
            self.black_window.attributes('-topmost', True)
            self.black_window.attributes('-alpha', 0.0)  # Start transparent
            
            # Remove window decorations
            self.black_window.overrideredirect(True)
            
            # Disable all interactions
            self.black_window.focus_force()
            self.black_window.grab_set_global()
            
            # Create black canvas covering entire screen
            canvas = tk.Canvas(self.black_window, bg='black', highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # Add some text (optional - can be removed for pure black)
            canvas.create_text(
                self.black_window.winfo_screenwidth() // 2,
                self.black_window.winfo_screenheight() // 2,
                text="🖤 SCREEN TAKEOVER ACTIVE 🖤",  # EDIT THIS TEXT
                fill='red',
                font=('Arial', 24, 'bold'),
                anchor='center'
            )
            
            # Fade in effect
            self._fade_in(fade_speed)
            
            # Keep window alive and check duration
            self._maintain_black_screen()
            
        except Exception as e:
            print(f"Error creating black screen: {e}")
            self.is_active = False
    
    def _fade_in(self, fade_speed: float):
        """Fade in the black screen"""
        try:
            alpha = 0.0
            while alpha < 1.0 and self.is_active:
                alpha += fade_speed
                if alpha > 1.0:
                    alpha = 1.0
                    
                self.black_window.attributes('-alpha', alpha)
                time.sleep(0.05)  # 50ms intervals
                
        except Exception as e:
            print(f"Error during fade in: {e}")
    
    def _maintain_black_screen(self):
        """Maintain the black screen and check duration"""
        try:
            while self.is_active:
                # Check if duration has expired
                if self.duration > 0:
                    elapsed = time.time() - self.start_time
                    if elapsed >= self.duration:
                        self.deactivate_black_screen()
                        break
                
                # Update window to keep it active
                self.black_window.update()
                time.sleep(0.1)  # 100ms update interval
                
        except Exception as e:
            print(f"Error maintaining black screen: {e}")
        finally:
            self.is_active = False
    
    def is_screen_black(self) -> bool:
        """Check if black screen is currently active"""
        return self.is_active
    
    def get_remaining_time(self) -> float:
        """Get remaining time for black screen (if duration is set)"""
        if not self.is_active or self.duration == 0:
            return -1  # Infinite or not active
            
        elapsed = time.time() - self.start_time
        remaining = self.duration - elapsed
        return max(0, remaining)
    
    def emergency_exit(self):
        """Emergency exit - force close black screen"""
        self.is_active = False
        
        if self.black_window:
            try:
                self.black_window.quit()
                self.black_window.destroy()
            except:
                pass
            self.black_window = None
        
        # Force exit if needed
        try:
            os._exit(0)
        except:
            pass

# Global instance
black_screen_takeover = BlackScreenTakeover()

def activate_black_screen_takeover(duration: int = 0, fade_speed: float = 0.1) -> bool:
    """
    Activate black screen takeover (global function)
    
    Args:
        duration: Duration in seconds (0 = infinite)
        fade_speed: Fade speed (0.1 = fast, 1.0 = slow)
    
    Returns:
        bool: True if activated successfully
    """
    return black_screen_takeover.activate_black_screen(duration, fade_speed)

def deactivate_black_screen_takeover() -> bool:
    """
    Deactivate black screen takeover (global function)
    
    Returns:
        bool: True if deactivated successfully
    """
    return black_screen_takeover.deactivate_black_screen()

def is_black_screen_active() -> bool:
    """
    Check if black screen is active (global function)
    
    Returns:
        bool: True if black screen is active
    """
    return black_screen_takeover.is_screen_black()

def emergency_exit_black_screen():
    """Emergency exit from black screen (global function)"""
    black_screen_takeover.emergency_exit()

# Test function
def test_black_screen_takeover():
    """Test the black screen takeover functionality"""
    print("🖤 Testing Black Screen Takeover...")
    
    # Activate for 10 seconds
    if activate_black_screen_takeover(duration=10, fade_speed=0.2):
        print("✅ Black screen activated for 10 seconds")
        
        # Monitor status
        while is_black_screen_active():
            remaining = black_screen_takeover.get_remaining_time()
            if remaining > 0:
                print(f"⏰ Remaining time: {remaining:.1f} seconds")
            time.sleep(1)
        
        print("✅ Black screen deactivated")
    else:
        print("❌ Failed to activate black screen")

if __name__ == "__main__":
    # Run test
    test_black_screen_takeover()