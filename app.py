from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # لتفعيل استخدام flash messages

# دالة لربط قاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('tenants.db')  # قاعدة البيانات بجانب التطبيق
    conn.row_factory = sqlite3.Row  # لتمكين الوصول إلى الأعمدة بأسمائها
    return conn

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')  # الملف في نفس المجلد

# دالة لإضافة المستأجر إلى قاعدة البيانات
@app.route('/add_tenant', methods=['POST'])
def add_tenant():
    if request.method == 'POST':
        tenant_name = request.form['tenant_name']
        land_paper = request.form['land_paper']
        plot_number = request.form['plot_number']
        feddan = request.form['feddan']
        qirat = request.form['qirat']
        share = request.form['share']
        violations = request.form['violations']
        
        # التحقق من أن المدخلات غير فارغة
        if not tenant_name or not land_paper or not plot_number or not feddan or not qirat or not share:
            flash('جميع الحقول مطلوبة', 'error')
            return redirect(url_for('index'))

        try:
            # تحويل المدخلات إلى قيم صحيحة حيثما كان ذلك مناسبًا
            feddan = int(feddan)
            qirat = int(qirat)
            share = int(share)
        except ValueError:
            flash('يرجى إدخال قيم صحيحة للفدادين، القيراط، والأسهم', 'error')
            return redirect(url_for('index'))

        # الاتصال بقاعدة البيانات
        conn = get_db_connection()
        c = conn.cursor()

        # إضافة بيانات المستأجر إلى الجدول
        c.execute('''
            INSERT INTO tenants (tenant_name, land_paper, plot_number, feddan, qirat, share, violations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tenant_name, land_paper, plot_number, feddan, qirat, share, violations))
        
        # حفظ التغييرات
        conn.commit()
        conn.close()

        flash('تم إضافة المستأجر بنجاح!', 'success')
        return redirect(url_for('index'))

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
