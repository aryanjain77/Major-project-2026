

# from resume_analyzer import ResumeAnalyzer
# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import joblib
# import pdfplumber
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.units import inch
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import nltk
# from nltk.corpus import stopwords
# import pandas as pd
# import json
# import re
# from io import BytesIO
# import uuid
# from datetime import datetime

# resume_analyzer = ResumeAnalyzer(os.getenv('GEMINI_API_KEY'))

# # ===================== RESUME-BASED ROADMAP ROUTES =====================

# @app.route('/api/roadmap/analyze-resume', methods=['POST'])
# def analyze_resume_for_roadmap():
#     """Analyze resume and generate personalized career roadmap"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume using Gemini
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get primary role recommendation
#         primary_role = career_info.get('primary_role', 'Software Developer')
        
#         # Generate personalized roadmap for primary role
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, primary_role
#         )
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         # Save the personalized roadmap to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{primary_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'career_analysis': {
#                 'primary_role': primary_role,
#                 'experience_level': career_info.get('experience_level'),
#                 'skills': career_info.get('skills', []),
#                 'skill_gaps': personalized_roadmap.get('skill_gaps', []),
#                 'strengths': career_info.get('strengths', []),
#             },
#             'personalized_roadmap': personalized_roadmap,
#             'alternative_careers': alternative_careers,
#             'message': 'Resume analyzed successfully'
#         })
        
#     except Exception as e:
#         print(f"Error analyzing resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500


# @app.route('/api/roadmap/generate-for-role', methods=['POST'])
# def generate_roadmap_for_specific_role():
#     """Generate roadmap for a specific role based on resume analysis"""
#     try:
#         data = request.json
        
#         if 'resume_text' not in data and 'career_info' not in data:
#             return jsonify({'error': 'Resume text or career info required'}), 400
        
#         job_role = data.get('job_role')
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         # If career_info is provided, use it; otherwise analyze resume_text
#         if 'career_info' in data:
#             career_info = data['career_info']
#         else:
#             resume_text = data['resume_text']
#             career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Generate personalized roadmap
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, job_role
#         )
        
#         # Save to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{job_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'roadmap': personalized_roadmap,
#             'message': f'Personalized roadmap generated for {job_role}'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap for role: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500


# @app.route('/api/career/analyze', methods=['POST'])
# def quick_career_analysis():
#     """Quick career analysis from resume (without full roadmap generation)"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         return jsonify({
#             'success': True,
#             'career_info': career_info,
#             'alternative_careers': alternative_careers
#         })
        
#     except Exception as e:
#         print(f"Error in career analysis: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze career: {str(e)}'}), 500

# # Import new modules for roadmap features
# from database import DatabaseManager
# from roadmap_generator import RoadmapGenerator
# from resource_finder import ResourceFinder

# app = Flask(__name__)
# # CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
# CORS(app, origins="http://localhost:3000")

# # NLTK setup
# nltk.download('stopwords', quiet=True)
# try:
#     stop = set(stopwords.words('english'))
# except Exception:
#     print("Warning: NLTK stopwords not available")
#     stop = set()

# # Load existing model
# try:
#     model1 = joblib.load('resume_model.pkl')
# except FileNotFoundError:
#     print("Error: resume_model.pkl not found. Run train_model.py first.")
#     model1 = None

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# # Initialize new components for roadmap features
# db_manager = DatabaseManager()
# roadmap_generator = RoadmapGenerator(os.getenv('GEMINI_API_KEY'))
# resource_finder = ResourceFinder()

# # for m in genai.list_models():
# #     print(m.name)

# # ===================== EXISTING ROUTES =====================

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Welcome to the Resume Screening API'})

# @app.route('/predict', methods=['POST'])
# def predict():

#     if not model1:
#         return jsonify({'error': 'Model not loaded'}), 500
    
#     file = request.files['resume']
#     experience_years = float(request.form.get('experience_years', 0))
#     projects_count = int(request.form.get('projects_count', 0))
#     salary_expectation = float(request.form.get('salary_expectation', 0))
    
#     with pdfplumber.open(file) as pdf:
#         resume_text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    
#     cleaned_text = resume_text.lower().replace(r'[^\w\s]', '')
#     cleaned_text = ' '.join(word for word in str(cleaned_text).split() if word not in stop)
    
#     input_data = pd.DataFrame({
#         'Text': [cleaned_text],
#         'Experience (Years)': [experience_years],
#         'Projects Count': [projects_count],
#         'Salary Expectation ($)': [salary_expectation]
#     })
    
#     prob = model1.predict_proba(input_data)[0][1] * 100
#     return jsonify({'chance': prob})


# def extract_contact_info(resume_text):
#     name = resume_text.split("\n")[0].strip()  # usually first line
#     email = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
#     phone = re.search(r'\b\d{10}\b', resume_text)  # Indian 10-digit number
#     linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/[^\s]+', resume_text)
#     github = re.search(r'(https?://)?(www\.)?github\.com/[^\s]+', resume_text)

#     return {
#         "name": name,
#         "email": email.group() if email else "",
#         "phone": phone.group() if phone else "",
#         "linkedin": linkedin.group() if linkedin else "",
#         "github": github.group() if github else ""
#     }

# @app.route('/generate_cover_letter', methods=['POST'])
# def generate_cover():
#     try:
#         job_desc = request.form['job_desc']
#         hr_name = request.form['hr_name']
#         resume_file = request.files['resume_file']

#         # Extract text from PDF
#         # with pdfplumber.open(resume_file) as pdf:
#         #     resume_text = ' '.join(
#         #         page.extract_text() or '' for page in pdf.pages
#         #     )
#         #     contact_info = extract_contact_info(resume_text)

#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(page.extract_text() or '' for page in pdf.pages)

#         contact_info = extract_contact_info(resume_text)

#         model = genai.GenerativeModel('gemini-2.0-flash')
#         prompt = f"""
#         Write a professional cover letter for this job: {job_desc}.
#         Address it to {hr_name}.
        
#         Incorporate details from this resume: {resume_text}.

#         Important: Do NOT include headers like [Your Name], [Your Address], [Date],
#         or any placeholder personal/contact information at the top.
#         Start directly with the greeting (e.g., 'Dear {hr_name},').
#         Do NOT include placeholders such as [Platform where you saw the advertisement],
#         [Address], or any square-bracketed text.
#         Do NOT fabricate details not present in the resume or job description.
#         End with a professional closing (e.g., "Sincerely, Aryan Jain") including my name and contact info.

#         """

#         cover_text = ""
#         response = model.generate_content(prompt)
#         print(response)
#         if response and hasattr(response, "candidates"):
#             for candidate in response.candidates:
#                 for part in candidate.content.parts:
#                     if part.text:
#                         cover_text += part.text + "\n"

#         if not cover_text.strip():
#             raise Exception("api returned empty text")

#         return jsonify({'cover_letter': cover_text.strip()})

#         # print(response)
#         # return jsonify({'cover_letter': response.text})

#     except Exception as e:
#         print(f"Error generating cover letter: {e}")
#         return jsonify({'error': 'Failed to generate cover letter'}), 500


# def safe_parse_json(data_str):
#     """Safely parse JSON string, return empty list if parsing fails"""
#     if not data_str:
#         return []
#     try:
#         parsed = json.loads(data_str)
#         return parsed if isinstance(parsed, list) else []
#     except (json.JSONDecodeError, TypeError):
#         return []

# @app.route('/api/resume/create', methods=['POST'])
# def generate_resume():
#     try:
#         # Handle both JSON and FormData
#         if request.content_type and 'multipart/form-data' in request.content_type:
#             # Extract data from form
#             data = {}
#             for key in request.form:
#                 if key in ['workExperience', 'education', 'projects', 'certifications', 'achievements']:
#                     data[key] = safe_parse_json(request.form[key])
#                 else:
#                     data[key] = request.form[key]
            
#             # Handle file upload
#             photo_file = request.files.get('photo')
#         else:
#             # Handle JSON data
#             data = request.json or {}
#             photo_file = None

#         # Create PDF in memory
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
#         # Define styles
#         styles = getSampleStyleSheet()
#         title_style = ParagraphStyle(
#             'CustomTitle',
#             parent=styles['Heading1'],
#             fontSize=18,
#             spaceAfter=12,
#             alignment=1,  # Center alignment
#             textColor='#2C5AA0'
#         )
#         heading_style = ParagraphStyle(
#             'CustomHeading',
#             parent=styles['Heading2'],
#             fontSize=14,
#             spaceAfter=8,
#             spaceBefore=12,
#             textColor='#1F4788',
#             borderWidth=1,
#             borderColor='#1F4788',
#             borderPadding=4
#         )
#         normal_style = styles['Normal']
#         normal_style.fontSize = 10
#         normal_style.leading = 12
        
#         # Build content
#         content = []
        
#         # Name (Title)
#         if data.get('fullName'):
#             content.append(Paragraph(data['fullName'].upper(), title_style))
#             content.append(Spacer(1, 12))
        
#         # Contact Info
#         contact_info = []
#         if data.get('email'):
#             contact_info.append(f"📧 {data['email']}")
#         if data.get('phoneNumber'):
#             contact_info.append(f"📱 {data['phoneNumber']}")
#         if data.get('location'):
#             contact_info.append(f"📍 {data['location']}")
        
#         if contact_info:
#             content.append(Paragraph(" | ".join(contact_info), normal_style))
#             content.append(Spacer(1, 8))
        
#         # Professional Links
#         profile_links = []
#         if data.get('linkedinUrl'):
#             profile_links.append(f"LinkedIn: {data['linkedinUrl']}")
#         if data.get('githubPortfolioUrl'):
#             profile_links.append(f"Portfolio: {data['githubPortfolioUrl']}")
        
#         if profile_links:
#             content.append(Paragraph(" | ".join(profile_links), normal_style))
#             content.append(Spacer(1, 12))
        
#         # Job Title
#         if data.get('jobTitle'):
#             job_title_style = ParagraphStyle(
#                 'JobTitle',
#                 parent=styles['Heading2'],
#                 fontSize=12,
#                 spaceAfter=8,
#                 alignment=1,
#                 textColor='#555555'
#             )
#             content.append(Paragraph(data['jobTitle'], job_title_style))
        
#         # Professional Summary
#         if data.get('professionalSummary'):
#             content.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
#             content.append(Paragraph(data['professionalSummary'], normal_style))
#             content.append(Spacer(1, 12))
        
#         # Skills
#         if data.get('technicalSkills') or data.get('softSkills'):
#             content.append(Paragraph("SKILLS", heading_style))
#             if data.get('technicalSkills'):
#                 content.append(Paragraph(f"<b>Technical Skills:</b> {data['technicalSkills']}", normal_style))
#             if data.get('softSkills'):
#                 content.append(Paragraph(f"<b>Soft Skills:</b> {data['softSkills']}", normal_style))
#             content.append(Spacer(1, 12))
        
#         # Work Experience
#         work_experience = data.get('workExperience', [])
#         if work_experience and any(exp.get('jobTitle') or exp.get('companyName') for exp in work_experience):
#             content.append(Paragraph("WORK EXPERIENCE", heading_style))
#             for exp in work_experience:
#                 if exp.get('jobTitle') or exp.get('companyName'):
#                     # Job title and company
#                     job_title = exp.get('jobTitle', 'N/A')
#                     company = exp.get('companyName', 'N/A')
#                     exp_header = f"<b>{job_title}</b> | {company}"
#                     content.append(Paragraph(exp_header, normal_style))
                    
#                     # Date and location
#                     date_info = []
#                     if exp.get('startDate') or exp.get('endDate'):
#                         start_date = exp.get('startDate', 'N/A')
#                         end_date = exp.get('endDate', 'Present')
#                         date_info.append(f"{start_date} - {end_date}")
#                     if exp.get('location'):
#                         date_info.append(exp.get('location'))
                    
#                     if date_info:
#                         content.append(Paragraph(" | ".join(date_info), normal_style))
                    
#                     # Responsibilities
#                     if exp.get('responsibilities'):
#                         responsibilities = exp.get('responsibilities').strip()
#                         if responsibilities:
#                             # Split by bullet points or newlines
#                             resp_lines = [line.strip() for line in responsibilities.replace('•', '\n').split('\n') if line.strip()]
#                             for line in resp_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     # Achievements
#                     if exp.get('achievements'):
#                         achievements = exp.get('achievements').strip()
#                         if achievements:
#                             # Split by bullet points or newlines
#                             ach_lines = [line.strip() for line in achievements.replace('•', '\n').split('\n') if line.strip()]
#                             for line in ach_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         # Education
#         education = data.get('education', [])
#         if education and any(edu.get('degree') or edu.get('universityName') for edu in education):
#             content.append(Paragraph("EDUCATION", heading_style))
#             for edu in education:
#                 if edu.get('degree') or edu.get('universityName'):
#                     degree = edu.get('degree', 'N/A')
#                     university = edu.get('universityName', 'N/A')
#                     edu_header = f"<b>{degree}</b>"
#                     content.append(Paragraph(edu_header, normal_style))
#                     content.append(Paragraph(university, normal_style))
                    
#                     # Date, location, GPA
#                     edu_details = []
#                     if edu.get('location'):
#                         edu_details.append(edu.get('location'))
#                     if edu.get('startDate') or edu.get('endDate'):
#                         start_date = edu.get('startDate', 'N/A')
#                         end_date = edu.get('endDate', 'N/A')
#                         edu_details.append(f"{start_date} - {end_date}")
#                     if edu.get('gpa'):
#                         edu_details.append(f"GPA: {edu.get('gpa')}")
                    
#                     if edu_details:
#                         content.append(Paragraph(" | ".join(edu_details), normal_style))
                    
#                     if edu.get('relevantCoursework'):
#                         content.append(Paragraph(f"<b>Relevant Coursework:</b> {edu.get('relevantCoursework')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         # Projects
#         projects = data.get('projects', [])
#         if projects and any(proj.get('projectTitle') for proj in projects):
#             content.append(Paragraph("PROJECTS", heading_style))
#             for proj in projects:
#                 if proj.get('projectTitle'):
#                     content.append(Paragraph(f"<b>{proj.get('projectTitle')}</b>", normal_style))
                    
#                     if proj.get('description'):
#                         content.append(Paragraph(proj.get('description'), normal_style))
                    
#                     if proj.get('technologiesUsed'):
#                         content.append(Paragraph(f"<b>Technologies:</b> {proj.get('technologiesUsed')}", normal_style))
                    
#                     if proj.get('impact'):
#                         content.append(Paragraph(f"<b>Impact:</b> {proj.get('impact')}", normal_style))
                    
#                     if proj.get('projectLink'):
#                         content.append(Paragraph(f"<b>Link:</b> {proj.get('projectLink')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         # Certifications
#         certifications = data.get('certifications', [])
#         if certifications and any(cert.get('certificationName') for cert in certifications):
#             content.append(Paragraph("CERTIFICATIONS", heading_style))
#             for cert in certifications:
#                 if cert.get('certificationName'):
#                     cert_text = f"• <b>{cert.get('certificationName')}</b>"
#                     if cert.get('issuingAuthority'):
#                         cert_text += f" - {cert.get('issuingAuthority')}"
#                     if cert.get('date'):
#                         cert_text += f" ({cert.get('date')})"
#                     content.append(Paragraph(cert_text, normal_style))
#             content.append(Spacer(1, 12))
        
#         # Achievements
#         achievements = data.get('achievements', [])
#         if achievements and any(ach.get('title') for ach in achievements):
#             content.append(Paragraph("ACHIEVEMENTS", heading_style))
#             for ach in achievements:
#                 if ach.get('title'):
#                     ach_text = f"• <b>{ach.get('title')}</b>"
#                     if ach.get('organization'):
#                         ach_text += f" - {ach.get('organization')}"
#                     if ach.get('date'):
#                         ach_text += f" ({ach.get('date')})"
#                     content.append(Paragraph(ach_text, normal_style))
#                     if ach.get('description'):
#                         content.append(Paragraph(f"  {ach.get('description')}", normal_style))
#             content.append(Spacer(1, 12))
        
#         # Additional sections
#         if data.get('languages'):
#             content.append(Paragraph("LANGUAGES", heading_style))
#             content.append(Paragraph(data['languages'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('publications'):
#             content.append(Paragraph("PUBLICATIONS", heading_style))
#             content.append(Paragraph(data['publications'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('volunteering'):
#             content.append(Paragraph("VOLUNTEERING", heading_style))
#             content.append(Paragraph(data['volunteering'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('hobbies'):
#             content.append(Paragraph("HOBBIES & INTERESTS", heading_style))
#             content.append(Paragraph(data['hobbies'], normal_style))
        
#         # Build PDF
#         doc.build(content)
#         buffer.seek(0)
        
#         return send_file(
#             buffer,
#             as_attachment=True,
#             download_name='resume.pdf',
#             mimetype='application/pdf'
#         )
        
#     except Exception as e:
#         print(f"Error generating resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate resume: {str(e)}'}), 500


# # ===================== NEW ROADMAP ROUTES =====================

# @app.route('/api/roadmap/generate', methods=['POST'])
# def generate_roadmap():
#     """Generate a new roadmap for a job role"""
#     try:
#         data = request.json
#         job_role = data.get('job_role')
#         experience_level = data.get('experience_level', 'beginner')
#         target_company = data.get('target_company')
#         user_skills = data.get('user_skills', [])
#         available_hours = data.get('available_hours_per_week', 10)
        
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         # Check if roadmap already exists
#         existing_roadmap_id, existing_roadmap = db_manager.get_roadmap(job_role)
        
#         if existing_roadmap:
#             # Customize existing roadmap for user
#             if user_skills:
#                 customized_roadmap = roadmap_generator.update_roadmap_for_user(
#                     existing_roadmap, user_skills, available_hours
#                 )
#             else:
#                 customized_roadmap = existing_roadmap
            
#             return jsonify({
#                 'roadmap_id': existing_roadmap_id,
#                 'roadmap': customized_roadmap,
#                 'message': 'Retrieved existing roadmap'
#             })
        
#         # Generate new roadmap
#         roadmap_data = roadmap_generator.generate_roadmap(
#             job_role, experience_level, target_company
#         )
        
#         # Customize for user if skills provided
#         if user_skills:
#             roadmap_data = roadmap_generator.update_roadmap_for_user(
#                 roadmap_data, user_skills, available_hours
#             )
        
#         # Save to database
#         roadmap_id = db_manager.save_roadmap(job_role, roadmap_data)
        
#         # Add roadmap_id to the data for frontend
#         roadmap_data['roadmap_id'] = roadmap_id
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data,
#             'message': 'Roadmap generated successfully'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/resources/<step_id>', methods=['GET'])
# def get_step_resources(roadmap_id, step_id):
#     """Get resources for a specific step"""
#     try:
#         # Check if resources already exist in database
#         existing_resources = db_manager.get_resources(step_id)
        
#         if existing_resources:
#             return jsonify({
#                 'step_id': step_id,
#                 'resources': existing_resources
#             })
        
#         # Get step details from roadmap
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         # Find the step
#         step_data = None
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 if step['step_id'] == step_id:
#                     step_data = step
#                     break
#             if step_data:
#                 break
        
#         if not step_data:
#             return jsonify({'error': 'Step not found'}), 404
        
#         # Find resources for this step
#         resources = resource_finder.get_all_resources_for_step(
#             step_data['title'], 
#             step_data['description']
#         )
        
#         # Save resources to database
#         if resources:
#             db_manager.save_resources(step_id, resources)
        
#         return jsonify({
#             'step_id': step_id,
#             'resources': resources
#         })
        
#     except Exception as e:
#         print(f"Error getting step resources: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to get resources: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['GET'])
# def get_roadmap_progress(roadmap_id):
#     """Get user progress for a roadmap"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'user_id': user_id,
#             'progress': progress
#         })
        
#     except Exception as e:
#         print(f"Error getting progress: {str(e)}")
#         return jsonify({'error': f'Failed to get progress: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['POST'])
# def update_progress(roadmap_id):
#     """Update user progress for a step"""
#     try:
#         data = request.json
#         user_id = data.get('user_id', 'default_user')
#         step_id = data.get('step_id')
#         completed = data.get('completed', False)
#         time_spent = data.get('time_spent', 0)
        
#         if not step_id:
#             return jsonify({'error': 'Step ID is required'}), 400
        
#         db_manager.save_user_progress(user_id, roadmap_id, step_id, completed, time_spent)
        
#         return jsonify({
#             'message': 'Progress updated successfully',
#             'roadmap_id': roadmap_id,
#             'step_id': step_id,
#             'completed': completed
#         })
        
#     except Exception as e:
#         print(f"Error updating progress: {str(e)}")
#         return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500

# @app.route('/api/roadmap/popular-roles', methods=['GET'])
# def get_popular_roles():
#     """Get list of popular job roles for roadmap generation"""
#     try:
#         popular_roles = [
#             {
#                 'id': 'software-developer',
#                 'title': 'Software Developer',
#                 'description': 'Full-stack and backend development roles',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'Very High',
#                 'skills': ['Programming', 'Problem Solving', 'System Design']
#             },
#             {
#                 'id': 'data-scientist',
#                 'title': 'Data Scientist',
#                 'description': 'Analyze data to derive business insights',
#                 'avg_salary': '6-20 LPA',
#                 'demand': 'High',
#                 'skills': ['Python', 'Statistics', 'Machine Learning']
#             },
#             {
#                 'id': 'product-manager',
#                 'title': 'Product Manager',
#                 'description': 'Define product strategy and roadmap',
#                 'avg_salary': '8-25 LPA',
#                 'demand': 'High',
#                 'skills': ['Strategy', 'Analytics', 'Communication']
#             },
#             {
#                 'id': 'ui-ux-designer',
#                 'title': 'UI/UX Designer',
#                 'description': 'Design user interfaces and experiences',
#                 'avg_salary': '4-12 LPA',
#                 'demand': 'High',
#                 'skills': ['Design Tools', 'User Research', 'Prototyping']
#             },
#             {
#                 'id': 'business-analyst',
#                 'title': 'Business Analyst',
#                 'description': 'Bridge between business and technology',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'High',
#                 'skills': ['Analysis', 'Documentation', 'Process Improvement']
#             },
#             {
#                 'id': 'devops-engineer',
#                 'title': 'DevOps Engineer',
#                 'description': 'Manage deployment and infrastructure',
#                 'avg_salary': '6-18 LPA',
#                 'demand': 'Very High',
#                 'skills': ['Cloud', 'Automation', 'Monitoring']
#             },
#             {
#                 'id': 'consultant',
#                 'title': 'Management Consultant',
#                 'description': 'Provide strategic business advice',
#                 'avg_salary': '8-30 LPA',
#                 'demand': 'Medium',
#                 'skills': ['Problem Solving', 'Presentation', 'Business Acumen']
#             },
#             {
#                 'id': 'digital-marketing',
#                 'title': 'Digital Marketing Specialist',
#                 'description': 'Online marketing and growth strategies',
#                 'avg_salary': '3-10 LPA',
#                 'demand': 'High',
#                 'skills': ['SEO/SEM', 'Analytics', 'Content Marketing']
#             }
#         ]
        
#         return jsonify({'roles': popular_roles})
        
#     except Exception as e:
#         print(f"Error getting popular roles: {str(e)}")
#         return jsonify({'error': 'Failed to get popular roles'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>', methods=['GET'])
# def get_roadmap_by_id(roadmap_id):
#     """Get a specific roadmap by ID"""
#     try:
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
        
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data
#         })
        
#     except Exception as e:
#         print(f"Error getting roadmap: {str(e)}")
#         return jsonify({'error': f'Failed to get roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/analytics', methods=['GET'])
# def get_roadmap_analytics(roadmap_id):
#     """Get analytics for a roadmap (completion rates, time spent, etc.)"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
        
#         # Get roadmap data
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         # Get user progress
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         # Calculate analytics
#         total_steps = 0
#         completed_steps = 0
#         total_time_spent = 0
        
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 total_steps += 1
#                 step_id = step['step_id']
                
