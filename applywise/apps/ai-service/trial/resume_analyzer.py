import google.generativeai as genai
import json
import re

class ResumeAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def extract_career_info(self, resume_text):
        """Extract career-relevant information from resume using Gemini"""
        prompt = f"""
        Analyze this resume and extract the following information in JSON format:
        
        Resume Text:
        {resume_text}
        
        Please provide a JSON response with the following structure:
        {{
            "primary_role": "The main job role/title the candidate is suited for",
            "experience_level": "beginner/intermediate/advanced",
            "skills": ["list", "of", "key", "skills"],
            "domains": ["list", "of", "domain", "areas"],
            "career_interests": ["list", "of", "potential", "career", "paths"],
            "current_position": "Current or most recent job title",
            "years_of_experience": "Number of years (estimate if not explicit)",
            "education_level": "Highest degree",
            "certifications": ["list", "of", "certifications"],
            "strengths": ["key", "strengths", "identified"],
            "recommended_roles": [
                {{
                    "role": "Job Role Name",
                    "match_percentage": 85,
                    "reason": "Why this role fits"
                }},
                {{
                    "role": "Alternative Role Name",
                    "match_percentage": 75,
                    "reason": "Why this role fits"
                }}
            ]
        }}
        
        IMPORTANT: Return ONLY valid JSON, no markdown formatting or code blocks.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'^```\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            
            career_info = json.loads(response_text)
            return career_info
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text}")
            # Return a default structure
            return {
                "primary_role": "Software Developer",
                "experience_level": "beginner",
                "skills": [],
                "domains": [],
                "career_interests": [],
                "current_position": "Unknown",
                "years_of_experience": "0",
                "education_level": "Unknown",
                "certifications": [],
                "strengths": [],
                "recommended_roles": []
            }
    
    def generate_personalized_roadmap_prompt(self, career_info, job_role):
        """Generate a personalized roadmap prompt based on resume analysis"""
        prompt = f"""
        Create a comprehensive, personalized learning roadmap for the following profile:
        
        Target Role: {job_role}
        Current Position: {career_info.get('current_position', 'N/A')}
        Experience Level: {career_info.get('experience_level', 'beginner')}
        Current Skills: {', '.join(career_info.get('skills', []))}
        Education: {career_info.get('education_level', 'N/A')}
        Strengths: {', '.join(career_info.get('strengths', []))}
        
        Create a detailed roadmap in JSON format with the following structure:
        {{
            "job_role": "{job_role}",
            "personalized_intro": "A personalized introduction based on their current profile",
            "total_estimated_weeks": 24,
            "skill_gaps": ["skills", "they", "need", "to", "develop"],
            "phases": [
                {{
                    "phase_number": 1,
                    "phase_name": "Foundation Phase",
                    "duration_weeks": 4,
                    "description": "Build foundational knowledge",
                    "steps": [
                        {{
                            "step_id": "step_1_1",
                            "title": "Step Title",
                            "description": "Detailed description of what to learn",
                            "estimated_hours": 10,
                            "priority": "high",
                            "prerequisites": [],
                            "learning_objectives": ["objective 1", "objective 2"],
                            "key_topics": ["topic 1", "topic 2"]
                        }}
                    ]
                }}
            ],
            "milestone_projects": [
                {{
                    "title": "Project Title",
                    "description": "Project description",
                    "phase": 1,
                    "estimated_hours": 20,
                    "skills_demonstrated": ["skill1", "skill2"]
                }}
            ],
            "interview_prep": {{
                "technical_topics": ["topic1", "topic2"],
                "behavioral_prep": ["area1", "area2"],
                "system_design": ["concept1", "concept2"]
            }},
            "career_tips": [
                "Personalized tip 1 based on their background",
                "Personalized tip 2"
            ]
        }}
        
        Make the roadmap:
        1. Personalized to their current skill level and experience
        2. Focus on filling their skill gaps
        3. Leverage their existing strengths
        4. Include realistic timelines based on their background
        5. Provide actionable, specific steps
        
        IMPORTANT: Return ONLY valid JSON, no markdown formatting or code blocks.
        """
        
        return prompt
    
    def generate_personalized_roadmap(self, career_info, job_role):
        """Generate a personalized roadmap using Gemini"""
        prompt = self.generate_personalized_roadmap_prompt(career_info, job_role)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'^```\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            
            roadmap_data = json.loads(response_text)
            
            # Add career info to roadmap
            roadmap_data['career_analysis'] = career_info
            roadmap_data['is_personalized'] = True
            
            return roadmap_data
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in roadmap generation: {e}")
            print(f"Response text: {response_text}")
            # Return a basic structure
            return {
                "job_role": job_role,
                "personalized_intro": f"Custom roadmap for {job_role}",
                "total_estimated_weeks": 24,
                "skill_gaps": [],
                "phases": [],
                "career_analysis": career_info,
                "is_personalized": True
            }
    
    def suggest_alternative_careers(self, career_info):
        """Suggest alternative career paths based on resume analysis"""
        recommended = career_info.get('recommended_roles', [])
        
        # Sort by match percentage
        recommended.sort(key=lambda x: x.get('match_percentage', 0), reverse=True)
        
        return recommended[:5]  # Return top 5 recommendations