import google.generativeai as genai
import json
import uuid
from datetime import datetime

class RoadmapGenerator:
    def __init__(self, gemini_api_key):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_roadmap(self, job_role, experience_level="beginner", target_company=None):
        """Generate a detailed roadmap for a specific job role"""
        
        prompt = f"""
        Create a comprehensive learning roadmap for becoming a {job_role} in India.
        Experience level: {experience_level}
        Target company type: {target_company or "General companies"}
        
        Generate a JSON response with this exact structure:
        {{
            "job_role": "{job_role}",
            "total_duration_weeks": number,
            "difficulty_level": "beginner/intermediate/advanced",
            "prerequisites": ["skill1", "skill2"],
            "phases": [
                {{
                    "phase_id": "unique_id",
                    "phase_name": "Phase Name",
                    "duration_weeks": number,
                    "description": "Phase description",
                    "steps": [
                        {{
                            "step_id": "unique_id",
                            "title": "Step Title",
                            "description": "Detailed description",
                            "skills_gained": ["skill1", "skill2"],
                            "estimated_hours": number,
                            "difficulty": "easy/medium/hard",
                            "prerequisites": ["previous_step_id"],
                            "learning_objectives": ["objective1", "objective2"],
                            "practical_tasks": ["task1", "task2"],
                            "assessment_criteria": ["criteria1", "criteria2"]
                        }}
                    ]
                }}
            ],
            "key_skills": ["skill1", "skill2", "skill3"],
            "career_progression": {{
                "entry_level": "Job titles",
                "mid_level": "Job titles",
                "senior_level": "Job titles"
            }},
            "salary_expectations": {{
                "entry_level": "Range in INR",
                "mid_level": "Range in INR", 
                "senior_level": "Range in INR"
            }},
            "top_companies": ["Company1", "Company2"],
            "additional_tips": ["tip1", "tip2"]
        }}
        
        Make sure the roadmap is:
        1. Specific to Indian job market
        2. Practical and actionable
        3. Progressive (builds upon previous knowledge)
        4. Includes both technical and soft skills
        5. Has realistic time estimates
        6. Covers popular technologies/frameworks used in India
        
        Focus on skills that are actually required for {job_role} positions in Indian companies.
        """
        
        try:
            response = self.model.generate_content(prompt)
            roadmap_text = response.text.strip()
            
            # Clean up the response to extract JSON
            if "```json" in roadmap_text:
                roadmap_text = roadmap_text.split("```json")[1].split("```")[0].strip()
            elif "```" in roadmap_text:
                roadmap_text = roadmap_text.split("```")[1].strip()
            
            roadmap_data = json.loads(roadmap_text)
            
            # Generate unique IDs if not present
            for phase in roadmap_data.get('phases', []):
                if 'phase_id' not in phase:
                    phase['phase_id'] = str(uuid.uuid4())
                for step in phase.get('steps', []):
                    if 'step_id' not in step:
                        step['step_id'] = str(uuid.uuid4())
            
            roadmap_data['created_at'] = datetime.now().isoformat()
            roadmap_data['updated_at'] = datetime.now().isoformat()
            
            return roadmap_data
            
        except Exception as e:
            print(f"Error generating roadmap: {str(e)}")
            return self._get_fallback_roadmap(job_role)
    
    def _get_fallback_roadmap(self, job_role):
        """Fallback roadmap if AI generation fails"""
        return {
            "job_role": job_role,
            "total_duration_weeks": 12,
            "difficulty_level": "beginner",
            "prerequisites": ["Basic computer skills", "English proficiency"],
            "phases": [
                {
                    "phase_id": str(uuid.uuid4()),
                    "phase_name": "Foundation Phase",
                    "duration_weeks": 4,
                    "description": f"Build foundational knowledge for {job_role}",
                    "steps": [
                        {
                            "step_id": str(uuid.uuid4()),
                            "title": "Industry Overview",
                            "description": f"Understand the {job_role} landscape",
                            "skills_gained": ["Industry knowledge", "Market awareness"],
                            "estimated_hours": 20,
                            "difficulty": "easy",
                            "prerequisites": [],
                            "learning_objectives": [f"Understand {job_role} responsibilities"],
                            "practical_tasks": ["Research top companies", "Read industry reports"],
                            "assessment_criteria": ["Complete industry overview quiz"]
                        }
                    ]
                }
            ],
            "key_skills": ["Problem solving", "Communication", "Technical skills"],
            "career_progression": {
                "entry_level": f"Junior {job_role}",
                "mid_level": f"Senior {job_role}",
                "senior_level": f"Lead {job_role}"
            },
            "salary_expectations": {
                "entry_level": "3-6 LPA",
                "mid_level": "6-15 LPA",
                "senior_level": "15-30 LPA"
            },
            "top_companies": ["TCS", "Infosys", "Wipro", "Accenture"],
            "additional_tips": ["Practice regularly", "Build a portfolio", "Network with professionals"]
        }
    
    def update_roadmap_for_user(self, base_roadmap, user_skills, available_hours_per_week):
        """Customize roadmap based on user's current skills and availability"""
        
        prompt = f"""
        Customize this learning roadmap based on user's profile:
        
        Base Roadmap: {json.dumps(base_roadmap, indent=2)}
        
        User Profile:
        - Current Skills: {user_skills}
        - Available Hours per Week: {available_hours_per_week}
        
        Modify the roadmap to:
        1. Skip steps for skills the user already has
        2. Adjust time estimates based on available hours
        3. Reorder steps if needed based on user's background
        4. Add prerequisite checks
        
        Return the modified roadmap in the same JSON format.
        """
        
        try:
            response = self.model.generate_content(prompt)
            roadmap_text = response.text.strip()
            
            if "```json" in roadmap_text:
                roadmap_text = roadmap_text.split("```json")[1].split("```")[0].strip()
            
            customized_roadmap = json.loads(roadmap_text)
            customized_roadmap['customized_for_user'] = True
            customized_roadmap['user_skills'] = user_skills
            customized_roadmap['available_hours_per_week'] = available_hours_per_week
            
            return customized_roadmap
            
        except Exception as e:
            print(f"Error customizing roadmap: {str(e)}")
            # Return original roadmap if customization fails
            return base_roadmap