#                 if step_id in progress:
#                     if progress[step_id]['completed']:
#                         completed_steps += 1
#                     total_time_spent += progress[step_id]['time_spent']
        
#         completion_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
#         estimated_total_hours = sum(
#             sum(step.get('estimated_hours', 0) for step in phase.get('steps', []))
#             for phase in roadmap_data.get('phases', [])
#         )
        
#         analytics = {
#             'completion_percentage': round(completion_percentage, 2),
#             'completed_steps': completed_steps,
#             'total_steps': total_steps,
#             'time_spent_hours': total_time_spent,
#             'estimated_total_hours': estimated_total_hours,
#             'progress_by_phase': [],
#             'recent_activity': []
#         }
        
#         # Phase-wise progress
#         for phase in roadmap_data.get('phases', []):
#             phase_steps = len(phase.get('steps', []))
#             phase_completed = sum(
#                 1 for step in phase.get('steps', [])
#                 if step['step_id'] in progress and progress[step['step_id']]['completed']
#             )
            
#             analytics['progress_by_phase'].append({
#                 'phase_name': phase['phase_name'],
#                 'completed_steps': phase_completed,
#                 'total_steps': phase_steps,
#                 'completion_percentage': (phase_completed / phase_steps * 100) if phase_steps > 0 else 0
#             })
        
#         return jsonify(analytics)
        
#     except Exception as e:
#         print(f"Error getting analytics: {str(e)}")
#         return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500

# # ===================== MAIN APPLICATION ====================

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print("📋 Features available:")
#     print("  • Resume screening and generation")
#     print("  • Cover letter generation")
#     print("  • AI-powered roadmap creation")
#     print("  • Progress tracking")
#     print("  • Resource recommendations")
#     print("🌐 Server running on http://localhost:5000")
#     app.run(debug=True)



# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import joblib
# import pdfplumber
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.units import inch
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import nltk
# from nltk.corpus import stopwords
# import pandas as pd
# import json
# import re
# from io import BytesIO
# import uuid
# from datetime import datetime

# # Import new modules for roadmap features
# from database import DatabaseManager
# from roadmap_generator import RoadmapGenerator
# from resource_finder import ResourceFinder
# from resume_analyzer import ResumeAnalyzer

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# # NLTK setup
# nltk.download('stopwords', quiet=True)
# try:
#     stop = set(stopwords.words('english'))
# except Exception:
#     print("Warning: NLTK stopwords not available")
#     stop = set()

# # Load existing model
# try:
#     model1 = joblib.load('resume_model.pkl')
# except FileNotFoundError:
#     print("Error: resume_model.pkl not found. Run train_model.py first.")
#     model1 = None

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# # Initialize new components for roadmap features
# db_manager = DatabaseManager()
# roadmap_generator = RoadmapGenerator(os.getenv('GEMINI_API_KEY'))
# resource_finder = ResourceFinder()
# resume_analyzer = ResumeAnalyzer(os.getenv('GEMINI_API_KEY'))

# # ===================== EXISTING ROUTES =====================

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Welcome to the Resume Screening API'})

# @app.route('/predict', methods=['POST'])
# def predict():
#     if not model1:
#         return jsonify({'error': 'Model not loaded'}), 500
    
#     file = request.files['resume']
#     experience_years = float(request.form.get('experience_years', 0))
#     projects_count = int(request.form.get('projects_count', 0))
#     salary_expectation = float(request.form.get('salary_expectation', 0))
    
#     with pdfplumber.open(file) as pdf:
#         resume_text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    
#     cleaned_text = resume_text.lower().replace(r'[^\w\s]', '')
#     cleaned_text = ' '.join(word for word in str(cleaned_text).split() if word not in stop)
    
#     input_data = pd.DataFrame({
#         'Text': [cleaned_text],
#         'Experience (Years)': [experience_years],
#         'Projects Count': [projects_count],
#         'Salary Expectation ($)': [salary_expectation]
#     })
    
#     prob = model1.predict_proba(input_data)[0][1] * 100
#     return jsonify({'chance': prob})


# def extract_contact_info(resume_text):
#     name = resume_text.split("\n")[0].strip()
#     email = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
#     phone = re.search(r'\b\d{10}\b', resume_text)
#     linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/[^\s]+', resume_text)
#     github = re.search(r'(https?://)?(www\.)?github\.com/[^\s]+', resume_text)

#     return {
#         "name": name,
#         "email": email.group() if email else "",
#         "phone": phone.group() if phone else "",
#         "linkedin": linkedin.group() if linkedin else "",
#         "github": github.group() if github else ""
#     }

# @app.route('/generate_cover_letter', methods=['POST'])
# def generate_cover():
#     try:
#         job_desc = request.form['job_desc']
#         hr_name = request.form['hr_name']
#         resume_file = request.files['resume_file']

#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(page.extract_text() or '' for page in pdf.pages)

#         contact_info = extract_contact_info(resume_text)

#         model = genai.GenerativeModel('gemini-2.0-flash')
#         prompt = f"""
#         Write a professional cover letter for this job: {job_desc}.
#         Address it to {hr_name}.
        
#         Incorporate details from this resume: {resume_text}.

#         Important: Do NOT include headers like [Your Name], [Your Address], [Date],
#         or any placeholder personal/contact information at the top.
#         Start directly with the greeting (e.g., 'Dear {hr_name},').
#         Do NOT include placeholders such as [Platform where you saw the advertisement],
#         [Address], or any square-bracketed text.
#         Do NOT fabricate details not present in the resume or job description.
#         End with a professional closing (e.g., "Sincerely, Aryan Jain") including my name and contact info.
#         """

#         cover_text = ""
#         response = model.generate_content(prompt)
#         if response and hasattr(response, "candidates"):
#             for candidate in response.candidates:
#                 for part in candidate.content.parts:
#                     if part.text:
#                         cover_text += part.text + "\n"

#         if not cover_text.strip():
#             raise Exception("api returned empty text")

#         return jsonify({'cover_letter': cover_text.strip()})

#     except Exception as e:
#         print(f"Error generating cover letter: {e}")
#         return jsonify({'error': 'Failed to generate cover letter'}), 500


# def safe_parse_json(data_str):
#     """Safely parse JSON string, return empty list if parsing fails"""
#     if not data_str:
#         return []
#     try:
#         parsed = json.loads(data_str)
#         return parsed if isinstance(parsed, list) else []
#     except (json.JSONDecodeError, TypeError):
#         return []

# @app.route('/api/resume/create', methods=['POST'])
# def generate_resume():
#     try:
#         if request.content_type and 'multipart/form-data' in request.content_type:
#             data = {}
#             for key in request.form:
#                 if key in ['workExperience', 'education', 'projects', 'certifications', 'achievements']:
#                     data[key] = safe_parse_json(request.form[key])
#                 else:
#                     data[key] = request.form[key]
            
#             photo_file = request.files.get('photo')
#         else:
#             data = request.json or {}
#             photo_file = None

#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
#         styles = getSampleStyleSheet()
#         title_style = ParagraphStyle(
#             'CustomTitle',
#             parent=styles['Heading1'],
#             fontSize=18,
#             spaceAfter=12,
#             alignment=1,
#             textColor='#2C5AA0'
#         )
#         heading_style = ParagraphStyle(
#             'CustomHeading',
#             parent=styles['Heading2'],
#             fontSize=14,
#             spaceAfter=8,
#             spaceBefore=12,
#             textColor='#1F4788',
#             borderWidth=1,
#             borderColor='#1F4788',
#             borderPadding=4
#         )
#         normal_style = styles['Normal']
#         normal_style.fontSize = 10
#         normal_style.leading = 12
        
#         content = []
        
#         if data.get('fullName'):
#             content.append(Paragraph(data['fullName'].upper(), title_style))
#             content.append(Spacer(1, 12))
        
#         contact_info = []
#         if data.get('email'):
#             contact_info.append(f"📧 {data['email']}")
#         if data.get('phoneNumber'):
#             contact_info.append(f"📱 {data['phoneNumber']}")
#         if data.get('location'):
#             contact_info.append(f"📍 {data['location']}")
        
#         if contact_info:
#             content.append(Paragraph(" | ".join(contact_info), normal_style))
#             content.append(Spacer(1, 8))
        
#         profile_links = []
#         if data.get('linkedinUrl'):
#             profile_links.append(f"LinkedIn: {data['linkedinUrl']}")
#         if data.get('githubPortfolioUrl'):
#             profile_links.append(f"Portfolio: {data['githubPortfolioUrl']}")
        
#         if profile_links:
#             content.append(Paragraph(" | ".join(profile_links), normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('jobTitle'):
#             job_title_style = ParagraphStyle(
#                 'JobTitle',
#                 parent=styles['Heading2'],
#                 fontSize=12,
#                 spaceAfter=8,
#                 alignment=1,
#                 textColor='#555555'
#             )
#             content.append(Paragraph(data['jobTitle'], job_title_style))
        
#         if data.get('professionalSummary'):
#             content.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
#             content.append(Paragraph(data['professionalSummary'], normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('technicalSkills') or data.get('softSkills'):
#             content.append(Paragraph("SKILLS", heading_style))
#             if data.get('technicalSkills'):
#                 content.append(Paragraph(f"<b>Technical Skills:</b> {data['technicalSkills']}", normal_style))
#             if data.get('softSkills'):
#                 content.append(Paragraph(f"<b>Soft Skills:</b> {data['softSkills']}", normal_style))
#             content.append(Spacer(1, 12))
        
#         work_experience = data.get('workExperience', [])
#         if work_experience and any(exp.get('jobTitle') or exp.get('companyName') for exp in work_experience):
#             content.append(Paragraph("WORK EXPERIENCE", heading_style))
#             for exp in work_experience:
#                 if exp.get('jobTitle') or exp.get('companyName'):
#                     job_title = exp.get('jobTitle', 'N/A')
#                     company = exp.get('companyName', 'N/A')
#                     exp_header = f"<b>{job_title}</b> | {company}"
#                     content.append(Paragraph(exp_header, normal_style))
                    
#                     date_info = []
#                     if exp.get('startDate') or exp.get('endDate'):
#                         start_date = exp.get('startDate', 'N/A')
#                         end_date = exp.get('endDate', 'Present')
#                         date_info.append(f"{start_date} - {end_date}")
#                     if exp.get('location'):
#                         date_info.append(exp.get('location'))
                    
#                     if date_info:
#                         content.append(Paragraph(" | ".join(date_info), normal_style))
                    
#                     if exp.get('responsibilities'):
#                         responsibilities = exp.get('responsibilities').strip()
#                         if responsibilities:
#                             resp_lines = [line.strip() for line in responsibilities.replace('•', '\n').split('\n') if line.strip()]
#                             for line in resp_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     if exp.get('achievements'):
#                         achievements = exp.get('achievements').strip()
#                         if achievements:
#                             ach_lines = [line.strip() for line in achievements.replace('•', '\n').split('\n') if line.strip()]
#                             for line in ach_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         education = data.get('education', [])
#         if education and any(edu.get('degree') or edu.get('universityName') for edu in education):
#             content.append(Paragraph("EDUCATION", heading_style))
#             for edu in education:
#                 if edu.get('degree') or edu.get('universityName'):
#                     degree = edu.get('degree', 'N/A')
#                     university = edu.get('universityName', 'N/A')
#                     edu_header = f"<b>{degree}</b>"
#                     content.append(Paragraph(edu_header, normal_style))
#                     content.append(Paragraph(university, normal_style))
                    
#                     edu_details = []
#                     if edu.get('location'):
#                         edu_details.append(edu.get('location'))
#                     if edu.get('startDate') or edu.get('endDate'):
#                         start_date = edu.get('startDate', 'N/A')
#                         end_date = edu.get('endDate', 'N/A')
#                         edu_details.append(f"{start_date} - {end_date}")
#                     if edu.get('gpa'):
#                         edu_details.append(f"GPA: {edu.get('gpa')}")
                    
#                     if edu_details:
#                         content.append(Paragraph(" | ".join(edu_details), normal_style))
                    
#                     if edu.get('relevantCoursework'):
#                         content.append(Paragraph(f"<b>Relevant Coursework:</b> {edu.get('relevantCoursework')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         projects = data.get('projects', [])
#         if projects and any(proj.get('projectTitle') for proj in projects):
#             content.append(Paragraph("PROJECTS", heading_style))
#             for proj in projects:
#                 if proj.get('projectTitle'):
#                     content.append(Paragraph(f"<b>{proj.get('projectTitle')}</b>", normal_style))
                    
#                     if proj.get('description'):
#                         content.append(Paragraph(proj.get('description'), normal_style))
                    
#                     if proj.get('technologiesUsed'):
#                         content.append(Paragraph(f"<b>Technologies:</b> {proj.get('technologiesUsed')}", normal_style))
                    
#                     if proj.get('impact'):
#                         content.append(Paragraph(f"<b>Impact:</b> {proj.get('impact')}", normal_style))
                    
#                     if proj.get('projectLink'):
#                         content.append(Paragraph(f"<b>Link:</b> {proj.get('projectLink')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         certifications = data.get('certifications', [])
#         if certifications and any(cert.get('certificationName') for cert in certifications):
#             content.append(Paragraph("CERTIFICATIONS", heading_style))
#             for cert in certifications:
#                 if cert.get('certificationName'):
#                     cert_text = f"• <b>{cert.get('certificationName')}</b>"
#                     if cert.get('issuingAuthority'):
#                         cert_text += f" - {cert.get('issuingAuthority')}"
#                     if cert.get('date'):
#                         cert_text += f" ({cert.get('date')})"
#                     content.append(Paragraph(cert_text, normal_style))
#             content.append(Spacer(1, 12))
        
#         achievements = data.get('achievements', [])
#         if achievements and any(ach.get('title') for ach in achievements):
#             content.append(Paragraph("ACHIEVEMENTS", heading_style))
#             for ach in achievements:
#                 if ach.get('title'):
#                     ach_text = f"• <b>{ach.get('title')}</b>"
#                     if ach.get('organization'):
#                         ach_text += f" - {ach.get('organization')}"
#                     if ach.get('date'):
#                         ach_text += f" ({ach.get('date')})"
#                     content.append(Paragraph(ach_text, normal_style))
#                     if ach.get('description'):
#                         content.append(Paragraph(f"  {ach.get('description')}", normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('languages'):
#             content.append(Paragraph("LANGUAGES", heading_style))
#             content.append(Paragraph(data['languages'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('publications'):
#             content.append(Paragraph("PUBLICATIONS", heading_style))
#             content.append(Paragraph(data['publications'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('volunteering'):
#             content.append(Paragraph("VOLUNTEERING", heading_style))
#             content.append(Paragraph(data['volunteering'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('hobbies'):
#             content.append(Paragraph("HOBBIES & INTERESTS", heading_style))
#             content.append(Paragraph(data['hobbies'], normal_style))
        
#         doc.build(content)
#         buffer.seek(0)
        
#         return send_file(
#             buffer,
#             as_attachment=True,
#             download_name='resume.pdf',
#             mimetype='application/pdf'
#         )
        
#     except Exception as e:
#         print(f"Error generating resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate resume: {str(e)}'}), 500


# # ===================== ROADMAP ROUTES =====================

# @app.route('/api/roadmap/generate', methods=['POST'])
# def generate_roadmap():
#     """Generate a new roadmap for a job role"""
#     try:
#         data = request.json
#         job_role = data.get('job_role')
#         experience_level = data.get('experience_level', 'beginner')
#         target_company = data.get('target_company')
#         user_skills = data.get('user_skills', [])
#         available_hours = data.get('available_hours_per_week', 10)
        
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         existing_roadmap_id, existing_roadmap = db_manager.get_roadmap(job_role)
        
#         if existing_roadmap:
#             if user_skills:
#                 customized_roadmap = roadmap_generator.update_roadmap_for_user(
#                     existing_roadmap, user_skills, available_hours
#                 )
#             else:
#                 customized_roadmap = existing_roadmap
            
#             return jsonify({
#                 'roadmap_id': existing_roadmap_id,
#                 'roadmap': customized_roadmap,
#                 'message': 'Retrieved existing roadmap'
#             })
        
#         roadmap_data = roadmap_generator.generate_roadmap(
#             job_role, experience_level, target_company
#         )
        
#         if user_skills:
#             roadmap_data = roadmap_generator.update_roadmap_for_user(
#                 roadmap_data, user_skills, available_hours
#             )
        
#         roadmap_id = db_manager.save_roadmap(job_role, roadmap_data)
#         roadmap_data['roadmap_id'] = roadmap_id
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data,
#             'message': 'Roadmap generated successfully'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/resources/<step_id>', methods=['GET'])
# def get_step_resources(roadmap_id, step_id):
#     """Get resources for a specific step"""
#     try:
#         existing_resources = db_manager.get_resources(step_id)
        
#         if existing_resources:
#             return jsonify({
#                 'step_id': step_id,
#                 'resources': existing_resources
#             })
        
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         step_data = None
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 if step['step_id'] == step_id:
#                     step_data = step
#                     break
#             if step_data:
#                 break
        
#         if not step_data:
#             return jsonify({'error': 'Step not found'}), 404
        
#         resources = resource_finder.get_all_resources_for_step(
#             step_data['title'], 
#             step_data['description']
#         )
        
#         if resources:
#             db_manager.save_resources(step_id, resources)
        
#         return jsonify({
#             'step_id': step_id,
#             'resources': resources
#         })
        
#     except Exception as e:
#         print(f"Error getting step resources: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to get resources: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['GET'])
# def get_roadmap_progress(roadmap_id):
#     """Get user progress for a roadmap"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'user_id': user_id,
#             'progress': progress
#         })
        
#     except Exception as e:
#         print(f"Error getting progress: {str(e)}")
#         return jsonify({'error': f'Failed to get progress: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['POST'])
# def update_progress(roadmap_id):
#     """Update user progress for a step"""
#     try:
#         data = request.json
#         user_id = data.get('user_id', 'default_user')
#         step_id = data.get('step_id')
#         completed = data.get('completed', False)
#         time_spent = data.get('time_spent', 0)
        
#         if not step_id:
#             return jsonify({'error': 'Step ID is required'}), 400
        
#         db_manager.save_user_progress(user_id, roadmap_id, step_id, completed, time_spent)
        
#         return jsonify({
#             'message': 'Progress updated successfully',
#             'roadmap_id': roadmap_id,
#             'step_id': step_id,
#             'completed': completed
#         })
        
#     except Exception as e:
#         print(f"Error updating progress: {str(e)}")
#         return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500

# @app.route('/api/roadmap/popular-roles', methods=['GET'])
# def get_popular_roles():
#     """Get list of popular job roles for roadmap generation"""
#     try:
#         popular_roles = [
#             {
#                 'id': 'software-developer',
#                 'title': 'Software Developer',
#                 'description': 'Full-stack and backend development roles',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'Very High',
#                 'skills': ['Programming', 'Problem Solving', 'System Design']
#             },
#             {
#                 'id': 'data-scientist',
#                 'title': 'Data Scientist',
#                 'description': 'Analyze data to derive business insights',
#                 'avg_salary': '6-20 LPA',
#                 'demand': 'High',
#                 'skills': ['Python', 'Statistics', 'Machine Learning']
#             },
#             {
#                 'id': 'product-manager',
#                 'title': 'Product Manager',
#                 'description': 'Define product strategy and roadmap',
#                 'avg_salary': '8-25 LPA',
#                 'demand': 'High',
#                 'skills': ['Strategy', 'Analytics', 'Communication']
#             },
#             {
#                 'id': 'ui-ux-designer',
#                 'title': 'UI/UX Designer',
#                 'description': 'Design user interfaces and experiences',
#                 'avg_salary': '4-12 LPA',
#                 'demand': 'High',
#                 'skills': ['Design Tools', 'User Research', 'Prototyping']
#             },
#             {
#                 'id': 'business-analyst',
#                 'title': 'Business Analyst',
#                 'description': 'Bridge between business and technology',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'High',
#                 'skills': ['Analysis', 'Documentation', 'Process Improvement']
#             },
#             {
#                 'id': 'devops-engineer',
#                 'title': 'DevOps Engineer',
#                 'description': 'Manage deployment and infrastructure',
#                 'avg_salary': '6-18 LPA',
#                 'demand': 'Very High',
#                 'skills': ['Cloud', 'Automation', 'Monitoring']
#             },
#             {
#                 'id': 'consultant',
#                 'title': 'Management Consultant',
#                 'description': 'Provide strategic business advice',
#                 'avg_salary': '8-30 LPA',
#                 'demand': 'Medium',
#                 'skills': ['Problem Solving', 'Presentation', 'Business Acumen']
#             },
#             {
#                 'id': 'digital-marketing',
#                 'title': 'Digital Marketing Specialist',
#                 'description': 'Online marketing and growth strategies',
#                 'avg_salary': '3-10 LPA',
#                 'demand': 'High',
#                 'skills': ['SEO/SEM', 'Analytics', 'Content Marketing']
#             }
#         ]
        
#         return jsonify({'roles': popular_roles})
        
#     except Exception as e:
#         print(f"Error getting popular roles: {str(e)}")
#         return jsonify({'error': 'Failed to get popular roles'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>', methods=['GET'])
# def get_roadmap_by_id(roadmap_id):
#     """Get a specific roadmap by ID"""
#     try:
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
        
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data
#         })
        
#     except Exception as e:
#         print(f"Error getting roadmap: {str(e)}")
#         return jsonify({'error': f'Failed to get roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/analytics', methods=['GET'])
# def get_roadmap_analytics(roadmap_id):
#     """Get analytics for a roadmap"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
        
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         total_steps = 0
#         completed_steps = 0
#         total_time_spent = 0
        
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 total_steps += 1
#                 step_id = step['step_id']
                
#                 if step_id in progress:
#                     if progress[step_id]['completed']:
#                         completed_steps += 1
#                     total_time_spent += progress[step_id]['time_spent']
        
#         completion_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
#         estimated_total_hours = sum(
#             sum(step.get('estimated_hours', 0) for step in phase.get('steps', []))
#             for phase in roadmap_data.get('phases', [])
#         )
        
#         analytics = {
#             'completion_percentage': round(completion_percentage, 2),
#             'completed_steps': completed_steps,
#             'total_steps': total_steps,
#             'time_spent_hours': total_time_spent,
#             'estimated_total_hours': estimated_total_hours,
#             'progress_by_phase': [],
#             'recent_activity': []
#         }
        
#         for phase in roadmap_data.get('phases', []):
#             phase_steps = len(phase.get('steps', []))
#             phase_completed = sum(
#                 1 for step in phase.get('steps', [])
#                 if step['step_id'] in progress and progress[step['step_id']]['completed']
#             )
            
#             analytics['progress_by_phase'].append({
#                 'phase_name': phase['phase_name'],
#                 'completed_steps': phase_completed,
#                 'total_steps': phase_steps,
#                 'completion_percentage': (phase_completed / phase_steps * 100) if phase_steps > 0 else 0
#             })
        
#         return jsonify(analytics)
        
#     except Exception as e:
#         print(f"Error getting analytics: {str(e)}")
#         return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500


# # ===================== RESUME-BASED ROADMAP ROUTES =====================

# @app.route('/api/roadmap/analyze-resume', methods=['POST'])
# def analyze_resume_for_roadmap():
#     """Analyze resume and generate personalized career roadmap"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume using Gemini
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get primary role recommendation
#         primary_role = career_info.get('primary_role', 'Software Developer')
        
#         # Generate personalized roadmap for primary role
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, primary_role
#         )
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         # Save the personalized roadmap to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{primary_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'career_analysis': {
#                 'primary_role': primary_role,
#                 'experience_level': career_info.get('experience_level'),
#                 'skills': career_info.get('skills', []),
#                 'skill_gaps': personalized_roadmap.get('skill_gaps', []),
#                 'strengths': career_info.get('strengths', []),
#             },
#             'personalized_roadmap': personalized_roadmap,
#             'alternative_careers': alternative_careers,
#             'message': 'Resume analyzed successfully'
#         })
        
#     except Exception as e:
#         print(f"Error analyzing resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500


