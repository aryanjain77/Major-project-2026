# from youtubesearchpython import VideosSearch
# import requests
# from bs4 import BeautifulSoup
# import re
# from urllib.parse import urlparse
# import time

# class ResourceFinder:
#     def __init__(self):
#         self.youtube_search = VideosSearch
#         self.quality_keywords = [
#             'tutorial', 'course', 'complete', 'beginner', 'guide', 'learning',
#             'master', 'crash course', 'full course', 'step by step'
#         ]
#         self.high_quality_channels = [
#             'freeCodeCamp.org', 'Traversy Media', 'The Net Ninja', 'Academind',
#             'Programming with Mosh', 'Clever Programmer', 'Derek Banas',
#             'Corey Schafer', 'sentdex', 'Tech With Tim', 'Edureka',
#             'Simplilearn', 'Great Learning', 'Gate Smashers', 'Jenny\'s lectures'
#         ]
    
#     def find_youtube_resources(self, topic, max_results=10):
#         """Find YouTube videos for a specific topic"""
#         try:
#             # Enhanced search query for better results
#             search_queries = [
#                 f"{topic} tutorial complete course",
#                 f"{topic} beginner guide full course",
#                 f"learn {topic} step by step",
#                 f"{topic} crash course programming"
#             ]
            
#             all_videos = []
            
#             for query in search_queries[:2]:  # Use first 2 queries
#                 try:
#                     videos_search = self.youtube_search(query, limit=max_results//2)
#                     results = videos_search.result()
                    
#                     for video in results['result']:
#                         video_data = {
#                             'type': 'youtube',
#                             'title': video['title'],
#                             'url': video['link'],
#                             'description': video.get('description', '')[:200] + '...',
#                             'duration': self._parse_duration(video.get('duration', '0:00')),
#                             'channel': video.get('channel', {}).get('name', ''),
#                             'views': video.get('viewCount', {}).get('text', '0'),
#                             'published': video.get('publishedTime', ''),
#                             'thumbnail': video.get('thumbnails', [{}])[0].get('url', ''),
#                             'quality_score': self._calculate_video_quality_score(video)
#                         }
#                         all_videos.append(video_data)
                    
#                     time.sleep(0.5)  # Rate limiting
                    
#                 except Exception as e:
#                     print(f"Error searching YouTube: {str(e)}")
#                     continue
            
#             # Remove duplicates and sort by quality score
#             unique_videos = {}
#             for video in all_videos:
#                 if video['url'] not in unique_videos:
#                     unique_videos[video['url']] = video
            
#             sorted_videos = sorted(unique_videos.values(), 
#                                  key=lambda x: x['quality_score'], reverse=True)
            
#             return sorted_videos[:max_results]
            
#         except Exception as e:
#             print(f"Error finding YouTube resources: {str(e)}")
#             return []
    
#     def find_documentation_resources(self, topic):
#         """Find official documentation and tutorial resources"""
#         docs_resources = []
        
#         # Common documentation patterns
#         doc_searches = [
#             f"{topic} official documentation",
#             f"{topic} docs tutorial",
#             f"learn {topic} official guide"
#         ]
        
#         # Known documentation sites
#         doc_sites = [
#             "docs.python.org", "developer.mozilla.org", "reactjs.org/docs",
#             "nodejs.org/docs", "angular.io/docs", "vuejs.org/guide",
#             "flask.palletsprojects.com", "django-documentation",
#             "tensorflow.org/tutorials", "pytorch.org/tutorials"
#         ]
        
#         for search_term in doc_searches:
#             try:
#                 # Simulate finding documentation (in real implementation, you'd use search APIs)
#                 docs_resources.extend(self._get_mock_documentation(topic))
#                 break
#             except Exception as e:
#                 print(f"Error finding documentation: {str(e)}")
#                 continue
        
#         return docs_resources[:5]
    
#     def find_practice_resources(self, topic):
#         """Find practice platforms and coding challenges"""
#         practice_resources = []
        
#         # Common practice platforms
#         platforms = {
#             'HackerRank': f"https://hackerrank.com/domains/{topic.lower()}",
#             'LeetCode': f"https://leetcode.com/tag/{topic.lower()}/",
#             'Codewars': f"https://codewars.com/kata/search/{topic}",
#             'FreeCodeCamp': f"https://freecodecamp.org/learn/{topic.lower()}",
#             'Codecademy': f"https://codecademy.com/learn/{topic.lower()}"
#         }
        
