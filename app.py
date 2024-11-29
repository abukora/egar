from flask import Flask, render_template_string, request, redirect
import sqlite3
import os

app = Flask(__name__)

# التأكد من وجود قاعدة البيانات وإنشاؤها إذا لم تكن موجودة
DB_NAME = 'tenants.db'

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        conn.execute('''
            CREATE TABLE tenants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_name TEXT NOT NULL,
                land_paper TEXT NOT NULL,
                plot_number TEXT NOT NULL,
                feddan INTEGER NOT NULL,
                qirat INTEGER NOT NULL,
                share INTEGER NOT NULL,
                violations TEXT
            )
        ''')
        conn.close()

init_db()

# دالة لربط قاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>إضافة مستأجر</title>
      <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 900px;
        margin: 50px auto;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        direction: rtl; /* جعل الاتجاه من اليمين إلى اليسار */
    }
    h1 {
        text-align: center;
        color: #333;
    }
    form {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    label {
        font-weight: bold;
        color: #333;
        text-align: right; /* محاذاة النصوص لليمين */
    }
    input, textarea, button {
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ddd;
        border-radius: 5px;
        text-align: right; /* محاذاة الإدخال لليمين */
    }
    button {
        background-color: #4CAF50;
        color: white;
        border: none;
        cursor: pointer;
    }
    button:hover {
        background-color: #45a049;
    }
    .view-btn {
        margin-top: 20px;
        text-align: center;
    }
    .view-btn a {
        text-decoration: none;
        color: white;
        background-color: #007BFF;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .view-btn a:hover {
        background-color: #0056b3;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    table, th, td {
        border: 1px solid #ddd;
    }
    th, td {
        padding: 10px;
        text-align: right; /* جعل النصوص داخل الجدول تبدأ من اليمين */
    }
    th {
        background-color: #f4f4f4;
    }
</style>

    </head>
    <body>
        <div class="container">
            <h1>إضافة مستأجر جديد</h1>
            <form method="POST" action="/add_tenant">
                <label for="tenant_name">اسم المستأجر:</label>
                <input type="text" id="tenant_name" name="tenant_name" required>
                <label for="land_paper">رقم الجريدة:</label>
                <input type="text" id="land_paper" name="land_paper" required>
                <label for="plot_number">رقم الحوض:</label>
                <input type="text" id="plot_number" name="plot_number" required>
                <label for="feddan">عدد الفدادين:</label>
                <input type="number" id="feddan" name="feddan" required>
                <label for="qirat">عدد القيراط:</label>
                <input type="number" id="qirat" name="qirat" required>
                <label for="share">عدد الأسهم:</label>
                <input type="number" id="share" name="share" required>
                <label for="violations">التعديات:</label>
                <textarea id="violations" name="violations"></textarea>
                <button type="submit">إضافة</button>
            </form>
            <div class="view-btn">
                <a href="/tenants">عرض المستأجرين</a>
            </div>
        </div>
    </body>
    </html>
    ''')

# إضافة مستأجر إلى قاعدة البيانات
@app.route('/add_tenant', methods=['POST'])
def add_tenant():
    tenant_name = request.form['tenant_name']
    land_paper = request.form['land_paper']
    plot_number = request.form['plot_number']
    feddan = int(request.form['feddan'])
    qirat = int(request.form['qirat'])
    share = int(request.form['share'])
    violations = request.form['violations']

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO tenants (tenant_name, land_paper, plot_number, feddan, qirat, share, violations)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (tenant_name, land_paper, plot_number, feddan, qirat, share, violations))
    conn.commit()
    conn.close()

    return redirect('/')

# عرض المستأجرين
@app.route('/tenants')
def tenants():
    conn = get_db_connection()
    tenants = conn.execute('SELECT * FROM tenants').fetchall()
    conn.close()

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>عرض المستأجرين</title>
       <style>
    body { 
        font-family: Arial, sans-serif; 
        background-color: #f4f4f4; 
        margin: 0; 
        padding: 0; 
        direction: rtl; /* تغيير اتجاه النصوص إلى اليمين */
    }
    .container { 
        max-width: 900px; 
        margin: 50px auto; 
        padding: 20px; 
        background-color: #fff; 
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1); 
    }
    h1 { 
        text-align: center; 
        color: #333; 
    }
    table { 
        width: 100%; 
        border-collapse: collapse; 
        margin-top: 20px; 
    }
    table, th, td { 
        border: 1px solid #ddd; 
    }
    th, td { 
        padding: 10px; 
        text-align: right; /* تغيير المحاذاة إلى اليمين */
    }
    th { 
        background-color: #f4f4f4; 
    }
</style>

    </head>
    <body>
        <div class="container">
            <h1>قائمة المستأجرين</h1>
            <table>
                <tr>
                    <th>الرقم</th>
                    <th>اسم المستأجر</th>
                    <th>رقم الجريدة</th>
                    <th>رقم الحوض</th>
                    <th>الفدادين</th>
                    <th>القيراط</th>
                    <th>الأسهم</th>
                    <th>التعديات</th>
                </tr>
                {% for tenant in tenants %}
                <tr>
                    <td>{{ tenant.id }}</td>
                    <td>{{ tenant.tenant_name }}</td>
                    <td>{{ tenant.land_paper }}</td>
                    <td>{{ tenant.plot_number }}</td>
                    <td>{{ tenant.feddan }}</td>
                    <td>{{ tenant.qirat }}</td>
                    <td>{{ tenant.share }}</td>
                    <td>{{ tenant.violations }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    ''', tenants=tenants)

if __name__ == '__main__':
    app.run(debug=True)