# @app.route('/api/roadmap/generate-for-role', methods=['POST'])
# def generate_roadmap_for_specific_role():
#     """Generate roadmap for a specific role based on resume analysis"""
#     try:
#         data = request.json
        
#         if 'resume_text' not in data and 'career_info' not in data:
#             return jsonify({'error': 'Resume text or career info required'}), 400
        
#         job_role = data.get('job_role')
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         # If career_info is provided, use it; otherwise analyze resume_text
#         if 'career_info' in data:
#             career_info = data['career_info']
#         else:
#             resume_text = data['resume_text']
#             career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Generate personalized roadmap
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, job_role
#         )
        
#         # Save to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{job_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'roadmap': personalized_roadmap,
#             'message': f'Personalized roadmap generated for {job_role}'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap for role: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500


# @app.route('/api/career/analyze', methods=['POST'])
# def quick_career_analysis():
#     """Quick career analysis from resume (without full roadmap generation)"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         return jsonify({
#             'success': True,
#             'career_info': career_info,
#             'alternative_careers': alternative_careers
#         })
        
#     except Exception as e:
#         print(f"Error in career analysis: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze career: {str(e)}'}), 500


# # ===================== MAIN APPLICATION ====================

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print("📋 Features available:")
#     print("  • Resume screening and generation")
#     print("  • Cover letter generation")
#     print("  • AI-powered roadmap creation")
#     print("  • Resume-based personalized roadmaps")
#     print("  • Progress tracking")
#     print("  • Resource recommendations")
#     print("🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)


# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import joblib
# import pdfplumber
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.units import inch
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import nltk
# from nltk.corpus import stopwords
# import pandas as pd
# import json
# import re
# from io import BytesIO
# import uuid
# from datetime import datetime

# # Import new modules for roadmap features
# from database import DatabaseManager
# from roadmap_generator import RoadmapGenerator
# from resource_finder import ResourceFinder
# from resume_analyzer import ResumeAnalyzer

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# # NLTK setup
# nltk.download('stopwords', quiet=True)
# try:
#     stop = set(stopwords.words('english'))
# except Exception:
#     print("Warning: NLTK stopwords not available")
#     stop = set()

# # Load existing model
# try:
#     model1 = joblib.load('resume_model.pkl')
# except FileNotFoundError:
#     print("Error: resume_model.pkl not found. Run train_model.py first.")
#     model1 = None

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# # Initialize new components for roadmap features
# db_manager = DatabaseManager()
# roadmap_generator = RoadmapGenerator(os.getenv('GEMINI_API_KEY'))
# resource_finder = ResourceFinder()
# resume_analyzer = ResumeAnalyzer(os.getenv('GEMINI_API_KEY'))

# # ===================== EXISTING ROUTES =====================

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Welcome to the Resume Screening API'})

# @app.route('/predict', methods=['POST'])
# def predict():
#     if not model1:
#         return jsonify({'error': 'Model not loaded'}), 500
    
#     file = request.files['resume']
#     experience_years = float(request.form.get('experience_years', 0))
#     projects_count = int(request.form.get('projects_count', 0))
#     salary_expectation = float(request.form.get('salary_expectation', 0))
    
#     with pdfplumber.open(file) as pdf:
#         resume_text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    
#     cleaned_text = resume_text.lower().replace(r'[^\w\s]', '')
#     cleaned_text = ' '.join(word for word in str(cleaned_text).split() if word not in stop)
    
#     input_data = pd.DataFrame({
#         'Text': [cleaned_text],
#         'Experience (Years)': [experience_years],
#         'Projects Count': [projects_count],
#         'Salary Expectation ($)': [salary_expectation]
#     })
    
#     prob = model1.predict_proba(input_data)[0][1] * 100
#     return jsonify({'chance': prob})


# def extract_contact_info(resume_text):
#     name = resume_text.split("\n")[0].strip()
#     email = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
#     phone = re.search(r'\b\d{10}\b', resume_text)
#     linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/[^\s]+', resume_text)
#     github = re.search(r'(https?://)?(www\.)?github\.com/[^\s]+', resume_text)

#     return {
#         "name": name,
#         "email": email.group() if email else "",
#         "phone": phone.group() if phone else "",
#         "linkedin": linkedin.group() if linkedin else "",
#         "github": github.group() if github else ""
#     }

# @app.route('/generate_cover_letter', methods=['POST'])
# def generate_cover():
#     try:
#         job_desc = request.form['job_desc']
#         hr_name = request.form['hr_name']
#         resume_file = request.files['resume_file']

#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(page.extract_text() or '' for page in pdf.pages)

#         contact_info = extract_contact_info(resume_text)

#         model = genai.GenerativeModel('gemini-2.0-flash')
#         prompt = f"""
#         Write a professional cover letter for this job: {job_desc}.
#         Address it to {hr_name}.
        
#         Incorporate details from this resume: {resume_text}.

#         Important: Do NOT include headers like [Your Name], [Your Address], [Date],
#         or any placeholder personal/contact information at the top.
#         Start directly with the greeting (e.g., 'Dear {hr_name},').
#         Do NOT include placeholders such as [Platform where you saw the advertisement],
#         [Address], or any square-bracketed text.
#         Do NOT fabricate details not present in the resume or job description.
#         End with a professional closing (e.g., "Sincerely, Aryan Jain") including my name and contact info.
#         """

#         cover_text = ""
#         response = model.generate_content(prompt)
#         if response and hasattr(response, "candidates"):
#             for candidate in response.candidates:
#                 for part in candidate.content.parts:
#                     if part.text:
#                         cover_text += part.text + "\n"

#         if not cover_text.strip():
#             raise Exception("api returned empty text")

#         return jsonify({'cover_letter': cover_text.strip()})

#     except Exception as e:
#         print(f"Error generating cover letter: {e}")
#         return jsonify({'error': 'Failed to generate cover letter'}), 500


# def safe_parse_json(data_str):
#     """Safely parse JSON string, return empty list if parsing fails"""
#     if not data_str:
#         return []
#     try:
#         parsed = json.loads(data_str)
#         return parsed if isinstance(parsed, list) else []
#     except (json.JSONDecodeError, TypeError):
#         return []

# @app.route('/api/resume/create', methods=['POST'])
# def generate_resume():
#     try:
#         if request.content_type and 'multipart/form-data' in request.content_type:
#             data = {}
#             for key in request.form:
#                 if key in ['workExperience', 'education', 'projects', 'certifications', 'achievements']:
#                     data[key] = safe_parse_json(request.form[key])
#                 else:
#                     data[key] = request.form[key]
            
#             photo_file = request.files.get('photo')
#         else:
#             data = request.json or {}
#             photo_file = None

#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
#         styles = getSampleStyleSheet()
#         title_style = ParagraphStyle(
#             'CustomTitle',
#             parent=styles['Heading1'],
#             fontSize=18,
#             spaceAfter=12,
#             alignment=1,
#             textColor='#2C5AA0'
#         )
#         heading_style = ParagraphStyle(
#             'CustomHeading',
#             parent=styles['Heading2'],
#             fontSize=14,
#             spaceAfter=8,
#             spaceBefore=12,
#             textColor='#1F4788',
#             borderWidth=1,
#             borderColor='#1F4788',
#             borderPadding=4
#         )
#         normal_style = styles['Normal']
#         normal_style.fontSize = 10
#         normal_style.leading = 12
        
#         content = []
        
#         if data.get('fullName'):
#             content.append(Paragraph(data['fullName'].upper(), title_style))
#             content.append(Spacer(1, 12))
        
#         contact_info = []
#         if data.get('email'):
#             contact_info.append(f"📧 {data['email']}")
#         if data.get('phoneNumber'):
#             contact_info.append(f"📱 {data['phoneNumber']}")
#         if data.get('location'):
#             contact_info.append(f"📍 {data['location']}")
        
#         if contact_info:
#             content.append(Paragraph(" | ".join(contact_info), normal_style))
#             content.append(Spacer(1, 8))
        
#         profile_links = []
#         if data.get('linkedinUrl'):
#             profile_links.append(f"LinkedIn: {data['linkedinUrl']}")
#         if data.get('githubPortfolioUrl'):
#             profile_links.append(f"Portfolio: {data['githubPortfolioUrl']}")
        
#         if profile_links:
#             content.append(Paragraph(" | ".join(profile_links), normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('jobTitle'):
#             job_title_style = ParagraphStyle(
#                 'JobTitle',
#                 parent=styles['Heading2'],
#                 fontSize=12,
#                 spaceAfter=8,
#                 alignment=1,
#                 textColor='#555555'
#             )
#             content.append(Paragraph(data['jobTitle'], job_title_style))
        
#         if data.get('professionalSummary'):
#             content.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
#             content.append(Paragraph(data['professionalSummary'], normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('technicalSkills') or data.get('softSkills'):
#             content.append(Paragraph("SKILLS", heading_style))
#             if data.get('technicalSkills'):
#                 content.append(Paragraph(f"<b>Technical Skills:</b> {data['technicalSkills']}", normal_style))
#             if data.get('softSkills'):
#                 content.append(Paragraph(f"<b>Soft Skills:</b> {data['softSkills']}", normal_style))
#             content.append(Spacer(1, 12))
        
#         work_experience = data.get('workExperience', [])
#         if work_experience and any(exp.get('jobTitle') or exp.get('companyName') for exp in work_experience):
#             content.append(Paragraph("WORK EXPERIENCE", heading_style))
#             for exp in work_experience:
#                 if exp.get('jobTitle') or exp.get('companyName'):
#                     job_title = exp.get('jobTitle', 'N/A')
#                     company = exp.get('companyName', 'N/A')
#                     exp_header = f"<b>{job_title}</b> | {company}"
#                     content.append(Paragraph(exp_header, normal_style))
                    
#                     date_info = []
#                     if exp.get('startDate') or exp.get('endDate'):
#                         start_date = exp.get('startDate', 'N/A')
#                         end_date = exp.get('endDate', 'Present')
#                         date_info.append(f"{start_date} - {end_date}")
#                     if exp.get('location'):
#                         date_info.append(exp.get('location'))
                    
#                     if date_info:
#                         content.append(Paragraph(" | ".join(date_info), normal_style))
                    
#                     if exp.get('responsibilities'):
#                         responsibilities = exp.get('responsibilities').strip()
#                         if responsibilities:
#                             resp_lines = [line.strip() for line in responsibilities.replace('•', '\n').split('\n') if line.strip()]
#                             for line in resp_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     if exp.get('achievements'):
#                         achievements = exp.get('achievements').strip()
#                         if achievements:
#                             ach_lines = [line.strip() for line in achievements.replace('•', '\n').split('\n') if line.strip()]
#                             for line in ach_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         education = data.get('education', [])
#         if education and any(edu.get('degree') or edu.get('universityName') for edu in education):
#             content.append(Paragraph("EDUCATION", heading_style))
#             for edu in education:
#                 if edu.get('degree') or edu.get('universityName'):
#                     degree = edu.get('degree', 'N/A')
#                     university = edu.get('universityName', 'N/A')
#                     edu_header = f"<b>{degree}</b>"
#                     content.append(Paragraph(edu_header, normal_style))
#                     content.append(Paragraph(university, normal_style))
                    
#                     edu_details = []
#                     if edu.get('location'):
#                         edu_details.append(edu.get('location'))
#                     if edu.get('startDate') or edu.get('endDate'):
#                         start_date = edu.get('startDate', 'N/A')
#                         end_date = edu.get('endDate', 'N/A')
#                         edu_details.append(f"{start_date} - {end_date}")
#                     if edu.get('gpa'):
#                         edu_details.append(f"GPA: {edu.get('gpa')}")
                    
#                     if edu_details:
#                         content.append(Paragraph(" | ".join(edu_details), normal_style))
                    
#                     if edu.get('relevantCoursework'):
#                         content.append(Paragraph(f"<b>Relevant Coursework:</b> {edu.get('relevantCoursework')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         projects = data.get('projects', [])
#         if projects and any(proj.get('projectTitle') for proj in projects):
#             content.append(Paragraph("PROJECTS", heading_style))
#             for proj in projects:
#                 if proj.get('projectTitle'):
#                     content.append(Paragraph(f"<b>{proj.get('projectTitle')}</b>", normal_style))
                    
#                     if proj.get('description'):
#                         content.append(Paragraph(proj.get('description'), normal_style))
                    
#                     if proj.get('technologiesUsed'):
#                         content.append(Paragraph(f"<b>Technologies:</b> {proj.get('technologiesUsed')}", normal_style))
                    
#                     if proj.get('impact'):
#                         content.append(Paragraph(f"<b>Impact:</b> {proj.get('impact')}", normal_style))
                    
#                     if proj.get('projectLink'):
#                         content.append(Paragraph(f"<b>Link:</b> {proj.get('projectLink')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         certifications = data.get('certifications', [])
#         if certifications and any(cert.get('certificationName') for cert in certifications):
#             content.append(Paragraph("CERTIFICATIONS", heading_style))
#             for cert in certifications:
#                 if cert.get('certificationName'):
#                     cert_text = f"• <b>{cert.get('certificationName')}</b>"
#                     if cert.get('issuingAuthority'):
#                         cert_text += f" - {cert.get('issuingAuthority')}"
#                     if cert.get('date'):
#                         cert_text += f" ({cert.get('date')})"
#                     content.append(Paragraph(cert_text, normal_style))
#             content.append(Spacer(1, 12))
        
#         achievements = data.get('achievements', [])
#         if achievements and any(ach.get('title') for ach in achievements):
#             content.append(Paragraph("ACHIEVEMENTS", heading_style))
#             for ach in achievements:
#                 if ach.get('title'):
#                     ach_text = f"• <b>{ach.get('title')}</b>"
#                     if ach.get('organization'):
#                         ach_text += f" - {ach.get('organization')}"
#                     if ach.get('date'):
#                         ach_text += f" ({ach.get('date')})"
#                     content.append(Paragraph(ach_text, normal_style))
#                     if ach.get('description'):
#                         content.append(Paragraph(f"  {ach.get('description')}", normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('languages'):
#             content.append(Paragraph("LANGUAGES", heading_style))
#             content.append(Paragraph(data['languages'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('publications'):
#             content.append(Paragraph("PUBLICATIONS", heading_style))
#             content.append(Paragraph(data['publications'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('volunteering'):
#             content.append(Paragraph("VOLUNTEERING", heading_style))
#             content.append(Paragraph(data['volunteering'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('hobbies'):
#             content.append(Paragraph("HOBBIES & INTERESTS", heading_style))
#             content.append(Paragraph(data['hobbies'], normal_style))
        
#         doc.build(content)
#         buffer.seek(0)
        
#         return send_file(
#             buffer,
#             as_attachment=True,
#             download_name='resume.pdf',
#             mimetype='application/pdf'
#         )
        
#     except Exception as e:
#         print(f"Error generating resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate resume: {str(e)}'}), 500


# # ===================== ROADMAP ROUTES =====================

# @app.route('/api/roadmap/generate', methods=['POST'])
# def generate_roadmap():
#     """Generate a new roadmap for a job role"""
#     try:
#         data = request.json
#         job_role = data.get('job_role')
#         experience_level = data.get('experience_level', 'beginner')
#         target_company = data.get('target_company')
#         user_skills = data.get('user_skills', [])
#         available_hours = data.get('available_hours_per_week', 10)
        
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         existing_roadmap_id, existing_roadmap = db_manager.get_roadmap(job_role)
        
#         if existing_roadmap:
#             if user_skills:
#                 customized_roadmap = roadmap_generator.update_roadmap_for_user(
#                     existing_roadmap, user_skills, available_hours
#                 )
#             else:
#                 customized_roadmap = existing_roadmap
            
#             return jsonify({
#                 'roadmap_id': existing_roadmap_id,
#                 'roadmap': customized_roadmap,
#                 'message': 'Retrieved existing roadmap'
#             })
        
#         roadmap_data = roadmap_generator.generate_roadmap(
#             job_role, experience_level, target_company
#         )
        
#         if user_skills:
#             roadmap_data = roadmap_generator.update_roadmap_for_user(
#                 roadmap_data, user_skills, available_hours
#             )
        
#         roadmap_id = db_manager.save_roadmap(job_role, roadmap_data)
#         roadmap_data['roadmap_id'] = roadmap_id
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data,
#             'message': 'Roadmap generated successfully'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/resources/<step_id>', methods=['GET'])
# def get_step_resources(roadmap_id, step_id):
#     """Get resources for a specific step"""
#     try:
#         existing_resources = db_manager.get_resources(step_id)
        
#         if existing_resources:
#             return jsonify({
#                 'step_id': step_id,
#                 'resources': existing_resources
#             })
        
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         step_data = None
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 if step['step_id'] == step_id:
#                     step_data = step
#                     break
#             if step_data:
#                 break
        
#         if not step_data:
#             return jsonify({'error': 'Step not found'}), 404
        
#         resources = resource_finder.get_all_resources_for_step(
#             step_data['title'], 
#             step_data['description']
#         )
        
#         if resources:
#             db_manager.save_resources(step_id, resources)
        
#         return jsonify({
#             'step_id': step_id,
#             'resources': resources
#         })
        
#     except Exception as e:
#         print(f"Error getting step resources: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to get resources: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['GET'])
# def get_roadmap_progress(roadmap_id):
#     """Get user progress for a roadmap"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'user_id': user_id,
#             'progress': progress
#         })
        
#     except Exception as e:
#         print(f"Error getting progress: {str(e)}")
#         return jsonify({'error': f'Failed to get progress: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['POST'])
# def update_progress(roadmap_id):
#     """Update user progress for a step"""
#     try:
#         data = request.json
#         user_id = data.get('user_id', 'default_user')
#         step_id = data.get('step_id')
#         completed = data.get('completed', False)
#         time_spent = data.get('time_spent', 0)
        
#         if not step_id:
#             return jsonify({'error': 'Step ID is required'}), 400
        
#         db_manager.save_user_progress(user_id, roadmap_id, step_id, completed, time_spent)
        
#         return jsonify({
#             'message': 'Progress updated successfully',
#             'roadmap_id': roadmap_id,
#             'step_id': step_id,
#             'completed': completed
#         })
        
#     except Exception as e:
#         print(f"Error updating progress: {str(e)}")
#         return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500

# @app.route('/api/roadmap/popular-roles', methods=['GET'])
# def get_popular_roles():
#     """Get list of popular job roles for roadmap generation"""
#     try:
#         popular_roles = [
#             {
#                 'id': 'software-developer',
#                 'title': 'Software Developer',
#                 'description': 'Full-stack and backend development roles',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'Very High',
#                 'skills': [
#                     {
#                         'name': 'Programming',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Python Programming',
#                                 'url': 'https://www.python.org/about/gettingstarted/',
#                                 'description': 'Official Python documentation and tutorials'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'JavaScript Fundamentals',
#                                 'url': 'https://javascript.info/',
#                                 'description': 'Modern JavaScript tutorial'
#                             },
#                             {
#                                 'type': 'practice',
#                                 'title': 'LeetCode',
#                                 'url': 'https://leetcode.com/',
#                                 'description': 'Practice coding problems'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'System Design',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'System Design Primer',
#                                 'url': 'https://github.com/donnemartin/system-design-primer',
#                                 'description': 'Learn how to design large-scale systems'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Web Development',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'MDN Web Docs',
#                                 'url': 'https://developer.mozilla.org/',
#                                 'description': 'Web development resources'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'data-scientist',
#                 'title': 'Data Scientist',
#                 'description': 'Analyze data to derive business insights',
#                 'avg_salary': '6-20 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Python',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Python for Data Science',
#                                 'url': 'https://www.coursera.org/specializations/python',
#                                 'description': 'Coursera Python specialization'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Machine Learning',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Scikit-learn Tutorial',
#                                 'url': 'https://scikit-learn.org/stable/tutorial/index.html',
#                                 'description': 'Official ML library documentation'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Kaggle Learn',
#                                 'url': 'https://www.kaggle.com/learn',
#                                 'description': 'Free ML courses and competitions'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Statistics',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Khan Academy Statistics',
#                                 'url': 'https://www.khanacademy.org/math/statistics-probability',
#                                 'description': 'Free statistics courses'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'product-manager',
#                 'title': 'Product Manager',
#                 'description': 'Define product strategy and roadmap',
#                 'avg_salary': '8-25 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Strategy',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Product Strategy Guide',
#                                 'url': 'https://www.productplan.com/learn/product-strategy/',
#                                 'description': 'Product strategy resources'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Analytics',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Google Analytics Academy',
#                                 'url': 'https://analytics.google.com/analytics/academy/',
#                                 'description': 'Free analytics courses'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Communication',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Product Management Resources',
#                                 'url': 'https://www.mindtheproduct.com/',
#                                 'description': 'PM community and articles'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'ui-ux-designer',
#                 'title': 'UI/UX Designer',
#                 'description': 'Design user interfaces and experiences',
#                 'avg_salary': '4-12 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Design Tools',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Figma Tutorial',
#                                 'url': 'https://www.figma.com/resources/learn-design/',
#                                 'description': 'Learn Figma design tool'
#                             },
#                             {
#                                 'type': 'practice',
#                                 'title': 'Dribbble',
#                                 'url': 'https://dribbble.com/',
#                                 'description': 'Design inspiration and community'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'User Research',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Nielsen Norman Group',
#                                 'url': 'https://www.nngroup.com/articles/',
#                                 'description': 'UX research articles'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Prototyping',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Interaction Design Foundation',
#                                 'url': 'https://www.interaction-design.org/',
#                                 'description': 'UX design courses'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'business-analyst',
#                 'title': 'Business Analyst',
#                 'description': 'Bridge between business and technology',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Analysis',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Business Analysis Fundamentals',
#                                 'url': 'https://www.iiba.org/',
#                                 'description': 'International Institute of Business Analysis'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Excel & SQL',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'SQL Tutorial',
#                                 'url': 'https://www.w3schools.com/sql/',
#                                 'description': 'Learn SQL for data analysis'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Excel Skills',
#                                 'url': 'https://support.microsoft.com/en-us/office/excel-video-training',
#                                 'description': 'Microsoft Excel tutorials'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Documentation',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Business Analysis Templates',
#                                 'url': 'https://www.bridging-the-gap.com/',
#                                 'description': 'BA resources and templates'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'devops-engineer',
#                 'title': 'DevOps Engineer',
#                 'description': 'Manage deployment and infrastructure',
#                 'avg_salary': '6-18 LPA',
#                 'demand': 'Very High',
#                 'skills': [
#                     {
#                         'name': 'Cloud (AWS/Azure)',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'AWS Free Tier',
#                                 'url': 'https://aws.amazon.com/free/',
#                                 'description': 'Learn AWS with free tier'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Azure Fundamentals',
#                                 'url': 'https://docs.microsoft.com/en-us/learn/azure/',
#                                 'description': 'Microsoft Azure learning path'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Docker & Kubernetes',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Docker Documentation',
#                                 'url': 'https://docs.docker.com/get-started/',
#                                 'description': 'Official Docker getting started guide'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Kubernetes Basics',
#                                 'url': 'https://kubernetes.io/docs/tutorials/kubernetes-basics/',
#                                 'description': 'Learn Kubernetes fundamentals'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'CI/CD',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Jenkins Tutorial',
#                                 'url': 'https://www.jenkins.io/doc/tutorials/',
#                                 'description': 'Learn Jenkins for CI/CD'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'consultant',
#                 'title': 'Management Consultant',
#                 'description': 'Provide strategic business advice',
#                 'avg_salary': '8-30 LPA',
#                 'demand': 'Medium',
#                 'skills': [
#                     {
#                         'name': 'Problem Solving',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Case Interview Prep',
#                                 'url': 'https://www.caseinterviewprep.com/',
#                                 'description': 'Management consulting case prep'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Business Frameworks',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Consulting Tools',
#                                 'url': 'https://www.mckinsey.com/capabilities',
#                                 'description': 'Business strategy frameworks'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Presentation',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'McKinsey Presentation Style',
#                                 'url': 'https://www.duarte.com/',
#                                 'description': 'Professional presentation skills'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'digital-marketing',
#                 'title': 'Digital Marketing Specialist',
#                 'description': 'Online marketing and growth strategies',
#                 'avg_salary': '3-10 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'SEO/SEM',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Google Digital Garage',
#                                 'url': 'https://learndigital.withgoogle.com/',
#                                 'description': 'Free digital marketing courses'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Moz SEO Learning Center',
#                                 'url': 'https://moz.com/learn/seo',
#                                 'description': 'SEO fundamentals and best practices'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Social Media Marketing',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'HubSpot Academy',
#                                 'url': 'https://academy.hubspot.com/',
#                                 'description': 'Free marketing certifications'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Analytics',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Google Analytics',
#                                 'url': 'https://analytics.google.com/analytics/academy/',
#                                 'description': 'Master Google Analytics'
#                             }
#                         ]
#                     }
#                 ]
#             }
#         ]
        
