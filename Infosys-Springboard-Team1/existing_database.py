import sqlite3

# Path to your SQLite database
DATABASE = 'C:\\Users\\gokul\\OneDrive\\Documents\\hifi_eats\\Infosys-Springboard-Team1\\existing_database.db'

def create_tables():
    print("Connecting to database...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("Creating Roles table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE,
        role_description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    print("Creating Users table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        phone_number TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        role_id INTEGER,
        is_admin INTEGER DEFAULT 0,
        FOREIGN KEY(role_id) REFERENCES roles(role_id) ON DELETE SET NULL
    )
    ''')

    print("Creating EmailVerifications table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_verifications (
        verification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        verification_token TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        verified_at TIMESTAMP,
        status TEXT CHECK(status IN ('Pending', 'Verified')) DEFAULT 'Pending',
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Tables created successfully.")

def insert_initial_data():
    print("Inserting initial data...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("Inserting roles...")
    roles = [
        ('admin', 'Administrator role'),
        ('user', 'Regular user role')
    ]
    cursor.executemany('INSERT OR IGNORE INTO roles (role_name, role_description) VALUES (?, ?)', roles)

    print("Inserting admin user...")
    admin_user = ('new_admin@example.com', 'hashed_password', 'Admin Name', '1234567890', 1)
    cursor.execute('INSERT OR IGNORE INTO users (email, password_hash, full_name, phone_number, role_id) VALUES (?, ?, ?, ?, ?)', admin_user)

    conn.commit()
    conn.close()
    print("Initial data inserted successfully.")

if __name__ == '__main__':
    create_tables()
    insert_initial_data()