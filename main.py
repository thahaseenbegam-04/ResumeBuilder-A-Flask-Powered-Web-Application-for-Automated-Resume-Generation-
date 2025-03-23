from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Add header if needed
        pass

    def footer(self):
        # Add footer if needed
        pass

    def add_section_line(self):
        # Add a horizontal line after each section
        self.ln(3)  # Add some space before the line
        self.set_line_width(0.2)  # Thinner line
        self.set_draw_color(0, 0, 0)  # Black color
        self.line(10, self.get_y(), 200, self.get_y())  # Draw a horizontal line
        self.ln(3)  # Add some space after the line

def create_resume(data, photo_path=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)  # Smaller base font size

    # Header Section
    pdf.set_font("Arial", 'B', 16)  # Smaller font size for name
    pdf.set_text_color(150, 131, 236)  # Dark lavender color for name
    pdf.cell(0, 8, txt=data['name'].upper(), ln=True, align="C")  # Name in all caps
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)  # Black color for contact info
    pdf.cell(0, 6, txt=f"{data['phone']} | {data['email']} | LinkedIn | {data['github']}", ln=True, align="C")
    pdf.ln(5)

    # Add photo if provided
    if photo_path:
        pdf.image(photo_path, x=160, y=10, w=30)  # Adjust position and size as needed
    pdf.add_section_line()  # Add a horizontal line after the header

    # Professional Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)  # Light lavender color for heading
    pdf.cell(0, 8, txt="PROFESSIONAL SUMMARY", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)  # Black color for content
    pdf.multi_cell(0, 6, txt=data['summary'])
    pdf.ln(3)
    pdf.add_section_line()  # Add a horizontal line after the summary

    # Education
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)  # Light lavender color for heading
    pdf.cell(0, 8, txt="EDUCATION", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)  # Black color for content
    education = f"10th Grade: {data['10th_grade']}\n12th Grade: {data['12th_grade']}\n{data['education']}"
    pdf.multi_cell(0, 6, txt=education)
    pdf.ln(3)
    pdf.add_section_line()  # Add a horizontal line after education

    # Skills
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)  # Light lavender color for heading
    pdf.cell(0, 8, txt="SKILLS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)  # Black color for content
    skills = data['skills'].split(',')
    for skill in skills:
        pdf.cell(0, 6, txt=f"- {skill.strip()}", ln=True)
    pdf.ln(3)
    pdf.add_section_line()  # Add a horizontal line after skills

    # Projects
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)  # Light lavender color for heading
    pdf.cell(0, 8, txt="PROJECTS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)  # Black color for content
    projects = data['projects'].split('\n')
    for project in projects:
        pdf.multi_cell(0, 6, txt=project.strip())
    pdf.ln(3)
    pdf.add_section_line()  # Add a horizontal line after projects

    # Achievements
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)  # Light lavender color for heading
    pdf.cell(0, 8, txt="ACHIEVEMENTS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)  # Black color for content
    achievements = data['achievements'].split('\n')
    for achievement in achievements:
        pdf.multi_cell(0, 6, txt=achievement.strip())
    pdf.ln(3)
    pdf.add_section_line()  # Add a horizontal line after achievements

    # Certifications
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(230, 230, 250)  # Light lavender color for heading
    pdf.cell(0, 8, txt="CERTIFICATIONS", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)  # Black color for content
    certifications = data['certifications'].split('\n')
    for certification in certifications:
        pdf.multi_cell(0, 6, txt=certification.strip())
    pdf.ln(3)
    pdf.add_section_line()  # Add a horizontal line after certifications

    # Save PDF
    pdf_path = "myresume.pdf"
    pdf.output(pdf_path)
    print(f"Resume saved as {pdf_path}")

def get_user_input():
    print("Welcome to the Resume Builder!")
    data = {
        "name": input("Enter your full name: "),
        "phone": input("Enter your phone number: "),
        "email": input("Enter your email: "),
        "github": input("Enter your GitHub profile URL: "),
        "summary": input("Enter your professional summary: "),
        "10th_grade": input("Enter your 10th grade details (School, Year, Percentage): "),
        "12th_grade": input("Enter your 12th grade details (School, Year, Percentage): "),
        "education": input("Enter your higher education details (Degree, Institution, Year): "),
        "skills": input("Enter your skills (comma-separated): "),
        "projects": input("Enter your projects (one per line, use Shift+Enter for multiple lines): "),
        "achievements": input("Enter your achievements (one per line, use Shift+Enter for multiple lines): "),
        "certifications": input("Enter your certifications (one per line, use Shift+Enter for multiple lines): "),
    }
    photo_path = input("Enter the path to your passport-size photo (leave blank if none): ").strip()
    return data, photo_path

if __name__ == "__main__":
    # Get user input
    resume_data, photo_path = get_user_input()

    # Replace Unicode characters
    for key, value in resume_data.items():
        if isinstance(value, str):
            resume_data[key] = value.replace('\u2013', '-')  # Replace en dash with hyphen

    # Generate the resume
    create_resume(resume_data, photo_path if photo_path else None)