#         return jsonify({'roles': popular_roles})
        
#     except Exception as e:
#         print(f"Error getting popular roles: {str(e)}")
#         return jsonify({'error': 'Failed to get popular roles'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>', methods=['GET'])
# def get_roadmap_by_id(roadmap_id):
#     """Get a specific roadmap by ID"""
#     try:
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
        
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data
#         })
        
#     except Exception as e:
#         print(f"Error getting roadmap: {str(e)}")
#         return jsonify({'error': f'Failed to get roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/analytics', methods=['GET'])
# def get_roadmap_analytics(roadmap_id):
#     """Get analytics for a roadmap"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
        
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         total_steps = 0
#         completed_steps = 0
#         total_time_spent = 0
        
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 total_steps += 1
#                 step_id = step['step_id']
                
#                 if step_id in progress:
#                     if progress[step_id]['completed']:
#                         completed_steps += 1
#                     total_time_spent += progress[step_id]['time_spent']
        
#         completion_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
#         estimated_total_hours = sum(
#             sum(step.get('estimated_hours', 0) for step in phase.get('steps', []))
#             for phase in roadmap_data.get('phases', [])
#         )
        
#         analytics = {
#             'completion_percentage': round(completion_percentage, 2),
#             'completed_steps': completed_steps,
#             'total_steps': total_steps,
#             'time_spent_hours': total_time_spent,
#             'estimated_total_hours': estimated_total_hours,
#             'progress_by_phase': [],
#             'recent_activity': []
#         }
        
#         for phase in roadmap_data.get('phases', []):
#             phase_steps = len(phase.get('steps', []))
#             phase_completed = sum(
#                 1 for step in phase.get('steps', [])
#                 if step['step_id'] in progress and progress[step['step_id']]['completed']
#             )
            
#             analytics['progress_by_phase'].append({
#                 'phase_name': phase['phase_name'],
#                 'completed_steps': phase_completed,
#                 'total_steps': phase_steps,
#                 'completion_percentage': (phase_completed / phase_steps * 100) if phase_steps > 0 else 0
#             })
        
#         return jsonify(analytics)
        
#     except Exception as e:
#         print(f"Error getting analytics: {str(e)}")
#         return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500


# # ===================== RESUME-BASED ROADMAP ROUTES =====================

# @app.route('/api/roadmap/analyze-resume', methods=['POST'])
# def analyze_resume_for_roadmap():
#     """Analyze resume and generate personalized career roadmap"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume using Gemini
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get primary role recommendation
#         primary_role = career_info.get('primary_role', 'Software Developer')
        
#         # Generate personalized roadmap for primary role
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, primary_role
#         )
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         # Save the personalized roadmap to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{primary_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'career_analysis': {
#                 'primary_role': primary_role,
#                 'experience_level': career_info.get('experience_level'),
#                 'skills': career_info.get('skills', []),
#                 'skill_gaps': personalized_roadmap.get('skill_gaps', []),
#                 'strengths': career_info.get('strengths', []),
#             },
#             'personalized_roadmap': personalized_roadmap,
#             'alternative_careers': alternative_careers,
#             'message': 'Resume analyzed successfully'
#         })
        
#     except Exception as e:
#         print(f"Error analyzing resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500


# @app.route('/api/roadmap/generate-for-role', methods=['POST'])
# def generate_roadmap_for_specific_role():
#     """Generate roadmap for a specific role based on resume analysis"""
#     try:
#         data = request.json
        
#         if 'resume_text' not in data and 'career_info' not in data:
#             return jsonify({'error': 'Resume text or career info required'}), 400
        
#         job_role = data.get('job_role')
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         # If career_info is provided, use it; otherwise analyze resume_text
#         if 'career_info' in data:
#             career_info = data['career_info']
#         else:
#             resume_text = data['resume_text']
#             career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Generate personalized roadmap
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, job_role
#         )
        
#         # Save to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{job_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'roadmap': personalized_roadmap,
#             'message': f'Personalized roadmap generated for {job_role}'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap for role: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500


# @app.route('/api/career/analyze', methods=['POST'])
# def quick_career_analysis():
#     """Quick career analysis from resume (without full roadmap generation)"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         return jsonify({
#             'success': True,
#             'career_info': career_info,
#             'alternative_careers': alternative_careers
#         })
        
#     except Exception as e:
#         print(f"Error in career analysis: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze career: {str(e)}'}), 500


# # ===================== MAIN APPLICATION ====================

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print("📋 Features available:")
#     print("  • Resume screening and generation")
#     print("  • Cover letter generation")
#     print("  • AI-powered roadmap creation")
#     print("  • Resume-based personalized roadmaps")
#     print("  • Progress tracking")
#     print("  • Resource recommendations")
#     print("🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)

# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import joblib
# import pdfplumber
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.units import inch
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import nltk
# from nltk.corpus import stopwords
# import pandas as pd
# import json
# import re
# from io import BytesIO
# import uuid
# from datetime import datetime

# # Import new modules for roadmap features
# from database import DatabaseManager
# from roadmap_generator import RoadmapGenerator
# from resource_finder import ResourceFinder
# from resume_analyzer import ResumeAnalyzer

# # Initialize Flask app
# app = Flask(__name__)

# # Configure CORS - Allow all origins for development
# CORS(app, resources={
#     r"/*": {
#         "origins": "*",
#         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#         "allow_headers": ["Content-Type", "Authorization"]
#     }
# })

# # NLTK setup
# nltk.download('stopwords', quiet=True)
# try:
#     stop = set(stopwords.words('english'))
# except Exception:
#     print("Warning: NLTK stopwords not available")
#     stop = set()

# # Load existing model
# try:
#     model1 = joblib.load('resume_model.pkl')
# except FileNotFoundError:
#     print("Error: resume_model.pkl not found. Run train_model.py first.")
#     model1 = None

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# # Initialize new components for roadmap features
# db_manager = DatabaseManager()
# roadmap_generator = RoadmapGenerator(os.getenv('GEMINI_API_KEY'))
# resource_finder = ResourceFinder()
# resume_analyzer = ResumeAnalyzer(os.getenv('GEMINI_API_KEY'))

# # ===================== EXISTING ROUTES =====================

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Welcome to the Resume Screening API'})

# @app.route('/predict', methods=['POST'])
# def predict():
#     if not model1:
#         return jsonify({'error': 'Model not loaded'}), 500
    
#     file = request.files['resume']
#     experience_years = float(request.form.get('experience_years', 0))
#     projects_count = int(request.form.get('projects_count', 0))
#     salary_expectation = float(request.form.get('salary_expectation', 0))
    
#     with pdfplumber.open(file) as pdf:
#         resume_text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    
#     cleaned_text = resume_text.lower().replace(r'[^\w\s]', '')
#     cleaned_text = ' '.join(word for word in str(cleaned_text).split() if word not in stop)
    
#     input_data = pd.DataFrame({
#         'Text': [cleaned_text],
#         'Experience (Years)': [experience_years],
#         'Projects Count': [projects_count],
#         'Salary Expectation ($)': [salary_expectation]
#     })
    
#     prob = model1.predict_proba(input_data)[0][1] * 100
#     return jsonify({'chance': prob})


# def extract_contact_info(resume_text):
#     name = resume_text.split("\n")[0].strip()
#     email = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
#     phone = re.search(r'\b\d{10}\b', resume_text)
#     linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/[^\s]+', resume_text)
#     github = re.search(r'(https?://)?(www\.)?github\.com/[^\s]+', resume_text)

#     return {
#         "name": name,
#         "email": email.group() if email else "",
#         "phone": phone.group() if phone else "",
#         "linkedin": linkedin.group() if linkedin else "",
#         "github": github.group() if github else ""
#     }

# @app.route('/generate_cover_letter', methods=['POST'])
# def generate_cover():
#     try:
#         job_desc = request.form['job_desc']
#         hr_name = request.form['hr_name']
#         resume_file = request.files['resume_file']

#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(page.extract_text() or '' for page in pdf.pages)

#         contact_info = extract_contact_info(resume_text)

#         model = genai.GenerativeModel('gemini-2.0-flash')
#         prompt = f"""
#         Write a professional cover letter for this job: {job_desc}.
#         Address it to {hr_name}.
        
#         Incorporate details from this resume: {resume_text}.

#         Important: Do NOT include headers like [Your Name], [Your Address], [Date],
#         or any placeholder personal/contact information at the top.
#         Start directly with the greeting (e.g., 'Dear {hr_name},').
#         Do NOT include placeholders such as [Platform where you saw the advertisement],
#         [Address], or any square-bracketed text.
#         Do NOT fabricate details not present in the resume or job description.
#         End with a professional closing (e.g., "Sincerely, Aryan Jain") including my name and contact info.
#         """

#         cover_text = ""
#         response = model.generate_content(prompt)
#         if response and hasattr(response, "candidates"):
#             for candidate in response.candidates:
#                 for part in candidate.content.parts:
#                     if part.text:
#                         cover_text += part.text + "\n"

#         if not cover_text.strip():
#             raise Exception("api returned empty text")

#         return jsonify({'cover_letter': cover_text.strip()})

#     except Exception as e:
#         print(f"Error generating cover letter: {e}")
#         return jsonify({'error': 'Failed to generate cover letter'}), 500


# def safe_parse_json(data_str):
#     """Safely parse JSON string, return empty list if parsing fails"""
#     if not data_str:
#         return []
#     try:
#         parsed = json.loads(data_str)
#         return parsed if isinstance(parsed, list) else []
#     except (json.JSONDecodeError, TypeError):
#         return []

# @app.route('/api/resume/create', methods=['POST'])
# def generate_resume():
#     try:
#         if request.content_type and 'multipart/form-data' in request.content_type:
#             data = {}
#             for key in request.form:
#                 if key in ['workExperience', 'education', 'projects', 'certifications', 'achievements']:
#                     data[key] = safe_parse_json(request.form[key])
#                 else:
#                     data[key] = request.form[key]
            
#             photo_file = request.files.get('photo')
#         else:
#             data = request.json or {}
#             photo_file = None

#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
#         styles = getSampleStyleSheet()
#         title_style = ParagraphStyle(
#             'CustomTitle',
#             parent=styles['Heading1'],
#             fontSize=18,
#             spaceAfter=12,
#             alignment=1,
#             textColor='#2C5AA0'
#         )
#         heading_style = ParagraphStyle(
#             'CustomHeading',
#             parent=styles['Heading2'],
#             fontSize=14,
#             spaceAfter=8,
#             spaceBefore=12,
#             textColor='#1F4788',
#             borderWidth=1,
#             borderColor='#1F4788',
#             borderPadding=4
#         )
#         normal_style = styles['Normal']
#         normal_style.fontSize = 10
#         normal_style.leading = 12
        
#         content = []
        
#         if data.get('fullName'):
#             content.append(Paragraph(data['fullName'].upper(), title_style))
#             content.append(Spacer(1, 12))
        
#         contact_info = []
#         if data.get('email'):
#             contact_info.append(f"📧 {data['email']}")
#         if data.get('phoneNumber'):
#             contact_info.append(f"📱 {data['phoneNumber']}")
#         if data.get('location'):
#             contact_info.append(f"📍 {data['location']}")
        
#         if contact_info:
#             content.append(Paragraph(" | ".join(contact_info), normal_style))
#             content.append(Spacer(1, 8))
        
#         profile_links = []
#         if data.get('linkedinUrl'):
#             profile_links.append(f"LinkedIn: {data['linkedinUrl']}")
#         if data.get('githubPortfolioUrl'):
#             profile_links.append(f"Portfolio: {data['githubPortfolioUrl']}")
        
#         if profile_links:
#             content.append(Paragraph(" | ".join(profile_links), normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('jobTitle'):
#             job_title_style = ParagraphStyle(
#                 'JobTitle',
#                 parent=styles['Heading2'],
#                 fontSize=12,
#                 spaceAfter=8,
#                 alignment=1,
#                 textColor='#555555'
#             )
#             content.append(Paragraph(data['jobTitle'], job_title_style))
        
#         if data.get('professionalSummary'):
#             content.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
#             content.append(Paragraph(data['professionalSummary'], normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('technicalSkills') or data.get('softSkills'):
#             content.append(Paragraph("SKILLS", heading_style))
#             if data.get('technicalSkills'):
#                 content.append(Paragraph(f"<b>Technical Skills:</b> {data['technicalSkills']}", normal_style))
#             if data.get('softSkills'):
#                 content.append(Paragraph(f"<b>Soft Skills:</b> {data['softSkills']}", normal_style))
#             content.append(Spacer(1, 12))
        
#         work_experience = data.get('workExperience', [])
#         if work_experience and any(exp.get('jobTitle') or exp.get('companyName') for exp in work_experience):
#             content.append(Paragraph("WORK EXPERIENCE", heading_style))
#             for exp in work_experience:
#                 if exp.get('jobTitle') or exp.get('companyName'):
#                     job_title = exp.get('jobTitle', 'N/A')
#                     company = exp.get('companyName', 'N/A')
#                     exp_header = f"<b>{job_title}</b> | {company}"
#                     content.append(Paragraph(exp_header, normal_style))
                    
#                     date_info = []
#                     if exp.get('startDate') or exp.get('endDate'):
#                         start_date = exp.get('startDate', 'N/A')
#                         end_date = exp.get('endDate', 'Present')
#                         date_info.append(f"{start_date} - {end_date}")
#                     if exp.get('location'):
#                         date_info.append(exp.get('location'))
                    
#                     if date_info:
#                         content.append(Paragraph(" | ".join(date_info), normal_style))
                    
#                     if exp.get('responsibilities'):
#                         responsibilities = exp.get('responsibilities').strip()
#                         if responsibilities:
#                             resp_lines = [line.strip() for line in responsibilities.replace('•', '\n').split('\n') if line.strip()]
#                             for line in resp_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     if exp.get('achievements'):
#                         achievements = exp.get('achievements').strip()
#                         if achievements:
#                             ach_lines = [line.strip() for line in achievements.replace('•', '\n').split('\n') if line.strip()]
#                             for line in ach_lines:
#                                 if line:
#                                     content.append(Paragraph(f"• {line}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         education = data.get('education', [])
#         if education and any(edu.get('degree') or edu.get('universityName') for edu in education):
#             content.append(Paragraph("EDUCATION", heading_style))
#             for edu in education:
#                 if edu.get('degree') or edu.get('universityName'):
#                     degree = edu.get('degree', 'N/A')
#                     university = edu.get('universityName', 'N/A')
#                     edu_header = f"<b>{degree}</b>"
#                     content.append(Paragraph(edu_header, normal_style))
#                     content.append(Paragraph(university, normal_style))
                    
#                     edu_details = []
#                     if edu.get('location'):
#                         edu_details.append(edu.get('location'))
#                     if edu.get('startDate') or edu.get('endDate'):
#                         start_date = edu.get('startDate', 'N/A')
#                         end_date = edu.get('endDate', 'N/A')
#                         edu_details.append(f"{start_date} - {end_date}")
#                     if edu.get('gpa'):
#                         edu_details.append(f"GPA: {edu.get('gpa')}")
                    
#                     if edu_details:
#                         content.append(Paragraph(" | ".join(edu_details), normal_style))
                    
#                     if edu.get('relevantCoursework'):
#                         content.append(Paragraph(f"<b>Relevant Coursework:</b> {edu.get('relevantCoursework')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         projects = data.get('projects', [])
#         if projects and any(proj.get('projectTitle') for proj in projects):
#             content.append(Paragraph("PROJECTS", heading_style))
#             for proj in projects:
#                 if proj.get('projectTitle'):
#                     content.append(Paragraph(f"<b>{proj.get('projectTitle')}</b>", normal_style))
                    
#                     if proj.get('description'):
#                         content.append(Paragraph(proj.get('description'), normal_style))
                    
#                     if proj.get('technologiesUsed'):
#                         content.append(Paragraph(f"<b>Technologies:</b> {proj.get('technologiesUsed')}", normal_style))
                    
#                     if proj.get('impact'):
#                         content.append(Paragraph(f"<b>Impact:</b> {proj.get('impact')}", normal_style))
                    
#                     if proj.get('projectLink'):
#                         content.append(Paragraph(f"<b>Link:</b> {proj.get('projectLink')}", normal_style))
                    
#                     content.append(Spacer(1, 8))
#             content.append(Spacer(1, 4))
        
#         certifications = data.get('certifications', [])
#         if certifications and any(cert.get('certificationName') for cert in certifications):
#             content.append(Paragraph("CERTIFICATIONS", heading_style))
#             for cert in certifications:
#                 if cert.get('certificationName'):
#                     cert_text = f"• <b>{cert.get('certificationName')}</b>"
#                     if cert.get('issuingAuthority'):
#                         cert_text += f" - {cert.get('issuingAuthority')}"
#                     if cert.get('date'):
#                         cert_text += f" ({cert.get('date')})"
#                     content.append(Paragraph(cert_text, normal_style))
#             content.append(Spacer(1, 12))
        
#         achievements = data.get('achievements', [])
#         if achievements and any(ach.get('title') for ach in achievements):
#             content.append(Paragraph("ACHIEVEMENTS", heading_style))
#             for ach in achievements:
#                 if ach.get('title'):
#                     ach_text = f"• <b>{ach.get('title')}</b>"
#                     if ach.get('organization'):
#                         ach_text += f" - {ach.get('organization')}"
#                     if ach.get('date'):
#                         ach_text += f" ({ach.get('date')})"
#                     content.append(Paragraph(ach_text, normal_style))
#                     if ach.get('description'):
#                         content.append(Paragraph(f"  {ach.get('description')}", normal_style))
#             content.append(Spacer(1, 12))
        
#         if data.get('languages'):
#             content.append(Paragraph("LANGUAGES", heading_style))
#             content.append(Paragraph(data['languages'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('publications'):
#             content.append(Paragraph("PUBLICATIONS", heading_style))
#             content.append(Paragraph(data['publications'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('volunteering'):
#             content.append(Paragraph("VOLUNTEERING", heading_style))
#             content.append(Paragraph(data['volunteering'], normal_style))
#             content.append(Spacer(1, 8))

#         if data.get('hobbies'):
#             content.append(Paragraph("HOBBIES & INTERESTS", heading_style))
#             content.append(Paragraph(data['hobbies'], normal_style))
        
#         doc.build(content)
#         buffer.seek(0)
        
#         return send_file(
#             buffer,
#             as_attachment=True,
#             download_name='resume.pdf',
#             mimetype='application/pdf'
#         )
        
#     except Exception as e:
#         print(f"Error generating resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate resume: {str(e)}'}), 500


# # ===================== ROADMAP ROUTES =====================

# @app.route('/api/roadmap/generate', methods=['POST'])
# def generate_roadmap():
#     """Generate a new roadmap for a job role"""
#     try:
#         data = request.json
#         job_role = data.get('job_role')
#         experience_level = data.get('experience_level', 'beginner')
#         target_company = data.get('target_company')
#         user_skills = data.get('user_skills', [])
#         available_hours = data.get('available_hours_per_week', 10)
        
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         existing_roadmap_id, existing_roadmap = db_manager.get_roadmap(job_role)
        
#         if existing_roadmap:
#             if user_skills:
#                 customized_roadmap = roadmap_generator.update_roadmap_for_user(
#                     existing_roadmap, user_skills, available_hours
#                 )
#             else:
#                 customized_roadmap = existing_roadmap
            
#             return jsonify({
#                 'roadmap_id': existing_roadmap_id,
#                 'roadmap': customized_roadmap,
#                 'message': 'Retrieved existing roadmap'
#             })
        
#         roadmap_data = roadmap_generator.generate_roadmap(
#             job_role, experience_level, target_company
#         )
        
#         if user_skills:
#             roadmap_data = roadmap_generator.update_roadmap_for_user(
#                 roadmap_data, user_skills, available_hours
#             )
        
#         roadmap_id = db_manager.save_roadmap(job_role, roadmap_data)
#         roadmap_data['roadmap_id'] = roadmap_id
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data,
#             'message': 'Roadmap generated successfully'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/resources/<step_id>', methods=['GET'])
# def get_step_resources(roadmap_id, step_id):
#     """Get resources for a specific step"""
#     try:
#         existing_resources = db_manager.get_resources(step_id)
        
#         if existing_resources:
#             return jsonify({
#                 'step_id': step_id,
#                 'resources': existing_resources
#             })
        
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         step_data = None
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 if step['step_id'] == step_id:
#                     step_data = step
#                     break
#             if step_data:
#                 break
        
#         if not step_data:
#             return jsonify({'error': 'Step not found'}), 404
        
#         resources = resource_finder.get_all_resources_for_step(
#             step_data['title'], 
#             step_data['description']
#         )
        
#         if resources:
#             db_manager.save_resources(step_id, resources)
        
#         return jsonify({
#             'step_id': step_id,
#             'resources': resources
#         })
        
#     except Exception as e:
#         print(f"Error getting step resources: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to get resources: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['GET'])
# def get_roadmap_progress(roadmap_id):
#     """Get user progress for a roadmap"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'user_id': user_id,
#             'progress': progress
#         })
        
#     except Exception as e:
#         print(f"Error getting progress: {str(e)}")
#         return jsonify({'error': f'Failed to get progress: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['POST'])
# def update_progress(roadmap_id):
#     """Update user progress for a step"""
#     try:
#         data = request.json
#         user_id = data.get('user_id', 'default_user')
#         step_id = data.get('step_id')
#         completed = data.get('completed', False)
#         time_spent = data.get('time_spent', 0)
        
#         if not step_id:
#             return jsonify({'error': 'Step ID is required'}), 400
        
#         db_manager.save_user_progress(user_id, roadmap_id, step_id, completed, time_spent)
        
#         return jsonify({
#             'message': 'Progress updated successfully',
#             'roadmap_id': roadmap_id,
#             'step_id': step_id,
#             'completed': completed
#         })
        
#     except Exception as e:
#         print(f"Error updating progress: {str(e)}")
#         return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500

