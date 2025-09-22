#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel PDF Generator
Advanced PDF generation with LaTeX, syntax highlighting, and VNC integration
"""

import os
import sys
import subprocess
import tempfile
import shutil
import json
import base64
import zlib
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

class TSMPDFGenerator:
    """Advanced PDF Generator with LaTeX and syntax highlighting"""
    
    def __init__(self):
        self.supported_languages = {
            'Python': 'Python',
            'C++': 'C++',
            'Java': 'Java',
            'JavaScript': 'JavaScript',
            'C': 'C',
            'C#': 'CSharp',
            'PHP': 'PHP',
            'Ruby': 'Ruby',
            'Go': 'Go',
            'Rust': 'Rust',
            'SQL': 'SQL',
            'HTML': 'HTML',
            'CSS': 'CSS',
            'XML': 'XML',
            'JSON': 'JSON',
            'Bash': 'Bash',
            'PowerShell': 'PowerShell',
            'Assembly': 'Assembler',
            'MATLAB': 'Matlab',
            'R': 'R',
            'Scala': 'Scala',
            'Kotlin': 'Kotlin',
            'Swift': 'Swift',
            'TypeScript': 'TypeScript',
            'Lua': 'Lua',
            'Perl': 'Perl',
            'Haskell': 'Haskell',
            'Clojure': 'Clojure',
            'Erlang': 'Erlang',
            'F#': 'FSharp',
            'OCaml': 'OCaml',
            'Prolog': 'Prolog',
            'Verilog': 'Verilog',
            'VHDL': 'VHDL',
            'YAML': 'YAML',
            'TOML': 'TOML',
            'INI': 'INI',
            'Markdown': 'Markdown',
            'LaTeX': 'TeX',
            'Dockerfile': 'Dockerfile',
            'Makefile': 'Makefile'
        }
        
        self.color_schemes = {
            'default': {
                'background': 'white',
                'keywords': 'blue',
                'comments': 'green!60!black',
                'strings': 'red',
                'numbers': 'purple',
                'functions': 'orange'
            },
            'dark': {
                'background': 'black!90',
                'keywords': 'blue!80',
                'comments': 'green!60',
                'strings': 'red!80',
                'numbers': 'purple!80',
                'functions': 'orange!80'
            },
            'monokai': {
                'background': 'gray!10',
                'keywords': 'purple!80',
                'comments': 'gray!60',
                'strings': 'yellow!80',
                'numbers': 'orange!80',
                'functions': 'green!80'
            }
        }
    
    def generate_pdf_with_code(self, code, language, output_path, title="TSM-SeniorOasisPanel Code", 
                              color_scheme='default', include_line_numbers=True, font_size='small'):
        """Generate PDF with syntax-highlighted code using LaTeX"""
        try:
            # Create temporary LaTeX file
            temp_tex = tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8')
            
            # Escape special LaTeX characters in code
            escaped_code = self._escape_latex(code)
            
            # Get LaTeX language name
            latex_lang = self.supported_languages.get(language, 'Python')
            
            # Get color scheme
            colors = self.color_schemes.get(color_scheme, self.color_schemes['default'])
            
            # Generate LaTeX content
            latex_content = self._generate_latex_template(
                escaped_code, latex_lang, title, colors, include_line_numbers, font_size
            )
            
            temp_tex.write(latex_content)
            temp_tex.close()
            
            # Compile LaTeX to PDF
            result = subprocess.run([
                'pdflatex', '-interaction=nonstopmode', temp_tex.name
            ], capture_output=True, text=True, cwd=os.path.dirname(temp_tex.name))
            
            if result.returncode == 0:
                # Move PDF to output location
                pdf_path = temp_tex.name.replace('.tex', '.pdf')
                if os.path.exists(pdf_path):
                    shutil.move(pdf_path, output_path)
                    
                    # Clean up temporary files
                    self._cleanup_temp_files(temp_tex.name)
                    
                    return True, "PDF generated successfully!"
                else:
                    return False, "PDF file not found after compilation"
            else:
                error_msg = f"LaTeX compilation failed: {result.stderr}"
                return False, error_msg
                
        except FileNotFoundError:
            return False, "Error: pdflatex not found. Please install a LaTeX distribution (e.g., TeX Live, MiKTeX)"
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"
    
    def _generate_latex_template(self, code, language, title, colors, include_line_numbers, font_size):
        """Generate LaTeX template with syntax highlighting"""
        
        # Font size mapping
        font_sizes = {
            'tiny': '\\tiny',
            'small': '\\small',
            'normalsize': '\\normalsize',
            'large': '\\large',
            'Large': '\\Large'
        }
        
        font_size_cmd = font_sizes.get(font_size, '\\small')
        
        # Line numbers configuration
        numbers_config = "numbers=left, numberstyle=\\tiny\\color{gray}," if include_line_numbers else ""
        
        latex_content = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{listings}}
\\usepackage{{xcolor}}
\\usepackage{{geometry}}
\\usepackage{{fancyhdr}}
\\usepackage{{graphicx}}
\\geometry{{margin=1in}}

% Color definitions
\\definecolor{{bgcolor}}{{HTML}}{{f8f8f8}}
\\definecolor{{keywordcolor}}{{{colors['keywords']}}}
\\definecolor{{commentcolor}}{{{colors['comments']}}}
\\definecolor{{stringcolor}}{{{colors['strings']}}}
\\definecolor{{numbercolor}}{{{colors['numbers']}}}
\\definecolor{{functioncolor}}{{{colors['functions']}}}

% Listings configuration
\\lstset{{
    language={language},
    {numbers_config}
    stepnumber=1,
    numbersep=5pt,
    backgroundcolor=\\color{{bgcolor}},
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    frame=single,
    rulecolor=\\color{{gray!30}},
    tabsize=2,
    captionpos=b,
    breaklines=true,
    breakatwhitespace=false,
    keywordstyle=\\color{{keywordcolor}}\\bfseries,
    commentstyle=\\color{{commentcolor}}\\itshape,
    stringstyle=\\color{{stringcolor}},
    numberstyle=\\color{{numbercolor}},
    basicstyle={font_size_cmd}\\ttfamily,
    columns=fullflexible,
    keepspaces=true,
    xleftmargin=10pt,
    xrightmargin=10pt,
    aboveskip=10pt,
    belowskip=10pt
}}

% Header and footer
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{TSM-SeniorOasisPanel}}
\\fancyhead[R]{{\\today}}
\\fancyfoot[C]{{\\thepage}}

\\title{{\\textbf{{{title}}}}}
\\author{{TSM-SeniorOasisPanel PDF Generator}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\section*{{Source Code}}
\\begin{{lstlisting}}
{code}
\\end{{lstlisting}}

\\vspace{{1cm}}

\\section*{{Document Information}}
\\begin{{itemize}}
\\item \\textbf{{Language:}} {language}
\\item \\textbf{{Generated:}} \\today
\\item \\textbf{{Generator:}} TSM-SeniorOasisPanel PDF Generator
\\item \\textbf{{Color Scheme:}} {colors.get('background', 'default')}
\\item \\textbf{{Font Size:}} {font_size}
\\end{{itemize}}

\\vspace{{0.5cm}}

\\section*{{About TSM-SeniorOasisPanel}}
This PDF was generated using the TSM-SeniorOasisPanel system, which provides:
\\begin{{itemize}}
\\item Advanced file transfer capabilities
\\item VNC remote desktop integration
\\item Steganographic image embedding
\\item PDF generation with syntax highlighting
\\item Stealth mode operation
\\end{{itemize}}

\\end{{document}}"""
        
        return latex_content
    
    def generate_pdf_from_files(self, file_paths, output_path, title="TSM-SeniorOasisPanel Code Collection"):
        """Generate PDF from multiple source files"""
        try:
            all_code = []
            file_info = []
            
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Detect language from file extension
                    language = self._detect_language_from_extension(file_path)
                    
                    all_code.append(f"\\section{{{os.path.basename(file_path)}}}\\label{{file:{os.path.basename(file_path)}}}\n\\begin{{lstlisting}}[language={language}]\n{self._escape_latex(content)}\n\\end{{lstlisting}}\n")
                    file_info.append({
                        'name': os.path.basename(file_path),
                        'language': language,
                        'size': len(content)
                    })
            
            if not all_code:
                return False, "No valid files found"
            
            # Create combined LaTeX content
            combined_code = '\n'.join(all_code)
            
            # Generate PDF
            return self.generate_pdf_with_code(combined_code, 'Python', output_path, title)
            
        except Exception as e:
            return False, f"Error generating PDF from files: {str(e)}"
    
    def generate_pdf_with_screenshots(self, code, language, screenshots, output_path, title="TSM-SeniorOasisPanel Code with Screenshots"):
        """Generate PDF with code and embedded screenshots"""
        try:
            # Create temporary LaTeX file
            temp_tex = tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8')
            
            # Escape special LaTeX characters in code
            escaped_code = self._escape_latex(code)
            
            # Get LaTeX language name
            latex_lang = self.supported_languages.get(language, 'Python')
            
            # Process screenshots
            screenshot_latex = self._process_screenshots_for_latex(screenshots, os.path.dirname(temp_tex.name))
            
            # Generate LaTeX content with screenshots
            latex_content = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{listings}}
