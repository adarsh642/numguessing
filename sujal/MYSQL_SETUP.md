# MySQL Setup Guide for Number Guessing Game

## Prerequisites
1. Install MySQL Server (if not already installed)
2. Install MySQL Workbench (for database management)
3. Have Python 3.7+ installed

## Step 1: Install Python Dependencies
Run the following command in your terminal/command prompt:

```bash
pip install -r requirements.txt
```

This will install:
- mysql-connector-python (for MySQL database connection)
- python-dotenv (for environment variable management)

## Step 2: Configure MySQL Database

### Option A: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Create a new database called `number_guessing_game`:
   ```sql
   CREATE DATABASE number_guessing_game;
   ```

### Option B: Using MySQL Command Line
1. Open MySQL command line
2. Login with your credentials
3. Create database:
   ```sql
   CREATE DATABASE number_guessing_game;
   ```

## Step 3: Configure Environment Variables
1. Open the `.env` file in your project folder
2. Update the following values with your MySQL connection details:

```env
# Replace these with your actual MySQL configuration
DB_HOST=localhost          # Your MySQL server host (usually localhost)
DB_PORT=3306              # MySQL port (default is 3306)
DB_NAME=number_guessing_game  # Database name (keep this as is)
DB_USER=root              # Your MySQL username
DB_PASSWORD=your_password_here  # Your MySQL password
```

### Example Configuration:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=number_guessing_game
DB_USER=root
DB_PASSWORD=mypassword123
```

## Step 4: Run the Application
After configuring the `.env` file, run:

```bash
python number_guessing_game.py
```

## Troubleshooting

### Common Issues:

1. **"Access denied for user"**
   - Check your DB_USER and DB_PASSWORD in .env file
   - Ensure the MySQL user has proper permissions

2. **"Can't connect to MySQL server"**
   - Verify MySQL server is running
   - Check DB_HOST and DB_PORT values
   - Ensure firewall allows MySQL connections

3. **"Unknown database"**
   - Make sure you created the database `number_guessing_game`
   - Check DB_NAME in .env file

4. **Import errors**
   - Run `pip install -r requirements.txt` to install dependencies
   - Ensure you're using the correct Python environment

### MySQL Workbench Connection Test:
1. Open MySQL Workbench
2. Create a new connection using the same credentials from your .env file
3. Test the connection before running the Python application

### Database Tables:
The application will automatically create the required `users` table with the following structure:
- id (INT AUTO_INCREMENT PRIMARY KEY)
- username (VARCHAR(50) UNIQUE NOT NULL)
- password_hash (VARCHAR(64) NOT NULL)  
- best_score (INT DEFAULT NULL)

## Security Notes:
- Never commit the .env file with real passwords to version control
- Use strong passwords for your MySQL users
- Consider creating a dedicated MySQL user for this application with limited privileges