# @app.route('/api/roadmap/popular-roles', methods=['GET'])
# def get_popular_roles():
#     """Get list of popular job roles for roadmap generation"""
#     try:
#         popular_roles = [
#             {
#                 'id': 'software-developer',
#                 'title': 'Software Developer',
#                 'description': 'Full-stack and backend development roles',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'Very High',
#                 'skills': [
#                     {
#                         'name': 'Programming',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Python Programming',
#                                 'url': 'https://www.python.org/about/gettingstarted/',
#                                 'description': 'Official Python documentation and tutorials'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'JavaScript Fundamentals',
#                                 'url': 'https://javascript.info/',
#                                 'description': 'Modern JavaScript tutorial'
#                             },
#                             {
#                                 'type': 'practice',
#                                 'title': 'LeetCode',
#                                 'url': 'https://leetcode.com/',
#                                 'description': 'Practice coding problems'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'System Design',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'System Design Primer',
#                                 'url': 'https://github.com/donnemartin/system-design-primer',
#                                 'description': 'Learn how to design large-scale systems'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Web Development',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'MDN Web Docs',
#                                 'url': 'https://developer.mozilla.org/',
#                                 'description': 'Web development resources'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'data-scientist',
#                 'title': 'Data Scientist',
#                 'description': 'Analyze data to derive business insights',
#                 'avg_salary': '6-20 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Python',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Python for Data Science',
#                                 'url': 'https://www.coursera.org/specializations/python',
#                                 'description': 'Coursera Python specialization'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Machine Learning',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Scikit-learn Tutorial',
#                                 'url': 'https://scikit-learn.org/stable/tutorial/index.html',
#                                 'description': 'Official ML library documentation'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Kaggle Learn',
#                                 'url': 'https://www.kaggle.com/learn',
#                                 'description': 'Free ML courses and competitions'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Statistics',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Khan Academy Statistics',
#                                 'url': 'https://www.khanacademy.org/math/statistics-probability',
#                                 'description': 'Free statistics courses'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'product-manager',
#                 'title': 'Product Manager',
#                 'description': 'Define product strategy and roadmap',
#                 'avg_salary': '8-25 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Strategy',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Product Strategy Guide',
#                                 'url': 'https://www.productplan.com/learn/product-strategy/',
#                                 'description': 'Product strategy resources'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Analytics',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Google Analytics Academy',
#                                 'url': 'https://analytics.google.com/analytics/academy/',
#                                 'description': 'Free analytics courses'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Communication',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Product Management Resources',
#                                 'url': 'https://www.mindtheproduct.com/',
#                                 'description': 'PM community and articles'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'ui-ux-designer',
#                 'title': 'UI/UX Designer',
#                 'description': 'Design user interfaces and experiences',
#                 'avg_salary': '4-12 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Design Tools',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Figma Tutorial',
#                                 'url': 'https://www.figma.com/resources/learn-design/',
#                                 'description': 'Learn Figma design tool'
#                             },
#                             {
#                                 'type': 'practice',
#                                 'title': 'Dribbble',
#                                 'url': 'https://dribbble.com/',
#                                 'description': 'Design inspiration and community'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'User Research',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Nielsen Norman Group',
#                                 'url': 'https://www.nngroup.com/articles/',
#                                 'description': 'UX research articles'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Prototyping',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Interaction Design Foundation',
#                                 'url': 'https://www.interaction-design.org/',
#                                 'description': 'UX design courses'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'business-analyst',
#                 'title': 'Business Analyst',
#                 'description': 'Bridge between business and technology',
#                 'avg_salary': '4-15 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'Analysis',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Business Analysis Fundamentals',
#                                 'url': 'https://www.iiba.org/',
#                                 'description': 'International Institute of Business Analysis'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Excel & SQL',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'SQL Tutorial',
#                                 'url': 'https://www.w3schools.com/sql/',
#                                 'description': 'Learn SQL for data analysis'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Excel Skills',
#                                 'url': 'https://support.microsoft.com/en-us/office/excel-video-training',
#                                 'description': 'Microsoft Excel tutorials'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Documentation',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Business Analysis Templates',
#                                 'url': 'https://www.bridging-the-gap.com/',
#                                 'description': 'BA resources and templates'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'devops-engineer',
#                 'title': 'DevOps Engineer',
#                 'description': 'Manage deployment and infrastructure',
#                 'avg_salary': '6-18 LPA',
#                 'demand': 'Very High',
#                 'skills': [
#                     {
#                         'name': 'Cloud (AWS/Azure)',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'AWS Free Tier',
#                                 'url': 'https://aws.amazon.com/free/',
#                                 'description': 'Learn AWS with free tier'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Azure Fundamentals',
#                                 'url': 'https://docs.microsoft.com/en-us/learn/azure/',
#                                 'description': 'Microsoft Azure learning path'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Docker & Kubernetes',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Docker Documentation',
#                                 'url': 'https://docs.docker.com/get-started/',
#                                 'description': 'Official Docker getting started guide'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Kubernetes Basics',
#                                 'url': 'https://kubernetes.io/docs/tutorials/kubernetes-basics/',
#                                 'description': 'Learn Kubernetes fundamentals'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'CI/CD',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Jenkins Tutorial',
#                                 'url': 'https://www.jenkins.io/doc/tutorials/',
#                                 'description': 'Learn Jenkins for CI/CD'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'consultant',
#                 'title': 'Management Consultant',
#                 'description': 'Provide strategic business advice',
#                 'avg_salary': '8-30 LPA',
#                 'demand': 'Medium',
#                 'skills': [
#                     {
#                         'name': 'Problem Solving',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Case Interview Prep',
#                                 'url': 'https://www.caseinterviewprep.com/',
#                                 'description': 'Management consulting case prep'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Business Frameworks',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Consulting Tools',
#                                 'url': 'https://www.mckinsey.com/capabilities',
#                                 'description': 'Business strategy frameworks'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Presentation',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'McKinsey Presentation Style',
#                                 'url': 'https://www.duarte.com/',
#                                 'description': 'Professional presentation skills'
#                             }
#                         ]
#                     }
#                 ]
#             },
#             {
#                 'id': 'digital-marketing',
#                 'title': 'Digital Marketing Specialist',
#                 'description': 'Online marketing and growth strategies',
#                 'avg_salary': '3-10 LPA',
#                 'demand': 'High',
#                 'skills': [
#                     {
#                         'name': 'SEO/SEM',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Google Digital Garage',
#                                 'url': 'https://learndigital.withgoogle.com/',
#                                 'description': 'Free digital marketing courses'
#                             },
#                             {
#                                 'type': 'learning',
#                                 'title': 'Moz SEO Learning Center',
#                                 'url': 'https://moz.com/learn/seo',
#                                 'description': 'SEO fundamentals and best practices'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Social Media Marketing',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'HubSpot Academy',
#                                 'url': 'https://academy.hubspot.com/',
#                                 'description': 'Free marketing certifications'
#                             }
#                         ]
#                     },
#                     {
#                         'name': 'Analytics',
#                         'resources': [
#                             {
#                                 'type': 'learning',
#                                 'title': 'Google Analytics',
#                                 'url': 'https://analytics.google.com/analytics/academy/',
#                                 'description': 'Master Google Analytics'
#                             }
#                         ]
#                     }
#                 ]
#             }
#         ]
        
#         return jsonify({'roles': popular_roles})
        
#     except Exception as e:
#         print(f"Error getting popular roles: {str(e)}")
#         return jsonify({'error': 'Failed to get popular roles'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>', methods=['GET'])
# def get_roadmap_by_id(roadmap_id):
#     """Get a specific roadmap by ID"""
#     try:
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
        
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         return jsonify({
#             'roadmap_id': roadmap_id,
#             'roadmap': roadmap_data
#         })
        
#     except Exception as e:
#         print(f"Error getting roadmap: {str(e)}")
#         return jsonify({'error': f'Failed to get roadmap: {str(e)}'}), 500

# @app.route('/api/roadmap/<int:roadmap_id>/analytics', methods=['GET'])
# def get_roadmap_analytics(roadmap_id):
#     """Get analytics for a roadmap"""
#     try:
#         user_id = request.args.get('user_id', 'default_user')
        
#         roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
#         if not roadmap_data:
#             return jsonify({'error': 'Roadmap not found'}), 404
        
#         progress = db_manager.get_user_progress(user_id, roadmap_id)
        
#         total_steps = 0
#         completed_steps = 0
#         total_time_spent = 0
        
#         for phase in roadmap_data.get('phases', []):
#             for step in phase.get('steps', []):
#                 total_steps += 1
#                 step_id = step['step_id']
                
#                 if step_id in progress:
#                     if progress[step_id]['completed']:
#                         completed_steps += 1
#                     total_time_spent += progress[step_id]['time_spent']
        
#         completion_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
#         estimated_total_hours = sum(
#             sum(step.get('estimated_hours', 0) for step in phase.get('steps', []))
#             for phase in roadmap_data.get('phases', [])
#         )
        
#         analytics = {
#             'completion_percentage': round(completion_percentage, 2),
#             'completed_steps': completed_steps,
#             'total_steps': total_steps,
#             'time_spent_hours': total_time_spent,
#             'estimated_total_hours': estimated_total_hours,
#             'progress_by_phase': [],
#             'recent_activity': []
#         }
        
#         for phase in roadmap_data.get('phases', []):
#             phase_steps = len(phase.get('steps', []))
#             phase_completed = sum(
#                 1 for step in phase.get('steps', [])
#                 if step['step_id'] in progress and progress[step['step_id']]['completed']
#             )
            
#             analytics['progress_by_phase'].append({
#                 'phase_name': phase['phase_name'],
#                 'completed_steps': phase_completed,
#                 'total_steps': phase_steps,
#                 'completion_percentage': (phase_completed / phase_steps * 100) if phase_steps > 0 else 0
#             })
        
#         return jsonify(analytics)
        
#     except Exception as e:
#         print(f"Error getting analytics: {str(e)}")
#         return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500


# # ===================== RESUME-BASED ROADMAP ROUTES =====================

# @app.route('/api/roadmap/analyze-resume', methods=['POST'])
# def analyze_resume_for_roadmap():
#     """Analyze resume and generate personalized career roadmap"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume using Gemini
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get primary role recommendation
#         primary_role = career_info.get('primary_role', 'Software Developer')
        
#         # Generate personalized roadmap for primary role
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, primary_role
#         )
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         # Save the personalized roadmap to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{primary_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'career_analysis': {
#                 'primary_role': primary_role,
#                 'experience_level': career_info.get('experience_level'),
#                 'skills': career_info.get('skills', []),
#                 'skill_gaps': personalized_roadmap.get('skill_gaps', []),
#                 'strengths': career_info.get('strengths', []),
#             },
#             'personalized_roadmap': personalized_roadmap,
#             'alternative_careers': alternative_careers,
#             'message': 'Resume analyzed successfully'
#         })
        
#     except Exception as e:
#         print(f"Error analyzing resume: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500


# @app.route('/api/roadmap/generate-for-role', methods=['POST'])
# def generate_roadmap_for_specific_role():
#     """Generate roadmap for a specific role based on resume analysis"""
#     try:
#         data = request.json
        
#         if 'resume_text' not in data and 'career_info' not in data:
#             return jsonify({'error': 'Resume text or career info required'}), 400
        
#         job_role = data.get('job_role')
#         if not job_role:
#             return jsonify({'error': 'Job role is required'}), 400
        
#         # If career_info is provided, use it; otherwise analyze resume_text
#         if 'career_info' in data:
#             career_info = data['career_info']
#         else:
#             resume_text = data['resume_text']
#             career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Generate personalized roadmap
#         personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
#             career_info, job_role
#         )
        
#         # Save to database
#         roadmap_id = db_manager.save_roadmap(
#             f"{job_role} (Personalized)", 
#             personalized_roadmap
#         )
        
#         return jsonify({
#             'success': True,
#             'roadmap_id': roadmap_id,
#             'roadmap': personalized_roadmap,
#             'message': f'Personalized roadmap generated for {job_role}'
#         })
        
#     except Exception as e:
#         print(f"Error generating roadmap for role: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500


# @app.route('/api/career/analyze', methods=['POST'])
# def quick_career_analysis():
#     """Quick career analysis from resume (without full roadmap generation)"""
#     try:
#         if 'resume' not in request.files:
#             return jsonify({'error': 'No resume file provided'}), 400
        
#         resume_file = request.files['resume']
        
#         # Extract text from PDF
#         with pdfplumber.open(resume_file) as pdf:
#             resume_text = ' '.join(
#                 page.extract_text() or '' for page in pdf.pages
#             )
        
#         if not resume_text.strip():
#             return jsonify({'error': 'Could not extract text from resume'}), 400
        
#         # Analyze resume
#         career_info = resume_analyzer.extract_career_info(resume_text)
        
#         # Get alternative career suggestions
#         alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        
#         return jsonify({
#             'success': True,
#             'career_info': career_info,
#             'alternative_careers': alternative_careers
#         })
        
#     except Exception as e:
#         print(f"Error in career analysis: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'Failed to analyze career: {str(e)}'}), 500


# # ===================== MAIN APPLICATION ====================

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print("📋 Features available:")
#     print("  • Resume screening and generation")
#     print("  • Cover letter generation")
#     print("  • AI-powered roadmap creation")
#     print("  • Resume-based personalized roadmaps")
#     print("  • Progress tracking")
#     print("  • Resource recommendations")
#     print("🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)


#26 october 2025

# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# nltk.download('punkt')
# nltk.download('stopwords')

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# genai.configure(api_key=GEMINI_API_KEY)

# # Load models and vectorizer
# selection_model = joblib.load('selection_model.pkl')
# salary_model = joblib.load('salary_model.pkl')
# tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
# resume_data = pd.read_csv('resume_screening.csv')

# # In-memory score history
# score_history = []

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     text = text.lower()
#     text = re.sub(r'[^\w\s]', '', text)
#     tokens = word_tokenize(text)
#     stop_words = set(stopwords.words('english'))
#     tokens = [word for word in tokens if word not in stop_words]
#     return ' '.join(tokens)

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-pro')
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity. Provide a brief reasoning for the score.
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         score_match = re.search(r'Score: (\d+)', response.text)
#         score = int(score_match.group(1)) if score_match else 80
#         reasoning_match = re.search(r'Reasoning: (.*?)(?:\n|$)', response.text)
#         reasoning = reasoning_match.group(1) if reasoning_match else "No specific reasoning provided."

#         score_history.append({
#             'user_id': user_id,
#             'ats_score': score,
#             'timestamp': pd.Timestamp.now().isoformat()
#         })

#         return jsonify({"score": score, "reasoning": reasoning})
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-pro')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         tips = []
#         for line in response.text.split('\n'):
#             match = re.match(r'\* (.*?): (.*?)\((.*?)\)', line)
#             if match:
#                 tips.append({
#                     'category': match.group(1).strip(),
#                     'tip': match.group(2).strip(),
#                     'priority': match.group(3).strip()
#                 })
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-pro')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         similarity_match = re.search(r'Similarity: (\d+)%', response.text)
#         similarity = int(similarity_match.group(1)) if similarity_match else 50
#         missing_keywords_match = re.search(r'Missing Keywords: (.*?)(?:\n|$)', response.text)
#         missing_keywords = missing_keywords_match.group(1).split(', ') if missing_keywords_match else []
#         strengths_match = re.search(r'Strengths: (.*?)(?:\n|$)', response.text)
#         strengths = strengths_match.group(1).split(', ') if strengths_match else []
#         return jsonify({
#             "similarity_percentage": similarity,
#             "missing_keywords": missing_keywords,
#             "strengths": strengths
#         })
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-pro')
#         prompt = f"""
#         Extract skills from the resume text and compare them with top skills: {', '.join(all_skills)}.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         user_skills_match = re.search(r'Identified Skills: (.*?)(?:\n|$)', response.text)
#         user_skills = user_skills_match.group(1).split(', ') if user_skills_match else []
#         missing_skills = [skill for skill in all_skills if skill not in user_skills]
#         recommendation = f"Consider learning: {', '.join(missing_skills[:3])}" if missing_skills else "Your skills are well-aligned."
#         return jsonify({
#             "user_skills": user_skills,
#             "top_skills": all_skills,
#             "missing_skills": missing_skills,
#             "recommendation": recommendation
#         })
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-pro')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         companies = response.text.split('\n')[:5]
#         companies = [company.strip('* -') for company in companies if company.strip()]
#         return jsonify({"recommended_companies": companies})
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-pro')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a list of steps, each containing 'step', 'description', and 'estimated_time'.
#         """
#         response = model.generate_content(prompt)
#         roadmap = []
#         for line in response.text.split('\n'):
#             match = re.match(r'\* Step (\d+): (.*?)\((.*?)\)', line)
#             if match:
#                 roadmap.append({
#                     'step': int(match.group(1)),
#                     'description': match.group(2).strip(),
#                     'estimated_time': match.group(3).strip()
#                 })
#         return jsonify({"roadmap": roadmap})
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)


# 27 october 2025 working 
# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.tokenize import word_tokenize

# # Fallback stopwords list
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# # Download NLTK data
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('punkt_tab', quiet=True)
#     print("NLTK data downloaded successfully: punkt, punkt_tab")
# except Exception as e:
#     print(f"Error downloading NLTK data: {e}")

# # Initialize Gemini API
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available Gemini models: {available_models}")
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # Load models and vectorizer
# try:
#     selection_model = joblib.load('selection_model.pkl')
#     salary_model = joblib.load('salary_model.pkl')
#     tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
#     resume_data = pd.read_csv('resume_screening.csv')
# except Exception as e:
#     print(f"Error loading models or data: {e}")

# # In-memory score history
# score_history = []

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity. Provide a brief reasoning for the score.
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         score_match = re.search(r'Score: (\d+)', response.text)
#         score = int(score_match.group(1)) if score_match else 80
#         reasoning_match = re.search(r'Reasoning: (.*?)(?:\n|$)', response.text)
#         reasoning = reasoning_match.group(1) if reasoning_match else "No specific reasoning provided."

#         score_history.append({
#             'user_id': user_id,
#             'ats_score': score,
#             'timestamp': pd.Timestamp.now().isoformat()
#         })

#         return jsonify({"score": score, "reasoning": reasoning})
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         tips = []
#         for line in response.text.split('\n'):
#             match = re.match(r'\* (.*?): (.*?)\((.*?)\)', line)
#             if match:
#                 tips.append({
#                     'category': match.group(1).strip(),
#                     'tip': match.group(2).strip(),
#                     'priority': match.group(3).strip()
#                 })
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         similarity_match = re.search(r'Similarity: (\d+)%', response.text)
#         similarity = int(similarity_match.group(1)) if similarity_match else 50
#         missing_keywords_match = re.search(r'Missing Keywords: (.*?)(?:\n|$)', response.text)
#         missing_keywords = missing_keywords_match.group(1).split(', ') if missing_keywords_match else []
#         strengths_match = re.search(r'Strengths: (.*?)(?:\n|$)', response.text)
#         strengths = strengths_match.group(1).split(', ') if strengths_match else []
#         return jsonify({
#             "similarity_percentage": similarity,
#             "missing_keywords": missing_keywords,
#             "strengths": strengths
#         })
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Extract skills from the resume text and compare them with top skills: {', '.join(all_skills)}.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         user_skills_match = re.search(r'Identified Skills: (.*?)(?:\n|$)', response.text)
#         user_skills = user_skills_match.group(1).split(', ') if user_skills_match else []
#         missing_skills = [skill for skill in all_skills if skill not in user_skills]
#         recommendation = f"Consider learning: {', '.join(missing_skills[:3])}" if missing_skills else "Your skills are well-aligned."
#         return jsonify({
#             "user_skills": user_skills,
#             "top_skills": all_skills,
#             "missing_skills": missing_skills,
#             "recommendation": recommendation
#         })
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         companies = response.text.split('\n')[:5]
#         companies = [company.strip('* -') for company in companies if company.strip()]
#         return jsonify({"recommended_companies": companies})
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a list of steps, each containing 'step', 'description', and 'estimated_time'.
#         """
#         response = model.generate_content(prompt)
#         roadmap = []
#         for line in response.text.split('\n'):
#             match = re.match(r'\* Step (\d+): (.*?)\((.*?)\)', line)
#             if match:
#                 roadmap.append({
#                     'step': int(match.group(1)),
#                     'description': match.group(2).strip(),
#                     'estimated_time': match.group(3).strip()
#                 })
#         return jsonify({"roadmap": roadmap})
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)




#27 october secong iteration pikachu

# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.tokenize import word_tokenize

# # Fallback stopwords list
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# # Download NLTK data
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('punkt_tab', quiet=True)
#     print("NLTK data downloaded successfully: punkt, punkt_tab")
# except Exception as e:
#     print(f"Error downloading NLTK data: {e}")

# # Initialize Gemini API
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available Gemini models: {available_models}")
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # Load models and vectorizer
# try:
#     selection_model = joblib.load('selection_model.pkl')
#     salary_model = joblib.load('salary_model.pkl')
#     tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
#     resume_data = pd.read_csv('resume_screening.csv')
# except Exception as e:
#     print(f"Error loading models or data: {e}")

# # In-memory score history
# score_history = []

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity. Provide a brief reasoning for the score.
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         score_match = re.search(r'Score: (\d+)', response.text)
#         score = int(score_match.group(1)) if score_match else 80
#         reasoning_match = re.search(r'Reasoning: (.*?)(?:\n|$)', response.text)
#         reasoning = reasoning_match.group(1) if reasoning_match else "No specific reasoning provided."

#         score_history.append({
#             'user_id': user_id,
#             'ats_score': score,
#             'timestamp': pd.Timestamp.now().isoformat()
#         })

#         return jsonify({"score": score, "reasoning": reasoning})
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         tips = []
#         for line in response.text.split('\n'):
#             match = re.match(r'\* (.*?): (.*?)\((.*?)\)', line)
#             if match:
#                 tips.append({
#                     'category': match.group(1).strip(),
#                     'tip': match.group(2).strip(),
#                     'priority': match.group(3).strip()
#                 })
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         similarity_match = re.search(r'Similarity: (\d+)%', response.text)
#         similarity = int(similarity_match.group(1)) if similarity_match else 50
#         missing_keywords_match = re.search(r'Missing Keywords: (.*?)(?:\n|$)', response.text)
#         missing_keywords = missing_keywords_match.group(1).split(', ') if missing_keywords_match else []
#         strengths_match = re.search(r'Strengths: (.*?)(?:\n|$)', response.text)
#         strengths = strengths_match.group(1).split(', ') if strengths_match else []
#         return jsonify({
#             "similarity_percentage": similarity,
#             "missing_keywords": missing_keywords,
#             "strengths": strengths
#         })
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Extract skills from the resume text and compare them with top skills: {', '.join(all_skills)}.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         user_skills_match = re.search(r'Identified Skills: (.*?)(?:\n|$)', response.text)
#         user_skills = user_skills_match.group(1).split(', ') if user_skills_match else []
#         missing_skills = [skill for skill in all_skills if skill not in user_skills]
#         recommendation = f"Consider learning: {', '.join(missing_skills[:3])}" if missing_skills else "Your skills are well-aligned."
#         return jsonify({
#             "user_skills": user_skills,
#             "top_skills": all_skills,
#             "missing_skills": missing_skills,
#             "recommendation": recommendation
#         })
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
#         if features.shape[1] != expected_features:
#             print(f"Feature mismatch - Expected: {expected_features}, Got: {features.shape[1]}, Features: {features}")
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         print(f"Prediction input: {features}, Probability: {probability}")
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit. Include brief reasoning for each recommendation.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         companies = []
#         for line in response.text.split('\n'):
#             match = re.match(r'\* (.*?): (.*?)(?:\n|$)', line)
#             if match:
#                 companies.append({
#                     'name': match.group(1).strip(),
#                     'reason': match.group(2).strip()
#                 })
#         return jsonify({"recommended_companies": companies[:5]})
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-2.5-pro')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a list of steps, each containing 'step', 'description', and 'estimated_time'.
#         """
#         response = model.generate_content(prompt)
#         roadmap = []
#         for line in response.text.split('\n'):
#             match = re.match(r'\* Step (\d+): (.*?)\((.*?)\)', line)
#             if match:
#                 roadmap.append({
#                     'step': int(match.group(1)),
#                     'description': match.group(2).strip(),
#                     'estimated_time': match.group(3).strip()
#                 })
#         return jsonify({"roadmap": roadmap})
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)



#27 october 2025 3rd iteration

# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.tokenize import word_tokenize
# import json  # Added for JSON parsing

# # Fallback stopwords list
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# # Download NLTK data
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('punkt_tab', quiet=True)
#     print("NLTK data downloaded successfully: punkt, punkt_tab")
# except Exception as e:
#     print(f"Error downloading NLTK data: {e}")

# # Initialize Gemini API
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available Gemini models: {available_models}")
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # Load models and vectorizer
# try:
#     selection_model = joblib.load('selection_model.pkl')
#     salary_model = joblib.load('salary_model.pkl')
#     tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
#     resume_data = pd.read_csv('resume_screening.csv')
# except Exception as e:
#     print(f"Error loading models or data: {e}")

# # In-memory score history
# score_history = []

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')  # Changed to flash for higher free tier limits
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity. Provide a brief reasoning for the score.
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         score_match = re.search(r'Score: (\d+)', response.text)
#         score = int(score_match.group(1)) if score_match else 80
#         reasoning_match = re.search(r'Reasoning: (.*?)(?:\n|$)', response.text)
#         reasoning = reasoning_match.group(1) if reasoning_match else "No specific reasoning provided."

