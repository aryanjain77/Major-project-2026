import sqlite3
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="study_assistant.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Roadmaps table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roadmaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_role TEXT NOT NULL,
                roadmap_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                roadmap_id INTEGER NOT NULL,
                step_id TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                time_spent INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, roadmap_id, step_id),
                FOREIGN KEY (roadmap_id) REFERENCES roadmaps (id)
            )
        ''')
        
        # Resources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                step_id TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                duration INTEGER DEFAULT 0,
                quality_score REAL DEFAULT 0.0,
                channel TEXT,
                views TEXT,
                thumbnail TEXT,
                published TEXT,
                platform TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User profiles table (for storing user preferences)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                full_name TEXT,
                email TEXT,
                skills TEXT,
                experience_level TEXT DEFAULT 'beginner',
                target_role TEXT,
                available_hours_per_week INTEGER DEFAULT 10,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Study sessions table (for detailed time tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                roadmap_id INTEGER NOT NULL,
                step_id TEXT NOT NULL,
                session_start TIMESTAMP NOT NULL,
                session_end TIMESTAMP,
                duration_minutes INTEGER DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (roadmap_id) REFERENCES roadmaps (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_progress_user_roadmap ON user_progress(user_id, roadmap_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_resources_step_id ON resources(step_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_roadmaps_job_role ON roadmaps(job_role)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_study_sessions_user ON study_sessions(user_id, roadmap_id)')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    
    def save_roadmap(self, job_role, roadmap_data):
        """Save a generated roadmap"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO roadmaps (job_role, roadmap_data, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (job_role, json.dumps(roadmap_data)))
            
            roadmap_id = cursor.lastrowid
            conn.commit()
            print(f"✅ Roadmap saved for {job_role} with ID: {roadmap_id}")
            return roadmap_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error saving roadmap: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def get_roadmap(self, job_role):
        """Get roadmap for a specific job role"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, roadmap_data FROM roadmaps 
                WHERE job_role = ? 
                ORDER BY created_at DESC LIMIT 1
            ''', (job_role,))
            
            result = cursor.fetchone()
            
            if result:
                return result[0], json.loads(result[1])
            return None, None
        except Exception as e:
            print(f"❌ Error getting roadmap: {str(e)}")
            return None, None
        finally:
            conn.close()
    
    def get_roadmap_by_id(self, roadmap_id):
        """Get roadmap data by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT roadmap_data FROM roadmaps WHERE id = ?
            ''', (roadmap_id,))
            
            result = cursor.fetchone()
            
            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            print(f"❌ Error getting roadmap by ID: {str(e)}")
            return None
        finally:
            conn.close()
    
    def get_all_roadmaps(self):
        """Get all roadmaps with basic info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, job_role, created_at FROM roadmaps 
                ORDER BY created_at DESC
            ''')
            
            results = cursor.fetchall()
            roadmaps = []
            
            for row in results:
                roadmaps.append({
                    'id': row[0],
                    'job_role': row[1],
                    'created_at': row[2]
                })
            
            return roadmaps
        except Exception as e:
            print(f"❌ Error getting all roadmaps: {str(e)}")
            return []
        finally:
            conn.close()
    
    def save_user_progress(self, user_id, roadmap_id, step_id, completed=False, time_spent=0):
        """Save or update user progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO user_progress 
                (user_id, roadmap_id, step_id, completed, time_spent, completed_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, roadmap_id, step_id, completed, time_spent, 
                  datetime.now().isoformat() if completed else None))
            
            conn.commit()
            print(f"✅ Progress updated for user {user_id}, step {step_id}")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error saving user progress: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def get_user_progress(self, user_id, roadmap_id):
        """Get user progress for a roadmap"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT step_id, completed, time_spent, completed_at 
                FROM user_progress 
                WHERE user_id = ? AND roadmap_id = ?
            ''', (user_id, roadmap_id))
            
            results = cursor.fetchall()
            progress = {}
            
            for row in results:
                progress[row[0]] = {
                    'completed': bool(row[1]),
                    'time_spent': row[2],
                    'completed_at': row[3]
                }
            
            return progress
        except Exception as e:
            print(f"❌ Error getting user progress: {str(e)}")
            return {}
        finally:
            conn.close()
    
    def get_user_overall_progress(self, user_id):
        """Get overall progress across all roadmaps for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    r.id,
                    r.job_role,
                    COUNT(up.step_id) as total_steps,
                    SUM(CASE WHEN up.completed = 1 THEN 1 ELSE 0 END) as completed_steps,
                    SUM(up.time_spent) as total_time_spent
                FROM roadmaps r
                LEFT JOIN user_progress up ON r.id = up.roadmap_id AND up.user_id = ?
                GROUP BY r.id, r.job_role
                HAVING total_steps > 0
                ORDER BY r.job_role
            ''', (user_id,))
            
            results = cursor.fetchall()
            progress_summary = []
            
            for row in results:
                completion_percentage = (row[3] / row[2] * 100) if row[2] > 0 else 0
                progress_summary.append({
                    'roadmap_id': row[0],
                    'job_role': row[1],
                    'total_steps': row[2],
                    'completed_steps': row[3],
                    'completion_percentage': round(completion_percentage, 2),
                    'total_time_spent': row[4] or 0
                })
            
            return progress_summary
        except Exception as e:
            print(f"❌ Error getting overall progress: {str(e)}")
            return []
        finally:
            conn.close()
    
    def save_resources(self, step_id, resources):
        """Save resources for a step"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # First, check if resources already exist for this step
            cursor.execute('SELECT COUNT(*) FROM resources WHERE step_id = ?', (step_id,))
            existing_count = cursor.fetchone()[0]
            
            if existing_count > 0:
                print(f"ℹ️  Resources already exist for step {step_id}")
                return
            
            for resource in resources:
                cursor.execute('''
                    INSERT INTO resources 
                    (step_id, resource_type, title, url, description, duration, 
                     quality_score, channel, views, thumbnail, published, platform)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    step_id, 
                    resource['type'], 
                    resource['title'], 
                    resource['url'],
                    resource.get('description', ''), 
                    resource.get('duration', 0),
                    resource.get('quality_score', 0.0),
                    resource.get('channel', ''),
                    resource.get('views', ''),
                    resource.get('thumbnail', ''),
                    resource.get('published', ''),
                    resource.get('platform', resource['type'])
                ))
            
            conn.commit()
            print(f"✅ Saved {len(resources)} resources for step {step_id}")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error saving resources: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def get_resources(self, step_id):
        """Get resources for a step"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT resource_type, title, url, description, duration, quality_score,
                       channel, views, thumbnail, published, platform
                FROM resources 
                WHERE step_id = ?
                ORDER BY quality_score DESC
            ''', (step_id,))
            
            results = cursor.fetchall()
            resources = []
            
            for row in results:
                resources.append({
                    'type': row[0],
                    'title': row[1],
                    'url': row[2],
                    'description': row[3],
                    'duration': row[4],
                    'quality_score': row[5],
                    'channel': row[6],
                    'views': row[7],
                    'thumbnail': row[8],
                    'published': row[9],
                    'platform': row[10]
                })
            
            return resources
        except Exception as e:
            print(f"❌ Error getting resources: {str(e)}")
            return []
        finally:
            conn.close()
    
    def save_user_profile(self, user_id, profile_data):
        """Save or update user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO user_profiles 
                (user_id, full_name, email, skills, experience_level, target_role, 
                 available_hours_per_week, preferences, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                user_id,
                profile_data.get('full_name', ''),
                profile_data.get('email', ''),
                json.dumps(profile_data.get('skills', [])),
                profile_data.get('experience_level', 'beginner'),
                profile_data.get('target_role', ''),
                profile_data.get('available_hours_per_week', 10),
                json.dumps(profile_data.get('preferences', {}))
            ))
            
            conn.commit()
            print(f"✅ User profile saved for {user_id}")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error saving user profile: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def get_user_profile(self, user_id):
        """Get user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT full_name, email, skills, experience_level, target_role,
                       available_hours_per_week, preferences, created_at, updated_at
                FROM user_profiles 
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            
            if result:
                return {
                    'user_id': user_id,
                    'full_name': result[0],
                    'email': result[1],
                    'skills': json.loads(result[2]) if result[2] else [],
                    'experience_level': result[3],
                    'target_role': result[4],
                    'available_hours_per_week': result[5],
                    'preferences': json.loads(result[6]) if result[6] else {},
                    'created_at': result[7],
                    'updated_at': result[8]
                }
            return None
        except Exception as e:
            print(f"❌ Error getting user profile: {str(e)}")
            return None
        finally:
            conn.close()
    
    def start_study_session(self, user_id, roadmap_id, step_id, notes=""):
        """Start a study session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO study_sessions 
                (user_id, roadmap_id, step_id, session_start, notes)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
            ''', (user_id, roadmap_id, step_id, notes))
            
            session_id = cursor.lastrowid
            conn.commit()
            print(f"✅ Study session started with ID: {session_id}")
            return session_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error starting study session: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def end_study_session(self, session_id, notes=""):
        """End a study session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE study_sessions 
                SET session_end = CURRENT_TIMESTAMP,
                    duration_minutes = (
                        (julianday(CURRENT_TIMESTAMP) - julianday(session_start)) * 24 * 60
                    ),
                    notes = ?
                WHERE id = ?
            ''', (notes, session_id))
            
            conn.commit()
            
            # Get the session details
            cursor.execute('''
                SELECT duration_minutes FROM study_sessions WHERE id = ?
            ''', (session_id,))
            
            result = cursor.fetchone()
            duration = result[0] if result else 0
            
            print(f"✅ Study session ended. Duration: {duration:.1f} minutes")
            return duration
        except Exception as e:
            conn.rollback()
            print(f"❌ Error ending study session: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def get_study_sessions(self, user_id, roadmap_id=None, limit=50):
        """Get study sessions for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if roadmap_id:
                cursor.execute('''
                    SELECT id, step_id, session_start, session_end, duration_minutes, notes
                    FROM study_sessions 
                    WHERE user_id = ? AND roadmap_id = ?
                    ORDER BY session_start DESC
                    LIMIT ?
                ''', (user_id, roadmap_id, limit))
            else:
                cursor.execute('''
                    SELECT id, roadmap_id, step_id, session_start, session_end, duration_minutes, notes
                    FROM study_sessions 
                    WHERE user_id = ?
                    ORDER BY session_start DESC
                    LIMIT ?
                ''', (user_id, limit))
            
            results = cursor.fetchall()
            sessions = []
            
            for row in results:
                if roadmap_id:
                    sessions.append({
                        'session_id': row[0],
                        'step_id': row[1],
                        'session_start': row[2],
                        'session_end': row[3],
                        'duration_minutes': row[4],
                        'notes': row[5]
                    })
                else:
                    sessions.append({
                        'session_id': row[0],
                        'roadmap_id': row[1],
                        'step_id': row[2],
                        'session_start': row[3],
                        'session_end': row[4],
                        'duration_minutes': row[5],
                        'notes': row[6]
                    })
            
            return sessions
        except Exception as e:
            print(f"❌ Error getting study sessions: {str(e)}")
            return []
        finally:
            conn.close()
    
    def get_database_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            stats = {}
            
            # Count roadmaps
            cursor.execute('SELECT COUNT(*) FROM roadmaps')
            stats['total_roadmaps'] = cursor.fetchone()[0]
            
            # Count users with progress
            cursor.execute('SELECT COUNT(DISTINCT user_id) FROM user_progress')
            stats['active_users'] = cursor.fetchone()[0]
            
            # Count total resources
            cursor.execute('SELECT COUNT(*) FROM resources')
            stats['total_resources'] = cursor.fetchone()[0]
            
            # Count study sessions
            cursor.execute('SELECT COUNT(*) FROM study_sessions')
            stats['total_study_sessions'] = cursor.fetchone()[0]
            
            # Get most popular job roles
            cursor.execute('''
                SELECT job_role, COUNT(*) as usage_count 
                FROM roadmaps 
                GROUP BY job_role 
                ORDER BY usage_count DESC 
                LIMIT 5
            ''')
            
            popular_roles = cursor.fetchall()
            stats['popular_roles'] = [{'role': row[0], 'count': row[1]} for row in popular_roles]
            
            return stats
        except Exception as e:
            print(f"❌ Error getting database stats: {str(e)}")
            return {}
        finally:
            conn.close()
    
    def cleanup_old_data(self, days_old=90):
        """Clean up old data (optional maintenance function)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Clean up old study sessions
            cursor.execute('''
                DELETE FROM study_sessions 
                WHERE created_at < datetime('now', '-{} days')
            '''.format(days_old))
            
            deleted_sessions = cursor.rowcount
            
            conn.commit()
            print(f"✅ Cleaned up {deleted_sessions} old study sessions")
            return deleted_sessions
        except Exception as e:
            conn.rollback()
            print(f"❌ Error cleaning up old data: {str(e)}")
            return 0
        finally:
            conn.close()
    
    def close(self):
        """Close database connection (cleanup method)"""
        print("📝 Database manager cleanup completed")

# Example usage and testing
if __name__ == "__main__":
    # Test the database manager
    db = DatabaseManager()
    stats = db.get_database_stats()
    print("📊 Database Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")