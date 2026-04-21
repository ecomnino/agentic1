import sqlite3
import pandas as pd

def create_database(db_name):
    """Maak een SQLite-database aan."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Maak een tabel aan als deze nog niet bestaat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def process_data(data_frame, db_name):
    """Verwerk de gegevens en sla ze op in de SQLite-database."""
    # Controleer of de DataFrame niet leeg is
    if data_frame.empty:
        print("De DataFrame is leeg. Geen gegevens om te verwerken.")
        return
    
    # Maak verbinding met de database
    conn = sqlite3.connect(db_name)
    
    # Sla de gegevens op in de database
    data_frame.to_sql('data', conn, if_exists='append', index=False)
    
    conn.close()
    print(f"{len(data_frame)} rijen succesvol toegevoegd aan de database.")

# Voorbeeldgebruik
if __name__ == "__main__":
    # Stap 1: Maak de database aan
    db_name = 'local_database.db'
    create_database(db_name)
    
    # Stap 2: Maak een voorbeeld DataFrame aan
    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['Amsterdam', 'Rotterdam', 'Utrecht']
    }
    df = pd.DataFrame(data)
    
    # Stap 3: Verwerk de gegevens en sla ze op in de database
    process_data(df, db_name)