\\usepackage{{xcolor}}
\\usepackage{{geometry}}
\\usepackage{{graphicx}}
\\usepackage{{float}}
\\geometry{{margin=1in}}

\\lstset{{
    language={latex_lang},
    numbers=left,
    numberstyle=\\tiny\\color{{gray}},
    stepnumber=1,
    numbersep=5pt,
    backgroundcolor=\\color{{gray!10}},
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    frame=single,
    tabsize=2,
    captionpos=b,
    breaklines=true,
    breakatwhitespace=false,
    keywordstyle=\\color{{blue}}\\bfseries,
    commentstyle=\\color{{green!60!black}}\\itshape,
    stringstyle=\\color{{red}},
    basicstyle=\\small\\ttfamily,
    columns=fullflexible
}}

\\title{{\\textbf{{{title}}}}}
\\author{{TSM-SeniorOasisPanel}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\section*{{Source Code}}
\\begin{{lstlisting}}
{escaped_code}
\\end{{lstlisting}}

{screenshot_latex}

\\section*{{Generated by TSM-SeniorOasisPanel}}
This PDF was generated using the TSM-SeniorOasisPanel system with LaTeX and the listings package for syntax highlighting.

\\end{{document}}"""
            
            temp_tex.write(latex_content)
            temp_tex.close()
            
            # Compile LaTeX to PDF
            result = subprocess.run([
                'pdflatex', '-interaction=nonstopmode', temp_tex.name
            ], capture_output=True, text=True, cwd=os.path.dirname(temp_tex.name))
            
            if result.returncode == 0:
                # Move PDF to output location
                pdf_path = temp_tex.name.replace('.tex', '.pdf')
                if os.path.exists(pdf_path):
                    shutil.move(pdf_path, output_path)
                    
                    # Clean up temporary files
                    self._cleanup_temp_files(temp_tex.name)
                    
                    return True, "PDF with screenshots generated successfully!"
                else:
                    return False, "PDF file not found after compilation"
            else:
                error_msg = f"LaTeX compilation failed: {result.stderr}"
                return False, error_msg
                
        except Exception as e:
            return False, f"Error generating PDF with screenshots: {str(e)}"
    
    def _process_screenshots_for_latex(self, screenshots, temp_dir):
        """Process screenshots for LaTeX inclusion"""
        screenshot_latex = ""
        
        for i, screenshot in enumerate(screenshots):
            if isinstance(screenshot, str) and os.path.exists(screenshot):
                # Copy screenshot to temp directory
                screenshot_name = f"screenshot_{i}.png"
                screenshot_path = os.path.join(temp_dir, screenshot_name)
                shutil.copy2(screenshot, screenshot_path)
                
                screenshot_latex += f"""
\\section*{{Screenshot {i+1}}}
\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{screenshot_name}}}
\\caption{{Screenshot {i+1}}}
\\end{{figure}}
"""
            elif hasattr(screenshot, 'save'):  # PIL Image object
                screenshot_name = f"screenshot_{i}.png"
                screenshot_path = os.path.join(temp_dir, screenshot_name)
                screenshot.save(screenshot_path)
                
                screenshot_latex += f"""
