import pymysql
import sys
from datetime import datetime

# 🌟 CONFIGURAZIONE DATABASE ESTERNO (XAMPP SETUP)
db_config = {
    'host': 'localhost',      
    'user': 'root',           # Utente standard di XAMPP
    'password': '',           # Senza password per XAMPP
    'database': 'sistema_spese' 
}

def connect_db():
    print("Connessione al database con PyMySQL in corso...")
    try:
        conn = pymysql.connect(**db_config)
        print("✅ CONNESSO!")
        print("Benvenuto gentile Utente")
        return conn
    except pymysql.MySQLError as e:
        print("\n🚨 ERRORE CRITICO:")
        print(f"Motivo: {e}")
        print("💡 Suggerimento: Assicurati che MySQL sia ACCESO su XAMPP e di aver creato il database 'sistema_spese' su phpMyAdmin!\n")
        return None

def menu_principale():
    print("\n" + "-" * 15)
    print("✨ SISTEMA SPESE PERSONALI V1.0✨")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-" * 15)
    return input("Inserisci la tua scelta: ")

def modulo_categorie(conn):
    nome = input("Nome nuova categoria: ").strip()
    if not nome: return
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Categorie (nome) VALUES (%s)", (nome,))
        conn.commit()
        print("✅ Categoria aggiunta con successo")
    except pymysql.MySQLError:
        print("❌ Questa categoria è già presente o c'è un errore!")

def modulo_spese(conn):
    try:
        # Chiediamo nel formato Europeo
        data_input = input("Data (DD-MM-YYYY): ")
        
        # TRADUZIONE: Da stringa DD-MM-YYYY a formato database YYYY-MM-DD
        data_sql = datetime.strptime(data_input, '%d-%m-%Y').strftime('%Y-%m-%d')
        importo = float(input("Importo: "))
        if importo <= 0:
            print("❌ L'importo deve essere positivo!")
            return
        cat_nome = input("Categoria: ")
        desc = input("Descrizione (opzionale): ")

        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria FROM Categorie WHERE nome = %s", (cat_nome,))
        res = cursor.fetchone()
        
        if not res:
            print("❌ Categoria non trovata! Creala prima dal menu Opzione 1.")
            return

        cursor.execute("INSERT INTO Spese (data_spesa, id_categoria, importo, descrizione) VALUES (%s, %s, %s, %s)",
                       (data_sql, res[0], importo, desc))
        conn.commit()
        print("✅ Spesa registrata con successo!")
    except ValueError:
        print("❌ Dati non validi! Inserisci un numero per l'importo.")

def modulo_budget(conn):
    print("\n--- DEFINISCI BUDGET MENSILE ---")
    mese_input = input("Mese (MM-YYYY): ").strip()
    mese_sql = datetime.strptime(mese_input, '%m-%Y').strftime('%Y-%m')
    nome_cat = input("Nome della categoria: ").strip()
    
    try:
        importo = float(input("Importo del budget: "))
        if importo <= 0:
            print("❌ Errore: il budget deve essere maggiore di zero.")
            return
    except ValueError:
         print("❌ Errore: Inserire un numero valido per l'importo.")
         return

    cursor = conn.cursor()
    # 1. Controllo dell'esistenza della categoria
    cursor.execute("SELECT id_categoria FROM Categorie WHERE nome = %s", (nome_cat,))
    cat = cursor.fetchone()

    if not cat:
        print("❌ Errore: la categoria non esiste. Aggiungila prima dal Menu opzione 1.")
        return

    # 2. Inserimento o aggiornamento del budget
    try:
        sql = """
            INSERT INTO Budget (mese, id_categoria, importo) 
            VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE importo = VALUES(importo)
        """
        cursor.execute(sql, (mese_sql, cat[0], importo))
        conn.commit()
        print("✅ Budget mensile salvato correttamente.")
    except pymysql.MySQLError as e:
        print(f"❌ Errore nel salvataggio del budget: {e}")

def modulo_report(conn):
    print("\nSELEZIONA IL REPORT")
    print("1. Totale spese per Categoria\n2. Spese mensili vs budget\n3. Elenco completo delle spese ordinate per data\n4. Ritorna al menu principale")
    scelta = input("Scelta: ")
    cursor = conn.cursor()

    if scelta == '1':
        cursor.execute("SELECT C.nome, SUM(S.importo) FROM Spese S JOIN Categorie C ON S.id_categoria = C.id_categoria GROUP BY C.nome")
        print("\nCategoria        Totale Speso")
        for row in cursor.fetchall(): 
            print(f"{row[0]:<15} {row[1]:.2f}")
    
    elif scelta == '2':
        mese_input = input("Mese (MM-YYYY): ").strip()
        mese_sql = datetime.strptime(mese_input, '%m-%Y').strftime('%Y-%m')
        cursor.execute("""
            SELECT C.nome, B.importo, COALESCE(SUM(S.importo), 0)
            FROM Budget B
            JOIN Categorie C ON B.id_categoria = C.id_categoria
            LEFT JOIN Spese S ON C.id_categoria = S.id_categoria AND DATE_FORMAT(S.data_spesa, '%%Y-%%m') = B.mese
            WHERE B.mese = %s
            GROUP BY C.nome, B.importo
        """, (mese_sql,))
        for row in cursor.fetchall():
            cat, bud, spe = row
            stato = "⚠️ SUPERAMENTO BUDGET" if float(spe) > float(bud) else "✅ OK"
            print(f"\nCat: {cat} | Budget: {bud} | Speso: {spe} | Stato: {stato}")
            
    elif scelta == '3':
       cursor.execute("SELECT S.data_spesa, C.nome, S.importo, S.descrizione FROM Spese S JOIN Categorie C ON S.id_categoria = C.id_categoria ORDER BY S.data_spesa ASC")
       print("\nData        Categoria       Importo   Descrizione")
       for row in cursor.fetchall():
            # row[0] è la data del database. La formatta da americano ad europeo
            data_eu = row[0].strftime('%d-%m-%Y')
            
            print(f"{data_eu}  {row[1]:<15} {row[2]:<10.2f} {row[3]}")
    elif scelta == '4':
        exit
def main():
    conn = connect_db()
    if conn is None:
        return # Termina se il db non è pronto
        
    while True:
        s = menu_principale()
        if s == '1': modulo_categorie(conn)
        elif s == '2': modulo_spese(conn)
        elif s == '3': modulo_budget(conn)
        elif s == '4': modulo_report(conn)
        elif s == '5': 
            print("Arrivederci!")
            break
        else: print("❌ Scelta non valida!")
        
    conn.close()

if __name__ == "__main__":
    main()
