import sqlite3
from datetime import datetime


DB_NAME = "genome_x.db"


def init_db():
    """Database နဲ့ Table မရှိသေးရင် အလိုအလျောက် ဆောက်ပေးမယ့် Function"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # alignment_results ဆိုတဲ့ Table ကို ဆောက်မယ်
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alignment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name TEXT,
            sequence1 TEXT,
            sequence2 TEXT,
            score INTEGER,
            result_file TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("📁 Database & Table Initialized Successfully!")


def insert_result(job_name, seq1, seq2, score, result_file):
    """ထွက်လာတဲ့ DNA ရလဒ်တွေကို Database ထဲ လှမ်းသိမ်းမယ့် Function"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO alignment_results (job_name, sequence1, sequence2, score, result_file, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (job_name, seq1, seq2, score, result_file, current_time))

    conn.commit()
    conn.close()
    print(f"✅ Saved Record: {job_name} to Database!")


# ဒီဖိုင်ကို တိုက်ရိုက် Run ရင် Database အရင်ဆောက်ပေးမယ်
if __name__ == "__main__":
    init_db()
