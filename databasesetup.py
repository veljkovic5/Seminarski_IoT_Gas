import sqlite3

def init_db():
    conn = sqlite3.connect('gas_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS readouts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER NOT NULL,
        status TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    print('Baza gas_data.db uspesno kreirana i tabela readouts je spremna.')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()