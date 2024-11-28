from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# دالة لربط قاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('tenants.db')
    conn.row_factory = sqlite3.Row  # لتمكين الوصول إلى الأعمدة بأسمائها
    return conn

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# دالة لإضافة مستأجر جديد
@app.route('/add_tenant', methods=['POST'])
def add_tenant():
    tenant_name = request.form['tenant_name']
    land_paper = request.form['land_paper']
    plot_number = request.form['plot_number']
    feddan = int(request.form['feddan'])
    qirat = int(request.form['qirat'])
    share = int(request.form['share'])
    violations = request.form['violations']
    
    # الاتصال بقاعدة البيانات
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO tenants (tenant_name, land_paper, plot_number, feddan, qirat, share, violations)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (tenant_name, land_paper, plot_number, feddan, qirat, share, violations))
    
    # حفظ التغييرات
    conn.commit()
    conn.close()

    return redirect(url_for('tenants'))

# صفحة عرض جميع المستأجرين
@app.route('/tenants')
def tenants():
    conn = get_db_connection()
    tenants = conn.execute('SELECT * FROM tenants').fetchall()
    conn.close()
    return render_template('tenants.html', tenants=tenants)

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
