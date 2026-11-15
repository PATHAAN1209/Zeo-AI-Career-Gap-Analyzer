import sys, os
import pymupdf as fitz

doc = fitz.open()
page = doc.new_page(width=595, height=842) # A4 size

text = """
ALEX CHEN
Full-Stack & Machine Learning Software Engineer
Email: alex.chen@example.com | GitHub: github.com/alexchen-dev | LinkedIn: linkedin.com/in/alexchen

PROFESSIONAL SUMMARY
Motivated Software Engineer with 2+ years of academic and internship experience in Python,
JavaScript, React.js, and Machine Learning pipelines. Proven track record of developing full-stack
web applications and training predictive models.

TECHNICAL SKILLS
- Programming Languages: Python, JavaScript (ES6+), HTML5, CSS3, SQL (PostgreSQL, SQLite)
- Frontend Development: React.js, Tailwind CSS, Responsive Design, REST API Integration, Context API
- Machine Learning & Data: Scikit-Learn, Pandas, NumPy, Data Preprocessing, Feature Engineering, EDA, Matplotlib
- Developer Tools: Git, GitHub, Docker (Basic), VS Code, Linux

EXPERIENCE
Machine Learning Intern | TechNova AI Solutions (May 2024 - Aug 2024)
- Developed end-to-end data preprocessing pipelines in Pandas handling missing values, scaling, and one-hot encoding.
- Trained predictive classification models using Scikit-Learn (Random Forest, Logistic Regression, XGBoost) achieving 87% F1-score.
- Evaluated models using 5-fold cross-validation, ROC-AUC curves, and confusion matrices.
- Integrated model inference into a lightweight FastAPI service for internal testing.

Frontend Engineering Co-op | Horizon Interactive (Jan 2024 - Apr 2024)
- Engineered responsive client-side components using React.js and modern CSS3 Flexbox/Grid layouts.
- Integrated REST APIs with Axios, implementing comprehensive error boundary handling and loading skeletons.
- Improved Lighthouse accessibility scores from 74 to 96 across 12 product pages.

PROJECTS
Smart Energy Consumption Predictor | Python, Scikit-Learn, Pandas, Streamlit
- Performed extensive exploratory data analysis (EDA) on 150,000+ time-series electrical grid readings.
- Engineered lag features and seasonal indicators to boost gradient boosting prediction accuracy by 14%.

Collaborative Task Matrix Dashboard | React.js, JavaScript, Tailwind CSS
- Created a Kanban productivity application featuring mobile-first responsive layout and local storage state persistence.

EDUCATION
B.S. in Computer Science | State University (Graduated 2024)
- Relevant Coursework: Linear Algebra, Probability & Statistics, Data Structures & Algorithms, Database Systems.
"""

# Insert text onto page
page.insert_text((50, 60), text.strip(), fontsize=10, lineheight=1.2)
pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_resume.pdf")
doc.save(pdf_path)
doc.close()
print("Created sample_resume.pdf successfully at:", pdf_path)
