"""
Number Guessing Game with GUI
==============================
A complete multi-featured number guessing game using Python and Tkinter.

Features:
- User authentication (login/registration)
- Persistent data storage using MySQL
- Password hashing for security
- Game with configurable range
- Scoring system (lower attempts = better score)
- Global high score board (top 10 players)

Data Persistence:
- Uses MySQL database
- Stores: username, hashed password, and best score (lowest attempts)
- Passwords are hashed using SHA-256 from hashlib

Configuration:
- Database connection details stored in .env file
- Compatible with MySQL Workbench
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class NumberGuessingGame:
    """Main application class managing all game windows and functionality"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Number Guessing Game")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Color scheme
        self.colors = {
            'primary': '#6366f1',      # Indigo
            'secondary': '#8b5cf6',    # Purple
            'success': '#10b981',      # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Orange
            'info': '#3b82f6',         # Blue
            'dark': '#1f2937',         # Dark gray
            'light': '#f3f4f6',        # Light gray
            'bg_gradient_start': '#667eea',
            'bg_gradient_end': '#764ba2',
            'card_bg': '#ffffff',
            'text_dark': '#111827',
            'text_light': '#6b7280'
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['primary'])
        
        # Game configuration
        self.min_range = 1
        self.max_range = 100
        
        # Game state
        self.current_user = None
        self.target_number = None
        self.attempts = 0
        
        # Configure styles
        self.setup_styles()
        
        # Initialize database
        self.init_database()
        
        # Start with login screen
        self.show_login_screen()
    
    def init_database(self):
        """Initialize MySQL database and create users table if not exists"""
        try:
            # Get database configuration from environment variables
            self.db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', 3306)),
                'database': os.getenv('DB_NAME', 'number_guessing_game'),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD'),
                'autocommit': True
            }
            
            # Connect to MySQL server first (without database) to create database if needed
            temp_config = self.db_config.copy()
            database_name = temp_config.pop('database')
            
            temp_conn = mysql.connector.connect(**temp_config)
            temp_cursor = temp_conn.cursor()
            
            # Create database if not exists
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            temp_conn.close()
            
            # Now connect to the specific database
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            
            # Create users table: username, hashed_password, best_score (lowest attempts)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(64) NOT NULL,
                    best_score INT DEFAULT NULL
                )
            ''')
            self.conn.commit()
            
        except Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to connect to MySQL database.\n"
                               f"Please check your .env configuration.\n"
                               f"Error: {str(e)}")
            self.root.quit()
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=12,
                       font=('Arial', 11, 'bold'))
        style.map('Primary.TButton',
                 background=[('active', self.colors['secondary'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=12,
                       font=('Arial', 11, 'bold'))
        style.map('Success.TButton',
                 background=[('active', '#059669')])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=10,
                       font=('Arial', 10))
        style.map('Danger.TButton',
                 background=[('active', '#dc2626')])
        
        # Configure entry styles
        style.configure('Custom.TEntry',
                       fieldbackground='white',
                       borderwidth=2,
                       relief='solid',
                       padding=10,
                       font=('Arial', 12))
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['card_bg'],
                       relief='raised',
                       borderwidth=0)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ==================== LOGIN SCREEN ====================
    
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_window()
        
        # Background canvas with gradient effect
        canvas = tk.Canvas(self.root, width=700, height=600, bg=self.colors['primary'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create card frame
        card = tk.Frame(canvas, bg=self.colors['card_bg'], relief='raised', bd=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=450, height=500)
        
        # Add shadow effect with multiple frames
        shadow = tk.Frame(canvas, bg='#9ca3af')
        shadow.place(relx=0.5, rely=0.505, anchor='center', width=450, height=500)
        shadow.lower()
        
        # Title with emoji
        title_label = tk.Label(card, text="🎮 Number Guessing Game", 
                              font=("Arial", 26, "bold"),
                              bg=self.colors['card_bg'],
                              fg=self.colors['primary'])
        title_label.pack(pady=(40, 10))
        
        # Subtitle
        subtitle_label = tk.Label(card, text="Login to Play", 
                                 font=("Arial", 14),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_light'])
        subtitle_label.pack(pady=(0, 30))
        
        # Username
        username_label = tk.Label(card, text="Username", 
                                 font=("Arial", 11, "bold"),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_dark'],
                                 anchor='w')
        username_label.pack(pady=(10, 5), padx=50, fill='x')
        
        self.login_username_entry = tk.Entry(card, 
                                            font=("Arial", 12),
                                            relief='solid',
                                            bd=2,
                                            highlightthickness=1,
                                            highlightbackground=self.colors['light'],
                                            highlightcolor=self.colors['primary'])
        self.login_username_entry.pack(pady=(0, 15), padx=50, ipady=8, fill='x')
        
        # Password
        password_label = tk.Label(card, text="Password", 
                                 font=("Arial", 11, "bold"),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_dark'],
                                 anchor='w')
        password_label.pack(pady=(10, 5), padx=50, fill='x')
        
        self.login_password_entry = tk.Entry(card, 
                                            show="●",
                                            font=("Arial", 12),
                                            relief='solid',
                                            bd=2,
                                            highlightthickness=1,
                                            highlightbackground=self.colors['light'],
                                            highlightcolor=self.colors['primary'])
        self.login_password_entry.pack(pady=(0, 25), padx=50, ipady=8, fill='x')
        
        # Bind Enter key to login
        self.login_password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = tk.Button(card, 
                             text="LOGIN",
                             command=self.login,
                             bg=self.colors['primary'],
                             fg='white',
                             font=("Arial", 12, "bold"),
                             relief='flat',
                             cursor='hand2',
                             activebackground=self.colors['secondary'],
                             activeforeground='white',
                             bd=0,
                             padx=20,
                             pady=12)
        login_btn.pack(pady=10, padx=50, fill='x')
        
        # Register link
        register_frame = tk.Frame(card, bg=self.colors['card_bg'])
        register_frame.pack(pady=20)
        
        register_label = tk.Label(register_frame, 
                                 text="Don't have an account? ",
                                 font=("Arial", 10),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_light'])
        register_label.pack(side='left')
        
        register_link = tk.Label(register_frame,
                                text="Register Here",
                                font=("Arial", 10, "bold"),
                                bg=self.colors['card_bg'],
                                fg=self.colors['primary'],
                                cursor='hand2')
        register_link.pack(side='left')
        register_link.bind('<Button-1>', lambda e: self.show_register_screen())
    
    def login(self):
        """Handle user login"""
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check credentials
        password_hash = self.hash_password(password)
        self.cursor.execute(
            "SELECT username FROM users WHERE username = %s AND password_hash = %s",
            (username, password_hash)
        )
        
        result = self.cursor.fetchone()
        
        if result:
            self.current_user = username
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    # ==================== REGISTER SCREEN ====================
    
    def show_register_screen(self):
        """Display the registration screen"""
        self.clear_window()
        
        # Background canvas
        canvas = tk.Canvas(self.root, width=700, height=600, bg=self.colors['secondary'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create card frame
        card = tk.Frame(canvas, bg=self.colors['card_bg'], relief='raised', bd=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=450, height=550)
        
        # Shadow effect
        shadow = tk.Frame(canvas, bg='#9ca3af')
        shadow.place(relx=0.5, rely=0.505, anchor='center', width=450, height=550)
        shadow.lower()
        
        # Title
        title_label = tk.Label(card, text="✨ Create Account", 
                              font=("Arial", 26, "bold"),
                              bg=self.colors['card_bg'],
                              fg=self.colors['secondary'])
        title_label.pack(pady=(40, 30))
        
        # Username
        username_label = tk.Label(card, text="Username", 
                                 font=("Arial", 11, "bold"),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_dark'],
                                 anchor='w')
        username_label.pack(pady=(10, 5), padx=50, fill='x')
        
        self.register_username_entry = tk.Entry(card, 
                                               font=("Arial", 12),
                                               relief='solid',
                                               bd=2,
                                               highlightthickness=1,
                                               highlightbackground=self.colors['light'],
                                               highlightcolor=self.colors['secondary'])
        self.register_username_entry.pack(pady=(0, 10), padx=50, ipady=8, fill='x')
        
        # Password
        password_label = tk.Label(card, text="Password", 
                                 font=("Arial", 11, "bold"),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_dark'],
                                 anchor='w')
        password_label.pack(pady=(10, 5), padx=50, fill='x')
        
        self.register_password_entry = tk.Entry(card, 
                                               show="●",
                                               font=("Arial", 12),
                                               relief='solid',
                                               bd=2,
                                               highlightthickness=1,
                                               highlightbackground=self.colors['light'],
                                               highlightcolor=self.colors['secondary'])
        self.register_password_entry.pack(pady=(0, 10), padx=50, ipady=8, fill='x')
        
        # Confirm Password
        confirm_label = tk.Label(card, text="Confirm Password", 
                                font=("Arial", 11, "bold"),
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_dark'],
                                anchor='w')
        confirm_label.pack(pady=(10, 5), padx=50, fill='x')
        
        self.register_confirm_entry = tk.Entry(card, 
                                              show="●",
                                              font=("Arial", 12),
                                              relief='solid',
                                              bd=2,
                                              highlightthickness=1,
                                              highlightbackground=self.colors['light'],
                                              highlightcolor=self.colors['secondary'])
        self.register_confirm_entry.pack(pady=(0, 20), padx=50, ipady=8, fill='x')
        
        # Bind Enter key to register
        self.register_confirm_entry.bind('<Return>', lambda e: self.register())
        
        # Register button
        register_btn = tk.Button(card, 
                                text="CREATE ACCOUNT",
                                command=self.register,
                                bg=self.colors['secondary'],
                                fg='white',
                                font=("Arial", 12, "bold"),
                                relief='flat',
                                cursor='hand2',
                                activebackground=self.colors['primary'],
                                activeforeground='white',
                                bd=0,
                                padx=20,
                                pady=12)
        register_btn.pack(pady=10, padx=50, fill='x')
        
        # Back to login link
        back_frame = tk.Frame(card, bg=self.colors['card_bg'])
        back_frame.pack(pady=15)
        
        back_label = tk.Label(back_frame, 
                             text="Already have an account? ",
                             font=("Arial", 10),
                             bg=self.colors['card_bg'],
                             fg=self.colors['text_light'])
        back_label.pack(side='left')
        
        back_link = tk.Label(back_frame,
                            text="Back to Login",
                            font=("Arial", 10, "bold"),
                            bg=self.colors['card_bg'],
                            fg=self.colors['secondary'],
                            cursor='hand2')
        back_link.pack(side='left')
        back_link.bind('<Button-1>', lambda e: self.show_login_screen())
    
    def register(self):
        """Handle user registration"""
        username = self.register_username_entry.get().strip()
        password = self.register_password_entry.get()
        confirm = self.register_confirm_entry.get()
        
        # Validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Try to insert new user
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            self.conn.commit()
            
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.show_login_screen()
        
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
    
    # ==================== MAIN MENU ====================
    
    def show_main_menu(self):
        """Display the main menu after login"""
        self.clear_window()
        
        # Background canvas with gradient
        canvas = tk.Canvas(self.root, width=700, height=600, bg=self.colors['info'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create card frame
        card = tk.Frame(canvas, bg=self.colors['card_bg'], relief='raised', bd=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=500, height=550)
        
        # Shadow effect
        shadow = tk.Frame(canvas, bg='#9ca3af')
        shadow.place(relx=0.5, rely=0.505, anchor='center', width=500, height=550)
        shadow.lower()
        
        # Welcome message
        welcome_label = tk.Label(card, text=f"👋 Welcome, {self.current_user}!", 
                                font=("Arial", 26, "bold"),
                                bg=self.colors['card_bg'],
                                fg=self.colors['primary'])
        welcome_label.pack(pady=(40, 10))
        
        # Get user's best score
        self.cursor.execute("SELECT best_score FROM users WHERE username = %s", 
                           (self.current_user,))
        result = self.cursor.fetchone()
        best_score = result[0] if result and result[0] else "N/A"
        
        # Score badge
        score_frame = tk.Frame(card, bg=self.colors['light'], relief='flat', bd=0)
        score_frame.pack(pady=(10, 30), padx=60, fill='x')
        
        score_label = tk.Label(score_frame, 
                              text=f"🏆 Your Best Score: {best_score} attempts", 
                              font=("Arial", 13, "bold"),
                              bg=self.colors['light'],
                              fg=self.colors['text_dark'],
                              pady=12)
        score_label.pack()
        
        # Menu buttons
        btn_config = {
            'font': ('Arial', 13, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'bd': 0,
            'pady': 14
        }
        
        play_btn = tk.Button(card, text="🎮 Play Game", 
                            command=self.start_game,
                            bg=self.colors['success'],
                            fg='white',
                            activebackground='#059669',
                            activeforeground='white',
                            **btn_config)
        play_btn.pack(pady=8, padx=60, fill='x')
        
        scoreboard_btn = tk.Button(card, text="🏆 View High Scores", 
                                  command=self.show_scoreboard,
                                  bg=self.colors['warning'],
                                  fg='white',
                                  activebackground='#d97706',
                                  activeforeground='white',
                                  **btn_config)
        scoreboard_btn.pack(pady=8, padx=60, fill='x')
        
        settings_btn = tk.Button(card, text="⚙️ Game Settings", 
                                command=self.show_settings,
                                bg=self.colors['info'],
                                fg='white',
                                activebackground='#2563eb',
                                activeforeground='white',
                                **btn_config)
        settings_btn.pack(pady=8, padx=60, fill='x')
        
        logout_btn = tk.Button(card, text="🚪 Logout", 
                              command=self.logout,
                              bg=self.colors['danger'],
                              fg='white',
                              activebackground='#dc2626',
                              activeforeground='white',
                              **btn_config)
        logout_btn.pack(pady=8, padx=60, fill='x')
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.show_login_screen()
    
    # ==================== GAME SETTINGS ====================
    
    def show_settings(self):
        """Display game settings screen"""
        self.clear_window()
        
        # Background canvas
        canvas = tk.Canvas(self.root, width=700, height=600, bg=self.colors['info'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create card frame
        card = tk.Frame(canvas, bg=self.colors['card_bg'], relief='raised', bd=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=500, height=450)
        
        # Shadow effect
        shadow = tk.Frame(canvas, bg='#9ca3af')
        shadow.place(relx=0.5, rely=0.505, anchor='center', width=500, height=450)
        shadow.lower()
        
        # Title
        title_label = tk.Label(card, text="⚙️ Game Settings", 
                              font=("Arial", 26, "bold"),
                              bg=self.colors['card_bg'],
                              fg=self.colors['info'])
        title_label.pack(pady=(40, 10))
        
        # Subtitle
        subtitle_label = tk.Label(card, text="Number Range Configuration", 
                                 font=("Arial", 14),
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_light'])
        subtitle_label.pack(pady=(0, 30))
        
        # Settings container
        settings_frame = tk.Frame(card, bg=self.colors['light'])
        settings_frame.pack(pady=20, padx=60, fill='x')
        
        # Min range
        min_label = tk.Label(settings_frame, text="Minimum Value:", 
                            font=("Arial", 12, "bold"),
                            bg=self.colors['light'],
                            fg=self.colors['text_dark'])
        min_label.pack(pady=(15, 5), padx=20, anchor='w')
        
        self.min_range_entry = tk.Entry(settings_frame, 
                                        font=("Arial", 13),
                                        relief='solid',
                                        bd=2,
                                        highlightthickness=1,
                                        highlightbackground=self.colors['light'],
                                        highlightcolor=self.colors['info'])
        self.min_range_entry.insert(0, str(self.min_range))
        self.min_range_entry.pack(pady=(0, 15), padx=20, ipady=8, fill='x')
        
        # Max range
        max_label = tk.Label(settings_frame, text="Maximum Value:", 
                            font=("Arial", 12, "bold"),
                            bg=self.colors['light'],
                            fg=self.colors['text_dark'])
        max_label.pack(pady=(5, 5), padx=20, anchor='w')
        
        self.max_range_entry = tk.Entry(settings_frame, 
                                        font=("Arial", 13),
                                        relief='solid',
                                        bd=2,
                                        highlightthickness=1,
                                        highlightbackground=self.colors['light'],
                                        highlightcolor=self.colors['info'])
        self.max_range_entry.insert(0, str(self.max_range))
        self.max_range_entry.pack(pady=(0, 15), padx=20, ipady=8, fill='x')
        
        # Buttons
        btn_frame = tk.Frame(card, bg=self.colors['card_bg'])
        btn_frame.pack(pady=20, padx=60, fill='x')
        
        save_btn = tk.Button(btn_frame, 
                            text="💾 Save Settings",
                            command=self.save_settings,
                            bg=self.colors['success'],
                            fg='white',
                            font=("Arial", 12, "bold"),
                            relief='flat',
                            cursor='hand2',
                            activebackground='#059669',
                            activeforeground='white',
                            bd=0,
                            pady=12)
        save_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        back_btn = tk.Button(btn_frame, 
                            text="← Back",
                            command=self.show_main_menu,
                            bg=self.colors['text_light'],
                            fg='white',
                            font=("Arial", 12, "bold"),
                            relief='flat',
                            cursor='hand2',
                            activebackground=self.colors['dark'],
                            activeforeground='white',
                            bd=0,
                            pady=12)
        back_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
    
    def save_settings(self):
        """Save game settings"""
        try:
            min_val = int(self.min_range_entry.get())
            max_val = int(self.max_range_entry.get())
            
            if min_val >= max_val:
                messagebox.showerror("Error", "Minimum must be less than maximum")
                return
            
            if max_val - min_val < 5:
                messagebox.showerror("Error", "Range must be at least 5 numbers")
                return
            
            self.min_range = min_val
            self.max_range = max_val
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.show_main_menu()
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    # ==================== GAME SCREEN ====================
    
    def start_game(self):
        """Start a new game"""
        self.target_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.show_game_screen()
    
    def show_game_screen(self):
        """Display the game screen"""
        self.clear_window()
        
        # Background canvas with gradient
        canvas = tk.Canvas(self.root, width=700, height=600, bg=self.colors['success'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create card frame
        card = tk.Frame(canvas, bg=self.colors['card_bg'], relief='raised', bd=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=550, height=520)
        
        # Shadow effect
        shadow = tk.Frame(canvas, bg='#9ca3af')
        shadow.place(relx=0.5, rely=0.505, anchor='center', width=550, height=520)
        shadow.lower()
        
        # Title
        title_label = tk.Label(card, text="🎯 Guess the Number!", 
                              font=("Arial", 28, "bold"),
                              bg=self.colors['card_bg'],
                              fg=self.colors['success'])
        title_label.pack(pady=(30, 10))
        
        # Instructions
        instructions = tk.Label(card, 
                               text=f"I'm thinking of a number between {self.min_range} and {self.max_range}", 
                               font=("Arial", 13),
                               bg=self.colors['card_bg'],
                               fg=self.colors['text_light'])
        instructions.pack(pady=(0, 20))
        
        # Attempts badge
        attempts_frame = tk.Frame(card, bg=self.colors['warning'], relief='flat', bd=0)
        attempts_frame.pack(pady=10)
        
        self.attempts_label = tk.Label(attempts_frame, 
                                      text=f"Attempts: {self.attempts}", 
                                      font=("Arial", 16, "bold"),
                                      bg=self.colors['warning'],
                                      fg='white',
                                      padx=30,
                                      pady=10)
        self.attempts_label.pack()
        
        # Guess input section
        input_frame = tk.Frame(card, bg=self.colors['light'])
        input_frame.pack(pady=25, padx=60, fill='x')
        
        guess_label = tk.Label(input_frame, text="Enter Your Guess:", 
                              font=("Arial", 12, "bold"),
                              bg=self.colors['light'],
                              fg=self.colors['text_dark'])
        guess_label.pack(pady=(15, 8))
        
        self.guess_entry = tk.Entry(input_frame, 
                                   font=("Arial", 16),
                                   relief='solid',
                                   bd=2,
                                   justify='center',
                                   highlightthickness=1,
                                   highlightbackground=self.colors['light'],
                                   highlightcolor=self.colors['success'])
        self.guess_entry.pack(pady=(0, 15), padx=20, ipady=10, fill='x')
        self.guess_entry.focus()
        
        # Bind Enter key to submit guess
        self.guess_entry.bind('<Return>', lambda e: self.check_guess())
        
        # Submit button
        submit_btn = tk.Button(card, 
                              text="🚀 Submit Guess",
                              command=self.check_guess,
                              bg=self.colors['success'],
                              fg='white',
                              font=("Arial", 13, "bold"),
                              relief='flat',
                              cursor='hand2',
                              activebackground='#059669',
                              activeforeground='white',
                              bd=0,
                              pady=14)
        submit_btn.pack(pady=10, padx=60, fill='x')
        
        # Feedback label
        self.feedback_label = tk.Label(card, text="", 
                                      font=("Arial", 15, "bold"),
                                      bg=self.colors['card_bg'],
                                      pady=10)
        self.feedback_label.pack(pady=10)
        
        # Back to menu button
        back_btn = tk.Button(card, 
                            text="← Back to Menu",
                            command=self.show_main_menu,
                            bg=self.colors['text_light'],
                            fg='white',
                            font=("Arial", 10),
                            relief='flat',
                            cursor='hand2',
                            activebackground=self.colors['dark'],
                            activeforeground='white',
                            bd=0,
                            pady=8)
        back_btn.pack(pady=(5, 20), padx=60, fill='x')
    
    def check_guess(self):
        """Check the user's guess"""
        try:
            guess = int(self.guess_entry.get())
            
            if guess < self.min_range or guess > self.max_range:
                self.feedback_label.config(text=f"⚠️ Please enter a number between {self.min_range} and {self.max_range}", 
                                          foreground=self.colors['warning'])
                return
            
            self.attempts += 1
            self.attempts_label.config(text=f"Attempts: {self.attempts}")
            
            if guess < self.target_number:
                self.feedback_label.config(text="📉 Too Low! Try a higher number.", foreground=self.colors['info'])
            elif guess > self.target_number:
                self.feedback_label.config(text="📈 Too High! Try a lower number.", foreground=self.colors['danger'])
            else:
                # Correct guess!
                self.feedback_label.config(text="🎉 Correct! You Win! 🎉", foreground=self.colors['success'])
                self.game_won()
                return
            
            # Clear entry for next guess
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus()
        
        except ValueError:
            self.feedback_label.config(text="❌ Please enter a valid number", foreground=self.colors['danger'])
    
    def game_won(self):
        """Handle game win - update score if better"""
        # Get current best score
        self.cursor.execute("SELECT best_score FROM users WHERE username = %s", 
                           (self.current_user,))
        result = self.cursor.fetchone()
        current_best = result[0] if result and result[0] else None
        
        # Check if new score is better (lower attempts)
        is_new_best = False
        if current_best is None or self.attempts < current_best:
            self.cursor.execute(
                "UPDATE users SET best_score = %s WHERE username = %s",
                (self.attempts, self.current_user)
            )
            self.conn.commit()
            is_new_best = True
        
        # Show result message
        if is_new_best:
            message = f"Congratulations! New personal best!\n\nAttempts: {self.attempts}"
        else:
            message = f"You won in {self.attempts} attempts!\n\nYour best: {current_best} attempts"
        
        messagebox.showinfo("Game Over", message)
        
        # Ask to play again
        play_again = messagebox.askyesno("Play Again?", "Would you like to play another game?")
        if play_again:
            self.start_game()
        else:
            self.show_main_menu()
    
    # ==================== SCOREBOARD ====================
    
    def show_scoreboard(self):
        """Display the high scores board"""
        self.clear_window()
        
        # Background canvas
        canvas = tk.Canvas(self.root, width=700, height=600, bg=self.colors['warning'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create card frame
        card = tk.Frame(canvas, bg=self.colors['card_bg'], relief='raised', bd=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=600, height=550)
        
        # Shadow effect
        shadow = tk.Frame(canvas, bg='#9ca3af')
        shadow.place(relx=0.5, rely=0.505, anchor='center', width=600, height=550)
        shadow.lower()
        
        # Title
        title_label = tk.Label(card, text="🏆 Top 10 High Scores 🏆", 
                              font=("Arial", 26, "bold"),
                              bg=self.colors['card_bg'],
                              fg=self.colors['warning'])
        title_label.pack(pady=(30, 20))
        
        # Get top 10 scores
        self.cursor.execute(
            "SELECT username, best_score FROM users WHERE best_score IS NOT NULL ORDER BY best_score ASC LIMIT 10"
        )
        scores = self.cursor.fetchall()
        
        if not scores:
            no_scores_frame = tk.Frame(card, bg=self.colors['light'])
            no_scores_frame.pack(pady=40, padx=60, fill='both', expand=True)
            
            no_scores_label = tk.Label(no_scores_frame, 
                                      text="🎮 No scores yet.\nBe the first to play!", 
                                      font=("Arial", 16, "bold"),
                                      bg=self.colors['light'],
                                      fg=self.colors['text_dark'],
                                      justify='center')
            no_scores_label.pack(expand=True)
        else:
            # Scoreboard container
            scoreboard_frame = tk.Frame(card, bg=self.colors['card_bg'])
            scoreboard_frame.pack(pady=10, padx=40, fill='both', expand=True)
            
            # Header
            header_frame = tk.Frame(scoreboard_frame, bg=self.colors['warning'], relief='flat')
            header_frame.pack(fill='x', pady=(0, 2))
            
            tk.Label(header_frame, text="Rank", font=("Arial", 11, "bold"),
                    bg=self.colors['warning'], fg='white', width=8, pady=8).pack(side='left', padx=5)
            tk.Label(header_frame, text="Username", font=("Arial", 11, "bold"),
                    bg=self.colors['warning'], fg='white', width=25, pady=8).pack(side='left', padx=5)
            tk.Label(header_frame, text="Best Score", font=("Arial", 11, "bold"),
                    bg=self.colors['warning'], fg='white', width=12, pady=8).pack(side='left', padx=5)
            
            # Scrollable scores list
            scores_container = tk.Frame(scoreboard_frame, bg=self.colors['card_bg'])
            scores_container.pack(fill='both', expand=True)
            
            # Insert data
            for idx, (username, score) in enumerate(scores, 1):
                # Determine row color
                if username == self.current_user:
                    row_bg = '#dbeafe'  # Light blue for current user
                    row_fg = self.colors['primary']
                    font_weight = 'bold'
                elif idx <= 3:
                    # Medal colors for top 3
                    medal_colors = ['#ffd700', '#c0c0c0', '#cd7f32']  # Gold, Silver, Bronze
                    row_bg = medal_colors[idx-1]
                    row_fg = 'white'
                    font_weight = 'bold'
                else:
                    row_bg = self.colors['light'] if idx % 2 == 0 else 'white'
                    row_fg = self.colors['text_dark']
                    font_weight = 'normal'
                
                row_frame = tk.Frame(scores_container, bg=row_bg, relief='flat')
                row_frame.pack(fill='x', pady=1)
                
                # Rank with medal emoji for top 3
                rank_text = ['🥇', '🥈', '🥉'][idx-1] if idx <= 3 else str(idx)
                tk.Label(row_frame, text=rank_text, font=("Arial", 11, font_weight),
                        bg=row_bg, fg=row_fg, width=8, pady=10).pack(side='left', padx=5)
                tk.Label(row_frame, text=username, font=("Arial", 11, font_weight),
                        bg=row_bg, fg=row_fg, width=25, pady=10, anchor='w').pack(side='left', padx=5)
                tk.Label(row_frame, text=f"{score} attempts", font=("Arial", 11, font_weight),
                        bg=row_bg, fg=row_fg, width=12, pady=10).pack(side='left', padx=5)
        
        # Back button
        back_btn = tk.Button(card, 
                            text="← Back to Menu",
                            command=self.show_main_menu,
                            bg=self.colors['warning'],
                            fg='white',
                            font=("Arial", 12, "bold"),
                            relief='flat',
                            cursor='hand2',
                            activebackground='#d97706',
                            activeforeground='white',
                            bd=0,
                            pady=12)
        back_btn.pack(pady=15, padx=40, fill='x')
    
    def __del__(self):
        """Close database connection when application closes"""
        if hasattr(self, 'conn'):
            self.conn.close()


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