\\section*{{Screenshot {i+1}}}
\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{screenshot_name}}}
\\caption{{Screenshot {i+1}}}
\\end{{figure}}
"""
        
        return screenshot_latex
    
    def _detect_language_from_extension(self, file_path):
        """Detect programming language from file extension"""
        extension_map = {
            '.py': 'Python',
            '.cpp': 'C++',
            '.c': 'C',
            '.java': 'Java',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.sql': 'SQL',
            '.html': 'HTML',
            '.css': 'CSS',
            '.xml': 'XML',
            '.json': 'JSON',
            '.sh': 'Bash',
            '.ps1': 'PowerShell',
            '.asm': 'Assembly',
            '.m': 'MATLAB',
            '.r': 'R',
            '.scala': 'Scala',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
            '.lua': 'Lua',
            '.pl': 'Perl',
            '.hs': 'Haskell',
            '.clj': 'Clojure',
            '.erl': 'Erlang',
            '.fs': 'F#',
            '.ml': 'OCaml',
            '.pro': 'Prolog',
            '.v': 'Verilog',
            '.vhdl': 'VHDL',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.toml': 'TOML',
            '.ini': 'INI',
            '.md': 'Markdown',
            '.tex': 'LaTeX',
            '.dockerfile': 'Dockerfile',
            'Dockerfile': 'Dockerfile',
            'Makefile': 'Makefile'
        }
        
        _, ext = os.path.splitext(file_path)
        return extension_map.get(ext.lower(), 'Python')
    
    def _escape_latex(self, text):
        """Escape special LaTeX characters"""
        replacements = {
            '\\': '\\textbackslash{}',
            '{': '\\{',
            '}': '\\}',
            '$': '\\$',
            '&': '\\&',
            '%': '\\%',
            '#': '\\#',
            '^': '\\textasciicircum{}',
            '_': '\\_',
            '~': '\\textasciitilde{}'
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def _cleanup_temp_files(self, tex_file):
        """Clean up temporary LaTeX files"""
        try:
            base_name = tex_file.replace('.tex', '')
            temp_files = [tex_file, f"{base_name}.aux", f"{base_name}.log", f"{base_name}.out", f"{base_name}.toc"]
            
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        except Exception:
            pass  # Silent cleanup
    
    def create_code_image(self, code, language, output_path, width=800, height=600, 
                         background_color='white', text_color='black', font_size=12):
        """Create an image with syntax-highlighted code"""
        try:
            # Create image
            img = Image.new('RGB', (width, height), background_color)
            draw = ImageDraw.Draw(img)
            
            # Try to load a monospace font
            try:
                font = ImageFont.truetype("consola.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("Courier New", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Split code into lines
            lines = code.split('\n')
            
            # Calculate line height
            line_height = font_size + 2
            max_lines = height // line_height
            
            # Draw code lines
            y = 10
            for i, line in enumerate(lines[:max_lines]):
                if y + line_height > height:
                    break
                
                # Simple syntax highlighting (basic implementation)
                colored_line = self._apply_simple_syntax_highlighting(line, language)
                
                # Draw line
                draw.text((10, y), line, fill=text_color, font=font)
                y += line_height
            
            # Save image
            img.save(output_path)
            return True, f"Code image created: {output_path}"
            
        except Exception as e:
            return False, f"Error creating code image: {str(e)}"
    
    def _apply_simple_syntax_highlighting(self, line, language):
        """Apply simple syntax highlighting to a line of code"""
        # This is a basic implementation
        # In a real scenario, you would use a proper syntax highlighter
        keywords = {
            'Python': ['def', 'class', 'if', 'else', 'for', 'while', 'import', 'from', 'return', 'True', 'False', 'None'],
            'C++': ['int', 'float', 'double', 'char', 'void', 'if', 'else', 'for', 'while', 'class', 'public', 'private'],
            'Java': ['public', 'private', 'protected', 'class', 'interface', 'if', 'else', 'for', 'while', 'return']
        }
        
        # For now, just return the original line
        # In a full implementation, you would parse and highlight keywords
        return line

def main():
    """Main function for testing PDF generation"""
    if len(sys.argv) < 4:
        print("Usage:")
        print("  Generate PDF: python TSM_PDFGenerator.py generate <code_file> <language> <output_pdf>")
        print("  Generate from files: python TSM_PDFGenerator.py files <file1> <file2> ... <output_pdf>")
        print("  Create code image: python TSM_PDFGenerator.py image <code_file> <output_image>")
        sys.exit(1)
    
    generator = TSMPDFGenerator()
    operation = sys.argv[1].lower()
    
    if operation == 'generate':
        if len(sys.argv) != 5:
            print("Usage: python TSM_PDFGenerator.py generate <code_file> <language> <output_pdf>")
            sys.exit(1)
        
        code_file = sys.argv[2]
        language = sys.argv[3]
        output_pdf = sys.argv[4]
        
        if not os.path.exists(code_file):
            print(f"Error: Code file '{code_file}' not found")
            sys.exit(1)
        
        with open(code_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        success, message = generator.generate_pdf_with_code(code, language, output_pdf)
        print(f"TSM-SeniorOasisPanel: {message}")
        
    elif operation == 'files':
        if len(sys.argv) < 4:
            print("Usage: python TSM_PDFGenerator.py files <file1> <file2> ... <output_pdf>")
            sys.exit(1)
        
        file_paths = sys.argv[2:-1]
        output_pdf = sys.argv[-1]
        
        success, message = generator.generate_pdf_from_files(file_paths, output_pdf)
        print(f"TSM-SeniorOasisPanel: {message}")
        
    elif operation == 'image':
        if len(sys.argv) != 4:
            print("Usage: python TSM_PDFGenerator.py image <code_file> <output_image>")
            sys.exit(1)
        
        code_file = sys.argv[2]
        output_image = sys.argv[3]
        
        if not os.path.exists(code_file):
            print(f"Error: Code file '{code_file}' not found")
            sys.exit(1)
        
        with open(code_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        success, message = generator.create_code_image(code, 'Python', output_image)
        print(f"TSM-SeniorOasisPanel: {message}")
        
    else:
        print("Invalid operation. Use 'generate', 'files', or 'image'")
        sys.exit(1)

if __name__ == "__main__":
    main()