#         for platform, url in platforms.items():
#             practice_resources.append({
#                 'type': 'practice',
#                 'title': f"{topic} Practice on {platform}",
#                 'url': url,
#                 'description': f"Practice {topic} problems and challenges on {platform}",
#                 'duration': 0,  # Self-paced
#                 'quality_score': 0.8,
#                 'platform': platform
#             })
        
#         return practice_resources
    
#     def _calculate_video_quality_score(self, video):
#         """Calculate quality score for a video"""
#         score = 0.5  # Base score
        
#         title = video.get('title', '').lower()
#         channel = video.get('channel', {}).get('name', '').lower()
#         views_text = video.get('viewCount', {}).get('text', '0')
#         duration = video.get('duration', '0:00')
        
#         # Channel quality bonus
#         if any(quality_channel.lower() in channel for quality_channel in self.high_quality_channels):
#             score += 0.3
        
#         # Title quality indicators
#         quality_words = sum(1 for word in self.quality_keywords if word in title)
#         score += min(quality_words * 0.05, 0.2)
        
#         # Duration bonus (prefer longer, comprehensive content)
#         duration_minutes = self._parse_duration(duration)
#         if 30 <= duration_minutes <= 180:  # 30 mins to 3 hours is ideal
#             score += 0.15
#         elif duration_minutes > 180:
#             score += 0.1
        
#         # Views bonus (parse view count)
#         try:
#             views_num = self._parse_views(views_text)
#             if views_num > 100000:
#                 score += 0.1
#             elif views_num > 10000:
#                 score += 0.05
#         except:
#             pass
        
#         return min(score, 1.0)
    
#     def _parse_duration(self, duration_str):
#         """Parse duration string to minutes"""
#         try:
#             if ':' not in duration_str:
#                 return 0
            
#             parts = duration_str.split(':')
#             if len(parts) == 2:  # MM:SS
#                 return int(parts[0])
#             elif len(parts) == 3:  # HH:MM:SS
#                 return int(parts[0]) * 60 + int(parts[1])
#             return 0
#         except:
#             return 0
    
#     def _parse_views(self, views_text):
#         """Parse view count text to number"""
#         try:
#             # Remove non-digit characters except for K, M, B
#             views_clean = re.sub(r'[^\d.KMB]', '', views_text.upper())
            
#             if 'K' in views_clean:
#                 return int(float(views_clean.replace('K', '')) * 1000)
#             elif 'M' in views_clean:
#                 return int(float(views_clean.replace('M', '')) * 1000000)
#             elif 'B' in views_clean:
#                 return int(float(views_clean.replace('B', '')) * 1000000000)
#             else:
#                 return int(views_clean) if views_clean.isdigit() else 0
#         except:
#             return 0
    
#     def _get_mock_documentation(self, topic):
#         """Mock documentation resources (replace with real search in production)"""
#         topic_docs = {
#             'python': [
#                 {
#                     'type': 'documentation',
#                     'title': 'Python Official Documentation',
#                     'url': 'https://docs.python.org/3/',
#                     'description': 'Official Python 3 documentation and tutorials',
#                     'duration': 0,
#                     'quality_score': 0.9
#                 }
#             ],
#             'javascript': [
#                 {
#                     'type': 'documentation',
#                     'title': 'MDN JavaScript Guide',
#                     'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
#                     'description': 'Complete JavaScript reference and guide by Mozilla',
#                     'duration': 0,
#                     'quality_score': 0.95
#                 }
#             ],
#             'react': [
#                 {
#                     'type': 'documentation',
#                     'title': 'React Official Documentation',
#                     'url': 'https://reactjs.org/docs/getting-started.html',
#                     'description': 'Official React documentation and tutorial',
#                     'duration': 0,
#                     'quality_score': 0.9
#                 }
#             ]
#         }
        