#         score_history.append({
#             'user_id': user_id,
#             'ats_score': score,
#             'timestamp': pd.Timestamp.now().isoformat()
#         })

#         return jsonify({"score": score, "reasoning": reasoning})
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Return the response as a JSON object with a 'tips' array, where each tip has 'category', 'tip', and 'priority' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         try:
#             tips = json.loads(response.text) if response.text.strip().startswith('{') else []
#             if not tips or 'tips' not in tips:
#                 tips = [{'category': 'General', 'tip': 'No specific tips identified', 'priority': 'Low'}]
#         except json.JSONDecodeError:
#             tips = [{'category': 'General', 'tip': 'Failed to parse tips', 'priority': 'Low'}]
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Return the response as a JSON object with 'similarity_percentage', 'missing_keywords', and 'strengths' fields.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         try:
#             result = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'similarity_percentage': 50,
#                 'missing_keywords': [],
#                 'strengths': []
#             }
#         except json.JSONDecodeError:
#             result = {'similarity_percentage': 50, 'missing_keywords': [], 'strengths': []}
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Extract skills from the resume text and compare them with top skills: {', '.join(all_skills)}.
#         Return the response as a JSON object with 'user_skills', 'top_skills', 'missing_skills', and 'recommendation' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         try:
#             result = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'user_skills': [],
#                 'top_skills': all_skills,
#                 'missing_skills': all_skills,
#                 'recommendation': 'Consider learning more skills'
#             }
#         except json.JSONDecodeError:
#             result = {'user_skills': [], 'top_skills': all_skills, 'missing_skills': all_skills, 'recommendation': 'Consider learning more skills'}
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
#         if features.shape[1] != expected_features:
#             print(f"Feature mismatch - Expected: {expected_features}, Got: {features.shape[1]}, Features: {features}")
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         # Apply minimum threshold of 10% to avoid 0%
#         probability = max(probability, 10.0)
#         print(f"Prediction input: {features}, Probability: {probability}")
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit. 
#         Return the response as a JSON object with a 'companies' array, where each company has 'name' and 'reason' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         try:
#             companies = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]
#             }
#             if 'companies' not in companies:
#                 companies = {'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]}
#         except json.JSONDecodeError:
#             companies = {'companies': [{'name': 'Default Company', 'reason': 'Failed to parse recommendations'}]}
#         return jsonify(companies)
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a 'roadmap' array, where each step has 'step', 'description', and 'estimated_time' fields.
#         """
#         response = model.generate_content(prompt)
#         try:
#             roadmap = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]
#             }
#             if 'roadmap' not in roadmap:
#                 roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         except json.JSONDecodeError:
#             roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         return jsonify(roadmap)
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)











#charmendar not very nice

# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.tokenize import word_tokenize
# import json

# # Fallback stopwords list
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# # Download NLTK data
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('punkt_tab', quiet=True)
#     print("NLTK data downloaded successfully: punkt, punkt_tab")
# except Exception as e:
#     print(f"Error downloading NLTK data: {e}")

# # Initialize Gemini API
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available Gemini models: {available_models}")
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # Load models and vectorizer
# try:
#     selection_model = joblib.load('selection_model.pkl')
#     salary_model = joblib.load('salary_model.pkl')
#     tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
#     resume_data = pd.read_csv('resume_screening.csv')
# except Exception as e:
#     print(f"Error loading models or data: {e}")

# # In-memory score history
# score_history = []

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity. 
#         Provide a brief reasoning for the score and 2-3 specific improvement tips to enhance ATS compatibility.
#         Return the response as a JSON object with 'score', 'reasoning', and 'improvement_tips' fields (each tip as an object with 'tip' and 'priority').
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         try:
#             result = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'score': 80,
#                 'reasoning': 'Default reasoning',
#                 'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#             }
#             if 'score' not in result or 'reasoning' not in result or 'improvement_tips' not in result:
#                 result = {
#                     'score': 80,
#                     'reasoning': 'Default reasoning',
#                     'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#                 }
#         except json.JSONDecodeError:
#             result = {
#                 'score': 80,
#                 'reasoning': 'Default reasoning',
#                 'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#             }
#         score_history.append({
#             'user_id': user_id,
#             'ats_score': result['score'],
#             'timestamp': pd.Timestamp.now().isoformat()
#         })
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Return the response as a JSON object with a 'tips' array, where each tip has 'category', 'tip', and 'priority' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         try:
#             tips = json.loads(response.text) if response.text.strip().startswith('{') else []
#             if not tips or 'tips' not in tips:
#                 tips = [{'tips': [{'category': 'General', 'tip': 'No specific tips identified', 'priority': 'Low'}]}]
#         except json.JSONDecodeError:
#             tips = [{'tips': [{'category': 'General', 'tip': 'Failed to parse tips', 'priority': 'Low'}]}]
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Return the response as a JSON object with 'similarity_percentage', 'missing_keywords', and 'strengths' fields.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         try:
#             result = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'similarity_percentage': 50,
#                 'missing_keywords': [],
#                 'strengths': []
#             }
#         except json.JSONDecodeError:
#             result = {'similarity_percentage': 50, 'missing_keywords': [], 'strengths': []}
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Extract skills from the resume text and compare them with the following top skills: {', '.join(all_skills)}.
#         Return the response as a JSON object with 'user_skills', 'top_skills', 'missing_skills', and 'recommendation' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         try:
#             result = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'user_skills': [],
#                 'top_skills': all_skills,
#                 'missing_skills': [],
#                 'recommendation': 'Please review your skills alignment'
#             }
#             if 'missing_skills' not in result:
#                 result['missing_skills'] = [skill for skill in all_skills if skill not in result.get('user_skills', [])]
#                 result['recommendation'] = f"Consider learning: {', '.join(result['missing_skills'][:3])}" if result['missing_skills'] else "Your skills are well-aligned."
#         except json.JSONDecodeError:
#             result = {
#                 'user_skills': [],
#                 'top_skills': all_skills,
#                 'missing_skills': all_skills,
#                 'recommendation': 'Consider learning more skills'
#             }
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
#         if features.shape[1] != expected_features:
#             print(f"Feature mismatch - Expected: {expected_features}, Got: {features.shape[1]}, Features: {features}")
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         print(f"Prediction input: {features}, Probability: {probability}")
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit. 
#         Return the response as a JSON object with a 'companies' array, where each company has 'name' and 'reason' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         try:
#             companies = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]
#             }
#             if 'companies' not in companies:
#                 companies = {'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]}
#         except json.JSONDecodeError:
#             companies = {'companies': [{'name': 'Default Company', 'reason': 'Failed to parse recommendations'}]}
#         return jsonify(companies)
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a 'roadmap' array, where each step has 'step', 'description', and 'estimated_time' fields.
#         """
#         response = model.generate_content(prompt)
#         try:
#             roadmap = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]
#             }
#             if 'roadmap' not in roadmap:
#                 roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         except json.JSONDecodeError:
#             roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         return jsonify(roadmap)
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)


# wabbafet version-does not work

# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.tokenize import word_tokenize
# import json

# # Fallback stopwords list
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# # Download NLTK data
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('punkt_tab', quiet=True)
#     print("NLTK data downloaded successfully: punkt, punkt_tab")
# except Exception as e:
#     print(f"Error downloading NLTK data: {e}")

# # Initialize Gemini API
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available Gemini models: {available_models}")
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# # Load models and vectorizer
# try:
#     selection_model = joblib.load('selection_model.pkl')
#     salary_model = joblib.load('salary_model.pkl')
#     tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
#     resume_data = pd.read_csv('resume_screening.csv')
# except Exception as e:
#     print(f"Error loading models or data: {e}")

# # In-memory score history
# score_history = []

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity.
#         Provide a brief reasoning for the score and 2-3 specific improvement tips to enhance ATS compatibility.
#         Return ONLY a valid JSON object with 'score' (integer), 'reasoning' (string), and 'improvement_tips' (array of objects with 'tip' and 'priority' fields).
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw ATS response: {response.text}")  # Debug log
#         try:
#             result = json.loads(response.text)
#             if not all(k in result for k in ['score', 'reasoning', 'improvement_tips']):
#                 result = {
#                     'score': 80,
#                     'reasoning': 'Default reasoning due to invalid response format',
#                     'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#                 }
#         except json.JSONDecodeError:
#             result = {
#                 'score': 80,
#                 'reasoning': 'Default reasoning due to JSON parsing error',
#                 'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#             }
#         score_history.append({
#             'user_id': user_id,
#             'ats_score': result['score'],
#             'timestamp': pd.Timestamp.now().isoformat()
#         })
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Return ONLY a valid JSON object with a 'tips' array, where each tip has 'category', 'tip', and 'priority' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw improvement tips response: {response.text}")  # Debug log
#         try:
#             tips = json.loads(response.text)
#             if 'tips' not in tips or not isinstance(tips['tips'], list):
#                 tips = {'tips': [{'category': 'General', 'tip': 'No specific tips identified', 'priority': 'Low'}]}
#         except json.JSONDecodeError:
#             tips = {'tips': [{'category': 'General', 'tip': 'Failed to parse tips', 'priority': 'Low'}]}
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Return ONLY a valid JSON object with 'similarity_percentage' (integer), 'missing_keywords' (array of strings), and 'strengths' (array of strings) fields.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw role alignment response: {response.text}")  # Debug log
#         try:
#             result = json.loads(response.text)
#             if not all(k in result for k in ['similarity_percentage', 'missing_keywords', 'strengths']):
#                 result = {
#                     'similarity_percentage': 50,
#                     'missing_keywords': [],
#                     'strengths': []
#                 }
#         except json.JSONDecodeError:
#             result = {'similarity_percentage': 50, 'missing_keywords': [], 'strengths': []}
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Extract skills from the resume text and compare them with the following top skills: {', '.join(all_skills)}.
#         Return ONLY a valid JSON object with 'user_skills' (array of strings), 'top_skills' (array of strings), 'missing_skills' (array of strings), and 'recommendation' (string) fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw skill gap response: {response.text}")  # Debug log
#         try:
#             result = json.loads(response.text)
#             if not all(k in result for k in ['user_skills', 'top_skills', 'missing_skills', 'recommendation']):
#                 result = {
#                     'user_skills': [],
#                     'top_skills': all_skills,
#                     'missing_skills': [],
#                     'recommendation': 'Please review your skills alignment'
#                 }
#             if not result.get('missing_skills'):
#                 result['missing_skills'] = [skill for skill in all_skills if skill not in result.get('user_skills', [])]
#                 result['recommendation'] = f"Consider learning: {', '.join(result['missing_skills'][:3])}" if result['missing_skills'] else "Your skills are well-aligned."
#         except json.JSONDecodeError:
#             result = {
#                 'user_skills': [],
#                 'top_skills': all_skills,
#                 'missing_skills': all_skills,
#                 'recommendation': 'Consider learning more skills'
#             }
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
#         if features.shape[1] != expected_features:
#             print(f"Feature mismatch - Expected: {expected_features}, Got: {features.shape[1]}, Features: {features}")
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         print(f"Prediction input: {features}, Probability: {probability}, Raw resume text: {resume_text[:500]}")  # Extended debug
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit.
#         Return ONLY a valid JSON object with a 'companies' array, where each company has 'name' (string) and 'reason' (string) fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw recommend companies response: {response.text}")  # Debug log
#         try:
#             companies = json.loads(response.text)
#             if 'companies' not in companies or not isinstance(companies['companies'], list):
#                 companies = {'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]}
#         except json.JSONDecodeError:
#             companies = {'companies': [{'name': 'Default Company', 'reason': 'Failed to parse recommendations'}]}
#         return jsonify(companies)
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a 'roadmap' array, where each step has 'step' (integer), 'description' (string), and 'estimated_time' (string) fields.
#         """
#         response = model.generate_content(prompt)
#         try:
#             roadmap = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]
#             }
#             if 'roadmap' not in roadmap:
#                 roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         except json.JSONDecodeError:
#             roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         return jsonify(roadmap)
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)


# cinnamon roll version 

# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.tokenize import word_tokenize
# import json

# # Fallback stopwords list
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# # Download NLTK data
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('punkt_tab', quiet=True)
#     print("NLTK data downloaded successfully: punkt, punkt_tab")
# except Exception as e:
#     print(f"Error downloading NLTK data: {e}")

# # Initialize Gemini API
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available Gemini models: {available_models}")
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# # Load models and vectorizer
# try:
#     selection_model = joblib.load('selection_model.pkl')
#     salary_model = joblib.load('salary_model.pkl')
#     tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
#     resume_data = pd.read_csv('resume_screening.csv')
# except Exception as e:
#     print(f"Error loading models or data: {e}")

# # In-memory score history
# score_history = []

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity.
#         Provide a brief reasoning for the score and 2-3 specific improvement tips to enhance ATS compatibility.
#         Return ONLY a valid JSON object with 'score' (integer), 'reasoning' (string), and 'improvement_tips' (array of objects with 'tip' and 'priority' fields).
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw ATS response: {response.text}")  # Debug log
#         try:
#             result = json.loads(response.text)
#             if not all(k in result for k in ['score', 'reasoning', 'improvement_tips']):
#                 result = {
#                     'score': 80,
#                     'reasoning': 'Default reasoning due to invalid response format',
#                     'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#                 }
#         except json.JSONDecodeError:
#             result = {
#                 'score': 80,
#                 'reasoning': 'Default reasoning due to JSON parsing error',
#                 'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#             }
#         score_history.append({
#             'user_id': user_id,
#             'ats_score': result['score'],
#             'timestamp': pd.Timestamp.now().isoformat()
#         })
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Return ONLY a valid JSON object with a 'tips' array, where each tip has 'category', 'tip', and 'priority' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw improvement tips response: {response.text}")  # Debug log
#         try:
#             tips = json.loads(response.text)
#             if 'tips' not in tips or not isinstance(tips['tips'], list):
#                 tips = {'tips': [{'category': 'General', 'tip': 'No specific tips identified', 'priority': 'Low'}]}
#         except json.JSONDecodeError:
#             tips = {'tips': [{'category': 'General', 'tip': 'Failed to parse tips', 'priority': 'Low'}]}
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Return ONLY a valid JSON object with 'similarity_percentage' (integer), 'missing_keywords' (array of strings), and 'strengths' (array of strings) fields.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw role alignment response: {response.text}")  # Debug log
#         try:
#             result = json.loads(response.text)
#             if not all(k in result for k in ['similarity_percentage', 'missing_keywords', 'strengths']):
#                 result = {
#                     'similarity_percentage': 50,
#                     'missing_keywords': [],
#                     'strengths': []
#                 }
#         except json.JSONDecodeError:
#             result = {'similarity_percentage': 50, 'missing_keywords': [], 'strengths': []}
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Extract skills from the resume text and compare them with the following top skills: {', '.join(all_skills)}.
#         Return ONLY a valid JSON object with 'user_skills' (array of strings), 'top_skills' (array of strings), 'missing_skills' (array of strings), and 'recommendation' (string) fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw skill gap response: {response.text}")  # Debug log
#         try:
#             result = json.loads(response.text)
#             if not all(k in result for k in ['user_skills', 'top_skills', 'missing_skills', 'recommendation']):
#                 result = {
#                     'user_skills': [],
#                     'top_skills': all_skills,
#                     'missing_skills': [],
#                     'recommendation': 'Please review your skills alignment'
#                 }
#             if not result.get('missing_skills'):
#                 result['missing_skills'] = [skill for skill in all_skills if skill not in result.get('user_skills', [])]
#                 result['recommendation'] = f"Consider learning: {', '.join(result['missing_skills'][:3])}" if result['missing_skills'] else "Your skills are well-aligned."
#         except json.JSONDecodeError:
#             result = {
#                 'user_skills': [],
#                 'top_skills': all_skills,
#                 'missing_skills': all_skills,
#                 'recommendation': 'Consider learning more skills'
#             }
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
#         if features.shape[1] != expected_features:
#             print(f"Feature mismatch - Expected: {expected_features}, Got: {features.shape[1]}, Features: {features}")
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         print(f"Prediction input: {features}, Probability: {probability}, Raw resume text: {resume_text[:500]}")  # Extended debug
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit.
#         Return ONLY a valid JSON object with a 'companies' array, where each company has 'name' (string) and 'reason' (string) fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw recommend companies response: {response.text}")  # Debug log
#         try:
#             companies = json.loads(response.text)
#             if 'companies' not in companies or not isinstance(companies['companies'], list):
#                 companies = {'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]}
#         except json.JSONDecodeError:
#             companies = {'companies': [{'name': 'Default Company', 'reason': 'Failed to parse recommendations'}]}
#         return jsonify(companies)
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a 'roadmap' array, where each step has 'step' (integer), 'description' (string), and 'estimated_time' (string) fields.
#         """
#         response = model.generate_content(prompt)
#         try:
#             roadmap = json.loads(response.text) if response.text.strip().startswith('{') else {
#                 'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]
#             }
#             if 'roadmap' not in roadmap:
#                 roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         except json.JSONDecodeError:
#             roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         return jsonify(roadmap)
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# # New endpoint for popular roles
# @app.route('/api/roadmap/popular-roles', methods=['GET'])
# def popular_roles():
#     try:
#         # Hardcoded list of popular roles (can be expanded or generated dynamically)
#         popular_roles = [
#             {"role": "Software Engineer", "demand": "High"},
#             {"role": "Data Scientist", "demand": "High"},
#             {"role": "Machine Learning Engineer", "demand": "Medium"},
#             {"role": "DevOps Engineer", "demand": "Medium"},
#             {"role": "Product Manager", "demand": "High"}
#         ]
#         return jsonify({"popular_roles": popular_roles})
#     except Exception as e:
#         print(f"Error in /api/roadmap/popular-roles: {e}")
#         return jsonify({"error": f"Failed to fetch popular roles: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)

#and i just cant believe we aint together
# import os
# import re
# import nltk
# import joblib
# import numpy as np
# import pandas as pd
# import pdfplumber
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from dotenv import load_dotenv
# import google.generativeai as genai
# from nltk.tokenize import word_tokenize
# import json

# # Fallback stopwords list
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# # Download NLTK data
# try:
#     nltk.download('punkt', quiet=True)
#     nltk.download('punkt_tab', quiet=True)
#     print("NLTK data downloaded successfully: punkt, punkt_tab")
# except Exception as e:
#     print(f"Error downloading NLTK data: {e}")

# # Initialize Gemini API
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available Gemini models: {available_models}")
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# # Load models and vectorizer
# try:
#     selection_model = joblib.load('selection_model.pkl')
#     salary_model = joblib.load('salary_model.pkl')
#     tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
#     resume_data = pd.read_csv('resume_screening.csv')
# except Exception as e:
#     print(f"Error loading models or data: {e}")

# # In-memory score history
# score_history = []

# def extract_json_from_response(text):
#     """
#     Extract JSON from Gemini response that may be wrapped in markdown code blocks.
#     """
#     # Remove markdown code blocks if present
#     text = text.strip()
    
#     # Try to find JSON within ```json ... ``` blocks
#     json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
#     if json_match:
#         text = json_match.group(1)
#     else:
#         # Try to find JSON within ``` ... ``` blocks
#         json_match = re.search(r'```\s*(\{.*?\})\s*```', text, re.DOTALL)
#         if json_match:
#             text = json_match.group(1)
    
#     # If text starts with { and ends with }, it's likely JSON
#     if text.startswith('{') and text.endswith('}'):
#         return text
    
#     # Try to find any JSON object in the text
#     json_match = re.search(r'\{.*\}', text, re.DOTALL)
#     if json_match:
#         return json_match.group(0)
    
#     return text

# def extract_text_from_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             text = ''
#             for page in pdf.pages:
#                 text += page.extract_text() or ''
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ''

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the Resume Screening API"})

# @app.route('/api/ats-score', methods=['POST'])
# def ats_score():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         user_id = request.form.get('user_id', 'default_user')

#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity.
#         Provide a brief reasoning for the score and 2-3 specific improvement tips to enhance ATS compatibility.
#         Return ONLY a valid JSON object with 'score' (integer), 'reasoning' (string), and 'improvement_tips' (array of objects with 'tip' and 'priority' fields).
#         Resume: {processed_resume}
#         Job Description: {job_description if job_description else 'Not provided'}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw ATS response: {response.text}")  # Debug log
        
#         try:
#             # Extract JSON from markdown code blocks
#             json_text = extract_json_from_response(response.text)
#             result = json.loads(json_text)
            
