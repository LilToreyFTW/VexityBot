# ADDED - VexityBot Steganography GUI Module
# This module provides GUI components for the steganography functionality

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from VexityBotSteganography import VexityBotSteganography

class VexityBotSteganographyGUI:
    """GUI for VexityBot Steganography functionality"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.stego = VexityBotSteganography()
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the steganography GUI components"""
        
        # Main frame
        main_frame = ttk.Frame(self.parent_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🖼️ VexityBot Steganography", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for different functions
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Hide Script in Image
        self.create_hide_script_tab(notebook)
        
        # Tab 2: Create Payload
        self.create_payload_tab(notebook)
        
        # Tab 3: Image Validator
        self.create_validator_tab(notebook)
        
        # Tab 4: PowerShell Scripts
        self.create_scripts_tab(notebook)
    
    def create_hide_script_tab(self, notebook):
        """Create tab for hiding scripts in images"""
        
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Hide Script")
        
        # Script selection
        script_frame = ttk.LabelFrame(frame, text="PowerShell Script", padding=10)
        script_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(script_frame, text="Script File:").pack(anchor=tk.W)
        script_path_frame = ttk.Frame(script_frame)
        script_path_frame.pack(fill=tk.X, pady=5)
        
        self.script_path_var = tk.StringVar()
        script_entry = ttk.Entry(script_path_frame, textvariable=self.script_path_var, width=50)
        script_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(script_path_frame, text="Browse", 
                  command=self.browse_script_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Image selection
        image_frame = ttk.LabelFrame(frame, text="Image File", padding=10)
        image_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(image_frame, text="Image File:").pack(anchor=tk.W)
        image_path_frame = ttk.Frame(image_frame)
        image_path_frame.pack(fill=tk.X, pady=5)
        
        self.image_path_var = tk.StringVar()
        image_entry = ttk.Entry(image_path_frame, textvariable=self.image_path_var, width=50)
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(image_path_frame, text="Browse", 
                  command=self.browse_image_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Output selection
        output_frame = ttk.LabelFrame(frame, text="Output", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output Image:").pack(anchor=tk.W)
        output_path_frame = ttk.Frame(output_frame)
        output_path_frame.pack(fill=tk.X, pady=5)
        
        self.output_path_var = tk.StringVar()
        output_entry = ttk.Entry(output_path_frame, textvariable=self.output_path_var, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(output_path_frame, text="Browse", 
                  command=self.browse_output_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Execution path
        exec_frame = ttk.Frame(output_frame)
        exec_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(exec_frame, text="Execution Path:").pack(anchor=tk.W)
        self.exec_path_var = tk.StringVar()
        exec_entry = ttk.Entry(exec_frame, textvariable=self.exec_path_var, width=50)
        exec_entry.pack(fill=tk.X, pady=2)
        
        # Process button
        process_frame = ttk.Frame(frame)
        process_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(process_frame, text="Hide Script in Image", 
                  command=self.hide_script, style="Accent.TButton").pack(side=tk.LEFT)
        
        ttk.Button(process_frame, text="Clear All", 
                  command=self.clear_hide_form).pack(side=tk.RIGHT)
        
        # Results area
        results_frame = ttk.LabelFrame(frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_payload_tab(self, notebook):
        """Create tab for creating payloads"""
        
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Create Payload")
        
        # Payload type selection
        type_frame = ttk.LabelFrame(frame, text="Payload Type", padding=10)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.payload_type_var = tk.StringVar(value="simple")
        
        ttk.Radiobutton(type_frame, text="Simple Payload (Script Content)", 
                       variable=self.payload_type_var, value="simple").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Advanced Payload (Script File)", 
                       variable=self.payload_type_var, value="advanced").pack(anchor=tk.W)
        
        # Script content/file
        script_frame = ttk.LabelFrame(frame, text="Script", padding=10)
        script_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Script content text area
        ttk.Label(script_frame, text="Script Content:").pack(anchor=tk.W)
        self.script_content_text = scrolledtext.ScrolledText(script_frame, height=8, width=80)
        self.script_content_text.pack(fill=tk.X, pady=5)
        
        # Script file selection (for advanced)
        self.script_file_frame = ttk.Frame(script_frame)
        self.script_file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.script_file_frame, text="Or Script File:").pack(anchor=tk.W)
        script_file_path_frame = ttk.Frame(self.script_file_frame)
        script_file_path_frame.pack(fill=tk.X, pady=2)
        
        self.script_file_var = tk.StringVar()
        script_file_entry = ttk.Entry(script_file_path_frame, textvariable=self.script_file_var, width=50)
        script_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(script_file_path_frame, text="Browse", 
                  command=self.browse_script_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Image selection
        image_frame = ttk.LabelFrame(frame, text="Image File", padding=10)
        image_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(image_frame, text="Image File:").pack(anchor=tk.W)
        image_path_frame = ttk.Frame(image_frame)
        image_path_frame.pack(fill=tk.X, pady=5)
        
        self.payload_image_var = tk.StringVar()
        image_entry = ttk.Entry(image_path_frame, textvariable=self.payload_image_var, width=50)
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(image_path_frame, text="Browse", 
                  command=self.browse_payload_image).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Output selection
        output_frame = ttk.LabelFrame(frame, text="Output", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output Image:").pack(anchor=tk.W)
        output_path_frame = ttk.Frame(output_frame)
        output_path_frame.pack(fill=tk.X, pady=5)
        
        self.payload_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_path_frame, textvariable=self.payload_output_var, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(output_path_frame, text="Browse", 
                  command=self.browse_payload_output).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Process button
        process_frame = ttk.Frame(frame)
        process_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(process_frame, text="Create Payload", 
                  command=self.create_payload, style="Accent.TButton").pack(side=tk.LEFT)
        
        ttk.Button(process_frame, text="Clear All", 
                  command=self.clear_payload_form).pack(side=tk.RIGHT)
        
        # Results area
        results_frame = ttk.LabelFrame(frame, text="Generated Payload", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.payload_results_text = scrolledtext.ScrolledText(results_frame, height=10, width=80)
        self.payload_results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_validator_tab(self, notebook):
        """Create tab for image validation"""
        
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Image Validator")
        
        # Image selection
        image_frame = ttk.LabelFrame(frame, text="Image File", padding=10)
        image_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(image_frame, text="Image File:").pack(anchor=tk.W)
        image_path_frame = ttk.Frame(image_frame)
        image_path_frame.pack(fill=tk.X, pady=5)
        
        self.validator_image_var = tk.StringVar()
        image_entry = ttk.Entry(image_path_frame, textvariable=self.validator_image_var, width=50)
        image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(image_path_frame, text="Browse", 
                  command=self.browse_validator_image).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Validate button
        validate_frame = ttk.Frame(frame)
        validate_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(validate_frame, text="Validate Image", 
                  command=self.validate_image, style="Accent.TButton").pack(side=tk.LEFT)
        
        ttk.Button(validate_frame, text="Clear", 
                  command=self.clear_validator_form).pack(side=tk.RIGHT)
        
        # Results area
        results_frame = ttk.LabelFrame(frame, text="Validation Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.validator_results_text = scrolledtext.ScrolledText(results_frame, height=10, width=80)
        self.validator_results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_scripts_tab(self, notebook):
        """Create tab for PowerShell scripts"""
        
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="PowerShell Scripts")
        
        # Scripts info
        info_frame = ttk.LabelFrame(frame, text="Available Scripts", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        info_text = """
Available PowerShell Scripts:

1. Invoke-PixelScript.ps1 - Main steganography function
   Usage: Invoke-PixelScript -Script "script.ps1" -Image "image.png" -Out "output.png"

2. calc.ps1 - Sample calculator script for demonstration
   A simple calculator that can be hidden in images

3. Generated Payloads - Custom scripts created through the interface
"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W)
        
        # Script viewer
        viewer_frame = ttk.LabelFrame(frame, text="Script Viewer", padding=10)
        viewer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Script selection
        script_select_frame = ttk.Frame(viewer_frame)
        script_select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(script_select_frame, text="Select Script:").pack(side=tk.LEFT)
        
        self.script_viewer_var = tk.StringVar()
        script_combo = ttk.Combobox(script_select_frame, textvariable=self.script_viewer_var, 
                                   values=["Invoke-PixelScript.ps1", "calc.ps1"], width=30)
        script_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Button(script_select_frame, text="Load Script", 
                  command=self.load_script).pack(side=tk.LEFT, padx=(5, 0))
        
        # Script content
        self.script_viewer_text = scrolledtext.ScrolledText(viewer_frame, height=15, width=80)
        self.script_viewer_text.pack(fill=tk.BOTH, expand=True, pady=5)
    
    # Event handlers
    def browse_script_file(self):
        """Browse for script file"""
        filename = filedialog.askopenfilename(
            title="Select PowerShell Script",
            filetypes=[("PowerShell Scripts", "*.ps1"), ("All Files", "*.*")]
        )
        if filename:
            self.script_path_var.set(filename)
    
    def browse_image_file(self):
        """Browse for image file"""
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")]
        )
        if filename:
            self.image_path_var.set(filename)
    
    def browse_output_file(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            title="Save Output Image",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            self.output_path_var.set(filename)
    
    def browse_payload_image(self):
        """Browse for payload image file"""
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")]
        )
        if filename:
            self.payload_image_var.set(filename)
    
    def browse_payload_output(self):
        """Browse for payload output file"""
        filename = filedialog.asksaveasfilename(
            title="Save Output Image",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            self.payload_output_var.set(filename)
    
    def browse_validator_image(self):
        """Browse for validator image file"""
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")]
        )
        if filename:
            self.validator_image_var.set(filename)
    
    def hide_script(self):
        """Hide script in image"""
        try:
            script_path = self.script_path_var.get()
            image_path = self.image_path_var.get()
            output_path = self.output_path_var.get()
            exec_path = self.exec_path_var.get() or output_path
            
            if not all([script_path, image_path, output_path]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Hide the script
            ps_command = self.stego.hide_script_in_image(script_path, image_path, output_path, exec_path)
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "✅ Script successfully hidden in image!\n\n")
            self.results_text.insert(tk.END, f"Output Image: {output_path}\n")
            self.results_text.insert(tk.END, f"Execution Path: {exec_path}\n\n")
            self.results_text.insert(tk.END, "PowerShell Execution Command:\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n")
            self.results_text.insert(tk.END, ps_command)
            
            messagebox.showinfo("Success", "Script successfully hidden in image!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to hide script: {str(e)}")
    
    def create_payload(self):
        """Create steganography payload"""
        try:
            payload_type = self.payload_type_var.get()
            image_path = self.payload_image_var.get()
            output_path = self.payload_output_var.get()
            
            if not all([image_path, output_path]):
                messagebox.showerror("Error", "Please fill in image and output paths")
                return
            
            if payload_type == "simple":
                script_content = self.script_content_text.get(1.0, tk.END).strip()
                if not script_content:
                    messagebox.showerror("Error", "Please enter script content")
                    return
                
                ps_command = self.stego.create_simple_payload(script_content, image_path, output_path)
                
                self.payload_results_text.delete(1.0, tk.END)
                self.payload_results_text.insert(tk.END, "✅ Simple payload created!\n\n")
                self.payload_results_text.insert(tk.END, f"Output Image: {output_path}\n\n")
                self.payload_results_text.insert(tk.END, "PowerShell Execution Command:\n")
                self.payload_results_text.insert(tk.END, "=" * 50 + "\n")
                self.payload_results_text.insert(tk.END, ps_command)
                
            else:  # advanced
                script_file = self.script_file_var.get()
                if not script_file:
                    messagebox.showerror("Error", "Please select a script file")
                    return
                
                ps_command, batch_path = self.stego.create_advanced_payload(
                    script_file, image_path, output_path
                )
                
                self.payload_results_text.delete(1.0, tk.END)
                self.payload_results_text.insert(tk.END, "✅ Advanced payload created!\n\n")
                self.payload_results_text.insert(tk.END, f"Output Image: {output_path}\n")
                self.payload_results_text.insert(tk.END, f"Batch File: {batch_path}\n\n")
                self.payload_results_text.insert(tk.END, "PowerShell Execution Command:\n")
                self.payload_results_text.insert(tk.END, "=" * 50 + "\n")
                self.payload_results_text.insert(tk.END, ps_command)
            
            messagebox.showinfo("Success", "Payload created successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create payload: {str(e)}")
    
    def validate_image(self):
        """Validate image for steganography"""
        try:
            image_path = self.validator_image_var.get()
            if not image_path:
                messagebox.showerror("Error", "Please select an image file")
                return
            
            is_valid, message = self.stego.validate_image(image_path)
            max_size = self.stego.get_max_script_size(image_path)
            
            self.validator_results_text.delete(1.0, tk.END)
            
            if is_valid:
                self.validator_results_text.insert(tk.END, "✅ Image is valid for steganography!\n\n")
                self.validator_results_text.insert(tk.END, f"Status: {message}\n")
                self.validator_results_text.insert(tk.END, f"Maximum script size: {max_size} bytes\n")
                self.validator_results_text.insert(tk.END, f"Maximum script size: {max_size // 1024} KB\n")
            else:
                self.validator_results_text.insert(tk.END, "❌ Image is not valid for steganography!\n\n")
                self.validator_results_text.insert(tk.END, f"Error: {message}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to validate image: {str(e)}")
    
    def load_script(self):
        """Load script for viewing"""
        try:
            script_name = self.script_viewer_var.get()
            if not script_name:
                messagebox.showerror("Error", "Please select a script")
                return
            
            script_path = script_name
            if not os.path.exists(script_path):
                messagebox.showerror("Error", f"Script file not found: {script_path}")
                return
            
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.script_viewer_text.delete(1.0, tk.END)
            self.script_viewer_text.insert(tk.END, content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load script: {str(e)}")
    
    def clear_hide_form(self):
        """Clear hide script form"""
        self.script_path_var.set("")
        self.image_path_var.set("")
        self.output_path_var.set("")
        self.exec_path_var.set("")
        self.results_text.delete(1.0, tk.END)
    
    def clear_payload_form(self):
        """Clear payload form"""
        self.script_content_text.delete(1.0, tk.END)
        self.script_file_var.set("")
        self.payload_image_var.set("")
        self.payload_output_var.set("")
        self.payload_results_text.delete(1.0, tk.END)
    
    def clear_validator_form(self):
        """Clear validator form"""
        self.validator_image_var.set("")
        self.validator_results_text.delete(1.0, tk.END)
