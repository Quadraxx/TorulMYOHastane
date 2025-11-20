from flask import Flask, render_template, request, redirect
import pyodbc
import json 
from werkzeug.security import generate_password_hash, check_password_hash # Güvenlik için eklendi

app = Flask(__name__)

# -----------------------------------------
# AYARLAR
# -----------------------------------------
SERVER = 'localhost\\SQLEXPRESS' 
DATABASE = 'TorulMYOHastane'
# -----------------------------------------

def connect_db():
    """SQL Server veritabanına bağlanır"""
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
    return pyodbc.connect(connection_string)

@app.route("/")
def login():
    return render_template("login.html")

# --- GÜNCELLENMİŞ: GÜVENLİ LOGIN ---
@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Sadece HASH'lenmiş şifreyi çekiyoruz
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        user_row = cursor.fetchone()
        conn.close()

        if user_row and check_password_hash(user_row[0], password):
            # Gelen şifreyi veritabanındaki hash ile karşılaştır
            return redirect("/dashboard")
        else:
            return "Hatalı kullanıcı adı veya şifre! <a href='/'>Geri dön</a>"
            
    except Exception as e:
        return f"Bağlantı Hatası: {e}"
# ------------------------------------

@app.route("/dashboard")
def dashboard():
    conn = connect_db()
    cursor = conn.cursor()
    
    # --- İSTATİSTİK SORGULARI ---
    cursor.execute("SELECT COUNT(id) FROM patients")
    toplam_hasta = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(id) FROM appointments")
    toplam_randevu = cursor.fetchone()[0]

    bugun = cursor.execute("SELECT COUNT(id) FROM appointments WHERE CAST(randevu_tarihi AS DATE) = CAST(GETDATE() AS DATE)")
    bugun_randevu = cursor.fetchone()[0]
    
    # GRAFİK VERİSİ
    cursor.execute("SELECT doctor, COUNT(id) FROM appointments GROUP BY doctor")
    grafik_data = cursor.fetchall()
    conn.close()
    
    chart_labels = [row[0] for row in grafik_data]
    chart_counts = [row[1] for row in grafik_data]
    
    return render_template("dashboard.html", 
                           toplam_hasta=toplam_hasta, 
                           toplam_randevu=toplam_randevu, 
                           bugun_randevu=bugun_randevu,
                           chart_labels=json.dumps(chart_labels),
                           chart_counts=json.dumps(chart_counts))

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        tc = request.form["tc"]
        phone = request.form["phone"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients(name, surname, tc, phone) VALUES (?,?,?,?)",
                       (name, surname, tc, phone))
        conn.commit()
        conn.close()

        return redirect("/patients")

    return render_template("add_patient.html")

@app.route("/edit_patient/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        tc = request.form["tc"]
        phone = request.form["phone"]

        sorgu = "UPDATE patients SET name=?, surname=?, tc=?, phone=? WHERE id=?"
        cursor.execute(sorgu, (name, surname, tc, phone, id))
        conn.commit()
        conn.close()
        return redirect("/patients")

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()
    conn.close()

    if patient:
        return render_template("edit_patient.html", patient=patient)
    else:
        return "Hasta bulunamadı.", 404

@app.route("/patients")
def patients():
    conn = connect_db()
    cursor = conn.cursor()

    arama_terimi = request.args.get("q")

    if arama_terimi:
        sorgu = "SELECT * FROM patients WHERE name LIKE ? OR tc LIKE ?"
        parametre = f"%{arama_terimi}%"
        cursor.execute(sorgu, (parametre, parametre))
    else:
        cursor.execute("SELECT * FROM patients")
    
    data = cursor.fetchall()
    conn.close()
    return render_template("patients.html", patients=data)

@app.route("/appointment", methods=["GET", "POST"])
def appointment():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        doctor = request.form["doctor"]
        
        raw_date = request.form["datetime"]
        datetime_val = raw_date.replace("T", " ") 

        cursor.execute("INSERT INTO appointments(patient_id, doctor, randevu_tarihi, durum) VALUES (?,?,?, 'Bekliyor')",
                       (patient_id, doctor, datetime_val))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    cursor.execute("SELECT id, name, surname, tc FROM patients")
    patients_list = cursor.fetchall()
    conn.close()

    return render_template("appointment.html", patients=patients_list)

@app.route("/appointment_list")
def appointment_list():
    conn = connect_db()
    cursor = conn.cursor()
    
    arama_terimi = request.args.get("q")
    sorgu = ""
    parametreler = []

    if arama_terimi:
        parametre = f"%{arama_terimi}%"
        sorgu = """
        SELECT a.id, p.name, p.surname, p.tc, a.doctor, a.randevu_tarihi, a.durum, a.tani, a.recete
        FROM appointments a 
        JOIN patients p ON a.patient_id = p.id
        WHERE p.name LIKE ? OR p.surname LIKE ? OR a.doctor LIKE ?
        ORDER BY a.randevu_tarihi DESC
        """
        parametreler = [parametre, parametre, parametre]
        cursor.execute(sorgu, tuple(parametreler))
    else:
        sorgu = """
        SELECT a.id, p.name, p.surname, p.tc, a.doctor, a.randevu_tarihi, a.durum, a.tani, a.recete
        FROM appointments a 
        JOIN patients p ON a.patient_id = p.id
        ORDER BY a.randevu_tarihi DESC
        """
        cursor.execute(sorgu)

    data = cursor.fetchall()
    conn.close()
    
    return render_template("appointment_list.html", appointments=data)

@app.route("/complete_appointment", methods=["POST"])
def complete_appointment():
    randevu_id = request.form["randevu_id"]
    tani = request.form["tani"]
    recete = request.form["recete"]

    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE appointments 
        SET tani=?, recete=?, durum='Tamamlandı' 
        WHERE id=?
    """, (tani, recete, randevu_id))
    
    conn.commit()
    conn.close()
    
    return redirect("/appointment_list")

@app.route("/print_recete/<int:id>")
def print_recete(id):
    conn = connect_db()
    cursor = conn.cursor()
    
    sorgu = """
    SELECT a.id, p.name, p.surname, p.tc, a.doctor, a.randevu_tarihi, a.tani, a.recete
    FROM appointments a 
    JOIN patients p ON a.patient_id = p.id
    WHERE a.id = ?
    """
    
    cursor.execute(sorgu, (id,))
    data = cursor.fetchone()
    conn.close()
    
    return render_template("print_recete.html", item=data)

@app.route("/delete_appointment/<int:id>")
def delete_appointment(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/appointment_list")

if __name__ == "__main__":
    app.run(debug=True)