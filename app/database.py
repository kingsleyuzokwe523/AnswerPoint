from app import db
from app.models import Subject, HomeContent, ExamTimetable, Admin
from werkzeug.security import generate_password_hash
import os


def init_default_data():
    """Initialize database with default data if empty"""

    # Check if admin exists
    if Admin.query.count() == 0:
        default_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        admin = Admin(
            username=os.environ.get('ADMIN_USERNAME', 'admin'),
            password=generate_password_hash(default_password)
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created - Username: admin, Password: {default_password}")

    # Check if subjects exist
    if Subject.query.count() == 0:
        add_default_subjects()

    # Check if home content exists
    if HomeContent.query.count() == 0:
        add_default_home_content()

    # Check if timetable exists
    if ExamTimetable.query.count() == 0:
        add_default_timetable()


def add_default_subjects():
    """Add all WAEC and NECO subjects"""
    all_subjects = [
        "Agricultural Science", "Air-conditioning & Refrigeration", "Animal Husbandry (Alt B)",
        "Applied Electricity", "Arabic", "Auto Body Repairs & Spray Painting",
        "Auto Electrical Works", "Auto Mechanical Work", "Auto Mechanics",
        "Automobile Parts Merchandising", "Basic Electricity", "Basic Electronics",
        "Biology", "Block Laying, Bricklaying & Concrete Works", "Bookkeeping",
        "Building Construction", "Business Management", "Carpentry & Joinery",
        "Catering Craft Practice", "Chemistry", "Christian Religious Studies",
        "Civic Education", "Clothing & Textiles", "Commerce", "Computer Studies",
        "Cosmetology", "Data Processing", "Dyeing & Bleaching", "Economics",
        "Efik", "Electrical Installation & Maintenance", "Electronics",
        "English Language", "Edo", "Financial Accounting", "Fisheries (Alt B)",
        "Foods and Nutrition", "French", "Furniture Making",
        "Further Mathematics / Mathematics (Elective)", "Garment Making",
        "General Mathematics / Mathematics (Core)", "Geography", "Government",
        "GSM Phone Maintenance & Repair", "Hausa", "Health Education / Health Science",
        "History", "Home Management", "Ibibio", "Igbo", "Insurance",
        "Islamic Studies", "Leather Goods Manufacturing & Repairs", "Literature-in-English",
        "Machine Woodworking", "Marketing", "Metalwork", "Mining", "Music",
        "Office Practice", "Painting & Decorating", "Photography", "Physical Education",
        "Physics", "Plumbing & Pipe Fitting", "Principles of Cost Accounting",
        "Printing Craft Practice", "Radio, Television & Electronic Works", "Salesmanship",
        "Stenography", "Store Keeping", "Store Management", "Technical Drawing",
        "Tourism", "Upholstery", "Visual Art", "Welding & Fabrication Engineering Craft",
        "Woodwork", "Yoruba"
    ]

    practical_subjects = ["Physics", "Chemistry", "Biology", "Agricultural Science",
                          "Computer Studies", "Electronics", "Basic Electricity",
                          "Health Education / Health Science", "Physical Education",
                          "Applied Electricity", "Basic Electronics", "GSM Phone Maintenance & Repair"]

    # Add WAEC subjects
    for name in all_subjects:
        has_prac = name in practical_subjects
        subject = Subject(name=name, exam_type="WAEC", has_practical=has_prac)
        db.session.add(subject)

    # Add NECO subjects
    for name in all_subjects:
        has_prac = name in practical_subjects
        subject = Subject(name=name, exam_type="NECO", has_practical=has_prac)
        db.session.add(subject)

    db.session.commit()
    print(f"Added {len(all_subjects) * 2} subjects")


def add_default_home_content():
    """Add default home page content"""
    default_content = [
        ("hero_title", "AnswerPoint 2026"),
        ("hero_text",
         "Your reliable source for accurate WAEC & NECO exam answers. Get verified solutions and excel in your examinations with our trusted answers."),
        ("announcement",
         "📢 HOT: 2026 WAEC/NECO Examinations are underway! Get your PIN from admin for verified answers."),
        ("instructions",
         "📌 HOW TO USE AnswerPoint:\n\n1️⃣ Get your unique 3-digit PIN from your administrator\n2️⃣ Enter the PIN in the box above\n3️⃣ Click 'See Answer' to view the solution\n4️⃣ Study the answers and succeed!"),
        ("whatsapp_link", "https://whatsapp.com/channel/yourlink"),
        ("telegram_link", "https://t.me/yourchannel"),
        ("footer_text", "© 2026 AnswerPoint - Your Exam Success Partner | WAEC & NECO Answers Portal")
    ]

    for section, content in default_content:
        home_content = HomeContent(section=section, content=content)
        db.session.add(home_content)

    db.session.commit()


def add_default_timetable():
    """Add sample exam timetable entries"""
    timetable_entries = [
        ("WAEC", "General Mathematics", "Paper 1 & 2", "May 15th, 2026", "9:00 AM - 1:00 PM"),
        ("WAEC", "English Language", "Paper 1 & 2", "May 16th, 2026", "9:00 AM - 12:30 PM"),
        ("WAEC", "Physics", "Theory & Objective", "May 18th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Physics Practical", "Practical", "May 19th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Chemistry", "Theory & Objective", "May 20th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Chemistry Practical", "Practical", "May 21st, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Biology", "Theory & Objective", "May 22nd, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Biology Practical", "Practical", "May 23rd, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Economics", "Theory & Objective", "May 24th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Government", "Theory & Objective", "May 25th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Literature-in-English", "Paper 1 & 2", "May 26th, 2026", "9:00 AM - 12:30 PM"),
        ("WAEC", "Geography", "Theory & Objective", "May 27th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Commerce", "Theory & Objective", "May 28th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Financial Accounting", "Theory & Objective", "May 29th, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Christian Religious Studies", "Theory & Objective", "May 30th, 2026", "9:00 AM - 11:30 AM"),
        ("WAEC", "Islamic Studies", "Theory & Objective", "May 30th, 2026", "9:00 AM - 11:30 AM"),
        ("WAEC", "Further Mathematics", "Paper 1 & 2", "June 1st, 2026", "9:00 AM - 12:30 PM"),
        ("WAEC", "Data Processing", "Theory & Objective", "June 2nd, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Computer Studies", "Theory & Objective", "June 3rd, 2026", "9:00 AM - 12:00 PM"),
        ("WAEC", "Technical Drawing", "Paper 1 & 2", "June 4th, 2026", "9:00 AM - 12:30 PM"),

        ("NECO", "General Mathematics", "Paper 1 & 2", "June 10th, 2026", "9:00 AM - 1:00 PM"),
        ("NECO", "English Language", "Paper 1 & 2", "June 11th, 2026", "9:00 AM - 12:30 PM"),
        ("NECO", "Physics", "Theory & Objective", "June 13th, 2026", "9:00 AM - 12:00 PM"),
        ("NECO", "Physics Practical", "Practical", "June 14th, 2026", "9:00 AM - 12:00 PM"),
        ("NECO", "Chemistry", "Theory & Objective", "June 15th, 2026", "9:00 AM - 12:00 PM"),
        ("NECO", "Chemistry Practical", "Practical", "June 16th, 2026", "9:00 AM - 12:00 PM"),
        ("NECO", "Biology", "Theory & Objective", "June 17th, 2026", "9:00 AM - 12:00 PM"),
        ("NECO", "Biology Practical", "Practical", "June 18th, 2026", "9:00 AM - 12:00 PM"),
        ("NECO", "Economics", "Theory & Objective", "June 19th, 2026", "9:00 AM - 12:00 PM"),
        ("NECO", "Government", "Theory & Objective", "June 20th, 2026", "9:00 AM - 12:00 PM")
    ]

    for exam_type, subject, paper, date, time in timetable_entries:
        entry = ExamTimetable(exam_type=exam_type, subject=subject, paper=paper,
                              date=date, time=time, year=2026)
        db.session.add(entry)

    db.session.commit()
    print(f"Added {len(timetable_entries)} timetable entries")