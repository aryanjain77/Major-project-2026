import requests
import json
import csv
import time
from datetime import datetime
import re

class AdzunaJobScraper:
    def __init__(self, app_id="d3c024ad", app_key="b91efe137789aaa6fcd09d96cef3c9d1", country='in'):
        """
        Initialize Adzuna Job Scraper with your credentials
        """
        self.app_id = app_id
        self.app_key = app_key
        self.country = country
        self.base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search"
        self.session = requests.Session()
        
    def search_jobs(self, query, location="", page=1, results_per_page=20, 
                   sort_by="relevance", salary_min=None, salary_max=None,
                   contract_time="", company="", category=""):
        """
        Search for jobs using Adzuna API
        """
        params = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'results_per_page': min(results_per_page, 50),
            'page': page,
            'sort_by': sort_by
        }
        
        if query:
            params['what'] = query
        if location:
            params['where'] = location
        if salary_min:
            params['salary_min'] = salary_min
        if salary_max:
            params['salary_max'] = salary_max
        if contract_time:
            params['full_time'] = 1 if contract_time == 'full_time' else 0
            params['part_time'] = 1 if contract_time == 'part_time' else 0
            params['contract'] = 1 if contract_time == 'contract' else 0
        if company:
            params['company'] = company
        if category:
            params['category'] = category
            
        try:
            print(f"Searching page {page}: '{query}' in '{location}'...")
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
    
    def get_job_details(self, job_data):
        """
        Extract and format job details from API response
        """
        # Clean HTML tags from description
        description = job_data.get('description', '')
        description_clean = re.sub('<.*?>', '', description) if description else ''
        
        # Format salary
        salary_info = ""
        if job_data.get('salary_min') or job_data.get('salary_max'):
            min_sal = job_data.get('salary_min', 0)
            max_sal = job_data.get('salary_max', 0)
            if min_sal and max_sal:
                salary_info = f"₹{min_sal:,.0f} - ₹{max_sal:,.0f}"
            elif min_sal:
                salary_info = f"₹{min_sal:,.0f}+"
            elif max_sal:
                salary_info = f"Up to ₹{max_sal:,.0f}"
        
        return {
            'job_id': job_data.get('id', ''),
            'title': job_data.get('title', ''),
            'company': job_data.get('company', {}).get('display_name', ''),
            'location': f"{job_data.get('location', {}).get('display_name', '')}",
            'description': description_clean[:500],  # Limit for display
            'full_description': description_clean,
            'url': job_data.get('redirect_url', ''),
            'created_date': job_data.get('created', ''),
            'salary_min': job_data.get('salary_min', ''),
            'salary_max': job_data.get('salary_max', ''),
            'salary_formatted': salary_info,
            'contract_type': job_data.get('contract_type', ''),
            'contract_time': job_data.get('contract_time', ''),
            'category': job_data.get('category', {}).get('label', ''),
            'latitude': job_data.get('latitude', ''),
            'longitude': job_data.get('longitude', ''),
            'adref': job_data.get('adref', ''),
            'company_logo': job_data.get('company', {}).get('logo_url', '')
        }
    
    def scrape_software_jobs_india(self, max_pages=5, delay=1):
        """
        Specifically scrape software jobs in India
        """
        software_queries = [
            "Software Developer",
            "Software Engineer", 
            "Full Stack Developer",
            "Frontend Developer",
            "Backend Developer",
            "Python Developer",
            "Java Developer",
            "React Developer",
            "Node.js Developer",
            "DevOps Engineer"
        ]
        
        all_jobs = []
        
        for query in software_queries:
            print(f"\n🔍 Searching for: {query}")
            
            for page in range(1, max_pages + 1):
                response = self.search_jobs(
                    query=query,
                    location="India",
                    page=page,
                    results_per_page=20,
                    sort_by="date",
                    contract_time="full_time"
                )
                
                if not response or 'results' not in response:
                    print(f"No results for {query} on page {page}")
                    break
                    
                jobs = response['results']
                
                if not jobs:
                    print(f"No jobs found for {query} on page {page}")
                    break
                    
                for job in jobs:
                    job_details = self.get_job_details(job)
                    job_details['search_query'] = query
                    all_jobs.append(job_details)
                    
                print(f"Found {len(jobs)} {query} jobs on page {page}")
                
                if len(jobs) < 20:  # Last page
                    break
                
                time.sleep(delay)
            
            # Small delay between different queries
            time.sleep(2)
        
        return all_jobs
    
    def scrape_specific_software_jobs(self, location="India", max_results=50):
        """
        Scrape specific software jobs with detailed filtering
        """
        response = self.search_jobs(
            query="Software Engineer OR Software Developer OR Full Stack Developer",
            location=location,
            page=1,
            results_per_page=min(max_results, 50),
            sort_by="date",
            contract_time="full_time"
        )
        
        if not response or 'results' not in response:
            print("No software jobs found")
            return []
            
        jobs = []
        for job_data in response['results']:
            job = self.get_job_details(job_data)
            jobs.append(job)
            
        return jobs
    
    def get_trending_tech_jobs(self):
        """
        Get trending technology jobs in India
        """
        tech_categories = [
            'it-jobs',
            'computing-technology-jobs', 
            'engineering-jobs'
        ]
        
        all_jobs = []
        
        for category in tech_categories:
            print(f"Fetching jobs for category: {category}")
            
            try:
                url = f"https://api.adzuna.com/v1/api/jobs/{self.country}/categories/{category}"
                params = {
                    'app_id': self.app_id,
                    'app_key': self.app_key,
                    'page': 1,
                    'results_per_page': 20,
                    'where': 'India'
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'results' in data:
                    for job_data in data['results']:
                        job = self.get_job_details(job_data)
                        job['category_searched'] = category
                        all_jobs.append(job)
                        
                time.sleep(1)
                
            except Exception as e:
                print(f"Error fetching {category}: {e}")
                
        return all_jobs
    
    def save_to_csv(self, jobs, filename=None):
        """Save job data to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"india_software_jobs_{timestamp}.csv"
            
        if not jobs:
            print("No jobs to save")
            return
            
        csv_fields = [
            'job_id', 'title', 'company', 'location', 'salary_formatted',
            'contract_type', 'category', 'created_date', 'description', 'url'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
            writer.writeheader()
            
            for job in jobs:
                csv_row = {field: job.get(field, '') for field in csv_fields}
                writer.writerow(csv_row)
            
        print(f"✅ Saved {len(jobs)} jobs to {filename}")
        return filename
    
    def save_to_json(self, jobs, filename=None):
        """Save job data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"india_software_jobs_{timestamp}.json"
            
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(jobs, jsonfile, indent=2, ensure_ascii=False)
            
        print(f"✅ Saved {len(jobs)} jobs to {filename}")
        return filename
    
    def display_jobs(self, jobs, max_display=10):
        """Display job information in console"""
        print(f"\n📋 Displaying top {min(len(jobs), max_display)} jobs:")
        print("=" * 80)
        
        for i, job in enumerate(jobs[:max_display]):
            print(f"\n🔸 Job {i + 1}")
            print(f"Title: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Salary: {job['salary_formatted'] or 'Not specified'}")
            print(f"Category: {job['category']}")
            print(f"Posted: {job['created_date']}")
            print(f"Description: {job['description'][:200]}...")
            print(f"Apply: {job['url']}")
            print("-" * 80)


def main():
    """
    Main function to scrape software jobs in India
    """
    print("🚀 Starting Adzuna India Software Jobs Scraper")
    print("=" * 50)
    
    # Initialize scraper with your credentials
    scraper = AdzunaJobScraper()
    
    print("🎯 Searching for software jobs in India...")
    
    # Method 1: Quick search for software jobs
    print("\n📊 Method 1: Quick Software Jobs Search")
    quick_jobs = scraper.scrape_specific_software_jobs(max_results=30)
    
    if quick_jobs:
        print(f"✅ Found {len(quick_jobs)} software jobs")
        scraper.display_jobs(quick_jobs, max_display=5)
        
        # Save results
        csv_file = scraper.save_to_csv(quick_jobs, "india_software_jobs_quick.csv")
        json_file = scraper.save_to_json(quick_jobs, "india_software_jobs_quick.json")
        
        # Statistics
        companies = set(job['company'] for job in quick_jobs if job['company'])
        locations = set(job['location'] for job in quick_jobs if job['location'])
        
        print(f"\n📈 Quick Search Summary:")
        print(f"Total jobs found: {len(quick_jobs)}")
        print(f"Unique companies: {len(companies)}")
        print(f"Unique locations: {len(locations)}")
        print(f"Files saved: {csv_file}, {json_file}")
    
    # Method 2: Trending tech jobs by category
    print(f"\n📊 Method 2: Trending Tech Jobs by Category")
    trending_jobs = scraper.get_trending_tech_jobs()
    
    if trending_jobs:
        print(f"✅ Found {len(trending_jobs)} trending tech jobs")
        scraper.display_jobs(trending_jobs, max_display=3)
        
        scraper.save_to_csv(trending_jobs, "india_trending_tech_jobs.csv")
        scraper.save_to_json(trending_jobs, "india_trending_tech_jobs.json")
    
    print(f"\n🎉 Scraping completed successfully!")


def search_custom_jobs(query, location="India", max_results=20):
    """
    Custom function to search for specific jobs
    """
    scraper = AdzunaJobScraper()
    
    print(f"🔍 Searching for '{query}' in {location}")
    
    response = scraper.search_jobs(
        query=query,
        location=location,
        results_per_page=max_results,
        sort_by="date"
    )
    
    if response and 'results' in response:
        jobs = [scraper.get_job_details(job_data) for job_data in response['results']]
        scraper.display_jobs(jobs, max_display=5)
        
        filename = f"{query.replace(' ', '_').lower()}_jobs.csv"
        scraper.save_to_csv(jobs, filename)
        
        return jobs
    
    return []


if __name__ == "__main__":
    # Run main scraper
    main()
    
    # Example of custom searches
    print(f"\n" + "="*50)
    print("🎯 Custom Job Searches")
    print("="*50)
    
    # Custom searches you can uncomment and run
    # search_custom_jobs("Python Developer", "Mumbai")
    # search_custom_jobs("React Developer", "Bangalore") 
    # search_custom_jobs("DevOps Engineer", "Pune")
    # search_custom_jobs("Data Scientist", "Delhi")