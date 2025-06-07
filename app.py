from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from marks_scraper import scrape_and_generate_pdf
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        prn = request.form.get('prn', '').strip()
        day = request.form.get('day', '').strip()
        month = request.form.get('month', '').strip()
        year = request.form.get('year', '').strip()

        # Basic validation
        if not (prn and day and month and year):
            flash("All fields are required.", "error")
            return redirect(url_for('index'))

        pdf_path = scrape_and_generate_pdf(prn, day, month, year)

        if not os.path.exists(pdf_path):
            flash("PDF could not be generated. Try again.", "error")
            return redirect(url_for('index'))

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        flash("Something went wrong while generating the PDF. Please check your inputs.", "error")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