#         return topic_docs.get(topic.lower(), [
#             {
#                 'type': 'documentation',
#                 'title': f'{topic} Documentation',
#                 'url': f'https://docs.{topic.lower()}.org',
#                 'description': f'Official {topic} documentation and guides',
#                 'duration': 0,
#                 'quality_score': 0.8
#             }
#         ])
    
#     def get_all_resources_for_step(self, step_title, step_description):
#         """Get all types of resources for a learning step"""
#         search_topic = f"{step_title} {step_description}"
        
#         # Get different types of resources
#         youtube_resources = self.find_youtube_resources(step_title, max_results=5)
#         doc_resources = self.find_documentation_resources(step_title)
#         practice_resources = self.find_practice_resources(step_title)
        
#         # Combine all resources
#         all_resources = youtube_resources + doc_resources + practice_resources
        
#         # Sort by quality score
#         all_resources.sort(key=lambda x: x['quality_score'], reverse=True)
        
#         return all_resources[:10]  # Return top 10 resources

import requests
from youtubesearchpython import VideosSearch
import re
from urllib.parse import urlparse
import time

class ResourceFinder:
    def __init__(self):
        self.youtube_search = VideosSearch
        self.quality_keywords = [
            'tutorial', 'course', 'complete', 'beginner', 'guide', 'learning',
            'master', 'crash course', 'full course', 'step by step'
        ]
        self.high_quality_channels = [
            'freeCodeCamp.org', 'Traversy Media', 'The Net Ninja', 'Academind',
            'Programming with Mosh', 'Clever Programmer', 'Derek Banas',
            'Corey Schafer', 'sentdex', 'Tech With Tim', 'Edureka',
            'Simplilearn', 'Great Learning', 'Gate Smashers', "Jenny's lectures"
        ]
        self.session = requests.Session()  # For URL validation

    def _validate_url(self, url, timeout=5):
        """Check if a URL is valid and accessible"""
        try:
            response = self.session.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code in (200, 301, 302)
        except requests.RequestException:
            return False

    def find_youtube_resources(self, topic, max_results=10):
        """Find YouTube videos for a specific topic"""
        try:
            search_queries = [
                f"{topic} tutorial complete course",
                f"{topic} beginner guide full course",
                f"learn {topic} step by step",
                f"{topic} crash course programming"
            ]
            
            all_videos = []
            
            for query in search_queries[:2]:  # Use first 2 queries
                try:
                    videos_search = self.youtube_search(query, limit=max_results//2)
                    results = videos_search.result()
                    
                    for video in results['result']:
                        url = video['link']
                        if not self._validate_url(url):
                            continue  # Skip invalid YouTube links
                        
                        video_data = {
                            'type': 'youtube',
                            'title': video['title'],
                            'url': url,
                            'description': video.get('description', '')[:200] + '...' if video.get('description') else '',
                            'duration': self._parse_duration(video.get('duration', '0:00')),
                            'channel': video.get('channel', {}).get('name', ''),
                            'views': video.get('viewCount', {}).get('text', '0'),
                            'published': video.get('publishedTime', ''),
                            'thumbnail': video.get('thumbnails', [{}])[0].get('url', ''),
                            'quality_score': self._calculate_video_quality_score(video)
                        }
                        all_videos.append(video_data)
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    print(f"Error searching YouTube for query '{query}': {str(e)}")
                    continue
            
            # Remove duplicates and sort by quality score
            unique_videos = {video['url']: video for video in all_videos}
            sorted_videos = sorted(unique_videos.values(), 
                                key=lambda x: x['quality_score'], reverse=True)
            
            return sorted_videos[:max_results]
            
        except Exception as e:
            print(f"Error finding YouTube resources for topic '{topic}': {str(e)}")
            return []

    def find_documentation_resources(self, topic):
        """Find official documentation and tutorial resources"""
        topic = topic.lower()
        doc_resources = []
        
        # Mapping of topics to real documentation URLs
        doc_mapping = {
            'python': [
                {
                    'type': 'documentation',
                    'title': 'Python Official Documentation',
                    'url': 'https://docs.python.org/3/',
                    'description': 'Official Python 3 documentation and tutorials',
                    'duration': 0,
                    'quality_score': 0.9
                },
                {
                    'type': 'documentation',
                    'title': 'Python Tutorial - W3Schools',
                    'url': 'https://www.w3schools.com/python/',
                    'description': 'Beginner-friendly Python tutorial',
                    'duration': 0,
                    'quality_score': 0.85
                }
            ],
            'javascript': [
                {
                    'type': 'documentation',
                    'title': 'MDN JavaScript Guide',
                    'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
                    'description': 'Complete JavaScript guide by Mozilla',
                    'duration': 0,
                    'quality_score': 0.95
                },
                {
                    'type': 'documentation',
                    'title': 'JavaScript.info Tutorial',
                    'url': 'https://javascript.info/',
                    'description': 'Modern JavaScript tutorial',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'react': [
                {
                    'type': 'documentation',
                    'title': 'React Official Documentation',
                    'url': 'https://react.dev/learn',
                    'description': 'Official React documentation and tutorial',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'nodejs': [
                {
                    'type': 'documentation',
                    'title': 'Node.js Official Documentation',
                    'url': 'https://nodejs.org/en/docs/',
                    'description': 'Official Node.js documentation',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'angular': [
                {
                    'type': 'documentation',
                    'title': 'Angular Official Documentation',
                    'url': 'https://angular.io/docs',
                    'description': 'Official Angular documentation',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'vue': [
                {
                    'type': 'documentation',
                    'title': 'Vue.js Official Guide',
                    'url': 'https://vuejs.org/guide/introduction.html',
                    'description': 'Official Vue.js documentation and guide',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'flask': [
                {
                    'type': 'documentation',
                    'title': 'Flask Official Documentation',
                    'url': 'https://flask.palletsprojects.com/en/stable/',
                    'description': 'Official Flask documentation',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'django': [
                {
                    'type': 'documentation',
                    'title': 'Django Official Documentation',
                    'url': 'https://docs.djangoproject.com/en/stable/',
                    'description': 'Official Django documentation',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'tensorflow': [
                {
                    'type': 'documentation',
                    'title': 'TensorFlow Official Tutorials',
                    'url': 'https://www.tensorflow.org/tutorials',
                    'description': 'Official TensorFlow tutorials',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'pytorch': [
                {
                    'type': 'documentation',
                    'title': 'PyTorch Official Tutorials',
                    'url': 'https://pytorch.org/tutorials/',
                    'description': 'Official PyTorch tutorials',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ],
            'statistics': [
                {
                    'type': 'documentation',
                    'title': 'Khan Academy Statistics',
                    'url': 'https://www.khanacademy.org/math/statistics-probability',
                    'description': 'Free statistics and probability course',
                    'duration': 0,
                    'quality_score': 0.9
                }
            ]
        }
        
        # Return validated documentation resources
        resources = doc_mapping.get(topic, [])
        validated_resources = []
        for resource in resources:
            if self._validate_url(resource['url']):
                validated_resources.append(resource)
            else:
                print(f"Skipping invalid documentation URL: {resource['url']}")
        
        # Fallback if no specific resources found
        if not validated_resources:
            fallback = {
                'type': 'documentation',
                'title': f'{topic.capitalize()} General Documentation',
                'url': f'https://www.w3schools.com/{topic.lower()}/',
                'description': f'General learning resources for {topic}',
                'duration': 0,
                'quality_score': 0.8
            }
            if self._validate_url(fallback['url']):
                validated_resources.append(fallback)
        
        return validated_resources[:5]

    def find_practice_resources(self, topic):
        """Find practice platforms and coding challenges"""
        topic = topic.lower()
        practice_resources = []
        
        # Mapping of topics to practice platform URLs
        practice_mapping = {
            'python': {
                'HackerRank': 'https://www.hackerrank.com/domains/python',
                'LeetCode': 'https://leetcode.com/problemset/?topicSlugs=python-3',
                'Codewars': 'https://www.codewars.com/kata/search/python',
                'FreeCodeCamp': 'https://www.freecodecamp.org/learn/scientific-computing-with-python/',
                'Codecademy': 'https://www.codecademy.com/learn/learn-python-3'
            },
            'javascript': {
                'HackerRank': 'https://www.hackerrank.com/domains/javascript',
                'LeetCode': 'https://leetcode.com/problemset/?topicSlugs=javascript',
                'Codewars': 'https://www.codewars.com/kata/search/javascript',
                'FreeCodeCamp': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
                'Codecademy': 'https://www.codecademy.com/learn/introduction-to-javascript'
            },
            'react': {
                'HackerRank': 'https://www.hackerrank.com/domains/javascript',  # React uses JS
                'LeetCode': 'https://leetcode.com/problemset/?topicSlugs=javascript',
                'Codewars': 'https://www.codewars.com/kata/search/javascript',
                'FreeCodeCamp': 'https://www.freecodecamp.org/learn/front-end-development-libraries/#react',
                'Codecademy': 'https://www.codecademy.com/learn/learn-react'
            },
            'statistics': {
                'Kaggle': 'https://www.kaggle.com/learn',
                'DataCamp': 'https://www.datacamp.com/learn/statistics'
            }
        }
        
        platforms = practice_mapping.get(topic, {
            'HackerRank': f"https://www.hackerrank.com/domains/{topic}",
            'LeetCode': f"https://leetcode.com/problemset/?topicSlugs={topic}",
            'Codewars': f"https://www.codewars.com/kata/search/{topic}",
            'FreeCodeCamp': f"https://www.freecodecamp.org/learn/{topic}",
            'Codecademy': f"https://www.codecademy.com/learn/{topic}"
        })
        
        for platform, url in platforms.items():
            if self._validate_url(url):
                practice_resources.append({
                    'type': 'practice',
                    'title': f"{topic.capitalize()} Practice on {platform}",
                    'url': url,
                    'description': f"Practice {topic} problems and challenges on {platform}",
                    'duration': 0,
                    'quality_score': 0.8,
                    'platform': platform
                })
            else:
                print(f"Skipping invalid practice URL: {url}")
        
        return practice_resources[:5]

    def _calculate_video_quality_score(self, video):
        """Calculate quality score for a video"""
        score = 0.5  # Base score
        
        title = video.get('title', '').lower()
        channel = video.get('channel', {}).get('name', '').lower()
        views_text = video.get('viewCount', {}).get('text', '0')
        duration = video.get('duration', '0:00')
        
        # Channel quality bonus
        if any(quality_channel.lower() in channel for quality_channel in self.high_quality_channels):
            score += 0.3
        
        # Title quality indicators
        quality_words = sum(1 for word in self.quality_keywords if word in title)
        score += min(quality_words * 0.05, 0.2)
        
        # Duration bonus (prefer longer, comprehensive content)
        duration_minutes = self._parse_duration(duration)
        if 30 <= duration_minutes <= 180:  # 30 mins to 3 hours is ideal
            score += 0.15
        elif duration_minutes > 180:
            score += 0.1
        
        # Views bonus
        try:
            views_num = self._parse_views(views_text)
            if views_num > 100000:
                score += 0.1
            elif views_num > 10000:
                score += 0.05
        except:
            pass
        
        return min(score, 1.0)

    def _parse_duration(self, duration_str):
        """Parse duration string to minutes"""
        try:
            if ':' not in duration_str:
                return 0
            
            parts = duration_str.split(':')
            if len(parts) == 2:  # MM:SS
                return int(parts[0])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            return 0
        except:
            return 0

    def _parse_views(self, views_text):
        """Parse view count text to number"""
        try:
            views_clean = re.sub(r'[^\d.KMB]', '', views_text.upper())
            
            if 'K' in views_clean:
                return int(float(views_clean.replace('K', '')) * 1000)
            elif 'M' in views_clean:
                return int(float(views_clean.replace('M', '')) * 1000000)
            elif 'B' in views_clean:
                return int(float(views_clean.replace('B', '')) * 1000000000)
            else:
                return int(views_clean) if views_clean.isdigit() else 0
        except:
            return 0

    def get_all_resources_for_step(self, step_title, step_description):
        """Get all types of resources for a learning step"""
        search_topic = f"{step_title} {step_description}"
        
        youtube_resources = self.find_youtube_resources(step_title, max_results=5)
        doc_resources = self.find_documentation_resources(step_title)
        practice_resources = self.find_practice_resources(step_title)
        
        all_resources = youtube_resources + doc_resources + practice_resources
        all_resources.sort(key=lambda x: x['quality_score'], reverse=True)
        
        return all_resources[:10]