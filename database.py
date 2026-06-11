import sqlite3


def init_db():
    conn = sqlite3.connect("genome_x.db")
    cursor = conn.cursor()

    # 🛠️ Table ဆောက်တဲ့နေရာမှာ result_type TEXT ဆိုတဲ့ ကော်လံအသစ် ဖြည့်လိုက်တယ်
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna_text TEXT NOT NULL,
            result_type TEXT NOT NULL,
            result_text TEXT NOT NULL,
            search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_history(dna, res_type, result):
    # 🛠️ သီချင်းအသစ်သွင်းသလိုပဲ res_type (Result Type) ပါ တွဲသိမ်းဖို့ ? အကွက်တစ်ခု တိုးလိုက်တယ်
    conn = sqlite3.connect("genome_x.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (dna_text, result_type, result_text) VALUES (?, ?, ?)", (dna, res_type, result))
    conn.commit()
    conn.close()


def get_history():
    # 🛠️ ဆွဲထုတ်တဲ့နေရာမှာလည်း result_type ပါ ပူးတွဲပါလာအောင် ထည့်ခိုင်းလိုက်တယ်
    conn = sqlite3.connect("genome_x.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT dna_text, result_type, result_text, search_time FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ...existing code...


def clear_all_history():
    """Remove all records from the history table."""
    conn = sqlite3.connect('genome_x.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()


def delete_history_by_id(row_id):
    """Delete a specific record by its ID from the history table."""

    conn = sqlite3.connect('genome_x.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()

# ...existing code...


init_db()