#             # Validate required fields
#             if not all(k in result for k in ['score', 'reasoning', 'improvement_tips']):
#                 result = {
#                     'score': 80,
#                     'reasoning': 'Default reasoning due to invalid response format',
#                     'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#                 }
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             result = {
#                 'score': 80,
#                 'reasoning': 'Default reasoning due to JSON parsing error',
#                 'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
#             }
        
#         score_history.append({
#             'user_id': user_id,
#             'ats_score': result['score'],
#             'timestamp': pd.Timestamp.now().isoformat()
#         })
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/ats-score: {e}")
#         return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

# @app.route('/api/improvement-tips', methods=['POST'])
# def improvement_tips():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
#         Return ONLY a valid JSON object with a 'tips' array, where each tip has 'category', 'tip', and 'priority' fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw improvement tips response: {response.text}")  # Debug log
        
#         try:
#             json_text = extract_json_from_response(response.text)
#             tips = json.loads(json_text)
#             if 'tips' not in tips or not isinstance(tips['tips'], list):
#                 tips = {'tips': [{'category': 'General', 'tip': 'No specific tips identified', 'priority': 'Low'}]}
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             tips = {'tips': [{'category': 'General', 'tip': 'Failed to parse tips', 'priority': 'Low'}]}
        
#         return jsonify(tips)
#     except Exception as e:
#         print(f"Error in /api/improvement-tips: {e}")
#         return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

# @app.route('/api/role-alignment', methods=['POST'])
# def role_alignment():
#     try:
#         resume = request.files.get('resume')
#         job_description = request.form.get('job_description', '')
#         if not resume or not job_description:
#             return jsonify({"error": "Resume and job description required"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         processed_job = preprocess_text(job_description)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
#         Return ONLY a valid JSON object with 'similarity_percentage' (integer), 'missing_keywords' (array of strings), and 'strengths' (array of strings) fields.
#         Resume: {processed_resume}
#         Job Description: {processed_job}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw role alignment response: {response.text}")  # Debug log
        
#         try:
#             json_text = extract_json_from_response(response.text)
#             result = json.loads(json_text)
#             if not all(k in result for k in ['similarity_percentage', 'missing_keywords', 'strengths']):
#                 result = {
#                     'similarity_percentage': 50,
#                     'missing_keywords': [],
#                     'strengths': []
#                 }
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             result = {'similarity_percentage': 50, 'missing_keywords': [], 'strengths': []}
        
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/role-alignment: {e}")
#         return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

# @app.route('/api/skill-gap', methods=['POST'])
# def skill_gap():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Extract skills from the resume text and compare them with the following top skills: {', '.join(all_skills)}.
#         Return ONLY a valid JSON object with 'user_skills' (array of strings), 'top_skills' (array of strings), 'missing_skills' (array of strings), and 'recommendation' (string) fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw skill gap response: {response.text}")  # Debug log
        
#         try:
#             json_text = extract_json_from_response(response.text)
#             result = json.loads(json_text)
#             if not all(k in result for k in ['user_skills', 'top_skills', 'missing_skills', 'recommendation']):
#                 result = {
#                     'user_skills': [],
#                     'top_skills': all_skills,
#                     'missing_skills': [],
#                     'recommendation': 'Please review your skills alignment'
#                 }
#             if not result.get('missing_skills'):
#                 result['missing_skills'] = [skill for skill in all_skills if skill not in result.get('user_skills', [])]
#                 result['recommendation'] = f"Consider learning: {', '.join(result['missing_skills'][:3])}" if result['missing_skills'] else "Your skills are well-aligned."
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             result = {
#                 'user_skills': [],
#                 'top_skills': all_skills,
#                 'missing_skills': all_skills,
#                 'recommendation': 'Consider learning more skills'
#             }
        
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error in /api/skill-gap: {e}")
#         return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

# @app.route('/api/predict-selection', methods=['POST'])
# def predict_selection():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
#         skill_count = len(processed_resume.split())
#         features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
#         expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
#         if features.shape[1] != expected_features:
#             print(f"Feature mismatch - Expected: {expected_features}, Got: {features.shape[1]}, Features: {features}")
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         probability = selection_model.predict_proba(features)[0][1] * 100
#         print(f"Prediction input: {features}, Probability: {probability}, Raw resume text: {resume_text[:500]}")  # Extended debug
#         return jsonify({"selection_probability": round(probability, 2)})
#     except Exception as e:
#         print(f"Error in /api/predict-selection: {e}")
#         return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

# @app.route('/api/salary-estimate', methods=['POST'])
# def salary_estimate():
#     try:
#         resume = request.files.get('resume')
#         experience_years = request.form.get('experience_years')
#         if not resume or not experience_years:
#             return jsonify({"error": "Resume and experience years required"}), 400

#         try:
#             experience_years = float(experience_years)
#         except ValueError:
#             return jsonify({"error": "Invalid experience years"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         skill_count = len(processed_resume.split())
#         features = np.array([[experience_years, skill_count]])
#         expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
#         if features.shape[1] != expected_features:
#             raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
#         estimated_salary = salary_model.predict(features)[0]
#         return jsonify({"estimated_salary": round(estimated_salary, 2)})
#     except Exception as e:
#         print(f"Error in /api/salary-estimate: {e}")
#         return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

# @app.route('/api/recommend-companies', methods=['POST'])
# def recommend_companies():
#     try:
#         resume = request.files.get('resume')
#         if not resume:
#             return jsonify({"error": "No resume uploaded"}), 400

#         resume_text = extract_text_from_pdf(resume)
#         if not resume_text:
#             return jsonify({"error": "Failed to extract text from resume"}), 400

#         processed_resume = preprocess_text(resume_text)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Based on the resume text, recommend 3-5 companies that would be a good fit.
#         Return ONLY a valid JSON object with a 'companies' array, where each company has 'name' (string) and 'reason' (string) fields.
#         Resume: {processed_resume}
#         """
#         response = model.generate_content(prompt)
#         print(f"Raw recommend companies response: {response.text}")  # Debug log
        
#         try:
#             json_text = extract_json_from_response(response.text)
#             companies = json.loads(json_text)
#             if 'companies' not in companies or not isinstance(companies['companies'], list):
#                 companies = {'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]}
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             companies = {'companies': [{'name': 'Default Company', 'reason': 'Failed to parse recommendations'}]}
        
#         return jsonify(companies)
#     except Exception as e:
#         print(f"Error in /api/recommend-companies: {e}")
#         return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

# @app.route('/api/score-history', methods=['GET'])
# def score_history_endpoint():
#     try:
#         user_id = request.args.get('user_id', 'default_user')
#         user_history = [entry for entry in score_history if entry['user_id'] == user_id]
#         return jsonify({"score_history": user_history})
#     except Exception as e:
#         print(f"Error in /api/score-history: {e}")
#         return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

# @app.route('/api/roadmap', methods=['POST'])
# def roadmap():
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id', 'default_user')
#         skills = data.get('skills', [])
#         if not skills:
#             return jsonify({"error": "No skills provided"}), 400

#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = f"""
#         Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
#         Provide a JSON response with a 'roadmap' array, where each step has 'step' (integer), 'description' (string), and 'estimated_time' (string) fields.
#         """
#         response = model.generate_content(prompt)
        
#         try:
#             json_text = extract_json_from_response(response.text)
#             roadmap = json.loads(json_text)
#             if 'roadmap' not in roadmap:
#                 roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
        
#         return jsonify(roadmap)
#     except Exception as e:
#         print(f"Error in /api/roadmap: {e}")
#         return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

# @app.route('/api/roadmap/popular-roles', methods=['GET'])
# def popular_roles():
#     try:
#         popular_roles = [
#             {"role": "Software Engineer", "demand": "High"},
#             {"role": "Data Scientist", "demand": "High"},
#             {"role": "Machine Learning Engineer", "demand": "Medium"},
#             {"role": "DevOps Engineer", "demand": "Medium"},
#             {"role": "Product Manager", "demand": "High"}
#         ]
#         return jsonify({"popular_roles": popular_roles})
#     except Exception as e:
#         print(f"Error in /api/roadmap/popular-roles: {e}")
#         return jsonify({"error": f"Failed to fetch popular roles: {str(e)}"}), 500

# if __name__ == '__main__':
#     print("🚀 Starting Study Assistant API...")
#     print(f"🌐 Server running on http://localhost:5000")
#     app.run(debug=True, port=5000)

#and just shake me till you wake me from this bad dream

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import joblib
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import google.generativeai as genai
from dotenv import load_dotenv
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import json
import re
from io import BytesIO
import numpy as np
# Import new modules for roadmap features
from database import DatabaseManager
from roadmap_generator import RoadmapGenerator
from resource_finder import ResourceFinder
from resume_analyzer import ResumeAnalyzer

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - Allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Fallback stopwords list
FALLBACK_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', 'should', 'now'
}

# NLTK setup
nltk.download('stopwords', quiet=True)
try:
    stop = set(stopwords.words('english'))
except Exception:
    print("Warning: NLTK stopwords not available")
    stop = FALLBACK_STOPWORDS

# Download NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    print("NLTK data downloaded successfully: punkt, punkt_tab")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

# Load existing model
try:
    model1 = joblib.load('resume_model.pkl')
except FileNotFoundError:
    print("Error: resume_model.pkl not found. Run train_model.py first.")
    model1 = None

# Load models and vectorizer
try:
    selection_model = joblib.load('selection_model.pkl')
    salary_model = joblib.load('salary_model.pkl')
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
    resume_data = pd.read_csv('resume_screening.csv')
except Exception as e:
    print(f"Error loading models or data: {e}")

score_history = []

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize new components for roadmap features
db_manager = DatabaseManager()
roadmap_generator = RoadmapGenerator(os.getenv('GEMINI_API_KEY'))
resource_finder = ResourceFinder()
resume_analyzer = ResumeAnalyzer(os.getenv('GEMINI_API_KEY'))

# ===================== EXISTING ROUTES =====================

def extract_json_from_response(text):
    """
    Extract JSON from Gemini response that may be wrapped in markdown code blocks.
    """
    text = text.strip()
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1)
    else:
        json_match = re.search(r'```\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
   
    if text.startswith('{') and text.endswith('}'):
        return text
   
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
   
    return text

def extract_text_from_pdf(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ''

def preprocess_text(text):
    try:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text)
        stop_words = FALLBACK_STOPWORDS
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    except Exception as e:
        print(f"Error in preprocess_text: {e}")
        raise

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Resume Screening API"})

@app.route('/api/ats-score', methods=['POST'])
def ats_score():
    try:
        resume = request.files.get('resume')
        job_description = request.form.get('job_description', '')
        user_id = request.form.get('user_id', 'default_user')

        if not resume:
            return jsonify({"error": "No resume uploaded"}), 400

        resume_text = extract_text_from_pdf(resume)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 400

        processed_resume = preprocess_text(resume_text)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Evaluate the following resume text for ATS compatibility and assign a score out of 100 based on keyword relevance, formatting, and clarity.
        Provide a brief reasoning for the score and 2-3 specific improvement tips to enhance ATS compatibility.
        Return ONLY a valid JSON object with 'score' (integer), 'reasoning' (string), and 'improvement_tips' (array of objects with 'tip' and 'priority' fields).
        Resume: {processed_resume}
        Job Description: {job_description if job_description else 'Not provided'}
        """
        response = model.generate_content(prompt)
        print(f"Raw ATS response: {response.text}")  # Debug log
       
        try:
            json_text = extract_json_from_response(response.text)
            result = json.loads(json_text)
            if not all(k in result for k in ['score', 'reasoning', 'improvement_tips']):
                result = {
                    'score': 80,
                    'reasoning': 'Default reasoning due to invalid response format',
                    'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
                }
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            result = {
                'score': 80,
                'reasoning': 'Default reasoning due to JSON parsing error',
                'improvement_tips': [{'tip': 'Add relevant keywords', 'priority': 'High'}]
            }
       
        score_history.append({
            'user_id': user_id,
            'ats_score': result['score'],
            'timestamp': pd.Timestamp.now().isoformat()
        })
        return jsonify(result)
    except Exception as e:
        print(f"Error in /api/ats-score: {e}")
        return jsonify({"error": f"Failed to process ATS score: {str(e)}"}), 500

@app.route('/api/improvement-tips', methods=['POST'])
def improvement_tips():
    try:
        resume = request.files.get('resume')
        if not resume:
            return jsonify({"error": "No resume uploaded"}), 400

        resume_text = extract_text_from_pdf(resume)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 400

        processed_resume = preprocess_text(resume_text)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Analyze the following resume text and provide a list of improvement tips with categories (e.g., Formatting, Keywords, Content) and priority (High, Medium, Low).
        Return ONLY a valid JSON object with a 'tips' array, where each tip has 'category', 'tip', and 'priority' fields.
        Resume: {processed_resume}
        """
        response = model.generate_content(prompt)
        print(f"Raw improvement tips response: {response.text}")  # Debug log
       
        try:
            json_text = extract_json_from_response(response.text)
            tips = json.loads(json_text)
            if 'tips' not in tips or not isinstance(tips['tips'], list):
                tips = {'tips': [{'category': 'General', 'tip': 'No specific tips identified', 'priority': 'Low'}]}
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            tips = {'tips': [{'category': 'General', 'tip': 'Failed to parse tips', 'priority': 'Low'}]}
       
        return jsonify(tips)
    except Exception as e:
        print(f"Error in /api/improvement-tips: {e}")
        return jsonify({"error": f"Failed to process improvement tips: {str(e)}"}), 500

@app.route('/api/role-alignment', methods=['POST'])
def role_alignment():
    try:
        resume = request.files.get('resume')
        job_description = request.form.get('job_description', '')
        if not resume or not job_description:
            return jsonify({"error": "Resume and job description required"}), 400

        resume_text = extract_text_from_pdf(resume)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 400

        processed_resume = preprocess_text(resume_text)
        processed_job = preprocess_text(job_description)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Compare the resume text with the job description and calculate a similarity percentage (0-100). Identify missing keywords and strengths.
        Return ONLY a valid JSON object with 'similarity_percentage' (integer), 'missing_keywords' (array of strings), and 'strengths' (array of strings) fields.
        Resume: {processed_resume}
        Job Description: {processed_job}
        """
        response = model.generate_content(prompt)
        print(f"Raw role alignment response: {response.text}")  # Debug log
       
        try:
            json_text = extract_json_from_response(response.text)
            result = json.loads(json_text)
            if not all(k in result for k in ['similarity_percentage', 'missing_keywords', 'strengths']):
                result = {
                    'similarity_percentage': 50,
                    'missing_keywords': [],
                    'strengths': []
                }
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            result = {'similarity_percentage': 50, 'missing_keywords': [], 'strengths': []}
       
        return jsonify(result)
    except Exception as e:
        print(f"Error in /api/role-alignment: {e}")
        return jsonify({"error": f"Failed to process role alignment: {str(e)}"}), 500

@app.route('/api/skill-gap', methods=['POST'])
def skill_gap():
    try:
        resume = request.files.get('resume')
        if not resume:
            return jsonify({"error": "No resume uploaded"}), 400

        resume_text = extract_text_from_pdf(resume)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 400

        processed_resume = preprocess_text(resume_text)
        all_skills = resume_data['Skills'].str.split(', ').explode().value_counts().head(10).index.tolist()
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Extract skills from the resume text and compare them with the following top skills: {', '.join(all_skills)}.
        Return ONLY a valid JSON object with 'user_skills' (array of strings), 'top_skills' (array of strings), 'missing_skills' (array of strings), and 'recommendation' (string) fields.
        Resume: {processed_resume}
        """
        response = model.generate_content(prompt)
        print(f"Raw skill gap response: {response.text}")  # Debug log
       
        try:
            json_text = extract_json_from_response(response.text)
            result = json.loads(json_text)
            if not all(k in result for k in ['user_skills', 'top_skills', 'missing_skills', 'recommendation']):
                result = {
                    'user_skills': [],
                    'top_skills': all_skills,
                    'missing_skills': [],
                    'recommendation': 'Please review your skills alignment'
                }
            if not result.get('missing_skills'):
                result['missing_skills'] = [skill for skill in all_skills if skill not in result.get('user_skills', [])]
            result['recommendation'] = f"Consider learning: {', '.join(result['missing_skills'][:3])}" if result['missing_skills'] else "Your skills are well-aligned."
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            result = {
                'user_skills': [],
                'top_skills': all_skills,
                'missing_skills': all_skills,
                'recommendation': 'Consider learning more skills'
            }
       
        return jsonify(result)
    except Exception as e:
        print(f"Error in /api/skill-gap: {e}")
        return jsonify({"error": f"Failed to process skill gap: {str(e)}"}), 500

@app.route('/api/predict-selection', methods=['POST'])
def predict_selection():
    try:
        resume = request.files.get('resume')
        experience_years = request.form.get('experience_years')
        if not resume or not experience_years:
            return jsonify({"error": "Resume and experience years required"}), 400

        try:
            experience_years = float(experience_years)
        except ValueError:
            return jsonify({"error": "Invalid experience years"}), 400

        resume_text = extract_text_from_pdf(resume)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 400

        processed_resume = preprocess_text(resume_text)
        tfidf_matrix = tfidf_vectorizer.transform([processed_resume])
        skill_count = len(processed_resume.split())
        features = np.hstack([tfidf_matrix.toarray(), [[experience_years, skill_count]]])
        expected_features = selection_model.n_features_in_ if hasattr(selection_model, 'n_features_in_') else 17
        if features.shape[1] != expected_features:
            print(f"Feature mismatch - Expected: {expected_features}, Got: {features.shape[1]}, Features: {features}")
            raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
        probability = selection_model.predict_proba(features)[0][1] * 100
        print(f"Prediction input: {features}, Probability: {probability}, Raw resume text: {resume_text[:500]}")  # Extended debug
        return jsonify({"selection_probability": round(probability, 2)})
    except Exception as e:
        print(f"Error in /api/predict-selection: {e}")
        return jsonify({"error": f"Failed to predict selection: {str(e)}"}), 500

@app.route('/api/salary-estimate', methods=['POST'])
def salary_estimate():
    try:
        resume = request.files.get('resume')
        experience_years = request.form.get('experience_years')
        if not resume or not experience_years:
            return jsonify({"error": "Resume and experience years required"}), 400

        try:
            experience_years = float(experience_years)
        except ValueError:
            return jsonify({"error": "Invalid experience years"}), 400

        resume_text = extract_text_from_pdf(resume)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 400

        processed_resume = preprocess_text(resume_text)
        skill_count = len(processed_resume.split())
        features = np.array([[experience_years, skill_count]])
        expected_features = salary_model.n_features_in_ if hasattr(salary_model, 'n_features_in_') else 2
        if features.shape[1] != expected_features:
            raise ValueError(f"Feature mismatch: Expected {expected_features} features, got {features.shape[1]}")
        estimated_salary = salary_model.predict(features)[0]
        return jsonify({"estimated_salary": round(estimated_salary, 2)})
    except Exception as e:
        print(f"Error in /api/salary-estimate: {e}")
        return jsonify({"error": f"Failed to estimate salary: {str(e)}"}), 500

@app.route('/api/recommend-companies', methods=['POST'])
def recommend_companies():
    try:
        resume = request.files.get('resume')
        if not resume:
            return jsonify({"error": "No resume uploaded"}), 400

        resume_text = extract_text_from_pdf(resume)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 400

        processed_resume = preprocess_text(resume_text)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Based on the resume text, recommend 3-5 companies that would be a good fit.
        Return ONLY a valid JSON object with a 'companies' array, where each company has 'name' (string) and 'reason' (string) fields.
        Resume: {processed_resume}
        """
        response = model.generate_content(prompt)
        print(f"Raw recommend companies response: {response.text}")  # Debug log
       
        try:
            json_text = extract_json_from_response(response.text)
            companies = json.loads(json_text)
            if 'companies' not in companies or not isinstance(companies['companies'], list):
                companies = {'companies': [{'name': 'Default Company', 'reason': 'No specific match'}]}
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            companies = {'companies': [{'name': 'Default Company', 'reason': 'Failed to parse recommendations'}]}
       
        return jsonify(companies)
    except Exception as e:
        print(f"Error in /api/recommend-companies: {e}")
        return jsonify({"error": f"Failed to recommend companies: {str(e)}"}), 500

@app.route('/api/score-history', methods=['GET'])
def score_history_endpoint():
    try:
        user_id = request.args.get('user_id', 'default_user')
        user_history = [entry for entry in score_history if entry['user_id'] == user_id]
        return jsonify({"score_history": user_history})
    except Exception as e:
        print(f"Error in /api/score-history: {e}")
        return jsonify({"error": f"Failed to retrieve score history: {str(e)}"}), 500

@app.route('/api/roadmap', methods=['POST'])
def roadmap():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        skills = data.get('skills', [])
        if not skills:
            return jsonify({"error": "No skills provided"}), 400

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Create a personalized learning roadmap for a user to acquire the following skills: {', '.join(skills)}.
        Provide a JSON response with a 'roadmap' array, where each step has 'step' (integer), 'description' (string), and 'estimated_time' (string) fields.
        """
        response = model.generate_content(prompt)
       
        try:
            json_text = extract_json_from_response(response.text)
            roadmap = json.loads(json_text)
            if 'roadmap' not in roadmap:
                roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            roadmap = {'roadmap': [{'step': 1, 'description': 'Learn basics', 'estimated_time': '1 month'}]}
       
        return jsonify(roadmap)
    except Exception as e:
        print(f"Error in /api/roadmap: {e}")
        return jsonify({"error": f"Failed to generate roadmap: {str(e)}"}), 500

@app.route('/api/roadmap/popular-roles', methods=['GET'])
def popular_roles():
    try:
        popular_roles = [
            {"role": "Software Engineer", "demand": "High"},
            {"role": "Data Scientist", "demand": "High"},
            {"role": "Machine Learning Engineer", "demand": "Medium"},
            {"role": "DevOps Engineer", "demand": "Medium"},
            {"role": "Product Manager", "demand": "High"}
        ]
        return jsonify({"popular_roles": popular_roles})
    except Exception as e:
        print(f"Error in /api/roadmap/popular-roles: {e}")
        return jsonify({"error": f"Failed to fetch popular roles: {str(e)}"}), 500

@app.route('/predict', methods=['POST'])
def predict():
    if not model1:
        return jsonify({'error': 'Model not loaded'}), 500

    file = request.files['resume']
    experience_years = float(request.form.get('experience_years', 0))
    projects_count = int(request.form.get('projects_count', 0))
    salary_expectation = float(request.form.get('salary_expectation', 0))

    with pdfplumber.open(file) as pdf:
        resume_text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())

    cleaned_text = resume_text.lower()
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
    cleaned_text = ' '.join(word for word in cleaned_text.split() if word not in FALLBACK_STOPWORDS)

    input_data = pd.DataFrame({
        'Text': [cleaned_text],
        'Experience (Years)': [experience_years],
        'Projects Count': [projects_count],
        'Salary Expectation ($)': [salary_expectation]
    })

    prob = model1.predict_proba(input_data)[0][1] * 100
    return jsonify({'chance': prob})

def extract_contact_info(resume_text):
    name = resume_text.split("\n")[0].strip()
    email = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
    phone = re.search(r'\b\d{10}\b', resume_text)
    linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/[^\s]+', resume_text)
    github = re.search(r'(https?://)?(www\.)?github\.com/[^\s]+', resume_text)

    return {
        "name": name,
        "email": email.group() if email else "",
        "phone": phone.group() if phone else "",
        "linkedin": linkedin.group() if linkedin else "",
        "github": github.group() if github else ""
    }

