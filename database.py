import sqlite3
from datetime import datetime

DB_NAME = "genome_x.db"


def init_db():
    """Database နဲ့ Table မရှိသေးရင် အလိုအလျောက် ဆောက်ပေးမယ့် Function"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

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
    """ထွက်လာတဲ့ DNA ရလဒ်တွေကို အပြည့်အစုံ သိမ်းမယ့် Function"""
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

# 💡 [ADDED] app.py က လှမ်းခေါ်နေတဲ့ save_history နဲ့ ကိုက်ညီအောင် ပေါင်းကူးပေးတဲ့ Function


def save_history(user_dna, result_type, result):
    """app.py က ပို့လိုက်တဲ့ parameters (၃) ခုအတိုင်း လက်ခံပြီး သိမ်းပေးတာ"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO alignment_results (job_name, sequence1, score, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (result_type, user_dna, result, current_time))

    conn.commit()
    conn.close()
    print(f"💾 [History Saved]: {result_type}")

# 💡 [ADDED] AttributeError ကို ရှင်းထုတ်ဖို့နဲ့ UI မှာ ဒေတာပြဖို့အတွက် Function


def get_history():
    """Database ထဲက နောက်ဆုံးရလဒ် (၅) ခုကို HTML ဘက် ပြန်ပို့ပေးမယ့် Function"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM alignment_results ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
    except Exception as e:
        print(f"❌ Read Error: {e}")
        rows = []
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
