import React, { useState, useEffect, useRef } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import './index.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Histogram({ data, title }) {
  const chartData = {
    labels: Object.keys(data).map(salary => {
      const salaryNum = parseInt(salary);
      return salaryNum === 0
        ? '0-1M'
        : `${(salaryNum / 1000000).toFixed(0)}M-${((salaryNum + 1000000) / 1000000).toFixed(0)}M`;
    }),
    datasets: [
      {
        label: 'Number of Jobs',
        data: Object.values(data),
        backgroundColor: '#1976d2',
        borderColor: '#1565c0',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: { title: { display: true, text: 'Salary Range (₹)' } },
      y: { title: { display: true, text: 'Number of Jobs' } },
    },
    plugins: {
      legend: { display: false },
      title: { display: true, text: title },
    },
  };

  return (
    <div style={{ height: '300px' }}>
      <Bar data={chartData} options={options} />
    </div>
  );
}

function MarketTrends() {
  // Existing states
  const [categories, setCategories] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [combinedHistogram, setCombinedHistogram] = useState({});
  const [loadingCategories, setLoadingCategories] = useState(true);
  const [loadingJobs, setLoadingJobs] = useState(true);
  const [loadingHistogram, setLoadingHistogram] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // 'all' or 'software'

  // Resume and Cover Letter States
  const [uploadedResume, setUploadedResume] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [generatingCoverLetter, setGeneratingCoverLetter] = useState({});
  const [generatedCoverLetters, setGeneratedCoverLetters] = useState({});
  const [showCoverLetter, setShowCoverLetter] = useState({});
  const [selectedAIProvider, setSelectedAIProvider] = useState('local');
  const [aiProviderStatus, setAiProviderStatus] = useState({});
  const fileInputRef = useRef(null);

  // API credentials (use environment variables in production)
  const APP_ID = process.env.REACT_APP_ADZUNA_APP_ID || 'd3c024ad';
  const APP_KEY = process.env.REACT_APP_ADZUNA_APP_KEY || 'b91efe137789aaa6fcd09d96cef3c9d1';

  // AI Provider Configurations
  const AI_PROVIDERS = {
    gemini: {
      name: 'Google Gemini',
      apiKey: process.env.REACT_APP_GEMINI_API_KEY || 'AIzaSyDEmpBYHGQWCRc6YQCJ17OJ4y2KlpCzFaU',
      icon: '🤖',
      endpoint: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',
    },
    local: {
      name: 'Local Template Generator',
      apiKey: 'built-in',
      icon: '📝',
      endpoint: 'local',
    },
  };

  // Check AI provider status
  useEffect(() => {
    const checkProviders = () => {
      const status = {};
      Object.keys(AI_PROVIDERS).forEach(provider => {
        const config = AI_PROVIDERS[provider];
        status[provider] = {
          available: provider === 'local' || Boolean(config.apiKey),
          name: config.name,
          icon: config.icon,
        };
      });
      setAiProviderStatus(status);
    };
    checkProviders();
  }, []);

  // Fetch categories from Adzuna API
  useEffect(() => {
    const fetchCategories = async () => {
      setLoadingCategories(true);
      setError(null);
      try {
        const response = await fetch(
          `https://api.adzuna.com/v1/api/jobs/in/categories?app_id=${APP_ID}&app_key=${APP_KEY}`
        );
        if (!response.ok) throw new Error(`Failed to fetch categories: ${response.status}`);
        const data = await response.json();
        setCategories(data.results || []);
      } catch (err) {
        setError(`Error fetching categories: ${err.message}`);
        console.error(err);
      } finally {
        setLoadingCategories(false);
      }
    };
    fetchCategories();
  }, []);

  // Fetch jobs from Adzuna API
  useEffect(() => {
    const fetchJobs = async () => {
      setLoadingJobs(true);
      setError(null);
      try {
        const query = filter === 'software' ? 'software developer' : '';
        const response = await fetch(
          `https://api.adzuna.com/v1/api/jobs/in/search/1?app_id=${APP_ID}&app_key=${APP_KEY}&results_per_page=10&what=${encodeURIComponent(query)}`
        );
        if (!response.ok) throw new Error(`Failed to fetch jobs: ${response.status}`);
        const data = await response.json();
        setJobs(data.results || []);
      } catch (err) {
        setError(`Error fetching jobs: ${err.message}`);
        console.error(err);
      } finally {
        setLoadingJobs(false);
      }
    };
    fetchJobs();
  }, [filter]);

  // Fetch and combine histogram data for all categories
  useEffect(() => {
    const fetchCombinedHistogram = async () => {
      setLoadingHistogram(true);
      setError(null);
      try {
        const histogramData = {};
        for (const category of categories) {
          const response = await fetch(
            `https://api.adzuna.com/v1/api/jobs/in/histogram?app_id=${APP_ID}&app_key=${APP_KEY}&category=${encodeURIComponent(category.tag)}`
          );
          if (!response.ok) throw new Error(`Failed to fetch histogram for ${category.tag}: ${response.status}`);
          const data = await response.json();
          Object.entries(data.histogram || {}).forEach(([salary, count]) => {
            const salaryNum = parseInt(salary);
            histogramData[salaryNum] = (histogramData[salaryNum] || 0) + parseInt(count);
          });
        }
        setCombinedHistogram(histogramData);
      } catch (err) {
        setError(`Error fetching histogram data: ${err.message}`);
        console.error(err);
      } finally {
        setLoadingHistogram(false);
      }
    };
    if (categories.length > 0) {
      fetchCombinedHistogram();
    }
  }, [categories]);

  // Handle resume upload and text extraction
  const handleResumeUpload = async (event) => {
    const file = event.target.files[0];
    if (!file || file.type !== 'application/pdf') {
      alert('Please upload a PDF file only.');
      return;
    }
    setUploadedResume(file);
    // Simulate text extraction
    const mockResumeText = `Professional Resume - ${file.name}
Experience: Software Developer with expertise in React, JavaScript, Node.js, and Python.
Skills: Full-stack development, database management, API integration, and team collaboration.
Education: Computer Science degree with strong foundation in algorithms and software engineering.
Projects: Built multiple web applications using modern frameworks and cloud technologies.`;
    setResumeText(mockResumeText);
    console.log('Resume uploaded and text extracted');
  };

  // Generate local template cover letter
  const generateLocalCoverLetter = (job) => {
    return `Dear Hiring Manager,

I am writing to express my strong interest in the ${job.title} position at ${job.company?.display_name || 'your company'}. With my background in software development and relevant technical skills, I am excited about the opportunity to contribute to your team.

Based on the job requirements and my experience:

• I have hands-on experience in software development and programming
• My technical skills align well with the requirements mentioned in the job description
• I am passionate about creating efficient, scalable solutions
• I have strong problem-solving abilities and attention to detail

The opportunity at ${job.company?.display_name || 'your company'} particularly interests me because of your reputation for innovation and technical excellence. I am eager to bring my skills and enthusiasm to help drive your projects forward.

I have attached my resume for your review and would welcome the opportunity to discuss how my background and passion for technology can contribute to your team's success.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
[Your Name]

---
Generated using Local Template
Location: ${job.location?.display_name || 'India'}
Job Type: Software Development
Company: ${job.company?.display_name || 'Company'}`;
  };

  // Generate cover letter using selected AI provider
  const generateCoverLetter = async (job) => {
    if (!uploadedResume) {
      alert('Please upload your resume first!');
      return;
    }
    const jobId = job.id;
    setGeneratingCoverLetter(prev => ({ ...prev, [jobId]: true }));
    try {
      let coverLetter;
      if (selectedAIProvider === 'local') {
        await new Promise(resolve => setTimeout(resolve, 2000));
        coverLetter = generateLocalCoverLetter(job);
      } else {
        coverLetter = await callAIProvider(selectedAIProvider, job);
      }
      setGeneratedCoverLetters(prev => ({ ...prev, [jobId]: coverLetter }));
      setShowCoverLetter(prev => ({ ...prev, [jobId]: true }));
      console.log('Cover letter generated successfully using:', selectedAIProvider);
    } catch (error) {
      console.error('Error generating cover letter:', error);
      try {
        const fallbackLetter = generateLocalCoverLetter(job);
        setGeneratedCoverLetters(prev => ({ ...prev, [jobId]: fallbackLetter + '\n\n[Note: Generated using fallback template due to AI service error]' }));
        setShowCoverLetter(prev => ({ ...prev, [jobId]: true }));
        alert(`Primary AI service failed. Generated using local template instead. Error: ${error.message}`);
      } catch (fallbackError) {
        alert(`Error generating cover letter: ${error.message}`);
      }
    } finally {
      setGeneratingCoverLetter(prev => ({ ...prev, [jobId]: false }));
    }
  };

  // Call specific AI provider
  const callAIProvider = async (provider, job) => {
    const config = AI_PROVIDERS[provider];
    const prompt = `Generate a professional cover letter based on the following information:
        
JOB TITLE: ${job.title}
COMPANY: ${job.company?.display_name || 'the company'}
JOB DESCRIPTION: ${job.description_clean || job.description || 'No description available'}
LOCATION: ${job.location?.display_name || 'Location not specified'}

MY RESUME CONTENT:
${resumeText}

Please create a personalized, professional cover letter that:
1. Addresses the specific job title and company
2. Highlights relevant experience from my resume that matches the job requirements
3. Shows enthusiasm for the role and company
4. Is concise but compelling (around 250-350 words)
5. Includes a professional greeting and closing
6. Avoids generic phrases and focuses on specific qualifications

Format the response as a complete, ready-to-send cover letter.`;

    if (provider === 'gemini') {
      return await callGeminiAPI(config, prompt);
    }
    throw new Error('Unknown AI provider');
  };

  // Gemini API call
  const callGeminiAPI = async (config, prompt) => {
    const response = await fetch(`${config.endpoint}?key=${config.apiKey}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
      }),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Gemini API error: ${response.status} - ${errorData.error?.message || 'Unknown error'}`);
    }
    const data = await response.json();
    return data.candidates?.[0]?.content?.parts?.[0]?.text || 'Error generating cover letter';
  };

  // Copy cover letter to clipboard
  const copyCoverLetter = (coverLetter) => {
    navigator.clipboard.writeText(coverLetter).then(() => {
      alert('Cover letter copied to clipboard!');
    }).catch(err => {
      console.error('Error copying to clipboard:', err);
      alert('Error copying to clipboard');
    });
  };

  // Download cover letter as text file
  const downloadCoverLetter = (coverLetter, jobTitle, company) => {
    const fileName = `Cover_Letter_${jobTitle.replace(/\s+/g, '_')}_${company?.replace(/\s+/g, '_') || 'Company'}.txt`;
    const blob = new Blob([coverLetter], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Format salary helper function
  const formatSalary = (salaryMin, salaryMax) => {
    if (salaryMin && salaryMax) {
      return `₹${salaryMin.toLocaleString()} - ₹${salaryMax.toLocaleString()}`;
    } else if (salaryMin) {
      return `₹${salaryMin.toLocaleString()}+`;
    } else if (salaryMax) {
      return `Up to ₹${salaryMax.toLocaleString()}`;
    }
    return 'Salary not specified';
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1 style={{ color: '#2c3e50', textAlign: 'center', marginBottom: '10px' }}>Job Market Trends Dashboard</h1>
      <p style={{ textAlign: 'center', color: '#6c757d', marginBottom: '30px' }}>
        Explore job opportunities and salary distributions in the Indian job market.
      </p>

      {/* Resume Upload Section */}
      <div style={{ 
        marginBottom: '30px', 
        padding: '20px', 
        backgroundColor: '#f1f8ff', 
        borderRadius: '8px',
        border: '2px solid #b6d7ff'
      }}>
        <h3 style={{ color: '#0366d6', marginBottom: '15px' }}>📄 Upload Resume for AI Cover Letter Generation</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', flexWrap: 'wrap' }}>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleResumeUpload}
              accept=".pdf"
              style={{ display: 'none' }}
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              style={{
                backgroundColor: '#0366d6',
                color: 'white',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'background-color 0.3s ease'
              }}
            >
              📎 Upload Resume (PDF)
            </button>
            {uploadedResume && (
              <span style={{ 
                color: '#28a745', 
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}>
                ✅ {uploadedResume.name}
              </span>
            )}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label style={{ fontWeight: '600', color: '#586069' }}>
              🤖 Select AI Provider for Cover Letter Generation:
            </label>
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
              {Object.keys(AI_PROVIDERS).map(provider => (
                <button
                  key={provider}
                  onClick={() => setSelectedAIProvider(provider)}
                  disabled={!aiProviderStatus[provider]?.available}
                  style={{
                    backgroundColor: selectedAIProvider === provider ? '#28a745' : aiProviderStatus[provider]?.available ? '#6c757d' : '#dc3545',
                    color: 'white',
                    border: 'none',
                    padding: '8px 16px',
                    borderRadius: '4px',
                    fontSize: '12px',
                    fontWeight: '600',
                    cursor: aiProviderStatus[provider]?.available ? 'pointer' : 'not-allowed',
                    opacity: aiProviderStatus[provider]?.available ? 1 : 0.6,
                    transition: 'all 0.3s ease'
                  }}
                  title={aiProviderStatus[provider]?.available ? `Use ${aiProviderStatus[provider]?.name}` : `${aiProviderStatus[provider]?.name} - API key not configured`}
                >
                  {aiProviderStatus[provider]?.icon} {aiProviderStatus[provider]?.name}
                  {selectedAIProvider === provider && ' ✓'}
                </button>
              ))}
            </div>
            <small style={{ color: '#6c757d', fontStyle: 'italic' }}>
              Current selection: <strong>{aiProviderStatus[selectedAIProvider]?.icon} {aiProviderStatus[selectedAIProvider]?.name}</strong>
              {selectedAIProvider === 'local' && ' (No API key required - uses built-in template)'}
            </small>
          </div>
          {resumeText && (
            <div style={{ 
              backgroundColor: '#f6f8fa', 
              padding: '10px', 
              borderRadius: '4px', 
              border: '1px solid #e1e4e8',
              maxHeight: '100px',
              overflow: 'auto'
            }}>
              <small style={{ color: '#586069' }}>
                <strong>Resume Preview:</strong> {resumeText.substring(0, 200)}...
              </small>
            </div>
          )}
        </div>
      </div>

      {/* Combined Job Opportunities Section */}
      <div style={{ 
        marginBottom: '30px', 
        padding: '20px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '8px',
        border: '2px solid #e9ecef'
      }}>
        <h3 style={{ color: '#2c3e50', marginBottom: '15px' }}>🚀 Job Opportunities in India</h3>
        <p style={{ marginBottom: '15px', color: '#6c757d' }}>
          Discover the latest job opportunities across India
        </p>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
          <button
            onClick={() => setFilter('all')}
            style={{
              backgroundColor: filter === 'all' ? '#007bff' : '#6c757d',
              color: 'white',
              border: 'none',
              padding: '12px 24px',
              borderRadius: '6px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease'
            }}
          >
            All Jobs
          </button>
          <button
            onClick={() => setFilter('software')}
            style={{
              backgroundColor: filter === 'software' ? '#007bff' : '#6c757d',
              color: 'white',
              border: 'none',
              padding: '12px 24px',
              borderRadius: '6px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease'
            }}
          >
            Software Jobs
          </button>
        </div>
        {error && (
          <div style={{ 
            marginTop: '15px', 
            padding: '10px', 
            backgroundColor: '#f8d7da', 
            color: '#721c24', 
            borderRadius: '4px',
            border: '1px solid #f5c6cb'
          }}>
            {error}
          </div>
        )}
        {loadingJobs ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <span>Loading jobs...</span>
          </div>
        ) : jobs.length > 0 ? (
          <div style={{ marginTop: '20px' }}>
            <h4 style={{ color: '#2c3e50', marginBottom: '15px' }}>
              Found {jobs.length} Job{jobs.length !== 1 ? 's' : ''}
            </h4>
            <div style={{ display: 'grid', gap: '20px' }}>
              {jobs.map(job => (
                <div key={job.id} style={{ 
                  backgroundColor: 'white', 
                  padding: '20px', 
                  borderRadius: '8px', 
                  border: '1px solid #e9ecef',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                    <div>
                      <h5 style={{ margin: '0 0 8px 0', color: '#007bff', fontSize: '18px' }}>{job.title}</h5>
                      <p style={{ margin: '0 0 5px 0', color: '#28a745', fontWeight: '600' }}>
                        🏢 {job.company?.display_name}
                      </p>
                      <p style={{ margin: '0 0 5px 0', color: '#6c757d' }}>
                        📍 {job.location?.display_name}
                      </p>
                      <p style={{ margin: '0 0 10px 0', color: '#17a2b8', fontWeight: '600' }}>
                        💰 {job.salary_formatted || formatSalary(job.salary_min, job.salary_max)}
                      </p>
                    </div>
                    <span style={{ 
                      backgroundColor: '#e9ecef', 
                      color: '#495057', 
                      padding: '4px 8px', 
                      borderRadius: '12px', 
                      fontSize: '12px',
                      fontWeight: '600'
                    }}>
                      {job.created}
                    </span>
                  </div>
                  <p style={{ color: '#6c757d', marginBottom: '15px', lineHeight: '1.5' }}>
                    {job.description_clean || job.description}
                  </p>
                  <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                    <button
                      onClick={() => generateCoverLetter(job)}
                      disabled={generatingCoverLetter[job.id] || !uploadedResume}
                      style={{
                        backgroundColor: !uploadedResume ? '#6c757d' : generatingCoverLetter[job.id] ? '#ffc107' : '#28a745',
                        color: 'white',
                        border: 'none',
                        padding: '8px 16px',
                        borderRadius: '4px',
                        fontSize: '14px',
                        fontWeight: '600',
                        cursor: (!uploadedResume || generatingCoverLetter[job.id]) ? 'not-allowed' : 'pointer',
                        transition: 'background-color 0.3s ease'
                      }}
                      title={!uploadedResume ? 'Please upload your resume first' : ''}
                    >
                      {generatingCoverLetter[job.id] ? '⏳ Generating...' : '📝 Generate Cover Letter'}
                    </button>
                    {generatedCoverLetters[job.id] && (
                      <>
                        <button
                          onClick={() => setShowCoverLetter(prev => ({ ...prev, [job.id]: !prev[job.id] }))}
                          style={{
                            backgroundColor: '#17a2b8',
                            color: 'white',
                            border: 'none',
                            padding: '8px 16px',
                            borderRadius: '4px',
                            fontSize: '14px',
                            fontWeight: '600',
                            cursor: 'pointer'
                          }}
                        >
                          {showCoverLetter[job.id] ? '👁️ Hide Letter' : '👁️ View Letter'}
                        </button>
                        <button
                          onClick={() => copyCoverLetter(generatedCoverLetters[job.id])}
                          style={{
                            backgroundColor: '#6f42c1',
                            color: 'white',
                            border: 'none',
                            padding: '8px 16px',
                            borderRadius: '4px',
                            fontSize: '14px',
                            fontWeight: '600',
                            cursor: 'pointer'
                          }}
                        >
                          📋 Copy
                        </button>
                        <button
                          onClick={() => downloadCoverLetter(generatedCoverLetters[job.id], job.title, job.company?.display_name)}
                          style={{
                            backgroundColor: '#fd7e14',
                            color: 'white',
                            border: 'none',
                            padding: '8px 16px',
                            borderRadius: '4px',
                            fontSize: '14px',
                            fontWeight: '600',
                            cursor: 'pointer'
                          }}
                        >
                          💾 Download
                        </button>
                      </>
                    )}
                  </div>
                  {showCoverLetter[job.id] && generatedCoverLetters[job.id] && (
                    <div style={{ 
                      marginTop: '15px', 
                      padding: '15px', 
                      backgroundColor: '#f8f9fa', 
                      borderRadius: '6px',
                      border: '1px solid #e9ecef'
                    }}>
                      <h6 style={{ color: '#2c3e50', marginBottom: '10px' }}>Generated Cover Letter:</h6>
                      <pre style={{ 
                        whiteSpace: 'pre-wrap', 
                        fontSize: '14px', 
                        lineHeight: '1.5',
                        margin: 0,
                        fontFamily: 'inherit',
                        color: '#495057'
                      }}>
                        {generatedCoverLetters[job.id]}
                      </pre>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p>No jobs found.</p>
        )}
      </div>

      {/* Combined Histogram Section */}
      <div style={{ 
        marginBottom: '30px', 
        padding: '20px', 
        backgroundColor: '#fff3cd', 
        borderRadius: '8px',
        border: '2px solid #ffeaa7'
      }}>
        <h3 style={{ color: '#856404', marginBottom: '15px' }}>📊 Salary Distribution Across All Categories</h3>
        {loadingHistogram ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <span>Loading salary data...</span>
          </div>
        ) : error ? (
          <p style={{ color: '#dc3545' }}>{error}</p>
        ) : Object.keys(combinedHistogram).length > 0 ? (
          <Histogram data={combinedHistogram} title="Combined Salary Distribution" />
        ) : (
          <p>No salary data available.</p>
        )}
      </div>

      {/* Footer */}
      <div style={{ 
        textAlign: 'center', 
        padding: '20px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '8px',
        border: '1px solid #e9ecef',
        color: '#6c757d'
      }}>
        <p style={{ margin: 0, fontSize: '14px' }}>
          Job Market Trends Dashboard - Powered by AI Cover Letter Generation
        </p>
        <p style={{ margin: '5px 0 0 0', fontSize: '12px' }}>
          Upload your resume and generate personalized cover letters for any job posting
        </p>
      </div>
    </div>
  );
}

export default MarketTrends;