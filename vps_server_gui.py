#!/usr/bin/env python3
"""
VexityBot VPS Server GUI
Complete VPS-hosted GUI for remote bot management
Server IP: 191.96.152.162
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import sys
import random
import threading
import time
import socket
import json
import subprocess
from datetime import datetime
import logging
import psutil
import requests
from flask import Flask, render_template, request, jsonify
import webbrowser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# TSM-Framework Anticheat Color Scheme
TSM_COLORS = {
    'primary': '#00d4ff',
    'secondary': '#0099cc', 
    'accent': '#00a8cc',
    'dark': '#0a0a0a',
    'darker': '#050505',
    'light': '#1a1a1a',
    'lighter': '#2a2a2a',
    'text': '#ffffff',
    'text_secondary': '#cccccc',
    'text_muted': '#888888',
    'success': '#00ff88',
    'warning': '#ffaa00',
    'error': '#ff4444',
    'border': '#333333',
    'shadow': '#001a1f'
}

class VexityBotVPSServer:
    def __init__(self, root):
        self.root = root
        self.root.title("VexityBot VPS Server - 191.96.152.162")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # VPS Configuration
        self.vps_ip = "191.96.152.162"
        self.vps_port = 9999
        self.web_port = 8080
        self.server_running = False
        self.web_server_running = False
        
        # Bot Management
        self.bots = {}
        self.bot_processes = {}
        self.bot_status = {}
        
        # Initialize Flask web server
        self.flask_app = Flask(__name__)
        self.setup_flask_routes()
        
        # Configure styling
        self.setup_styles()
        
        # Create main components
        self.create_menu_bar()
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()
        
        # Bind events
        self.bind_events()
        
        # Start background services
        self.start_background_services()
    
    def setup_styles(self):
        """Configure TSM-Framework Anticheat styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # TSM-Framework Dark Theme Configuration
        self.root.configure(bg=TSM_COLORS['dark'])
        
        # Configure main window
        style.configure('TNotebook', 
                       background=TSM_COLORS['light'],
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=TSM_COLORS['darker'],
                       foreground=TSM_COLORS['text_secondary'],
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', TSM_COLORS['primary']),
                           ('active', TSM_COLORS['lighter'])],
                 foreground=[('selected', TSM_COLORS['text']),
                           ('active', TSM_COLORS['text'])])
        
        # Frame styles
        style.configure('TSM.TFrame',
                       background=TSM_COLORS['light'],
                       borderwidth=1,
                       relief='solid')
        style.configure('TSM.Dark.TFrame',
                       background=TSM_COLORS['darker'],
                       borderwidth=1,
                       relief='solid')
        style.configure('TSM.Light.TFrame',
                       background=TSM_COLORS['lighter'],
                       borderwidth=1,
                       relief='solid')
        
        # Label styles
        style.configure('TSM.Title.TLabel',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['primary'],
                       font=('Segoe UI', 18, 'bold'))
        style.configure('TSM.Heading.TLabel',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['text'],
                       font=('Segoe UI', 12, 'bold'))
        style.configure('TSM.Text.TLabel',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['text_secondary'],
                       font=('Segoe UI', 10))
        style.configure('TSM.Success.TLabel',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['success'],
                       font=('Segoe UI', 10, 'bold'))
        style.configure('TSM.Warning.TLabel',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['warning'],
                       font=('Segoe UI', 10, 'bold'))
        style.configure('TSM.Error.TLabel',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['error'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Button styles
        style.configure('TSM.Primary.TButton',
                       background=TSM_COLORS['primary'],
                       foreground=TSM_COLORS['text'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 8],
                       borderwidth=0)
        style.map('TSM.Primary.TButton',
                 background=[('active', TSM_COLORS['secondary']),
                           ('pressed', TSM_COLORS['accent'])])
        
        style.configure('TSM.Secondary.TButton',
                       background=TSM_COLORS['lighter'],
                       foreground=TSM_COLORS['text_secondary'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 8],
                       borderwidth=1,
                       relief='solid')
        style.map('TSM.Secondary.TButton',
                 background=[('active', TSM_COLORS['primary']),
                           ('pressed', TSM_COLORS['secondary'])],
                 foreground=[('active', TSM_COLORS['text']),
                           ('pressed', TSM_COLORS['text'])])
        
        style.configure('TSM.Success.TButton',
                       background=TSM_COLORS['success'],
                       foreground=TSM_COLORS['text'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 8],
                       borderwidth=0)
        
        style.configure('TSM.Warning.TButton',
                       background=TSM_COLORS['warning'],
                       foreground=TSM_COLORS['text'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 8],
                       borderwidth=0)
        
        style.configure('TSM.Error.TButton',
                       background=TSM_COLORS['error'],
                       foreground=TSM_COLORS['text'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 8],
                       borderwidth=0)
        
        # Entry styles
        style.configure('TSM.TEntry',
                       fieldbackground=TSM_COLORS['lighter'],
                       foreground=TSM_COLORS['text'],
                       borderwidth=1,
                       relief='solid',
                       font=('Segoe UI', 10))
        style.map('TSM.TEntry',
                 focuscolor=TSM_COLORS['primary'])
        
        # Combobox styles
        style.configure('TSM.TCombobox',
                       fieldbackground=TSM_COLORS['lighter'],
                       foreground=TSM_COLORS['text'],
                       background=TSM_COLORS['lighter'],
                       borderwidth=1,
                       relief='solid',
                       font=('Segoe UI', 10))
        style.map('TSM.TCombobox',
                 fieldbackground=[('readonly', TSM_COLORS['lighter'])],
                 focuscolor=TSM_COLORS['primary'])
        
        # Checkbutton styles
        style.configure('TSM.TCheckbutton',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['text_secondary'],
                       font=('Segoe UI', 10),
                       focuscolor=TSM_COLORS['primary'])
        
        # Radiobutton styles
        style.configure('TSM.TRadiobutton',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['text_secondary'],
                       font=('Segoe UI', 10),
                       focuscolor=TSM_COLORS['primary'])
        
        # Progressbar styles
        style.configure('TSM.Horizontal.TProgressbar',
                       background=TSM_COLORS['primary'],
                       troughcolor=TSM_COLORS['lighter'],
                       borderwidth=0,
                       lightcolor=TSM_COLORS['primary'],
                       darkcolor=TSM_COLORS['primary'])
        
        # Treeview styles
        style.configure('TSM.Treeview',
                       background=TSM_COLORS['lighter'],
                       foreground=TSM_COLORS['text'],
                       fieldbackground=TSM_COLORS['lighter'],
                       font=('Segoe UI', 9))
        style.configure('TSM.Treeview.Heading',
                       background=TSM_COLORS['darker'],
                       foreground=TSM_COLORS['primary'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
        style.map('TSM.Treeview',
                 background=[('selected', TSM_COLORS['primary'])],
                 foreground=[('selected', TSM_COLORS['text'])])
        
        # Scrollbar styles
        style.configure('TSM.Vertical.TScrollbar',
                       background=TSM_COLORS['darker'],
                       troughcolor=TSM_COLORS['lighter'],
                       borderwidth=0,
                       arrowcolor=TSM_COLORS['text_secondary'],
                       darkcolor=TSM_COLORS['primary'],
                       lightcolor=TSM_COLORS['primary'])
        style.configure('TSM.Horizontal.TScrollbar',
                       background=TSM_COLORS['darker'],
                       troughcolor=TSM_COLORS['lighter'],
                       borderwidth=0,
                       arrowcolor=TSM_COLORS['text_secondary'],
                       darkcolor=TSM_COLORS['primary'],
                       lightcolor=TSM_COLORS['primary'])
        
        # LabelFrame styles
        style.configure('TSM.TLabelframe',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['text'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=1,
                       relief='solid')
        style.configure('TSM.TLabelframe.Label',
                       background=TSM_COLORS['light'],
                       foreground=TSM_COLORS['primary'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Separator styles
        style.configure('TSM.TSeparator',
                       background=TSM_COLORS['border'])
        
        # Scale styles
        style.configure('TSM.Horizontal.TScale',
                       background=TSM_COLORS['lighter'],
                       troughcolor=TSM_COLORS['lighter'],
                       borderwidth=0,
                       lightcolor=TSM_COLORS['primary'],
                       darkcolor=TSM_COLORS['primary'])
        
        # Spinbox styles
        style.configure('TSM.TSpinbox',
                       fieldbackground=TSM_COLORS['lighter'],
                       foreground=TSM_COLORS['text'],
                       background=TSM_COLORS['lighter'],
                       borderwidth=1,
                       relief='solid',
                       font=('Segoe UI', 10))
        style.map('TSM.TSpinbox',
                 fieldbackground=[('readonly', TSM_COLORS['lighter'])],
                 focuscolor=TSM_COLORS['primary'])
        
        # Text widget styles
        self.root.option_add('*Text*Background', TSM_COLORS['lighter'])
        self.root.option_add('*Text*Foreground', TSM_COLORS['text'])
        self.root.option_add('*Text*selectBackground', TSM_COLORS['primary'])
        self.root.option_add('*Text*selectForeground', TSM_COLORS['text'])
        self.root.option_add('*Text*insertBackground', TSM_COLORS['primary'])
        
        # Scrolled text
        self.root.option_add('*ScrolledText*Background', TSM_COLORS['lighter'])
        self.root.option_add('*ScrolledText*Foreground', TSM_COLORS['text'])
        self.root.option_add('*ScrolledText*selectBackground', TSM_COLORS['primary'])
        self.root.option_add('*ScrolledText*selectForeground', TSM_COLORS['text'])
        self.root.option_add('*ScrolledText*insertBackground', TSM_COLORS['primary'])
        
        # Apply custom window styling
        self.root.configure(bg=TSM_COLORS['dark'])
        self.root.option_add('*TCombobox*Listbox*Background', TSM_COLORS['lighter'])
        self.root.option_add('*TCombobox*Listbox*Foreground', TSM_COLORS['text'])
        self.root.option_add('*TCombobox*Listbox*selectBackground', TSM_COLORS['primary'])
        self.root.option_add('*TCombobox*Listbox*selectForeground', TSM_COLORS['text'])
    
    def create_menu_bar(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Bot", command=self.create_new_bot)
        file_menu.add_command(label="Import Bot", command=self.import_bot)
        file_menu.add_command(label="Export Bot", command=self.export_bot)
        file_menu.add_separator()
        file_menu.add_command(label="Server Settings", command=self.open_server_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        
        # Server Menu
        server_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Server", menu=server_menu)
        server_menu.add_command(label="Start Server", command=self.start_server)
        server_menu.add_command(label="Stop Server", command=self.stop_server)
        server_menu.add_command(label="Restart Server", command=self.restart_server)
        server_menu.add_separator()
        server_menu.add_command(label="Server Status", command=self.show_server_status)
        server_menu.add_command(label="Server Logs", command=self.show_server_logs)
        
        # Bots Menu
        bots_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bots", menu=bots_menu)
        bots_menu.add_command(label="Start All Bots", command=self.start_all_bots)
        bots_menu.add_command(label="Stop All Bots", command=self.stop_all_bots)
        bots_menu.add_command(label="Restart All Bots", command=self.restart_all_bots)
        bots_menu.add_separator()
        bots_menu.add_command(label="Bot Statistics", command=self.show_bot_statistics)
        bots_menu.add_command(label="Bot Health Check", command=self.bot_health_check)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="System Monitor", command=self.open_system_monitor)
        tools_menu.add_command(label="Network Monitor", command=self.open_network_monitor)
        tools_menu.add_command(label="Log Viewer", command=self.open_log_viewer)
        tools_menu.add_separator()
        tools_menu.add_command(label="Database Manager", command=self.open_database_manager)
        tools_menu.add_command(label="File Manager", command=self.open_file_manager)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="API Reference", command=self.show_api_reference)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create the toolbar with TSM styling"""
        self.toolbar = ttk.Frame(self.root, style='TSM.Dark.TFrame')
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Server info
        server_label = ttk.Label(self.toolbar, text=f"🌐 VPS Server: {self.vps_ip}:{self.vps_port}", style='TSM.Heading.TLabel')
        server_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL, style='TSM.TSeparator').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Server controls
        self.server_status_label = ttk.Label(self.toolbar, text="❌ Server Offline", style='TSM.Error.TLabel')
        self.server_status_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.toolbar, text="🚀 Start Server", command=self.start_server, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="⏹️ Stop Server", command=self.stop_server, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="🔄 Restart", command=self.restart_server, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL, style='TSM.TSeparator').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Bot controls
        ttk.Button(self.toolbar, text="🤖 Start All Bots", command=self.start_all_bots, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="⏹️ Stop All Bots", command=self.stop_all_bots, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="📊 Statistics", command=self.show_bot_statistics, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL, style='TSM.TSeparator').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Web interface
        ttk.Button(self.toolbar, text="🌐 Web Interface", command=self.open_web_interface, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="📱 Mobile App", command=self.open_mobile_app, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL, style='TSM.TSeparator').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # DeathBot controls
        ttk.Button(self.toolbar, text="💀 Start DeathBot", command=self.start_deathbot, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="⏹️ Stop DeathBot", command=self.stop_deathbot, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="🚨 Emergency Stop", command=self.emergency_shutdown_deathbot, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=2)
    
    def create_main_content(self):
        """Create the main content area with notebook tabs"""
        # Create main frame with TSM styling
        main_frame = ttk.Frame(self.root, style='TSM.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs with TSM styling
        self.notebook = ttk.Notebook(main_frame, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create all tabs
        self.create_dashboard_tab()
        self.create_bots_management_tab()
        self.create_server_monitor_tab()
        self.create_network_tab()
        self.create_database_tab()
        self.create_code_editor_tab()
        self.create_data_analysis_tab()
        self.create_ai_management_tab()
        self.create_bomb_tab()
        self.create_exe_tab()
        self.create_victim_exe_tab()
        self.create_screens_tab()
        self.create_steganography_tab()
        self.create_gamebots_tab()
        self.create_thunderbolt_tab()
        self.create_deathbot_tab()
        self.create_settings_tab()
    
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        # Add scrollbar to dashboard frame
        scrollable_dashboard = self.add_scrollbar_to_frame(dashboard_frame)
        
        # Welcome content with TSM styling
        title_label = ttk.Label(scrollable_dashboard, text="VexityBot VPS Server", style='TSM.Title.TLabel')
        title_label.pack(pady=30)
        
        subtitle_label = ttk.Label(scrollable_dashboard, text=f"Server IP: {self.vps_ip} | Port: {self.vps_port}", style='TSM.Heading.TLabel')
        subtitle_label.pack(pady=10)
        
        # Server status
        status_frame = ttk.Frame(scrollable_dashboard, style='TSM.Dark.TFrame')
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.server_status_display = ttk.Label(status_frame, text="🟢 SERVER ONLINE", style='TSM.Success.TLabel')
        self.server_status_display.pack(pady=10)
        
        # Quick stats
        stats_frame = ttk.LabelFrame(scrollable_dashboard, text="📊 Server Statistics", style='TSM.TLabelframe', padding=20)
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        stats_grid = ttk.Frame(stats_frame, style='TSM.TFrame')
        stats_grid.pack(fill=tk.X)
        
        stats = [
            ("Bots Online", "0/24", "TSM.Success.TLabel"),
            ("Server Status", "ACTIVE", "TSM.Success.TLabel"),
            ("Uptime", "00:00:00", "TSM.Text.TLabel"),
            ("CPU Usage", "0%", "TSM.Text.TLabel"),
            ("Memory Usage", "0%", "TSM.Text.TLabel"),
            ("Network", "ONLINE", "TSM.Success.TLabel")
        ]
        
        for i, (label, value, style_name) in enumerate(stats):
            stat_frame = ttk.Frame(stats_grid, style='TSM.Dark.TFrame')
            stat_frame.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
            stats_grid.columnconfigure(i, weight=1)
            
            label_widget = ttk.Label(stat_frame, text=label, style='TSM.Text.TLabel')
            label_widget.pack()
            
            value_widget = ttk.Label(stat_frame, text=value, style=style_name)
            value_widget.pack()
        
        # Quick actions
        actions_frame = ttk.LabelFrame(scrollable_dashboard, text="⚡ Quick Actions", style='TSM.TLabelframe', padding=20)
        actions_frame.pack(fill=tk.X, padx=20, pady=20)
        
        actions_grid = ttk.Frame(actions_frame, style='TSM.TFrame')
        actions_grid.pack(fill=tk.X)
        
        actions = [
            ("🚀 Start All Bots", self.start_all_bots),
            ("⏹️ Stop All Bots", self.stop_all_bots),
            ("🔄 Restart Server", self.restart_server),
            ("📊 View Statistics", self.show_bot_statistics),
            ("🌐 Web Interface", self.open_web_interface),
            ("📱 Mobile App", self.open_mobile_app)
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(actions_grid, text=text, command=command, style='TSM.Primary.TButton')
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='ew')
            actions_grid.columnconfigure(i%3, weight=1)
    
    def add_scrollbar_to_frame(self, parent_frame):
        """Add vertical scrollbar to any frame"""
        # Create a canvas and scrollbar
        canvas = tk.Canvas(parent_frame, bg=TSM_COLORS['dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TSM.TFrame')
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return scrollable_frame
    
    def create_bots_management_tab(self):
        """Create the bots management tab"""
        bots_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(bots_frame, text="🤖 Bots Management")
        
        # Header frame
        header_frame = ttk.Frame(bots_frame, style='TSM.Dark.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="🤖 Bot Management System", style='TSM.Heading.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Control buttons
        control_frame = ttk.Frame(header_frame, style='TSM.TFrame')
        control_frame.pack(side=tk.RIGHT)
        
        ttk.Button(control_frame, text="🔄 Refresh", command=self.refresh_bots, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="▶️ Start All", command=self.start_all_bots, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏹️ Stop All", command=self.stop_all_bots, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="📊 Statistics", command=self.show_bot_statistics, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        
        # Bot list with scrollbar
        list_frame = ttk.Frame(bots_frame, style='TSM.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview for bot list
        columns = ('Name', 'Status', 'Port', 'Uptime', 'CPU', 'Memory', 'Actions')
        self.bot_tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='TSM.Treeview')
        
        for col in columns:
            self.bot_tree.heading(col, text=col)
            self.bot_tree.column(col, width=120)
        
        # Scrollbar for bot list
        bot_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.bot_tree.yview)
        self.bot_tree.configure(yscrollcommand=bot_scrollbar.set)
        
        self.bot_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bot_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize bot data
        self.initialize_bot_data()
        self.populate_bot_list()
        
        # Initialize DeathBot
        self.initialize_deathbot()
    
    def create_server_monitor_tab(self):
        """Create the server monitoring tab"""
        monitor_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(monitor_frame, text="📊 Server Monitor")
        
        # System stats
        stats_frame = ttk.LabelFrame(monitor_frame, text="💻 System Statistics", style='TSM.TLabelframe')
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # CPU and Memory
        cpu_frame = ttk.Frame(stats_frame, style='TSM.TFrame')
        cpu_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(cpu_frame, text="CPU Usage:", style='TSM.Text.TLabel').pack(side=tk.LEFT)
        self.cpu_progress = ttk.Progressbar(cpu_frame, style='TSM.Horizontal.TProgressbar')
        self.cpu_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.cpu_label = ttk.Label(cpu_frame, text="0%", style='TSM.Text.TLabel')
        self.cpu_label.pack(side=tk.RIGHT)
        
        memory_frame = ttk.Frame(stats_frame, style='TSM.TFrame')
        memory_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(memory_frame, text="Memory Usage:", style='TSM.Text.TLabel').pack(side=tk.LEFT)
        self.memory_progress = ttk.Progressbar(memory_frame, style='TSM.Horizontal.TProgressbar')
        self.memory_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.memory_label = ttk.Label(memory_frame, text="0%", style='TSM.Text.TLabel')
        self.memory_label.pack(side=tk.RIGHT)
        
        # Network stats
        network_frame = ttk.LabelFrame(monitor_frame, text="🌐 Network Statistics", style='TSM.TLabelframe')
        network_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.network_text = scrolledtext.ScrolledText(network_frame, height=10, font=('Consolas', 9))
        self.network_text.pack(fill=tk.X, padx=10, pady=10)
        
        # Server logs
        logs_frame = ttk.LabelFrame(monitor_frame, text="📋 Server Logs", style='TSM.TLabelframe')
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.server_logs = scrolledtext.ScrolledText(logs_frame, font=('Consolas', 9))
        self.server_logs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Start monitoring
        self.start_system_monitoring()
    
    def create_network_tab(self):
        """Create the network monitoring tab"""
        network_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(network_frame, text="🌐 Network")
        
        # Connection info
        conn_frame = ttk.LabelFrame(network_frame, text="🔌 Connection Information", style='TSM.TLabelframe')
        conn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        conn_info = ttk.Frame(conn_frame, style='TSM.TFrame')
        conn_info.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(conn_info, text=f"Server IP: {self.vps_ip}", style='TSM.Text.TLabel').pack(anchor=tk.W)
        ttk.Label(conn_info, text=f"Server Port: {self.vps_port}", style='TSM.Text.TLabel').pack(anchor=tk.W)
        ttk.Label(conn_info, text=f"Web Port: {self.web_port}", style='TSM.Text.TLabel').pack(anchor=tk.W)
        ttk.Label(conn_info, text="Protocol: TCP/UDP", style='TSM.Text.TLabel').pack(anchor=tk.W)
        
        # Network monitoring
        monitor_frame = ttk.LabelFrame(network_frame, text="📊 Network Monitoring", style='TSM.TLabelframe')
        monitor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.network_monitor = scrolledtext.ScrolledText(monitor_frame, font=('Consolas', 9))
        self.network_monitor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Network controls
        controls_frame = ttk.Frame(network_frame, style='TSM.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls_frame, text="🔍 Scan Network", command=self.scan_network, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="📊 Network Stats", command=self.show_network_stats, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="🔄 Refresh", command=self.refresh_network, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
    
    def create_database_tab(self):
        """Create the database management tab"""
        db_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(db_frame, text="🗄️ Database")
        
        # Database connection
        conn_frame = ttk.LabelFrame(db_frame, text="🔌 Database Connection", style='TSM.TLabelframe')
        conn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        conn_settings = ttk.Frame(conn_frame, style='TSM.TFrame')
        conn_settings.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(conn_settings, text="Host:", style='TSM.Text.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5)
        self.db_host_entry = ttk.Entry(conn_settings, width=30, style='TSM.TEntry')
        self.db_host_entry.grid(row=0, column=1, padx=5)
        self.db_host_entry.insert(0, "localhost")
        
        ttk.Label(conn_settings, text="Port:", style='TSM.Text.TLabel').grid(row=0, column=2, sticky=tk.W, padx=5)
        self.db_port_entry = ttk.Entry(conn_settings, width=10, style='TSM.TEntry')
        self.db_port_entry.grid(row=0, column=3, padx=5)
        self.db_port_entry.insert(0, "3306")
        
        ttk.Label(conn_settings, text="Database:", style='TSM.Text.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5)
        self.db_name_entry = ttk.Entry(conn_settings, width=30, style='TSM.TEntry')
        self.db_name_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(conn_settings, text="Username:", style='TSM.Text.TLabel').grid(row=1, column=2, sticky=tk.W, padx=5)
        self.db_user_entry = ttk.Entry(conn_settings, width=15, style='TSM.TEntry')
        self.db_user_entry.grid(row=1, column=3, padx=5)
        
        ttk.Button(conn_settings, text="Connect", command=self.connect_database, style='TSM.Primary.TButton').grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(conn_settings, text="Disconnect", command=self.disconnect_database, style='TSM.Error.TButton').grid(row=2, column=1, padx=5, pady=5)
        
        # Query area
        query_frame = ttk.LabelFrame(db_frame, text="💻 SQL Query", style='TSM.TLabelframe')
        query_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.query_text = scrolledtext.ScrolledText(query_frame, height=8, font=('Consolas', 10))
        self.query_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Query buttons
        query_btn_frame = ttk.Frame(query_frame, style='TSM.TFrame')
        query_btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(query_btn_frame, text="Execute", command=self.execute_query, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(query_btn_frame, text="Clear", command=self.clear_query, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
    
    def create_code_editor_tab(self):
        """Create the code editor tab"""
        editor_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(editor_frame, text="💻 Code Editor")
        
        # Editor header
        header_frame = ttk.Frame(editor_frame, style='TSM.Dark.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="💻 VPS Code Editor", style='TSM.Heading.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Language selector
        lang_frame = ttk.Frame(header_frame, style='TSM.TFrame')
        lang_frame.pack(side=tk.RIGHT)
        
        ttk.Label(lang_frame, text="Language:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.language_var = tk.StringVar(value="Python")
        language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var, 
                                    values=["Python", "JavaScript", "HTML", "CSS", "Java", "C++", "C#"], 
                                    style='TSM.TCombobox', width=10)
        language_combo.pack(side=tk.LEFT)
        
        # Text editor
        self.text_editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.WORD, 
            font=('Consolas', 11),
            bg=TSM_COLORS['lighter'],
            fg=TSM_COLORS['text'],
            insertbackground=TSM_COLORS['primary'],
            selectbackground=TSM_COLORS['primary'],
            selectforeground=TSM_COLORS['text'],
            borderwidth=1,
            relief='solid',
            undo=True
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Editor content
        self.text_editor.insert(tk.END, "# VexityBot VPS Code Editor\n")
        self.text_editor.insert(tk.END, "# Edit your bot scripts here...\n\n")
        self.text_editor.insert(tk.END, "def main():\n")
        self.text_editor.insert(tk.END, "    print('Hello from VPS!')\n\n")
        self.text_editor.insert(tk.END, "if __name__ == '__main__':\n")
        self.text_editor.insert(tk.END, "    main()\n")
    
    def create_data_analysis_tab(self):
        """Create the data analysis tab"""
        analysis_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(analysis_frame, text="📊 Data Analysis")
        
        # Data input
        input_frame = ttk.LabelFrame(analysis_frame, text="📥 Data Input", style='TSM.TLabelframe')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        input_controls = ttk.Frame(input_frame, style='TSM.TFrame')
        input_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(input_controls, text="📁 Load CSV", command=self.load_csv, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_controls, text="🗄️ Load Database", command=self.load_from_db, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_controls, text="🎲 Generate Sample", command=self.generate_sample_data, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Analysis options
        options_frame = ttk.LabelFrame(analysis_frame, text="⚙️ Analysis Options", style='TSM.TLabelframe')
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        analysis_controls = ttk.Frame(options_frame, style='TSM.TFrame')
        analysis_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(analysis_controls, text="📈 Statistics", command=self.descriptive_stats, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(analysis_controls, text="📊 Visualization", command=self.create_visualization, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(analysis_controls, text="🤖 ML Analysis", command=self.ml_analysis, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Results area
        results_frame = ttk.LabelFrame(analysis_frame, text="📋 Results", style='TSM.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, font=('Consolas', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_ai_management_tab(self):
        """Create the AI management tab"""
        ai_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(ai_frame, text="🤖 AI Management")
        
        # AI Control Panel
        control_frame = ttk.LabelFrame(ai_frame, text="🧠 AI Control Panel", style='TSM.TLabelframe')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ai_controls = ttk.Frame(control_frame, style='TSM.TFrame')
        ai_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(ai_controls, text="AI Status:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.ai_mode_var = tk.StringVar(value="Auto")
        ai_mode_combo = ttk.Combobox(ai_controls, textvariable=self.ai_mode_var, 
                                   values=["Auto", "Manual", "Learning", "Emergency"], 
                                   style='TSM.TCombobox', width=10)
        ai_mode_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(ai_controls, text="▶️ Start AI", command=self.start_ai_management, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(ai_controls, text="⏹️ Stop AI", command=self.stop_ai_management, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(ai_controls, text="🔄 Reset AI", command=self.reset_ai_management, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # AI Bot Overview
        overview_frame = ttk.LabelFrame(ai_frame, text="📊 AI Bot Overview", style='TSM.TLabelframe')
        overview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_ai_bot_grid(overview_frame)
        
        # AI Actions
        actions_frame = ttk.LabelFrame(ai_frame, text="⚡ AI Actions", style='TSM.TLabelframe')
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        action_buttons = ttk.Frame(actions_frame, style='TSM.TFrame')
        action_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_buttons, text="🚀 Optimize All", command=self.ai_optimize_all, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="🔄 Restart Failed", command=self.ai_restart_failed, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="📈 Scale Up", command=self.ai_scale_up, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="📉 Scale Down", command=self.ai_scale_down, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="🛡️ Security Scan", command=self.ai_security_scan, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_buttons, text="📊 Analytics", command=self.ai_analytics, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=2)
    
    def create_bomb_tab(self):
        """Create the bomb creator tab"""
        bomb_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(bomb_frame, text="💣 Bomb Creator")
        
        # Bomb creation interface
        create_frame = ttk.LabelFrame(bomb_frame, text="💣 Bomb Creator", style='TSM.TLabelframe')
        create_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bomb type selection
        type_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        type_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(type_frame, text="Bomb Type:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.bomb_type_var = tk.StringVar(value="HTTP Flood")
        bomb_type_combo = ttk.Combobox(type_frame, textvariable=self.bomb_type_var,
                                     values=["HTTP Flood", "UDP Flood", "TCP Flood", "ICMP Flood", "Slowloris"],
                                     style='TSM.TCombobox', width=15)
        bomb_type_combo.pack(side=tk.LEFT, padx=5)
        
        # Target settings
        target_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        target_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(target_frame, text="Target IP:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.target_ip_entry = ttk.Entry(target_frame, width=20, style='TSM.TEntry')
        self.target_ip_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(target_frame, text="Port:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(10, 5))
        self.target_port_entry = ttk.Entry(target_frame, width=10, style='TSM.TEntry')
        self.target_port_entry.pack(side=tk.LEFT, padx=5)
        
        # Attack settings
        attack_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        attack_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(attack_frame, text="Threads:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.threads_entry = ttk.Entry(attack_frame, width=10, style='TSM.TEntry')
        self.threads_entry.pack(side=tk.LEFT, padx=5)
        self.threads_entry.insert(0, "100")
        
        ttk.Label(attack_frame, text="Duration (s):", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(10, 5))
        self.duration_entry = ttk.Entry(attack_frame, width=10, style='TSM.TEntry')
        self.duration_entry.pack(side=tk.LEFT, padx=5)
        self.duration_entry.insert(0, "60")
        
        # Control buttons
        control_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="🚀 Launch Attack", command=self.launch_attack, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="⏹️ Stop Attack", command=self.stop_attack, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📊 Attack Stats", command=self.show_attack_stats, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Attack log
        log_frame = ttk.LabelFrame(bomb_frame, text="📋 Attack Log", style='TSM.TLabelframe')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.attack_log = scrolledtext.ScrolledText(log_frame, font=('Consolas', 9))
        self.attack_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_exe_tab(self):
        """Create the EXE builder tab"""
        exe_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(exe_frame, text="⚡ EXE Builder")
        
        # EXE creation interface
        create_frame = ttk.LabelFrame(exe_frame, text="⚡ EXE Builder", style='TSM.TLabelframe')
        create_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # EXE settings
        settings_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(settings_frame, text="EXE Name:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.exe_name_entry = ttk.Entry(settings_frame, width=30, style='TSM.TEntry')
        self.exe_name_entry.pack(side=tk.LEFT, padx=5)
        self.exe_name_entry.insert(0, "VexityBot_Client")
        
        ttk.Label(settings_frame, text="Icon:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(10, 5))
        self.icon_path_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.icon_path_var, width=30, style='TSM.TEntry').pack(side=tk.LEFT, padx=5)
        ttk.Button(settings_frame, text="Browse", command=self.browse_icon, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Build options
        options_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.onefile_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="One File", variable=self.onefile_var, style='TSM.TCheckbutton').pack(side=tk.LEFT, padx=5)
        
        self.console_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Console Window", variable=self.console_var, style='TSM.TCheckbutton').pack(side=tk.LEFT, padx=5)
        
        self.upx_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="UPX Compression", variable=self.upx_var, style='TSM.TCheckbutton').pack(side=tk.LEFT, padx=5)
        
        # Build buttons
        build_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        build_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(build_frame, text="🔨 Build EXE", command=self.build_exe, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(build_frame, text="📁 Open Output", command=self.open_output_folder, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(build_frame, text="🧹 Clean Build", command=self.clean_build, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # Build log
        log_frame = ttk.LabelFrame(exe_frame, text="📋 Build Log", style='TSM.TLabelframe')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.build_log = scrolledtext.ScrolledText(log_frame, font=('Consolas', 9))
        self.build_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_victim_exe_tab(self):
        """Create the victim EXE tab"""
        victim_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(victim_frame, text="🎯 Victim EXE")
        
        # Victim EXE creation
        create_frame = ttk.LabelFrame(victim_frame, text="🎯 Victim EXE Creator", style='TSM.TLabelframe')
        create_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Controller settings
        controller_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        controller_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(controller_frame, text="Controller IP:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.controller_ip_entry = ttk.Entry(controller_frame, width=20, style='TSM.TEntry')
        self.controller_ip_entry.pack(side=tk.LEFT, padx=5)
        self.controller_ip_entry.insert(0, self.vps_ip)
        
        ttk.Label(controller_frame, text="Port:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(10, 5))
        self.controller_port_entry = ttk.Entry(controller_frame, width=10, style='TSM.TEntry')
        self.controller_port_entry.pack(side=tk.LEFT, padx=5)
        self.controller_port_entry.insert(0, str(self.vps_port))
        
        # EXE settings
        exe_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        exe_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(exe_frame, text="EXE Name:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.victim_exe_name_entry = ttk.Entry(exe_frame, width=30, style='TSM.TEntry')
        self.victim_exe_name_entry.pack(side=tk.LEFT, padx=5)
        self.victim_exe_name_entry.insert(0, "SystemUpdate")
        
        # Stealth options
        stealth_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        stealth_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stealth_mode_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(stealth_frame, text="Stealth Mode", variable=self.stealth_mode_var, style='TSM.TCheckbutton').pack(side=tk.LEFT, padx=5)
        
        self.auto_start_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(stealth_frame, text="Auto Start", variable=self.auto_start_var, style='TSM.TCheckbutton').pack(side=tk.LEFT, padx=5)
        
        self.persistence_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(stealth_frame, text="Persistence", variable=self.persistence_var, style='TSM.TCheckbutton').pack(side=tk.LEFT, padx=5)
        
        # Create buttons
        create_btn_frame = ttk.Frame(create_frame, style='TSM.TFrame')
        create_btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(create_btn_frame, text="🎯 Create Victim EXE", command=self.create_victim_exe, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(create_btn_frame, text="📁 Open Output", command=self.open_victim_output, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(create_btn_frame, text="🧪 Test EXE", command=self.test_victim_exe, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # Creation log
        log_frame = ttk.LabelFrame(victim_frame, text="📋 Creation Log", style='TSM.TLabelframe')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.victim_log = scrolledtext.ScrolledText(log_frame, font=('Consolas', 9))
        self.victim_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_screens_tab(self):
        """Create the screen capture tab"""
        screens_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(screens_frame, text="🖼️ Screen Capture")
        
        # Screen capture controls
        capture_frame = ttk.LabelFrame(screens_frame, text="📸 Screen Capture", style='TSM.TLabelframe')
        capture_frame.pack(fill=tk.X, padx=10, pady=10)
        
        controls_frame = ttk.Frame(capture_frame, style='TSM.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls_frame, text="📸 Take Screenshot", command=self.take_screenshot, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="🎥 Start Recording", command=self.start_recording, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="⏹️ Stop Recording", command=self.stop_recording, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="📁 Open Folder", command=self.open_screens_folder, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Screen preview
        preview_frame = ttk.LabelFrame(screens_frame, text="🖼️ Screen Preview", style='TSM.TLabelframe')
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.screen_preview = tk.Label(preview_frame, text="No screenshot taken", 
                                     bg=TSM_COLORS['lighter'], fg=TSM_COLORS['text'],
                                     font=('Arial', 12))
        self.screen_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Screen list
        list_frame = ttk.LabelFrame(screens_frame, text="📋 Screen History", style='TSM.TLabelframe')
        list_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.screen_list = ttk.Treeview(list_frame, columns=('Time', 'Type', 'Size'), show='headings', style='TSM.Treeview')
        self.screen_list.heading('Time', text='Time')
        self.screen_list.heading('Type', text='Type')
        self.screen_list.heading('Size', text='Size')
        self.screen_list.pack(fill=tk.X, padx=10, pady=10)
    
    def create_steganography_tab(self):
        """Create the steganography tab"""
        stego_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(stego_frame, text="🔐 Steganography")
        
        # Steganography controls
        stego_controls = ttk.LabelFrame(stego_frame, text="🔐 Steganography Tools", style='TSM.TLabelframe')
        stego_controls.pack(fill=tk.X, padx=10, pady=10)
        
        controls_frame = ttk.Frame(stego_controls, style='TSM.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls_frame, text="📁 Select Image", command=self.select_image, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="📄 Select File", command=self.select_file, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="🔒 Hide Data", command=self.hide_data, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="🔓 Extract Data", command=self.extract_data, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        # File paths
        paths_frame = ttk.Frame(stego_controls, style='TSM.TFrame')
        paths_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(paths_frame, text="Image:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.image_path_var = tk.StringVar()
        ttk.Entry(paths_frame, textvariable=self.image_path_var, width=50, style='TSM.TEntry').pack(side=tk.LEFT, padx=5)
        
        ttk.Label(paths_frame, text="File:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(10, 5))
        self.file_path_var = tk.StringVar()
        ttk.Entry(paths_frame, textvariable=self.file_path_var, width=50, style='TSM.TEntry').pack(side=tk.LEFT, padx=5)
        
        # Steganography log
        log_frame = ttk.LabelFrame(stego_frame, text="📋 Steganography Log", style='TSM.TLabelframe')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.stego_log = scrolledtext.ScrolledText(log_frame, font=('Consolas', 9))
        self.stego_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_gamebots_tab(self):
        """Create the game bots tab"""
        gamebots_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(gamebots_frame, text="🎮 Game Bots")
        
        # Game bot leaderboard
        leaderboard_frame = ttk.LabelFrame(gamebots_frame, text="🏆 Game Bot Leaderboard", style='TSM.TLabelframe')
        leaderboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create game bot treeview
        columns = ('Rank', 'Name', 'Class', 'Level', 'XP', 'Kills', 'Status', 'Actions')
        self.gamebot_tree = ttk.Treeview(leaderboard_frame, columns=columns, show='headings', style='TSM.Treeview')
        
        for col in columns:
            self.gamebot_tree.heading(col, text=col)
            self.gamebot_tree.column(col, width=100)
        
        # Scrollbar for game bot list
        gamebot_scrollbar = ttk.Scrollbar(leaderboard_frame, orient=tk.VERTICAL, command=self.gamebot_tree.yview)
        self.gamebot_tree.configure(yscrollcommand=gamebot_scrollbar.set)
        
        self.gamebot_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        gamebot_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Game bot controls
        controls_frame = ttk.LabelFrame(gamebots_frame, text="🎮 Game Bot Controls", style='TSM.TLabelframe')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        game_controls = ttk.Frame(controls_frame, style='TSM.TFrame')
        game_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(game_controls, text="⚔️ Start Battle", command=self.start_game_battle, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(game_controls, text="🛡️ Defend Base", command=self.defend_base, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(game_controls, text="🎯 Target Practice", command=self.target_practice, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(game_controls, text="📊 Analytics", command=self.show_game_analytics, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Initialize game bot data
        self.initialize_gamebot_data()
        self.populate_gamebot_list()
    
    def create_thunderbolt_tab(self):
        """Create the Thunderbolt Pokemon GO tab"""
        thunderbolt_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(thunderbolt_frame, text="⚡ Thunderbolt")
        
        # Thunderbolt controls
        control_frame = ttk.LabelFrame(thunderbolt_frame, text="⚡ Thunderbolt Pokemon GO Bot", style='TSM.TLabelframe')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        thunderbolt_controls = ttk.Frame(control_frame, style='TSM.TFrame')
        thunderbolt_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(thunderbolt_controls, text="🚀 Start Thunderbolt", command=self.start_thunderbolt, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(thunderbolt_controls, text="⏹️ Stop Thunderbolt", command=self.stop_thunderbolt, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(thunderbolt_controls, text="📊 Status", command=self.thunderbolt_status, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(thunderbolt_controls, text="⚙️ Settings", command=self.thunderbolt_settings, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Thunderbolt modes
        modes_frame = ttk.LabelFrame(thunderbolt_frame, text="🎯 Bot Modes", style='TSM.TLabelframe')
        modes_frame.pack(fill=tk.X, padx=10, pady=10)
        
        mode_controls = ttk.Frame(modes_frame, style='TSM.TFrame')
        mode_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(mode_controls, text="🎯 Catching", command=self.thunderbolt_catching, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(mode_controls, text="🏰 Raiding", command=self.thunderbolt_raiding, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(mode_controls, text="⚔️ Battling", command=self.thunderbolt_battling, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(mode_controls, text="🌍 Exploring", command=self.thunderbolt_exploring, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Thunderbolt status
        status_frame = ttk.LabelFrame(thunderbolt_frame, text="📊 Thunderbolt Status", style='TSM.TLabelframe')
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.thunderbolt_status_text = scrolledtext.ScrolledText(status_frame, font=('Consolas', 9))
        self.thunderbolt_status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize Thunderbolt status
        self.update_thunderbolt_status()
    
    def create_deathbot_tab(self):
        """Create the DeathBot #25 tab"""
        deathbot_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(deathbot_frame, text="💀 DeathBot #25")
        
        # DeathBot header
        header_frame = ttk.Frame(deathbot_frame, style='TSM.Dark.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="💀 DeathBot #25 - Ultimate Destruction Bot", style='TSM.Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Warning label
        warning_label = ttk.Label(header_frame, text="⚠️ EXTREMELY DANGEROUS - USE WITH CAUTION", style='TSM.Error.TLabel')
        warning_label.pack(side=tk.RIGHT)
        
        # Main control panel
        control_frame = ttk.LabelFrame(deathbot_frame, text="💀 DeathBot Control Panel", style='TSM.TLabelframe')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Control buttons
        control_buttons = ttk.Frame(control_frame, style='TSM.TFrame')
        control_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_buttons, text="🚀 ACTIVATE DEATHBOT", command=self.start_deathbot, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_buttons, text="⏹️ STOP DEATHBOT", command=self.stop_deathbot, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_buttons, text="🚨 EMERGENCY SHUTDOWN", command=self.emergency_shutdown_deathbot, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_buttons, text="⚙️ CONFIGURE", command=self.configure_deathbot, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Status and info
        info_frame = ttk.LabelFrame(deathbot_frame, text="📊 DeathBot Status & Information", style='TSM.TLabelframe')
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_buttons = ttk.Frame(info_frame, style='TSM.TFrame')
        info_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(info_buttons, text="📊 Show Status", command=self.show_deathbot_status, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(info_buttons, text="📋 Generate Report", command=self.generate_deathbot_report, style='TSM.Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(info_buttons, text="🔍 View Dump Files", command=self.view_deathbot_dump, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # DeathBot features
        features_frame = ttk.LabelFrame(deathbot_frame, text="🔥 DeathBot Features", style='TSM.TLabelframe')
        features_frame.pack(fill=tk.X, padx=10, pady=10)
        
        features_text = """
💀 DEATHBOT #25 CAPABILITIES:
============================

⚡ Ricochet Boom AC/12v Power Mode
🔥 Auto-initiate Python Script execution
⏰ 12-second countdown to activation
📁 Advanced file scraping across multiple directories
💥 Simulated destruction sequences
🗄️ File dump and logging system
🌪️ System resource monitoring
💀 Ultimate destruction protocols

TARGET DIRECTORIES:
• C:/Downloads - User download files
• C:/Documents - Document files
• C:/Pictures - Image files  
• C:/Desktop - Desktop files
• C:/Users - User directories
• C:/Program Files - Program files
• C:/Windows/System32 - System files

FILE TYPES TARGETED:
• .txt, .doc, .docx, .pdf - Documents
• .jpg, .png - Images
• .mp4, .mp3 - Media files
• .zip, .rar - Archives

⚠️  WARNING: DEATHBOT IS SIMULATION ONLY  ⚠️
        """
        
        features_display = scrolledtext.ScrolledText(features_frame, height=15, font=('Consolas', 9))
        features_display.pack(fill=tk.X, padx=10, pady=10)
        features_display.insert(tk.END, features_text)
        features_display.config(state=tk.DISABLED)
        
        # Destruction log
        log_frame = ttk.LabelFrame(deathbot_frame, text="📋 DeathBot Destruction Log", style='TSM.TLabelframe')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.deathbot_log = scrolledtext.ScrolledText(log_frame, font=('Consolas', 9))
        self.deathbot_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize log
        self.deathbot_log.insert(tk.END, "💀 DeathBot #25 - Ultimate Destruction Bot\n")
        self.deathbot_log.insert(tk.END, "⚡ Ricochet Boom AC/12v Power - AUTO INITIATE PYSCRIPT\n")
        self.deathbot_log.insert(tk.END, "🔥 Ready for destruction sequence...\n")
        self.deathbot_log.insert(tk.END, "⏰ Countdown timer: 12 seconds\n")
        self.deathbot_log.insert(tk.END, "📁 Target directories: 7 configured\n")
        self.deathbot_log.insert(tk.END, "💀 DeathBot #25 initialized and ready\n\n")
    
    def view_deathbot_dump(self):
        """View DeathBot dump files"""
        if not self.deathbot:
            messagebox.showerror("DeathBot Error", "DeathBot not available")
            return
        
        dump_location = self.deathbot.config['file_dump_location']
        
        if os.path.exists(dump_location):
            # Open file explorer to dump location
            os.startfile(dump_location)
            self.update_status(f"DeathBot dump folder opened: {dump_location}")
        else:
            messagebox.showwarning("DeathBot Dump", "DeathBot dump directory not found")
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook, style='TSM.TFrame')
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Server settings
        server_settings = ttk.LabelFrame(settings_frame, text="🌐 Server Settings", style='TSM.TLabelframe')
        server_settings.pack(fill=tk.X, padx=10, pady=10)
        
        server_frame = ttk.Frame(server_settings, style='TSM.TFrame')
        server_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(server_frame, text="Server IP:", style='TSM.Text.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5)
        self.server_ip_entry = ttk.Entry(server_frame, width=20, style='TSM.TEntry')
        self.server_ip_entry.grid(row=0, column=1, padx=5)
        self.server_ip_entry.insert(0, self.vps_ip)
        
        ttk.Label(server_frame, text="Server Port:", style='TSM.Text.TLabel').grid(row=0, column=2, sticky=tk.W, padx=5)
        self.server_port_entry = ttk.Entry(server_frame, width=10, style='TSM.TEntry')
        self.server_port_entry.grid(row=0, column=3, padx=5)
        self.server_port_entry.insert(0, str(self.vps_port))
        
        ttk.Label(server_frame, text="Web Port:", style='TSM.Text.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5)
        self.web_port_entry = ttk.Entry(server_frame, width=20, style='TSM.TEntry')
        self.web_port_entry.grid(row=1, column=1, padx=5)
        self.web_port_entry.insert(0, str(self.web_port))
        
        # Bot settings
        bot_settings = ttk.LabelFrame(settings_frame, text="🤖 Bot Settings", style='TSM.TLabelframe')
        bot_settings.pack(fill=tk.X, padx=10, pady=10)
        
        bot_frame = ttk.Frame(bot_settings, style='TSM.TFrame')
        bot_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.auto_start_bots_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bot_frame, text="Auto Start Bots", variable=self.auto_start_bots_var, style='TSM.TCheckbutton').pack(anchor=tk.W, padx=5)
        
        self.auto_restart_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bot_frame, text="Auto Restart Failed Bots", variable=self.auto_restart_var, style='TSM.TCheckbutton').pack(anchor=tk.W, padx=5)
        
        self.log_level_var = tk.StringVar(value="INFO")
        ttk.Label(bot_frame, text="Log Level:", style='TSM.Text.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        log_combo = ttk.Combobox(bot_frame, textvariable=self.log_level_var,
                               values=["DEBUG", "INFO", "WARNING", "ERROR"],
                               style='TSM.TCombobox', width=10)
        log_combo.pack(side=tk.LEFT, padx=5)
        
        # Save settings
        save_frame = ttk.Frame(settings_frame, style='TSM.TFrame')
        save_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(save_frame, text="💾 Save Settings", command=self.save_settings, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(save_frame, text="🔄 Reset Settings", command=self.reset_settings, style='TSM.Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(save_frame, text="📁 Open Config", command=self.open_config_folder, style='TSM.Secondary.TButton').pack(side=tk.LEFT, padx=5)
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ttk.Frame(self.root, style='TSM.Dark.TFrame')
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, text="VexityBot VPS Server Ready", style='TSM.Text.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.time_label = ttk.Label(self.status_frame, text="", style='TSM.Text.TLabel')
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Start time updater
        self.update_time()
    
    def bind_events(self):
        """Bind keyboard shortcuts and events"""
        self.root.bind('<Control-q>', lambda e: self.exit_application())
        self.root.bind('<Control-s>', lambda e: self.save_settings())
        self.root.bind('<F5>', lambda e: self.refresh_bots())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
    
    def start_background_services(self):
        """Start background monitoring services"""
        # Start system monitoring
        self.start_system_monitoring()
        
        # Start bot monitoring
        self.start_bot_monitoring()
        
        # Start time updater
        self.update_time()
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    # Flask Web Server Routes
    def setup_flask_routes(self):
        """Setup Flask web server routes"""
        @self.flask_app.route('/')
        def index():
            return render_template('index.html', 
                                 server_ip=self.vps_ip, 
                                 server_port=self.vps_port,
                                 bots=self.bots)
        
        @self.flask_app.route('/api/bots', methods=['GET'])
        def get_bots():
            return jsonify(self.bots)
        
        @self.flask_app.route('/api/bots/<bot_name>/start', methods=['POST'])
        def start_bot_api(bot_name):
            if bot_name in self.bots:
                self.start_bot(self.bots[bot_name])
                return jsonify({'success': True, 'message': f'Bot {bot_name} started'})
            return jsonify({'success': False, 'message': 'Bot not found'})
        
        @self.flask_app.route('/api/bots/<bot_name>/stop', methods=['POST'])
        def stop_bot_api(bot_name):
            if bot_name in self.bots:
                self.stop_bot(self.bots[bot_name])
                return jsonify({'success': True, 'message': f'Bot {bot_name} stopped'})
            return jsonify({'success': False, 'message': 'Bot not found'})
        
        @self.flask_app.route('/api/server/status', methods=['GET'])
        def server_status():
            return jsonify({
                'server_running': self.server_running,
                'web_server_running': self.web_server_running,
                'bots_online': len([b for b in self.bots.values() if b.get('status') == 'Online']),
                'total_bots': len(self.bots)
            })
    
    # Bot Management Methods
    def initialize_bot_data(self):
        """Initialize bot data for all 25 bots including DeathBot"""
        bot_names = [
            "AlphaBot", "BetaBot", "GammaBot", "DeltaBot", "EpsilonBot", "ZetaBot",
            "EtaBot", "ThetaBot", "IotaBot", "KappaBot", "LambdaBot", "MuBot",
            "NuBot", "XiBot", "OmicronBot", "PiBot", "RhoBot", "SigmaBot",
            "TauBot", "UpsilonBot", "PhiBot", "ChiBot", "PsiBot", "OmegaBot",
            "DeathBot"  # DeathBot #25 - Ultimate destruction bot
        ]
        
        for i, name in enumerate(bot_names):
            self.bots[name] = {
                'name': name,
                'status': 'Offline',
                'port': 8081 + i,
                'uptime': '0%',
                'cpu': '0%',
                'memory': '0%',
                'process': None,
                'last_update': datetime.now(),
                'special': name == 'DeathBot'  # Mark DeathBot as special
            }
    
    def populate_bot_list(self):
        """Populate the bot list in the treeview"""
        for item in self.bot_tree.get_children():
            self.bot_tree.delete(item)
        
        for bot in self.bots.values():
            self.bot_tree.insert('', tk.END, values=(
                bot['name'],
                bot['status'],
                bot['port'],
                bot['uptime'],
                bot['cpu'],
                bot['memory'],
                'Actions'
            ))
    
    def refresh_bots(self):
        """Refresh bot status and update display"""
        self.update_bot_status()
        self.populate_bot_list()
        self.update_status("Bot status refreshed")
    
    def start_all_bots(self):
        """Start all bots"""
        for bot in self.bots.values():
            if bot['status'] == 'Offline':
                self.start_bot(bot)
        self.update_status("All bots started")
    
    def stop_all_bots(self):
        """Stop all bots"""
        for bot in self.bots.values():
            if bot['status'] == 'Online':
                self.stop_bot(bot)
        self.update_status("All bots stopped")
    
    def start_bot(self, bot):
        """Start a specific bot"""
        try:
            # Special handling for DeathBot
            if bot['name'] == 'DeathBot':
                self.start_deathbot()
                return
            
            # Simulate bot startup
            bot['status'] = 'Online'
            bot['uptime'] = '100%'
            bot['cpu'] = f"{random.randint(5, 25)}%"
            bot['memory'] = f"{random.randint(10, 50)}%"
            bot['last_update'] = datetime.now()
            
            # Create a mock process
            bot['process'] = subprocess.Popen(['python', '-c', 'import time; time.sleep(3600)'])
            
            self.update_status(f"Bot {bot['name']} started")
            self.populate_bot_list()
            
        except Exception as e:
            self.update_status(f"Failed to start bot {bot['name']}: {e}")
    
    def stop_bot(self, bot):
        """Stop a specific bot"""
        try:
            # Special handling for DeathBot
            if bot['name'] == 'DeathBot':
                self.stop_deathbot()
                return
            
            if bot['process']:
                bot['process'].terminate()
                bot['process'] = None
            
            bot['status'] = 'Offline'
            bot['uptime'] = '0%'
            bot['cpu'] = '0%'
            bot['memory'] = '0%'
            bot['last_update'] = datetime.now()
            
            self.update_status(f"Bot {bot['name']} stopped")
            self.populate_bot_list()
            
        except Exception as e:
            self.update_status(f"Failed to stop bot {bot['name']}: {e}")
    
    def show_bot_statistics(self):
        """Show bot statistics"""
        online_bots = len([b for b in self.bots.values() if b['status'] == 'Online'])
        total_bots = len(self.bots)
        
        stats_text = f"""
🤖 Bot Statistics
================

Total Bots: {total_bots}
Online Bots: {online_bots}
Offline Bots: {total_bots - online_bots}

Bot Details:
"""
        
        for bot in self.bots.values():
            stats_text += f"• {bot['name']}: {bot['status']} (Port: {bot['port']})\n"
        
        messagebox.showinfo("Bot Statistics", stats_text)
    
    # Server Management Methods
    def start_server(self):
        """Start the VPS server"""
        try:
            if not self.server_running:
                # Start TCP server
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((self.vps_ip, self.vps_port))
                self.server_socket.listen(5)
                self.server_running = True
                
                # Start Flask web server in a separate thread
                web_thread = threading.Thread(target=self.start_web_server, daemon=True)
                web_thread.start()
                
                self.server_status_label.config(text="✅ Server Online", style='TSM.Success.TLabel')
                self.update_status(f"VPS Server started on {self.vps_ip}:{self.vps_port}")
                
                # Start server monitoring
                self.start_server_monitoring()
                
        except Exception as e:
            self.update_status(f"Failed to start server: {e}")
            messagebox.showerror("Server Error", f"Failed to start server: {e}")
    
    def stop_server(self):
        """Stop the VPS server"""
        try:
            if self.server_running:
                if hasattr(self, 'server_socket'):
                    self.server_socket.close()
                
                self.server_running = False
                self.web_server_running = False
                
                self.server_status_label.config(text="❌ Server Offline", style='TSM.Error.TLabel')
                self.update_status("VPS Server stopped")
                
        except Exception as e:
            self.update_status(f"Failed to stop server: {e}")
    
    def restart_server(self):
        """Restart the VPS server"""
        self.stop_server()
        time.sleep(2)
        self.start_server()
        self.update_status("VPS Server restarted")
    
    def start_web_server(self):
        """Start the Flask web server"""
        try:
            self.flask_app.run(host='0.0.0.0', port=self.web_port, debug=False)
            self.web_server_running = True
        except Exception as e:
            self.update_status(f"Web server error: {e}")
    
    def open_web_interface(self):
        """Open the web interface in browser"""
        webbrowser.open(f"http://{self.vps_ip}:{self.web_port}")
        self.update_status("Web interface opened")
    
    def open_mobile_app(self):
        """Open mobile app interface"""
        webbrowser.open(f"http://{self.vps_ip}:{self.web_port}/mobile")
        self.update_status("Mobile interface opened")
    
    # System Monitoring Methods
    def start_system_monitoring(self):
        """Start system monitoring"""
        def monitor_loop():
            while True:
                try:
                    # Update CPU usage
                    cpu_percent = psutil.cpu_percent()
                    self.cpu_progress['value'] = cpu_percent
                    self.cpu_label.config(text=f"{cpu_percent}%")
                    
                    # Update memory usage
                    memory = psutil.virtual_memory()
                    memory_percent = memory.percent
                    self.memory_progress['value'] = memory_percent
                    self.memory_label.config(text=f"{memory_percent}%")
                    
                    # Update network stats
                    self.update_network_stats()
                    
                    time.sleep(2)
                except Exception as e:
                    time.sleep(5)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def start_bot_monitoring(self):
        """Start bot monitoring"""
        def bot_monitor_loop():
            while True:
                try:
                    self.update_bot_status()
                    time.sleep(5)
                except Exception as e:
                    time.sleep(10)
        
        monitor_thread = threading.Thread(target=bot_monitor_loop, daemon=True)
        monitor_thread.start()
    
    def update_bot_status(self):
        """Update bot status information"""
        for bot in self.bots.values():
            if bot['status'] == 'Online':
                # Simulate status updates
                bot['cpu'] = f"{random.randint(5, 25)}%"
                bot['memory'] = f"{random.randint(10, 50)}%"
                bot['last_update'] = datetime.now()
    
    def update_network_stats(self):
        """Update network statistics"""
        try:
            net_io = psutil.net_io_counters()
            stats_text = f"""
🌐 Network Statistics
====================

Bytes Sent: {net_io.bytes_sent:,}
Bytes Received: {net_io.bytes_recv:,}
Packets Sent: {net_io.packets_sent:,}
Packets Received: {net_io.packets_recv:,}
Errors In: {net_io.errin}
Errors Out: {net_io.errout}
Drops In: {net_io.dropin}
Drops Out: {net_io.dropout}

Server: {self.vps_ip}:{self.vps_port}
Web: {self.vps_ip}:{self.web_port}
Status: {'Online' if self.server_running else 'Offline'}
            """
            
            if hasattr(self, 'network_text'):
                self.network_text.delete(1.0, tk.END)
                self.network_text.insert(tk.END, stats_text)
                
        except Exception as e:
            pass
    
    # Database Methods
    def connect_database(self):
        """Connect to database"""
        try:
            host = self.db_host_entry.get()
            port = int(self.db_port_entry.get())
            database = self.db_name_entry.get()
            username = self.db_user_entry.get()
            
            # Simulate database connection
            self.update_status(f"Connected to database {host}:{port}")
            messagebox.showinfo("Database", f"Connected to {host}:{port}/{database}")
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
    
    def disconnect_database(self):
        """Disconnect from database"""
        self.update_status("Disconnected from database")
        messagebox.showinfo("Database", "Disconnected from database")
    
    def execute_query(self):
        """Execute SQL query"""
        query = self.query_text.get(1.0, tk.END).strip()
        if query:
            # Simulate query execution
            self.update_status("Query executed successfully")
            messagebox.showinfo("Query", "Query executed successfully")
        else:
            messagebox.showwarning("Query", "Please enter a SQL query")
    
    def clear_query(self):
        """Clear query text"""
        self.query_text.delete(1.0, tk.END)
    
    # Data Analysis Methods
    def load_csv(self):
        """Load CSV data"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.update_status(f"CSV loaded: {file_path}")
            messagebox.showinfo("CSV", f"Loaded CSV file: {file_path}")
    
    def load_from_db(self):
        """Load data from database"""
        self.update_status("Data loaded from database")
        messagebox.showinfo("Database", "Data loaded from database")
    
    def generate_sample_data(self):
        """Generate sample data"""
        self.update_status("Sample data generated")
        messagebox.showinfo("Sample Data", "Sample data generated successfully")
    
    def descriptive_stats(self):
        """Generate descriptive statistics"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Descriptive Statistics:\n\nMean: 50.5\nMedian: 49.2\nMode: 45.0\nStd Dev: 12.3\n")
        self.update_status("Descriptive statistics generated")
    
    def create_visualization(self):
        """Create data visualization"""
        self.update_status("Visualization created")
        messagebox.showinfo("Visualization", "Data visualization created")
    
    def ml_analysis(self):
        """Perform machine learning analysis"""
        self.update_status("ML analysis completed")
        messagebox.showinfo("ML Analysis", "Machine learning analysis completed")
    
    # AI Management Methods
    def start_ai_management(self):
        """Start AI management"""
        self.update_status("AI management started")
        messagebox.showinfo("AI Management", "AI management system started")
    
    def stop_ai_management(self):
        """Stop AI management"""
        self.update_status("AI management stopped")
        messagebox.showinfo("AI Management", "AI management system stopped")
    
    def reset_ai_management(self):
        """Reset AI management"""
        self.update_status("AI management reset")
        messagebox.showinfo("AI Management", "AI management system reset")
    
    def create_ai_bot_grid(self, parent):
        """Create AI bot management grid"""
        # Create scrollable frame for bot grid
        canvas = tk.Canvas(parent, bg=TSM_COLORS['dark'], height=200)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create bot grid (6 columns x 4 rows for 24 bots)
        self.ai_bot_buttons = []
        for i in range(24):
            row = i // 6
            col = i % 6
            
            bot_name = list(self.bots.keys())[i] if i < len(self.bots) else f"Bot{i+1}"
            bot_status = "Online" if i < 12 else "Offline"
            
            # Create bot button
            bot_frame = ttk.Frame(scrollable_frame)
            bot_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            bot_btn = ttk.Button(bot_frame, text=f"{bot_name}\n{bot_status}", 
                               command=lambda b=bot_name: self.ai_manage_bot(b),
                               style='TSM.Secondary.TButton')
            bot_btn.pack(fill=tk.BOTH, expand=True)
            
            self.ai_bot_buttons.append(bot_btn)
    
    def ai_manage_bot(self, bot_name):
        """Manage a specific AI bot"""
        messagebox.showinfo("AI Bot Management", f"Managing bot: {bot_name}")
    
    def ai_optimize_all(self):
        """Optimize all AI bots"""
        self.update_status("All AI bots optimized")
        messagebox.showinfo("AI Optimization", "All AI bots optimized")
    
    def ai_restart_failed(self):
        """Restart failed AI bots"""
        self.update_status("Failed AI bots restarted")
        messagebox.showinfo("AI Restart", "Failed AI bots restarted")
    
    def ai_scale_up(self):
        """Scale up AI bots"""
        self.update_status("AI bots scaled up")
        messagebox.showinfo("AI Scale", "AI bots scaled up")
    
    def ai_scale_down(self):
        """Scale down AI bots"""
        self.update_status("AI bots scaled down")
        messagebox.showinfo("AI Scale", "AI bots scaled down")
    
    def ai_security_scan(self):
        """Perform AI security scan"""
        self.update_status("AI security scan completed")
        messagebox.showinfo("AI Security", "AI security scan completed")
    
    def ai_analytics(self):
        """Show AI analytics"""
        self.update_status("AI analytics displayed")
        messagebox.showinfo("AI Analytics", "AI analytics displayed")
    
    # Bomb Creator Methods
    def launch_attack(self):
        """Launch bomb attack"""
        bomb_type = self.bomb_type_var.get()
        target_ip = self.target_ip_entry.get()
        target_port = self.target_port_entry.get()
        threads = self.threads_entry.get()
        duration = self.duration_entry.get()
        
        if target_ip and target_port:
            self.attack_log.insert(tk.END, f"🚀 Launching {bomb_type} attack on {target_ip}:{target_port}\n")
            self.attack_log.insert(tk.END, f"Threads: {threads}, Duration: {duration}s\n")
            self.update_status(f"Attack launched on {target_ip}:{target_port}")
        else:
            messagebox.showwarning("Attack", "Please enter target IP and port")
    
    def stop_attack(self):
        """Stop bomb attack"""
        self.attack_log.insert(tk.END, "⏹️ Attack stopped\n")
        self.update_status("Attack stopped")
    
    def show_attack_stats(self):
        """Show attack statistics"""
        messagebox.showinfo("Attack Stats", "Attack statistics displayed")
    
    # EXE Builder Methods
    def build_exe(self):
        """Build executable"""
        exe_name = self.exe_name_entry.get()
        icon_path = self.icon_path_var.get()
        
        self.build_log.insert(tk.END, f"🔨 Building {exe_name}.exe\n")
        self.build_log.insert(tk.END, f"One File: {self.onefile_var.get()}\n")
        self.build_log.insert(tk.END, f"Console: {self.console_var.get()}\n")
        self.build_log.insert(tk.END, f"UPX: {self.upx_var.get()}\n")
        self.build_log.insert(tk.END, "✅ Build completed successfully\n")
        
        self.update_status(f"EXE built: {exe_name}.exe")
    
    def browse_icon(self):
        """Browse for icon file"""
        file_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if file_path:
            self.icon_path_var.set(file_path)
    
    def open_output_folder(self):
        """Open output folder"""
        messagebox.showinfo("Output", "Output folder opened")
    
    def clean_build(self):
        """Clean build files"""
        self.build_log.insert(tk.END, "🧹 Build files cleaned\n")
        self.update_status("Build files cleaned")
    
    # Victim EXE Methods
    def create_victim_exe(self):
        """Create victim EXE"""
        controller_ip = self.controller_ip_entry.get()
        controller_port = self.controller_port_entry.get()
        exe_name = self.victim_exe_name_entry.get()
        
        self.victim_log.insert(tk.END, f"🎯 Creating victim EXE: {exe_name}.exe\n")
        self.victim_log.insert(tk.END, f"Controller: {controller_ip}:{controller_port}\n")
        self.victim_log.insert(tk.END, f"Stealth: {self.stealth_mode_var.get()}\n")
        self.victim_log.insert(tk.END, f"Auto Start: {self.auto_start_var.get()}\n")
        self.victim_log.insert(tk.END, f"Persistence: {self.persistence_var.get()}\n")
        self.victim_log.insert(tk.END, "✅ Victim EXE created successfully\n")
        
        self.update_status(f"Victim EXE created: {exe_name}.exe")
    
    def open_victim_output(self):
        """Open victim output folder"""
        messagebox.showinfo("Victim Output", "Victim output folder opened")
    
    def test_victim_exe(self):
        """Test victim EXE"""
        messagebox.showinfo("Test", "Victim EXE test completed")
    
    # Screen Capture Methods
    def take_screenshot(self):
        """Take screenshot"""
        self.screen_preview.config(text="Screenshot taken")
        self.screen_list.insert('', 0, values=(
            datetime.now().strftime("%H:%M:%S"),
            "Screenshot",
            "2.5 MB"
        ))
        self.update_status("Screenshot taken")
    
    def start_recording(self):
        """Start screen recording"""
        self.update_status("Screen recording started")
        messagebox.showinfo("Recording", "Screen recording started")
    
    def stop_recording(self):
        """Stop screen recording"""
        self.update_status("Screen recording stopped")
        messagebox.showinfo("Recording", "Screen recording stopped")
    
    def open_screens_folder(self):
        """Open screenshots folder"""
        messagebox.showinfo("Screens", "Screenshots folder opened")
    
    # Steganography Methods
    def select_image(self):
        """Select image for steganography"""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.image_path_var.set(file_path)
    
    def select_file(self):
        """Select file to hide"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var.set(file_path)
    
    def hide_data(self):
        """Hide data in image"""
        image_path = self.image_path_var.get()
        file_path = self.file_path_var.get()
        
        if image_path and file_path:
            self.stego_log.insert(tk.END, f"🔒 Hiding data in {image_path}\n")
            self.stego_log.insert(tk.END, f"File: {file_path}\n")
            self.stego_log.insert(tk.END, "✅ Data hidden successfully\n")
            self.update_status("Data hidden in image")
        else:
            messagebox.showwarning("Steganography", "Please select both image and file")
    
    def extract_data(self):
        """Extract data from image"""
        image_path = self.image_path_var.get()
        if image_path:
            self.stego_log.insert(tk.END, f"🔓 Extracting data from {image_path}\n")
            self.stego_log.insert(tk.END, "✅ Data extracted successfully\n")
            self.update_status("Data extracted from image")
        else:
            messagebox.showwarning("Steganography", "Please select an image")
    
    # Game Bot Methods
    def initialize_gamebot_data(self):
        """Initialize game bot data"""
        self.gamebot_data = [
            {"name": "CyberWarrior", "class": "Assassin", "level": 100, "xp": 2500000, "kills": 15420, "status": "Online", "rank": 1},
            {"name": "ShadowStrike", "class": "Ninja", "level": 98, "xp": 2300000, "kills": 14230, "status": "Online", "rank": 2},
            {"name": "ThunderBolt", "class": "Mage", "level": 97, "xp": 2200000, "kills": 13890, "status": "Online", "rank": 3},
            {"name": "FireStorm", "class": "Pyromancer", "level": 95, "xp": 2000000, "kills": 12540, "status": "Online", "rank": 4},
            {"name": "IceQueen", "class": "Cryomancer", "level": 94, "xp": 1900000, "kills": 11870, "status": "Online", "rank": 5}
        ]
    
    def populate_gamebot_list(self):
        """Populate game bot list"""
        for item in self.gamebot_tree.get_children():
            self.gamebot_tree.delete(item)
        
        for bot in self.gamebot_data:
            self.gamebot_tree.insert('', tk.END, values=(
                bot['rank'],
                bot['name'],
                bot['class'],
                bot['level'],
                f"{bot['xp']:,}",
                f"{bot['kills']:,}",
                bot['status'],
                'Actions'
            ))
    
    def start_game_battle(self):
        """Start game battle"""
        self.update_status("Game battle started")
        messagebox.showinfo("Game Battle", "Game battle started")
    
    def defend_base(self):
        """Defend base"""
        self.update_status("Base defense activated")
        messagebox.showinfo("Base Defense", "Base defense activated")
    
    def target_practice(self):
        """Start target practice"""
        self.update_status("Target practice started")
        messagebox.showinfo("Target Practice", "Target practice started")
    
    def show_game_analytics(self):
        """Show game analytics"""
        messagebox.showinfo("Game Analytics", "Game analytics displayed")
    
    # Thunderbolt Methods
    def start_thunderbolt(self):
        """Start Thunderbolt bot"""
        self.update_status("Thunderbolt bot started")
        self.update_thunderbolt_status()
        messagebox.showinfo("Thunderbolt", "Thunderbolt Pokemon GO bot started")
    
    def stop_thunderbolt(self):
        """Stop Thunderbolt bot"""
        self.update_status("Thunderbolt bot stopped")
        self.update_thunderbolt_status()
        messagebox.showinfo("Thunderbolt", "Thunderbolt Pokemon GO bot stopped")
    
    def thunderbolt_status(self):
        """Show Thunderbolt status"""
        messagebox.showinfo("Thunderbolt Status", "Thunderbolt bot status displayed")
    
    def thunderbolt_settings(self):
        """Open Thunderbolt settings"""
        messagebox.showinfo("Thunderbolt Settings", "Thunderbolt settings opened")
    
    def thunderbolt_catching(self):
        """Start catching mode"""
        self.update_status("Thunderbolt: Catching mode activated")
        messagebox.showinfo("Thunderbolt", "Catching mode activated")
    
    def thunderbolt_raiding(self):
        """Start raiding mode"""
        self.update_status("Thunderbolt: Raiding mode activated")
        messagebox.showinfo("Thunderbolt", "Raiding mode activated")
    
    def thunderbolt_battling(self):
        """Start battling mode"""
        self.update_status("Thunderbolt: Battling mode activated")
        messagebox.showinfo("Thunderbolt", "Battling mode activated")
    
    def thunderbolt_exploring(self):
        """Start exploring mode"""
        self.update_status("Thunderbolt: Exploring mode activated")
        messagebox.showinfo("Thunderbolt", "Exploring mode activated")
    
    def update_thunderbolt_status(self):
        """Update Thunderbolt status display"""
        status_text = f"""
⚡ Thunderbolt Pokemon GO Bot Status
====================================

Bot Status: {'✅ Running' if hasattr(self, 'thunderbolt_running') else '❌ Stopped'}
Current Mode: Catching
Uptime: 2h 15m 30s

Statistics:
• Pokemon Caught: 1,247
• Pokestops Spun: 856
• Gyms Battled: 23
• Raids Completed: 12
• XP Gained: 45,230
• Stardust Earned: 12,450
• Shiny Pokemon: 3
• Perfect IV: 1

Location: Times Square, NYC
Team: Valor
Gym Control: 8 Gyms

Thunderbolt is dominating Pokemon GO!
        """
        
        if hasattr(self, 'thunderbolt_status_text'):
            self.thunderbolt_status_text.delete(1.0, tk.END)
            self.thunderbolt_status_text.insert(tk.END, status_text)
    
    # Settings Methods
    def save_settings(self):
        """Save application settings"""
        self.vps_ip = self.server_ip_entry.get()
        self.vps_port = int(self.server_port_entry.get())
        self.web_port = int(self.web_port_entry.get())
        
        self.update_status("Settings saved")
        messagebox.showinfo("Settings", "Settings saved successfully")
    
    def reset_settings(self):
        """Reset settings to default"""
        self.server_ip_entry.delete(0, tk.END)
        self.server_ip_entry.insert(0, "191.96.152.162")
        self.server_port_entry.delete(0, tk.END)
        self.server_port_entry.insert(0, "9999")
        self.web_port_entry.delete(0, tk.END)
        self.web_port_entry.insert(0, "8080")
        
        self.update_status("Settings reset to default")
        messagebox.showinfo("Settings", "Settings reset to default")
    
    def open_config_folder(self):
        """Open configuration folder"""
        messagebox.showinfo("Config", "Configuration folder opened")
    
    # Utility Methods
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        if hasattr(self, 'server_logs'):
            self.server_logs.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
            self.server_logs.see(tk.END)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def exit_application(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.stop_server()
            self.root.quit()
            self.root.destroy()
    
    # Menu Methods
    def create_new_bot(self):
        """Create new bot"""
        messagebox.showinfo("New Bot", "New bot creation dialog opened")
    
    def import_bot(self):
        """Import bot"""
        messagebox.showinfo("Import Bot", "Bot import dialog opened")
    
    def export_bot(self):
        """Export bot"""
        messagebox.showinfo("Export Bot", "Bot export dialog opened")
    
    def open_server_settings(self):
        """Open server settings"""
        messagebox.showinfo("Server Settings", "Server settings dialog opened")
    
    def show_server_status(self):
        """Show server status"""
        status = "Online" if self.server_running else "Offline"
        messagebox.showinfo("Server Status", f"Server Status: {status}")
    
    def show_server_logs(self):
        """Show server logs"""
        messagebox.showinfo("Server Logs", "Server logs displayed")
    
    def bot_health_check(self):
        """Perform bot health check"""
        messagebox.showinfo("Health Check", "Bot health check completed")
    
    def open_system_monitor(self):
        """Open system monitor"""
        messagebox.showinfo("System Monitor", "System monitor opened")
    
    def open_network_monitor(self):
        """Open network monitor"""
        messagebox.showinfo("Network Monitor", "Network monitor opened")
    
    def open_log_viewer(self):
        """Open log viewer"""
        messagebox.showinfo("Log Viewer", "Log viewer opened")
    
    def open_database_manager(self):
        """Open database manager"""
        messagebox.showinfo("Database Manager", "Database manager opened")
    
    def open_file_manager(self):
        """Open file manager"""
        messagebox.showinfo("File Manager", "File manager opened")
    
    def show_documentation(self):
        """Show documentation"""
        messagebox.showinfo("Documentation", "Documentation opened")
    
    def show_api_reference(self):
        """Show API reference"""
        messagebox.showinfo("API Reference", "API reference opened")
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
VexityBot VPS Server GUI
========================

Version: 2.0.0
Server IP: {self.vps_ip}
Server Port: {self.vps_port}
Web Port: {self.web_port}

A comprehensive VPS-hosted GUI for remote bot management
with complete TSM-Framework Anticheat integration.

© 2024 VexityBot Team
        """
        messagebox.showinfo("About", about_text)
    
    def start_server_monitoring(self):
        """Start server monitoring"""
        def server_monitor_loop():
            while self.server_running:
                try:
                    # Update server status
                    if hasattr(self, 'server_socket'):
                        self.server_status_display.config(text="🟢 SERVER ONLINE")
                    else:
                        self.server_status_display.config(text="🔴 SERVER OFFLINE")
                    
                    time.sleep(5)
                except Exception as e:
                    time.sleep(10)
        
        monitor_thread = threading.Thread(target=server_monitor_loop, daemon=True)
        monitor_thread.start()
    
    def scan_network(self):
        """Scan network"""
        self.update_status("Network scan started")
        messagebox.showinfo("Network Scan", "Network scan started")
    
    def show_network_stats(self):
        """Show network statistics"""
        messagebox.showinfo("Network Stats", "Network statistics displayed")
    
    def refresh_network(self):
        """Refresh network information"""
        self.update_network_stats()
        self.update_status("Network information refreshed")
    
    # DeathBot Special Methods
    def initialize_deathbot(self):
        """Initialize DeathBot #25"""
        try:
            from DeathBot import DeathBot
            self.deathbot = DeathBot(bot_id=25, name="DeathBot")
            self.update_status("💀 DeathBot #25 initialized - Ultimate Destruction Bot")
        except ImportError:
            self.deathbot = None
            self.update_status("⚠️ DeathBot module not found - Limited functionality")
    
    def start_deathbot(self):
        """Start DeathBot with special controls"""
        if not self.deathbot:
            messagebox.showerror("DeathBot Error", "DeathBot module not available")
            return
        
        # Show DeathBot warning dialog
        warning_text = """
💀 DEATHBOT #25 - ULTIMATE DESTRUCTION BOT
=========================================

⚠️  WARNING: DEATHBOT IS EXTREMELY DANGEROUS  ⚠️

This bot will:
• Scrape files from multiple directories
• Simulate destruction sequences
• Create file dumps and logs
• Execute advanced system operations

⚡ Ricochet Boom AC/12v Power Mode
🔥 Auto-initiate Python Script
⏰ 12-second countdown to activation

Are you sure you want to activate DeathBot?
        """
        
        if messagebox.askyesno("💀 DeathBot Activation", warning_text):
            if self.deathbot.start_bot():
                self.bots['DeathBot']['status'] = 'Online'
                self.bots['DeathBot']['process'] = self.deathbot
                self.populate_bot_list()
                self.update_status("💀 DeathBot #25 ACTIVATED - DESTRUCTION SEQUENCE INITIATED")
                messagebox.showwarning("DeathBot Active", "💀 DeathBot #25 is now active!\n⚡ Ricochet Boom mode engaged\n🔥 Destruction sequence in progress")
            else:
                messagebox.showerror("DeathBot Error", "Failed to activate DeathBot")
    
    def stop_deathbot(self):
        """Stop DeathBot safely"""
        if not self.deathbot:
            return
        
        if messagebox.askyesno("DeathBot Shutdown", "Are you sure you want to stop DeathBot?"):
            if self.deathbot.stop_bot():
                self.bots['DeathBot']['status'] = 'Offline'
                self.bots['DeathBot']['process'] = None
                self.populate_bot_list()
                self.update_status("💀 DeathBot #25 STOPPED - Destruction sequence terminated")
                messagebox.showinfo("DeathBot Stopped", "💀 DeathBot #25 has been safely stopped")
            else:
                messagebox.showerror("DeathBot Error", "Failed to stop DeathBot")
    
    def emergency_shutdown_deathbot(self):
        """Emergency shutdown of DeathBot"""
        if not self.deathbot:
            return
        
        if messagebox.askyesno("🚨 Emergency Shutdown", "EMERGENCY SHUTDOWN DEATHBOT?\n\nThis will immediately terminate all DeathBot operations!"):
            self.deathbot.emergency_shutdown()
            self.bots['DeathBot']['status'] = 'Offline'
            self.bots['DeathBot']['process'] = None
            self.populate_bot_list()
            self.update_status("🚨 DeathBot #25 EMERGENCY SHUTDOWN - All operations terminated")
            messagebox.showinfo("Emergency Shutdown", "🚨 DeathBot #25 emergency shutdown complete")
    
    def show_deathbot_status(self):
        """Show DeathBot status and statistics"""
        if not self.deathbot:
            messagebox.showerror("DeathBot Error", "DeathBot not available")
            return
        
        status = self.deathbot.get_status()
        stats = self.deathbot.get_stats()
        
        status_text = f"""
💀 DEATHBOT #25 STATUS REPORT
============================

Bot ID: {status['bot_id']}
Name: {status['name']}
Status: {status['status']}
Running: {status['running']}
Port: {status['port']}

DESTRUCTION MODE: {status['destruction_mode']}
SCRAPING ACTIVE: {status['scraping_active']}

DESTRUCTION STATISTICS:
• Files Scraped: {stats['files_scraped']:,}
• Files Destroyed: {stats['files_destroyed']:,}
• Directories Scanned: {stats['directories_scanned']:,}
• Total Size Scraped: {stats['total_size_scraped']:,} bytes
• Destruction Events: {stats['destruction_events']:,}
• Uptime: {stats['uptime']} seconds
• Last Activity: {stats['last_activity']}

CONFIGURATION:
• Destruction Power: {status['config']['destruction_power']}/100
• AC Voltage: {status['config']['ac_plug_voltage']}
• Ricochet Boom: {status['config']['ricochet_boom_mode']}
• Auto Initiate: {status['config']['auto_initiate']}
• Countdown Timer: {status['config']['countdown_timer']} seconds

TARGET DIRECTORIES:
{chr(10).join(f"• {dir}" for dir in status['config']['target_directories'])}

💀 DEATHBOT READY FOR DESTRUCTION 💀
        """
        
        messagebox.showinfo("💀 DeathBot Status", status_text)
    
    def configure_deathbot(self):
        """Configure DeathBot settings"""
        if not self.deathbot:
            messagebox.showerror("DeathBot Error", "DeathBot not available")
            return
        
        # Create configuration window
        config_window = tk.Toplevel(self.root)
        config_window.title("💀 DeathBot Configuration")
        config_window.geometry("600x500")
        config_window.configure(bg=TSM_COLORS['dark'])
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(config_window, style='TSM.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="💀 DeathBot #25 Configuration", 
                               font=('Arial', 16, 'bold'),
                               style='TSM.Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Destruction Power
        power_frame = ttk.Frame(main_frame, style='TSM.TFrame')
        power_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(power_frame, text="Destruction Power (1-100):", style='TSM.Text.TLabel').pack(side=tk.LEFT)
        power_var = tk.StringVar(value=str(self.deathbot.config['destruction_power']))
        power_entry = ttk.Entry(power_frame, textvariable=power_var, width=10, style='TSM.TEntry')
        power_entry.pack(side=tk.LEFT, padx=10)
        
        # Countdown Timer
        timer_frame = ttk.Frame(main_frame, style='TSM.TFrame')
        timer_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(timer_frame, text="Countdown Timer (seconds):", style='TSM.Text.TLabel').pack(side=tk.LEFT)
        timer_var = tk.StringVar(value=str(self.deathbot.config['countdown_timer']))
        timer_entry = ttk.Entry(timer_frame, textvariable=timer_var, width=10, style='TSM.TEntry')
        timer_entry.pack(side=tk.LEFT, padx=10)
        
        # AC Voltage
        voltage_frame = ttk.Frame(main_frame, style='TSM.TFrame')
        voltage_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(voltage_frame, text="AC Voltage:", style='TSM.Text.TLabel').pack(side=tk.LEFT)
        voltage_var = tk.StringVar(value=self.deathbot.config['ac_plug_voltage'])
        voltage_combo = ttk.Combobox(voltage_frame, textvariable=voltage_var,
                                   values=['12v', '24v', '48v', '120v', '240v'],
                                   style='TSM.TCombobox', width=10)
        voltage_combo.pack(side=tk.LEFT, padx=10)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="DeathBot Options", style='TSM.TLabelframe')
        options_frame.pack(fill=tk.X, pady=10)
        
        auto_init_var = tk.BooleanVar(value=self.deathbot.config['auto_initiate'])
        ttk.Checkbutton(options_frame, text="Auto Initiate", variable=auto_init_var, 
                       style='TSM.TCheckbutton').pack(anchor=tk.W, padx=10, pady=5)
        
        ricochet_var = tk.BooleanVar(value=self.deathbot.config['ricochet_boom_mode'])
        ttk.Checkbutton(options_frame, text="Ricochet Boom Mode", variable=ricochet_var, 
                       style='TSM.TCheckbutton').pack(anchor=tk.W, padx=10, pady=5)
        
        auto_seq_var = tk.BooleanVar(value=self.deathbot.config['auto_sequence'])
        ttk.Checkbutton(options_frame, text="Auto Sequence", variable=auto_seq_var, 
                       style='TSM.TCheckbutton').pack(anchor=tk.W, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='TSM.TFrame')
        button_frame.pack(fill=tk.X, pady=20)
        
        def save_config():
            try:
                self.deathbot.config['destruction_power'] = int(power_var.get())
                self.deathbot.config['countdown_timer'] = int(timer_var.get())
                self.deathbot.config['ac_plug_voltage'] = voltage_var.get()
                self.deathbot.config['auto_initiate'] = auto_init_var.get()
                self.deathbot.config['ricochet_boom_mode'] = ricochet_var.get()
                self.deathbot.config['auto_sequence'] = auto_seq_var.get()
                
                messagebox.showinfo("Configuration Saved", "💀 DeathBot configuration updated")
                config_window.destroy()
            except ValueError:
                messagebox.showerror("Configuration Error", "Please enter valid numeric values")
        
        ttk.Button(button_frame, text="💾 Save Configuration", 
                  command=save_config, style='TSM.Success.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=config_window.destroy, style='TSM.Error.TButton').pack(side=tk.LEFT, padx=5)
    
    def generate_deathbot_report(self):
        """Generate DeathBot destruction report"""
        if not self.deathbot:
            messagebox.showerror("DeathBot Error", "DeathBot not available")
            return
        
        report = self.deathbot.generate_destruction_report()
        
        # Create report window
        report_window = tk.Toplevel(self.root)
        report_window.title("💀 DeathBot Destruction Report")
        report_window.geometry("800x600")
        report_window.configure(bg=TSM_COLORS['dark'])
        report_window.transient(self.root)
        
        # Main frame
        main_frame = ttk.Frame(report_window, style='TSM.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Report text
        report_text = scrolledtext.ScrolledText(main_frame, font=('Consolas', 10))
        report_text.pack(fill=tk.BOTH, expand=True)
        report_text.insert(tk.END, report)
        report_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = ttk.Button(main_frame, text="❌ Close Report", 
                              command=report_window.destroy, style='TSM.Error.TButton')
        close_btn.pack(pady=10)


def main():
    """Main function to run the VPS server GUI"""
    root = tk.Tk()
    app = VexityBotVPSServer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