@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover():
    try:
        job_desc = request.form['job_desc']
        hr_name = request.form['hr_name']
        resume_file = request.files['resume_file']

        with pdfplumber.open(resume_file) as pdf:
            resume_text = ' '.join(page.extract_text() or '' for page in pdf.pages)

        contact_info = extract_contact_info(resume_text)

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Write a professional cover letter for this job: {job_desc}.
        Address it to {hr_name}.
        Incorporate details from this resume: {resume_text}.
        Important: Do NOT include headers like [Your Name], [Your Address], [Date],
        or any placeholder personal/contact information at the top.
        Start directly with the greeting (e.g., 'Dear {hr_name},').
        Do NOT include placeholders such as [Platform where you saw the advertisement],
        [Address], or any square-bracketed text.
        Do NOT fabricate details not present in the resume or job description.
        End with a professional closing (e.g., "Sincerely, {contact_info['name']}") including my name and contact info.
        """

        cover_text = ""
        response = model.generate_content(prompt)
        try:
            if response and hasattr(response, "text"):
                cover_text = response.text
            elif response and hasattr(response, "candidates"):
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if part.text:
                            cover_text += part.text + "\n"
            else:
                raise Exception("No valid response from API")
        except Exception as e:
            print(f"Error parsing API response: {e}")
            raise Exception("API returned invalid response")

        if not cover_text.strip():
            raise Exception("API returned empty text")

        return jsonify({'cover_letter': cover_text.strip()})

    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return jsonify({'error': f'Failed to generate cover letter: {str(e)}'}), 500

def safe_parse_json(data_str):
    """Safely parse JSON string, return empty list if parsing fails"""
    if not data_str:
        return []
    try:
        parsed = json.loads(data_str)
        return parsed if isinstance(parsed, list) else []
    except (json.JSONDecodeError, TypeError):
        return []

@app.route('/api/resume/create', methods=['POST'])
def generate_resume():
    try:
        if request.content_type and 'multipart/form-data' in request.content_type:
            data = {}
            for key in request.form:
                if key in ['workExperience', 'education', 'projects', 'certifications', 'achievements']:
                    data[key] = safe_parse_json(request.form[key])
                else:
                    data[key] = request.form[key]
            photo_file = request.files.get('photo')
        else:
            data = request.json or {}
            photo_file = None

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            alignment=1,
            textColor='#2C5AA0'
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor='#1F4788',
            borderWidth=1,
            borderColor='#1F4788',
            borderPadding=4
        )
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.leading = 12

        content = []

        if data.get('fullName'):
            content.append(Paragraph(data['fullName'].upper(), title_style))
            content.append(Spacer(1, 12))

        contact_info = []
        if data.get('email'):
            contact_info.append(f"📧 {data['email']}")
        if data.get('phoneNumber'):
            contact_info.append(f"📱 {data['phoneNumber']}")
        if data.get('location'):
            contact_info.append(f"📍 {data['location']}")

        if contact_info:
            content.append(Paragraph(" | ".join(contact_info), normal_style))
            content.append(Spacer(1, 8))

        profile_links = []
        if data.get('linkedinUrl'):
            profile_links.append(f"LinkedIn: {data['linkedinUrl']}")
        if data.get('githubPortfolioUrl'):
            profile_links.append(f"Portfolio: {data['githubPortfolioUrl']}")

        if profile_links:
            content.append(Paragraph(" | ".join(profile_links), normal_style))
            content.append(Spacer(1, 12))

        if data.get('jobTitle'):
            job_title_style = ParagraphStyle(
                'JobTitle',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=8,
                alignment=1,
                textColor='#555555'
            )
            content.append(Paragraph(data['jobTitle'], job_title_style))

        if data.get('professionalSummary'):
            content.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
            content.append(Paragraph(data['professionalSummary'], normal_style))
            content.append(Spacer(1, 12))

        if data.get('technicalSkills') or data.get('softSkills'):
            content.append(Paragraph("SKILLS", heading_style))
            if data.get('technicalSkills'):
                content.append(Paragraph(f"<b>Technical Skills:</b> {data['technicalSkills']}", normal_style))
            if data.get('softSkills'):
                content.append(Paragraph(f"<b>Soft Skills:</b> {data['softSkills']}", normal_style))
            content.append(Spacer(1, 12))

        work_experience = data.get('workExperience', [])
        if work_experience and any(exp.get('jobTitle') or exp.get('companyName') for exp in work_experience):
            content.append(Paragraph("WORK EXPERIENCE", heading_style))
            for exp in work_experience:
                if exp.get('jobTitle') or exp.get('companyName'):
                    job_title = exp.get('jobTitle', 'N/A')
                    company = exp.get('companyName', 'N/A')
                    exp_header = f"<b>{job_title}</b> | {company}"
                    content.append(Paragraph(exp_header, normal_style))

                    date_info = []
                    if exp.get('startDate') or exp.get('endDate'):
                        start_date = exp.get('startDate', 'N/A')
                        end_date = exp.get('endDate', 'Present')
                        date_info.append(f"{start_date} - {end_date}")
                    if exp.get('location'):
                        date_info.append(exp.get('location'))

                    if date_info:
                        content.append(Paragraph(" | ".join(date_info), normal_style))

                    if exp.get('responsibilities'):
                        responsibilities = exp.get('responsibilities').strip()
                        if responsibilities:
                            resp_lines = [line.strip() for line in responsibilities.replace('•', '\n').split('\n') if line.strip()]
                            for line in resp_lines:
                                if line:
                                    content.append(Paragraph(f"• {line}", normal_style))

                    if exp.get('achievements'):
                        achievements = exp.get('achievements').strip()
                        if achievements:
                            ach_lines = [line.strip() for line in achievements.replace('•', '\n').split('\n') if line.strip()]
                            for line in ach_lines:
                                if line:
                                    content.append(Paragraph(f"• {line}", normal_style))

                    content.append(Spacer(1, 8))
                    content.append(Spacer(1, 4))

        education = data.get('education', [])
        if education and any(edu.get('degree') or edu.get('universityName') for edu in education):
            content.append(Paragraph("EDUCATION", heading_style))
            for edu in education:
                if edu.get('degree') or edu.get('universityName'):
                    degree = edu.get('degree', 'N/A')
                    university = edu.get('universityName', 'N/A')
                    edu_header = f"<b>{degree}</b>"
                    content.append(Paragraph(edu_header, normal_style))
                    content.append(Paragraph(university, normal_style))

                    edu_details = []
                    if edu.get('location'):
                        edu_details.append(edu.get('location'))
                    if edu.get('startDate') or edu.get('endDate'):
                        start_date = edu.get('startDate', 'N/A')
                        end_date = edu.get('endDate', 'N/A')
                        edu_details.append(f"{start_date} - {end_date}")
                    if edu.get('gpa'):
                        edu_details.append(f"GPA: {edu.get('gpa')}")

                    if edu_details:
                        content.append(Paragraph(" | ".join(edu_details), normal_style))

                    if edu.get('relevantCoursework'):
                        content.append(Paragraph(f"<b>Relevant Coursework:</b> {edu.get('relevantCoursework')}", normal_style))

                    content.append(Spacer(1, 8))
                    content.append(Spacer(1, 4))

        projects = data.get('projects', [])
        if projects and any(proj.get('projectTitle') for proj in projects):
            content.append(Paragraph("PROJECTS", heading_style))
            for proj in projects:
                if proj.get('projectTitle'):
                    content.append(Paragraph(f"<b>{proj.get('projectTitle')}</b>", normal_style))

                    if proj.get('description'):
                        content.append(Paragraph(proj.get('description'), normal_style))

                    if proj.get('technologiesUsed'):
                        content.append(Paragraph(f"<b>Technologies:</b> {proj.get('technologiesUsed')}", normal_style))

                    if proj.get('impact'):
                        content.append(Paragraph(f"<b>Impact:</b> {proj.get('impact')}", normal_style))

                    if proj.get('projectLink'):
                        content.append(Paragraph(f"<b>Link:</b> {proj.get('projectLink')}", normal_style))

                    content.append(Spacer(1, 8))
                    content.append(Spacer(1, 4))

        certifications = data.get('certifications', [])
        if certifications and any(cert.get('certificationName') for cert in certifications):
            content.append(Paragraph("CERTIFICATIONS", heading_style))
            for cert in certifications:
                if cert.get('certificationName'):
                    cert_text = f"• <b>{cert.get('certificationName')}</b>"
                    if cert.get('issuingAuthority'):
                        cert_text += f" - {cert.get('issuingAuthority')}"
                    if cert.get('date'):
                        cert_text += f" ({cert.get('date')})"
                    content.append(Paragraph(cert_text, normal_style))
                    content.append(Spacer(1, 12))

        achievements = data.get('achievements', [])
        if achievements and any(ach.get('title') for ach in achievements):
            content.append(Paragraph("ACHIEVEMENTS", heading_style))
            for ach in achievements:
                if ach.get('title'):
                    ach_text = f"• <b>{ach.get('title')}</b>"
                    if ach.get('organization'):
                        ach_text += f" - {ach.get('organization')}"
                    if ach.get('date'):
                        ach_text += f" ({ach.get('date')})"
                    content.append(Paragraph(ach_text, normal_style))
                    if ach.get('description'):
                        content.append(Paragraph(f" {ach.get('description')}", normal_style))
                    content.append(Spacer(1, 12))

        if data.get('languages'):
            content.append(Paragraph("LANGUAGES", heading_style))
            content.append(Paragraph(data['languages'], normal_style))
            content.append(Spacer(1, 8))

        if data.get('publications'):
            content.append(Paragraph("PUBLICATIONS", heading_style))
            content.append(Paragraph(data['publications'], normal_style))
            content.append(Spacer(1, 8))

        if data.get('volunteering'):
            content.append(Paragraph("VOLUNTEERING", heading_style))
            content.append(Paragraph(data['volunteering'], normal_style))
            content.append(Spacer(1, 8))

        if data.get('hobbies'):
            content.append(Paragraph("HOBBIES & INTERESTS", heading_style))
            content.append(Paragraph(data['hobbies'], normal_style))

        doc.build(content)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name='resume.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"Error generating resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate resume: {str(e)}'}), 500

# ===================== ROADMAP ROUTES =====================

@app.route('/api/roadmap/generate', methods=['POST'])
def generate_roadmap():
    """Generate a new roadmap for a job role"""
    try:
        data = request.json
        job_role = data.get('job_role')
        experience_level = data.get('experience_level', 'beginner')
        target_company = data.get('target_company')
        user_skills = data.get('user_skills', [])
        available_hours = data.get('available_hours_per_week', 10)

        if not job_role:
            return jsonify({'error': 'Job role is required'}), 400

        existing_roadmap_id, existing_roadmap = db_manager.get_roadmap(job_role)

        if existing_roadmap:
            if user_skills:
                customized_roadmap = roadmap_generator.update_roadmap_for_user(
                    existing_roadmap, user_skills, available_hours
                )
            else:
                customized_roadmap = existing_roadmap

            return jsonify({
                'roadmap_id': existing_roadmap_id,
                'roadmap': customized_roadmap,
                'message': 'Retrieved existing roadmap'
            })

        roadmap_data = roadmap_generator.generate_roadmap(
            job_role, experience_level, target_company
        )

        if user_skills:
            roadmap_data = roadmap_generator.update_roadmap_for_user(
                roadmap_data, user_skills, available_hours
            )

        roadmap_id = db_manager.save_roadmap(job_role, roadmap_data)
        roadmap_data['roadmap_id'] = roadmap_id

        return jsonify({
            'roadmap_id': roadmap_id,
            'roadmap': roadmap_data,
            'message': 'Roadmap generated successfully'
        })

    except Exception as e:
        print(f"Error generating roadmap: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

@app.route('/api/roadmap/<int:roadmap_id>/resources/<step_id>', methods=['GET'])
def get_step_resources(roadmap_id, step_id):
    """Get resources for a specific step"""
    try:
        existing_resources = db_manager.get_resources(step_id)

        if existing_resources:
            return jsonify({
                'step_id': step_id,
                'resources': existing_resources
            })

        roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
        if not roadmap_data:
            return jsonify({'error': 'Roadmap not found'}), 404

        step_data = None
        for phase in roadmap_data.get('phases', []):
            for step in phase.get('steps', []):
                if step['step_id'] == step_id:
                    step_data = step
                    break
            if step_data:
                break

        if not step_data:
            return jsonify({'error': 'Step not found'}), 404

        resources = resource_finder.get_all_resources_for_step(
            step_data['title'],
            step_data['description']
        )

        if resources:
            db_manager.save_resources(step_id, resources)

        return jsonify({
            'step_id': step_id,
            'resources': resources
        })

    except Exception as e:
        print(f"Error getting step resources: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to get resources: {str(e)}'}), 500

@app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['GET'])
def get_roadmap_progress(roadmap_id):
    """Get user progress for a roadmap"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        progress = db_manager.get_user_progress(user_id, roadmap_id)

        return jsonify({
            'roadmap_id': roadmap_id,
            'user_id': user_id,
            'progress': progress
        })

    except Exception as e:
        print(f"Error getting progress: {str(e)}")
        return jsonify({'error': f'Failed to get progress: {str(e)}'}), 500

@app.route('/api/roadmap/<int:roadmap_id>/progress', methods=['POST'])
def update_progress(roadmap_id):
    """Update user progress for a step"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')
        step_id = data.get('step_id')
        completed = data.get('completed', False)
        time_spent = data.get('time_spent', 0)

        if not step_id:
            return jsonify({'error': 'Step ID is required'}), 400

        db_manager.save_user_progress(user_id, roadmap_id, step_id, completed, time_spent)

        return jsonify({
            'message': 'Progress updated successfully',
            'roadmap_id': roadmap_id,
            'step_id': step_id,
            'completed': completed
        })

    except Exception as e:
        print(f"Error updating progress: {str(e)}")
        return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500

@app.route('/api/roadmap/popular-roles', methods=['GET'])
def get_popular_roles():
    """Get list of popular job roles for roadmap generation"""
    try:
        popular_roles = [
            {
                'id': 'software-developer',
                'title': 'Software Developer',
                'description': 'Full-stack and backend development roles',
                'avg_salary': '4-15 LPA',
                'demand': 'Very High',
                'skills': [
                    {
                        'name': 'Programming',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Python Programming',
                                'url': 'https://www.python.org/about/gettingstarted/',
                                'description': 'Official Python documentation and tutorials'
                            },
                            {
                                'type': 'learning',
                                'title': 'JavaScript Fundamentals',
                                'url': 'https://javascript.info/',
                                'description': 'Modern JavaScript tutorial'
                            },
                            {
                                'type': 'practice',
                                'title': 'LeetCode',
                                'url': 'https://leetcode.com/',
                                'description': 'Practice coding problems'
                            }
                        ]
                    },
                    {
                        'name': 'System Design',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'System Design Primer',
                                'url': 'https://github.com/donnemartin/system-design-primer',
                                'description': 'Learn how to design large-scale systems'
                            }
                        ]
                    },
                    {
                        'name': 'Web Development',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'MDN Web Docs',
                                'url': 'https://developer.mozilla.org/',
                                'description': 'Web development resources'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'data-scientist',
                'title': 'Data Scientist',
                'description': 'Analyze data to derive business insights',
                'avg_salary': '6-20 LPA',
                'demand': 'High',
                'skills': [
                    {
                        'name': 'Python',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Python for Data Science',
                                'url': 'https://www.coursera.org/specializations/python',
                                'description': 'Coursera Python specialization'
                            }
                        ]
                    },
                    {
                        'name': 'Machine Learning',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Scikit-learn Tutorial',
                                'url': 'https://scikit-learn.org/stable/tutorial/index.html',
                                'description': 'Official ML library documentation'
                            },
                            {
                                'type': 'learning',
                                'title': 'Kaggle Learn',
                                'url': 'https://www.kaggle.com/learn',
                                'description': 'Free ML courses and competitions'
                            }
                        ]
                    },
                    {
                        'name': 'Statistics',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Khan Academy Statistics',
                                'url': 'https://www.khanacademy.org/math/statistics-probability',
                                'description': 'Free statistics courses'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'product-manager',
                'title': 'Product Manager',
                'description': 'Define product strategy and roadmap',
                'avg_salary': '8-25 LPA',
                'demand': 'High',
                'skills': [
                    {
                        'name': 'Strategy',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Product Strategy Guide',
                                'url': 'https://www.productplan.com/learn/product-strategy/',
                                'description': 'Product strategy resources'
                            }
                        ]
                    },
                    {
                        'name': 'Analytics',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Google Analytics Academy',
                                'url': 'https://analytics.google.com/analytics/academy/',
                                'description': 'Free analytics courses'
                            }
                        ]
                    },
                    {
                        'name': 'Communication',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Product Management Resources',
                                'url': 'https://www.mindtheproduct.com/',
                                'description': 'PM community and articles'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'ui-ux-designer',
                'title': 'UI/UX Designer',
                'description': 'Design user interfaces and experiences',
                'avg_salary': '4-12 LPA',
                'demand': 'High',
                'skills': [
                    {
                        'name': 'Design Tools',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Figma Tutorial',
                                'url': 'https://www.figma.com/resources/learn-design/',
                                'description': 'Learn Figma design tool'
                            },
                            {
                                'type': 'practice',
                                'title': 'Dribbble',
                                'url': 'https://dribbble.com/',
                                'description': 'Design inspiration and community'
                            }
                        ]
                    },
                    {
                        'name': 'User Research',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Nielsen Norman Group',
                                'url': 'https://www.nngroup.com/articles/',
                                'description': 'UX research articles'
                            }
                        ]
                    },
                    {
                        'name': 'Prototyping',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Interaction Design Foundation',
                                'url': 'https://www.interaction-design.org/',
                                'description': 'UX design courses'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'business-analyst',
                'title': 'Business Analyst',
                'description': 'Bridge between business and technology',
                'avg_salary': '4-15 LPA',
                'demand': 'High',
                'skills': [
                    {
                        'name': 'Analysis',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Business Analysis Fundamentals',
                                'url': 'https://www.iiba.org/',
                                'description': 'International Institute of Business Analysis'
                            }
                        ]
                    },
                    {
                        'name': 'Excel & SQL',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'SQL Tutorial',
                                'url': 'https://www.w3schools.com/sql/',
                                'description': 'Learn SQL for data analysis'
                            },
                            {
                                'type': 'learning',
                                'title': 'Excel Skills',
                                'url': 'https://support.microsoft.com/en-us/office/excel-video-training',
                                'description': 'Microsoft Excel tutorials'
                            }
                        ]
                    },
                    {
                        'name': 'Documentation',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Business Analysis Templates',
                                'url': 'https://www.bridging-the-gap.com/',
                                'description': 'BA resources and templates'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'devops-engineer',
                'title': 'DevOps Engineer',
                'description': 'Manage deployment and infrastructure',
                'avg_salary': '6-18 LPA',
                'demand': 'Very High',
                'skills': [
                    {
                        'name': 'Cloud (AWS/Azure)',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'AWS Free Tier',
                                'url': 'https://aws.amazon.com/free/',
                                'description': 'Learn AWS with free tier'
                            },
                            {
                                'type': 'learning',
                                'title': 'Azure Fundamentals',
                                'url': 'https://docs.microsoft.com/en-us/learn/azure/',
                                'description': 'Microsoft Azure learning path'
                            }
                        ]
                    },
                    {
                        'name': 'Docker & Kubernetes',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Docker Documentation',
                                'url': 'https://docs.docker.com/get-started/',
                                'description': 'Official Docker getting started guide'
                            },
                            {
                                'type': 'learning',
                                'title': 'Kubernetes Basics',
                                'url': 'https://kubernetes.io/docs/tutorials/kubernetes-basics/',
                                'description': 'Learn Kubernetes fundamentals'
                            }
                        ]
                    },
                    {
                        'name': 'CI/CD',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Jenkins Tutorial',
                                'url': 'https://www.jenkins.io/doc/tutorials/',
                                'description': 'Learn Jenkins for CI/CD'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'consultant',
                'title': 'Management Consultant',
                'description': 'Provide strategic business advice',
                'avg_salary': '8-30 LPA',
                'demand': 'Medium',
                'skills': [
                    {
                        'name': 'Problem Solving',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Case Interview Prep',
                                'url': 'https://www.caseinterviewprep.com/',
                                'description': 'Management consulting case prep'
                            }
                        ]
                    },
                    {
                        'name': 'Business Frameworks',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Consulting Tools',
                                'url': 'https://www.mckinsey.com/capabilities',
                                'description': 'Business strategy frameworks'
                            }
                        ]
                    },
                    {
                        'name': 'Presentation',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'McKinsey Presentation Style',
                                'url': 'https://www.duarte.com/',
                                'description': 'Professional presentation skills'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'digital-marketing',
                'title': 'Digital Marketing Specialist',
                'description': 'Online marketing and growth strategies',
                'avg_salary': '3-10 LPA',
                'demand': 'High',
                'skills': [
                    {
                        'name': 'SEO/SEM',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Google Digital Garage',
                                'url': 'https://learndigital.withgoogle.com/',
                                'description': 'Free digital marketing courses'
                            },
                            {
                                'type': 'learning',
                                'title': 'Moz SEO Learning Center',
                                'url': 'https://moz.com/learn/seo',
                                'description': 'SEO fundamentals and best practices'
                            }
                        ]
                    },
                    {
                        'name': 'Social Media Marketing',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'HubSpot Academy',
                                'url': 'https://academy.hubspot.com/',
                                'description': 'Free marketing certifications'
                            }
                        ]
                    },
                    {
                        'name': 'Analytics',
                        'resources': [
                            {
                                'type': 'learning',
                                'title': 'Google Analytics',
                                'url': 'https://analytics.google.com/analytics/academy/',
                                'description': 'Master Google Analytics'
                            }
                        ]
                    }
                ]
            }
        ]

        return jsonify({'roles': popular_roles})

    except Exception as e:
        print(f"Error getting popular roles: {str(e)}")
        return jsonify({'error': 'Failed to get popular roles'}), 500

@app.route('/api/roadmap/<int:roadmap_id>', methods=['GET'])
def get_roadmap_by_id(roadmap_id):
    """Get a specific roadmap by ID"""
    try:
        roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)

        if not roadmap_data:
            return jsonify({'error': 'Roadmap not found'}), 404

        return jsonify({
            'roadmap_id': roadmap_id,
            'roadmap': roadmap_data
        })

    except Exception as e:
        print(f"Error getting roadmap: {str(e)}")
        return jsonify({'error': f'Failed to get roadmap: {str(e)}'}), 500

@app.route('/api/roadmap/<int:roadmap_id>/analytics', methods=['GET'])
def get_roadmap_analytics(roadmap_id):
    """Get analytics for a roadmap"""
    try:
        user_id = request.args.get('user_id', 'default_user')

        roadmap_data = db_manager.get_roadmap_by_id(roadmap_id)
        if not roadmap_data:
            return jsonify({'error': 'Roadmap not found'}), 404

        progress = db_manager.get_user_progress(user_id, roadmap_id)

        total_steps = 0
        completed_steps = 0
        total_time_spent = 0

        for phase in roadmap_data.get('phases', []):
            for step in phase.get('steps', []):
                total_steps += 1
                step_id = step['step_id']

                if step_id in progress:
                    if progress[step_id]['completed']:
                        completed_steps += 1
                    total_time_spent += progress[step_id]['time_spent']

        completion_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        estimated_total_hours = sum(
            sum(step.get('estimated_hours', 0) for step in phase.get('steps', []))
            for phase in roadmap_data.get('phases', [])
        )

        analytics = {
            'completion_percentage': round(completion_percentage, 2),
            'completed_steps': completed_steps,
            'total_steps': total_steps,
            'time_spent_hours': total_time_spent,
            'estimated_total_hours': estimated_total_hours,
            'progress_by_phase': [],
            'recent_activity': []
        }

        for phase in roadmap_data.get('phases', []):
            phase_steps = len(phase.get('steps', []))
            phase_completed = sum(
                1 for step in phase.get('steps', [])
                if step['step_id'] in progress and progress[step['step_id']]['completed']
            )

            analytics['progress_by_phase'].append({
                'phase_name': phase['phase_name'],
                'completed_steps': phase_completed,
                'total_steps': phase_steps,
                'completion_percentage': (phase_completed / phase_steps * 100) if phase_steps > 0 else 0
            })

        return jsonify(analytics)

    except Exception as e:
        print(f"Error getting analytics: {str(e)}")
        return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500

# ===================== RESUME-BASED ROADMAP ROUTES =====================

@app.route('/api/roadmap/analyze-resume', methods=['POST'])
def analyze_resume_for_roadmap():
    """Analyze resume and generate personalized career roadmap"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400

        resume_file = request.files['resume']

        with pdfplumber.open(resume_file) as pdf:
            resume_text = ' '.join(
                page.extract_text() or '' for page in pdf.pages
            )

        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from resume'}), 400

        career_info = resume_analyzer.extract_career_info(resume_text)
        primary_role = career_info.get('primary_role', 'Software Developer')
        personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
            career_info, primary_role
        )
        alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)
        roadmap_id = db_manager.save_roadmap(
            f"{primary_role} (Personalized)",
            personalized_roadmap
        )

        return jsonify({
            'success': True,
            'roadmap_id': roadmap_id,
            'career_analysis': {
                'primary_role': primary_role,
                'experience_level': career_info.get('experience_level'),
                'skills': career_info.get('skills', []),
                'skill_gaps': personalized_roadmap.get('skill_gaps', []),
                'strengths': career_info.get('strengths', []),
            },
            'personalized_roadmap': personalized_roadmap,
            'alternative_careers': alternative_careers,
            'message': 'Resume analyzed successfully'
        })

    except Exception as e:
        print(f"Error analyzing resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500

@app.route('/api/roadmap/generate-for-role', methods=['POST'])
def generate_roadmap_for_specific_role():
    """Generate roadmap for a specific role based on resume analysis"""
    try:
        data = request.json
        if 'resume_text' not in data and 'career_info' not in data:
            return jsonify({'error': 'Resume text or career info required'}), 400

        job_role = data.get('job_role')
        if not job_role:
            return jsonify({'error': 'Job role is required'}), 400

        if 'career_info' in data:
            career_info = data['career_info']
        else:
            resume_text = data['resume_text']
            career_info = resume_analyzer.extract_career_info(resume_text)

        personalized_roadmap = resume_analyzer.generate_personalized_roadmap(
            career_info, job_role
        )
        roadmap_id = db_manager.save_roadmap(
            f"{job_role} (Personalized)",
            personalized_roadmap
        )

        return jsonify({
            'success': True,
            'roadmap_id': roadmap_id,
            'roadmap': personalized_roadmap,
            'message': f'Personalized roadmap generated for {job_role}'
        })

    except Exception as e:
        print(f"Error generating roadmap for role: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

@app.route('/api/career/analyze', methods=['POST'])
def quick_career_analysis():
    """Quick career analysis from resume (without full roadmap generation)"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400

        resume_file = request.files['resume']
        with pdfplumber.open(resume_file) as pdf:
            resume_text = ' '.join(
                page.extract_text() or '' for page in pdf.pages
            )

        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from resume'}), 400

        career_info = resume_analyzer.extract_career_info(resume_text)
        alternative_careers = resume_analyzer.suggest_alternative_careers(career_info)

        return jsonify({
            'success': True,
            'career_info': career_info,
            'alternative_careers': alternative_careers
        })

    except Exception as e:
        print(f"Error in career analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to analyze career: {str(e)}'}), 500

# ===================== MAIN APPLICATION ====================

if __name__ == '__main__':
    print("🚀 Starting Study Assistant API...")
    print("📋 Features available:")
    print(" • Resume screening and generation")
    print(" • Cover letter generation")
    print(" • AI-powered roadmap creation")
    print(" • Resume-based personalized roadmaps")
    print(" • Progress tracking")
    print(" • Resource recommendations")
    print("🌐 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)