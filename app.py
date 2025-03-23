from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def sanitize_text(text):
    """
    Replace unsupported Unicode characters with their closest ASCII equivalents.
    """
    replacements = {
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201C': '"',  # Left double quotation mark
        '\u201D': '"',  # Right double quotation mark
        '\u2026': '...',  # Ellipsis
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    return text

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def add_section_line(self):
        self.ln(3)
        self.set_line_width(0.2)
        self.set_draw_color(0, 0, 0)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

def create_resume(data, photo_path=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Sanitize all text inputs
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = sanitize_text(value)

    # Header Section
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(150, 131, 236)
    pdf.cell(0, 8, txt=data['name'].upper(), ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, txt=f"{data['phone']} | {data['email']} | LinkedIn | {data['github']}", ln=True, align="C")
    pdf.ln(5)

    # Add photo if provided
    if photo_path:
        pdf.image(photo_path, x=160, y=10, w=30)
    pdf.add_section_line()

    # Professional Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)
    pdf.cell(0, 8, txt="PROFESSIONAL SUMMARY", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, txt=data['summary'])
    pdf.ln(3)
    pdf.add_section_line()

    # Education
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)
    pdf.cell(0, 8, txt="EDUCATION", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    education = f"10th Grade: {data['10th_grade']}\n12th Grade: {data['12th_grade']}\n{data['education']}"
    pdf.multi_cell(0, 6, txt=education)
    pdf.ln(3)
    pdf.add_section_line()

    # Skills
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)
    pdf.cell(0, 8, txt="SKILLS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    skills = data['skills'].split(',')
    for skill in skills:
        pdf.cell(0, 6, txt=f"- {skill.strip()}", ln=True)
    pdf.ln(3)
    pdf.add_section_line()

    # Projects
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)
    pdf.cell(0, 8, txt="PROJECTS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    projects = data['projects'].split('\n')
    for project in projects:
        pdf.multi_cell(0, 6, txt=project.strip())
    pdf.ln(3)
    pdf.add_section_line()

    # Achievements
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)
    pdf.cell(0, 8, txt="ACHIEVEMENTS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    achievements = data['achievements'].split('\n')
    for achievement in achievements:
        pdf.multi_cell(0, 6, txt=achievement.strip())
    pdf.ln(3)
    pdf.add_section_line()

    # Certifications
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)
    pdf.cell(0, 8, txt="CERTIFICATIONS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    certifications = data['certifications'].split('\n')
    for certification in certifications:
        pdf.multi_cell(0, 6, txt=certification.strip())
    pdf.ln(3)
    pdf.add_section_line()

    # Save PDF
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], "resume.pdf")
    pdf.output(pdf_path)
    return pdf_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = {
            "name": request.form['name'],
            "phone": request.form['phone'],
            "email": request.form['email'],
            "github": request.form['github'],
            "summary": request.form['summary'],
            "10th_grade": request.form['10th_grade'],
            "12th_grade": request.form['12th_grade'],
            "education": request.form['education'],
            "skills": request.form['skills'],
            "projects": request.form['projects'],
            "achievements": request.form['achievements'],
            "certifications": request.form['certifications'],
        }

        photo = request.files.get('photo')
        photo_path = None
        if photo and photo.filename:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_path)

        pdf_path = create_resume(data, photo_path)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)