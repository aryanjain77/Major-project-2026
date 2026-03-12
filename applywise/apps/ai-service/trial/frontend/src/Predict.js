// import React, { useState } from 'react';
// import axios from 'axios';
// import './index.css';

// const Predict = () => {
//   const [file, setFile] = useState(null);
//   const [experience, setExperience] = useState(0);
//   const [projects, setProjects] = useState(0);
//   const [salary, setSalary] = useState(0);
//   const [chance, setChance] = useState(null);
//   const [error, setError] = useState(null);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const formData = new FormData();
//     formData.append('resume', file);
//     formData.append('experience_years', experience);
//     formData.append('projects_count', projects);
//     formData.append('salary_expectation', salary);
//     try {
//       const res = await axios.post('http://localhost:5000/predict', formData);
//       setChance(res.data.chance);
//       setError(null);
//     } catch (err) {
//       setError('Failed to predict selection chance. Please try again.');
//       console.error(err);
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <div>
//         <label>Upload Resume (PDF)</label>
//         <input
//           type="file"
//           accept=".pdf"
//           onChange={(e) => setFile(e.target.files[0])}
//           required
//         />
//       </div>
//       <div>
//         <label>Experience (Years)</label>
//         <input
//           type="number"
//           style={{color: "black"}}
//           value={experience}
//           onChange={(e) => setExperience(e.target.value)}
//           placeholder="Enter years of experience"
//           required
//         />
//       </div>
//       <div>
//         <label>Number of Projects</label>
//         <input
//           type="number"
//           style={{color: "black"}}
//           value={projects}
//           onChange={(e) => setProjects(e.target.value)}
//           placeholder="Enter number of projects"
//           required
//         />
//       </div>
//       <div>
//         <label>Salary Expectation ($)</label>
//         <input
//           type="number"
//           style={{color: "black"}}
//           value={salary}
//           onChange={(e) => setSalary(e.target.value)}
//           placeholder="Enter salary expectation"
//           required
//         />
//       </div>
//       <button type="submit" className="button-primary">
//         Predict Chances
//       </button>
//       {error && (
//         <div className="alert alert-error">
//           {error}
//         </div>
//       )}
//       {chance && (
//         <div className="alert alert-success">
//           Your selection chance: {chance.toFixed(2)}%
//         </div>
//       )}
//     </form>
//   );
// };

// export default Predict;

//26 october




//27 october working 2nd iteration pikachu
// import React, { useState, useMemo } from 'react';
// import axios from 'axios';
// import {
//   Chart as ChartJS,
//   LineElement,
//   PointElement,
//   LinearScale,
//   TimeScale,
//   Title,
//   Tooltip,
//   Legend,
//   CategoryScale
// } from 'chart.js';
// import { Line } from 'react-chartjs-2';
// import 'chartjs-adapter-date-fns';
// import './Predict.css';

// ChartJS.register(
//   LineElement,
//   PointElement,
//   LinearScale,
//   TimeScale,
//   Title,
//   Tooltip,
//   Legend,
//   CategoryScale
// );

// function Predict() {
//   const [resumeFile, setResumeFile] = useState(null);
//   const [jobDescription, setJobDescription] = useState('');
//   const [experienceYears, setExperienceYears] = useState('');
//   const [results, setResults] = useState({
//     atsScore: null,
//     improvementTips: [],
//     roleAlignment: null,
//     skillGap: null,
//     selectionProbability: null,
//     salaryEstimate: null,
//     recommendedCompanies: [],
//     scoreHistory: []
//   });
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState('');

//   const handleFileChange = (e) => {
//     setResumeFile(e.target.files[0] || null);
//     setError('');
//   };

//   const handleAnalyze = async () => {
//     if (!resumeFile) {
//       setError('Please upload a resume (PDF format).');
//       return;
//     }
//     if (!experienceYears || isNaN(experienceYears) || Number(experienceYears) < 0) {
//       setError('Please enter valid years of experience.');
//       return;
//     }

//     setLoading(true);
//     setError('');
//     const formData = new FormData();
//     formData.append('resume', resumeFile);
//     formData.append('experience_years', experienceYears);
//     formData.append('job_description', jobDescription);
//     formData.append('user_id', 'default_user');

//     try {
//       // Run requests concurrently and handle individual failures safely
//       const [
//         atsResponse,
//         tipsResponse,
//         alignmentResponse,
//         skillGapResponse,
//         selectionResponse,
//         salaryResponse,
//         companiesResponse,
//         historyResponse
//       ] = await Promise.all([
//         axios.post('http://localhost:5000/api/ats-score', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' }
//         }).catch((err) => ({ data: null })),
//         axios.post('http://localhost:5000/api/improvement-tips', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' }
//         }).catch(() => ({ data: [] })),
//         jobDescription
//           ? axios.post('http://localhost:5000/api/role-alignment', formData, {
//               headers: { 'Content-Type': 'multipart/form-data' }
//             }).catch(() => ({ data: null }))
//           : Promise.resolve({ data: null }),
//         axios.post('http://localhost:5000/api/skill-gap', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' }
//         }).catch(() => ({ data: null })),
//         axios.post('http://localhost:5000/api/predict-selection', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' }
//         }).catch(() => ({ data: null })),
//         axios.post('http://localhost:5000/api/salary-estimate', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' }
//         }).catch(() => ({ data: null })),
//         axios.post('http://localhost:5000/api/recommend-companies', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' }
//         }).catch(() => ({ data: { recommended_companies: [] } })),
//         axios.get('http://localhost:5000/api/score-history?user_id=default_user')
//           .catch(() => ({ data: { score_history: [] } }))
//       ]);

//       // normalize / defensive parsing of responses
//       const atsData = atsResponse?.data || null;
//       const tipsData = Array.isArray(tipsResponse?.data)
//         ? tipsResponse.data
//         : tipsResponse?.data?.improvement_tips || [];
//       const alignmentData = alignmentResponse?.data || null;
//       const skillGapData = skillGapResponse?.data || null;
//       const selectionData = selectionResponse?.data || null;
//       const salaryData = salaryResponse?.data || null;
//       const companiesData = companiesResponse?.data?.recommended_companies || [];
//       const historyData = historyResponse?.data?.score_history || [];

//       setResults({
//         atsScore: atsData,
//         improvementTips: tipsData,
//         roleAlignment: alignmentData,
//         skillGap: skillGapData,
//         selectionProbability: selectionData,
//         salaryEstimate: salaryData,
//         recommendedCompanies: companiesData,
//         scoreHistory: historyData
//       });
//     } catch (err) {
//       console.error('Analysis error:', err);
//       setError('Failed to analyze resume. Please check your inputs and try again.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const chartData = useMemo(() => {
//     const dataset = (results.scoreHistory || []).map((entry) => {
//       // expected entry shape: { timestamp: "...", ats_score: 78 }
//       const t = entry.timestamp ? new Date(entry.timestamp) : new Date();
//       const y = typeof entry.ats_score === 'number' ? entry.ats_score : Number(entry.ats_score) || 0;
//       return { x: t, y };
//     });

//     return {
//       datasets: [
//         {
//           label: 'ATS Score Over Time',
//           data: dataset,
//           fill: true,
//           tension: 0.3,
//           // color choices are left to CSS or default; react-chartjs-2 will apply defaults
//           borderWidth: 2,
//           pointRadius: 4
//         }
//       ]
//     };
//   }, [results.scoreHistory]);

//   const chartOptions = useMemo(() => ({
//     responsive: true,
//     maintainAspectRatio: false,
//     scales: {
//       x: {
//         type: 'time',
//         time: {
//           unit: 'day'
//         },
//         title: {
//           display: true,
//           text: 'Date'
//         }
//       },
//       y: {
//         beginAtZero: true,
//         max: 100,
//         title: {
//           display: true,
//           text: 'ATS Score'
//         }
//       }
//     },
//     plugins: {
//       legend: {
//         display: true,
//         position: 'top'
//       },
//       tooltip: {
//         callbacks: {
//           label: (context) => `Score: ${context.parsed.y}`
//         }
//       }
//     }
//   }), []);

//   const formatCurrency = (value) => {
//     if (!value && value !== 0) return 'N/A';
//     try {
//       const num = Number(value);
//       if (Number.isNaN(num)) return String(value);
//       return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(num);
//     } catch {
//       return String(value);
//     }
//   };

//   return (
//     <div className="predict-container">
//       <h2>Resume Analysis</h2>

//       <div className="input-section">
//         <label className="file-label">
//           Upload Resume (PDF):
//           <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} />
//         </label>

//         <label>
//           Years of Experience:
//           <input
//             type="number"
//             placeholder="Enter years"
//             value={experienceYears}
//             onChange={(e) => setExperienceYears(e.target.value)}
//             min="0"
//           />
//         </label>

//         <label>
//           Job Description (Optional):
//           <textarea
//             placeholder="Paste job description here"
//             value={jobDescription}
//             onChange={(e) => setJobDescription(e.target.value)}
//           />
//         </label>

//         <div className="button-row">
//           <button onClick={handleAnalyze} disabled={loading}>
//             {loading ? 'Analyzing...' : 'Analyze Resume'}
//           </button>
//         </div>

//         {error && <p className="error">{error}</p>}
//       </div>

//       <div className="results-section">
//         {results.atsScore && (
//           <div className="card">
//             <h3>ATS Score</h3>
//             <p>
//               Score:{' '}
//               {typeof results.atsScore.score === 'number'
//                 ? `${results.atsScore.score}/100`
//                 : results.atsScore.score ?? 'N/A'}
//             </p>
//             {results.atsScore.reasoning && <p>{results.atsScore.reasoning}</p>}
//           </div>
//         )}

//         {results.improvementTips && results.improvementTips.length > 0 && (
//           <div className="card">
//             <h3>Improvement Tips</h3>
//             <ul>
//               {results.improvementTips.map((tip, index) => (
//                 <li key={index}>
//                   {tip.category ? <strong>{tip.category}: </strong> : null}
//                   {tip.priority ? `(${tip.priority}) ` : null}
//                   {tip.tip || tip}
//                 </li>
//               ))}
//             </ul>
//           </div>
//         )}

//         {results.roleAlignment && (
//           <div className="card">
//             <h3>Job Role Alignment</h3>
//             <p>Similarity: {results.roleAlignment.similarity_percentage ?? results.roleAlignment.similarity ?? 'N/A'}%</p>
//             <p>
//               Missing Keywords:{' '}
//               {Array.isArray(results.roleAlignment.missing_keywords) ? results.roleAlignment.missing_keywords.join(', ') : (results.roleAlignment.missing_keywords || 'None')}
//             </p>
//             <p>
//               Strengths:{' '}
//               {Array.isArray(results.roleAlignment.strengths) ? results.roleAlignment.strengths.join(', ') : (results.roleAlignment.strengths || 'None')}
//             </p>
//           </div>
//         )}

//         {results.skillGap && (
//           <div className="card">
//             <h3>Skill Gap Analysis</h3>
//             <p>Your Skills: {Array.isArray(results.skillGap.user_skills) ? results.skillGap.user_skills.join(', ') : (results.skillGap.user_skills || 'None')}</p>
//             <p>Top Skills: {Array.isArray(results.skillGap.top_skills) ? results.skillGap.top_skills.join(', ') : (results.skillGap.top_skills || 'None')}</p>
//             <p>Missing Skills: {Array.isArray(results.skillGap.missing_skills) ? results.skillGap.missing_skills.join(', ') : (results.skillGap.missing_skills || 'None')}</p>
//             {results.skillGap.recommendation && <p>{results.skillGap.recommendation}</p>}
//           </div>
//         )}

//         {results.selectionProbability && (
//           <div className="card">
//             <h3>Selection Probability</h3>
//             <p>
//               {typeof results.selectionProbability.selection_probability === 'number'
//                 ? `${Math.round(results.selectionProbability.selection_probability)}%`
//                 : results.selectionProbability.selection_probability ?? results.selectionProbability.probability ?? 'N/A'}
//             </p>
//           </div>
//         )}

//         {results.salaryEstimate && (
//           <div className="card">
//             <h3>Salary Estimation</h3>
//             <p>Estimated Salary: {formatCurrency(results.salaryEstimate.estimated_salary ?? results.salaryEstimate)}</p>
//           </div>
//         )}

//         {results.recommendedCompanies && results.recommendedCompanies.length > 0 && (
//           <div className="card">
//             <h3>Recommended Companies</h3>
//             <ul>
//               {results.recommendedCompanies.map((company, index) => (
//                 <li key={index}>{company}</li>
//               ))}
//             </ul>
//           </div>
//         )}

//         {results.scoreHistory && results.scoreHistory.length > 0 && (
//           <div className="card chart-card" style={{ height: '300px' }}>
//             <h3>Score History</h3>
//             <Line data={chartData} options={chartOptions} />
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default Predict;


// import React, { useState } from 'react';
// import axios from 'axios';

// const Predict = () => {
//   const [file, setFile] = useState(null);
//   const [experienceYears, setExperienceYears] = useState('');
//   const [jobDescription, setJobDescription] = useState('');
//   const [results, setResults] = useState({});
//   const [loading, setLoading] = useState(false);

//   const handleAnalyze = async () => {
//     if (!file || !experienceYears) {
//       alert('Please upload a resume and enter experience years.');
//       return;
//     }

//     setLoading(true);
//     const formData = new FormData();
//     formData.append('resume', file);
//     formData.append('experience_years', experienceYears);
//     formData.append('job_description', jobDescription);

//     try {
//       const requests = [
//         { url: '/api/ats-score', key: 'atsScore' },
//         { url: '/api/improvement-tips', key: 'improvementTips' },
//         { url: '/api/role-alignment', key: 'roleAlignment' },
//         { url: '/api/skill-gap', key: 'skillGap' },
//         { url: '/api/predict-selection', key: 'selectionProbability' },
//         { url: '/api/salary-estimate', key: 'salaryEstimate' },
//         { url: '/api/recommend-companies', key: 'recommendedCompanies' },
//       ];

//       const newResults = {};
//       for (const req of requests) {
//         const response = await axios.post(`http://localhost:5000${req.url}`, formData, {
//           headers: { 'Content-Type': 'multipart/form-data' },
//         });
//         newResults[req.key] = response.data;
//         // Wait 4 seconds between requests to respect ~15 RPM limit for gemini-2.5-flash
//         if (req.url !== '/api/predict-selection' && req.url !== '/api/salary-estimate') {
//           await new Promise(resolve => setTimeout(resolve, 4000));
//         }
//       }

//       setResults(newResults);
//     } catch (error) {
//       console.error(`Error analyzing resume: ${error.message}`);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div>
//       <input type="file" onChange={(e) => setFile(e.target.files[0])} />
//       <input
//         type="number"
//         value={experienceYears}
//         onChange={(e) => setExperienceYears(e.target.value)}
//         placeholder="Experience Years"
//       />
//       <textarea
//         value={jobDescription}
//         onChange={(e) => setJobDescription(e.target.value)}
//         placeholder="Job Description"
//       />
//       <button onClick={handleAnalyze} disabled={loading}>
//         {loading ? 'Analyzing...' : 'Analyze Resume'}
//       </button>
//       {loading && <p>Processing...</p>}
//       {results.atsScore && <div>ATS Score: {results.atsScore.score} - {results.atsScore.reasoning}</div>}
//       {results.improvementTips && (
//         <div>
//           Improvement Tips:
//           <ul>{results.improvementTips.map((tip, i) => <li key={i}>{tip.category}: {tip.tip} ({tip.priority})</li>)}</ul>
//         </div>
//       )}
//       {results.roleAlignment && (
//         <div>
//           Role Alignment: {results.roleAlignment.similarity_percentage}% (Missing: {results.roleAlignment.missing_keywords.join(', ')}, Strengths: {results.roleAlignment.strengths.join(', ')})
//         </div>
//       )}
//       {results.skillGap && (
//         <div>
//           Skill Gap: User Skills: {results.skillGap.user_skills.join(', ')}, Missing: {results.skillGap.missing_skills.join(', ')}, Recommendation: {results.skillGap.recommendation}
//         </div>
//       )}
//       {results.selectionProbability && <div>Selection Probability: {results.selectionProbability.selection_probability}%</div>}
//       {results.salaryEstimate && <div>Salary Estimate: ${results.salaryEstimate.estimated_salary}</div>}
//       {results.recommendedCompanies && (
//         <div>
//           Recommended Companies:
//           <ul>{results.recommendedCompanies.companies.map((co, i) => <li key={i}>{co.name}: {co.reason}</li>)}</ul>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Predict;


//bad friends-it does work but not very nice

// import React, { useState } from 'react';
// import axios from 'axios';

// const Predict = () => {
//   const [file, setFile] = useState(null);
//   const [experienceYears, setExperienceYears] = useState('');
//   const [jobDescription, setJobDescription] = useState('');
//   const [results, setResults] = useState({});
//   const [loading, setLoading] = useState(false);

//   const handleAnalyze = async () => {
//     if (!file || !experienceYears) {
//       alert('Please upload a resume and enter experience years.');
//       return;
//     }

//     setLoading(true);
//     const formData = new FormData();
//     formData.append('resume', file);
//     formData.append('experience_years', experienceYears);
//     formData.append('job_description', jobDescription);

//     try {
//       const requests = [
//         { url: '/api/ats-score', key: 'atsScore' },
//         { url: '/api/improvement-tips', key: 'improvementTips' },
//         { url: '/api/role-alignment', key: 'roleAlignment' },
//         { url: '/api/skill-gap', key: 'skillGap' },
//         { url: '/api/predict-selection', key: 'selectionProbability' },
//         { url: '/api/salary-estimate', key: 'salaryEstimate' },
//         { url: '/api/recommend-companies', key: 'recommendedCompanies' },
//       ];

//       const newResults = {};
//       for (const req of requests) {
//         const response = await axios.post(`http://localhost:5000${req.url}`, formData, {
//           headers: { 'Content-Type': 'multipart/form-data' },
//         });
//         newResults[req.key] = response.data;
//         if (req.url !== '/api/predict-selection' && req.url !== '/api/salary-estimate') {
//           await new Promise(resolve => setTimeout(resolve, 4000));
//         }
//       }

//       setResults(newResults);
//     } catch (error) {
//       console.error(`Error analyzing resume: ${error.message}`);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div>
//       <input type="file" onChange={(e) => setFile(e.target.files[0])} />
//       <input
//         type="number"
//         value={experienceYears}
//         onChange={(e) => setExperienceYears(e.target.value)}
//         placeholder="Experience Years"
//       />
//       <textarea
//         value={jobDescription}
//         onChange={(e) => setJobDescription(e.target.value)}
//         placeholder="Job Description"
//       />
//       <button onClick={handleAnalyze} disabled={loading}>
//         {loading ? 'Analyzing...' : 'Analyze Resume'}
//       </button>
//       {loading && <p>Processing...</p>}
//       {results.atsScore && (
//         <div>
//           ATS Score: {results.atsScore.score} - {results.atsScore.reasoning}
//           {results.atsScore.improvement_tips && results.atsScore.improvement_tips.length > 0 && (
//             <div>
//               Improvement Tips:
//               <ul>
//                 {results.atsScore.improvement_tips.map((tip, i) => (
//                   <li key={i}>{tip.tip} ({tip.priority})</li>
//                 ))}
//               </ul>
//             </div>
//           )}
//         </div>
//       )}
//       {results.improvementTips && results.improvementTips.tips && results.improvementTips.tips.length > 0 && (
//         <div>
//           Additional Improvement Tips:
//           <ul>
//             {results.improvementTips.tips.map((tip, i) => (
//               <li key={i}>{tip.category}: {tip.tip} ({tip.priority})</li>
//             ))}
//           </ul>
//         </div>
//       )}
//       {results.roleAlignment && (
//         <div>
//           Role Alignment: {results.roleAlignment.similarity_percentage}% (Missing: {results.roleAlignment.missing_keywords.join(', ')}, Strengths: {results.roleAlignment.strengths.join(', ')})
//         </div>
//       )}
//       {results.skillGap && (
//         <div>
//           Skill Gap: User Skills: {results.skillGap.user_skills.join(', ')}, Missing: {results.skillGap.missing_skills.join(', ')}, Recommendation: {results.skillGap.recommendation}
//         </div>
//       )}
//       {results.selectionProbability && <div>Selection Probability: {results.selectionProbability.selection_probability}%</div>}
//       {results.salaryEstimate && <div>Salary Estimate: ${results.salaryEstimate.estimated_salary}</div>}
//       {results.recommendedCompanies && results.recommendedCompanies.companies && results.recommendedCompanies.companies.length > 0 && (
//         <div>
//           Recommended Companies:
//           <ul>
//             {results.recommendedCompanies.companies.map((co, i) => <li key={i}>{co.name}: {co.reason}</li>)}
//           </ul>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Predict;



//the chronicals of rru san-gives fallback response

// import React, { useState } from 'react';
// import axios from 'axios';

// const Predict = () => {
//   const [file, setFile] = useState(null);
//   const [experienceYears, setExperienceYears] = useState('');
//   const [jobDescription, setJobDescription] = useState('');
//   const [results, setResults] = useState({});
//   const [loading, setLoading] = useState(false);

//   const handleAnalyze = async () => {
//     if (!file || !experienceYears) {
//       alert('Please upload a resume and enter experience years.');
//       return;
//     }

//     setLoading(true);
//     const formData = new FormData();
//     formData.append('resume', file);
//     formData.append('experience_years', experienceYears);
//     formData.append('job_description', jobDescription);

//     try {
//       const requests = [
//         { url: '/api/ats-score', key: 'atsScore' },
//         { url: '/api/improvement-tips', key: 'improvementTips' },
//         { url: '/api/role-alignment', key: 'roleAlignment' },
//         { url: '/api/skill-gap', key: 'skillGap' },
//         { url: '/api/predict-selection', key: 'selectionProbability' },
//         { url: '/api/salary-estimate', key: 'salaryEstimate' },
//         { url: '/api/recommend-companies', key: 'recommendedCompanies' },
//       ];

//       const newResults = {};
//       for (const req of requests) {
//         const response = await axios.post(`http://localhost:5000${req.url}`, formData, {
//           headers: { 'Content-Type': 'multipart/form-data' },
//         });
//         newResults[req.key] = response.data;
//         if (req.url !== '/api/predict-selection' && req.url !== '/api/salary-estimate') {
//           await new Promise(resolve => setTimeout(resolve, 4000));
//         }
//       }

//       setResults(newResults);
//     } catch (error) {
//       console.error(`Error analyzing resume: ${error.message}`);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div>
//       <input type="file" onChange={(e) => setFile(e.target.files[0])} />
//       <input
//         type="number"
//         value={experienceYears}
//         onChange={(e) => setExperienceYears(e.target.value)}
//         placeholder="Experience Years"
//       />
//       <textarea
//         value={jobDescription}
//         onChange={(e) => setJobDescription(e.target.value)}
//         placeholder="Job Description"
//       />
//       <button onClick={handleAnalyze} disabled={loading}>
//         {loading ? 'Analyzing...' : 'Analyze Resume'}
//       </button>
//       {loading && <p>Processing...</p>}
//       {results.atsScore && (
//         <div>
//           ATS Score: {results.atsScore.score || 80} - {results.atsScore.reasoning || 'Default reasoning due to JSON parsing error'}
//           {results.atsScore.improvement_tips && results.atsScore.improvement_tips.length > 0 && (
//             <div>
//               Improvement Tips:
//               <ul>
//                 {results.atsScore.improvement_tips.map((tip, i) => (
//                   <li key={i}>{tip.tip} ({tip.priority})</li>
//                 ))}
//               </ul>
//             </div>
//           )}
//         </div>
//       )}
//       {results.improvementTips && results.improvementTips.tips && results.improvementTips.tips.length > 0 && (
//         <div>
//           Additional Improvement Tips:
//           <ul>
//             {results.improvementTips.tips.map((tip, i) => (
//               <li key={i}>{tip.category}: {tip.tip} ({tip.priority})</li>
//             ))}
//           </ul>
//         </div>
//       )}
//       {results.roleAlignment && (
//         <div>
//           Role Alignment: {results.roleAlignment.similarity_percentage || 50}% (Missing: {results.roleAlignment.missing_keywords?.join(', ') || ''}, Strengths: {results.roleAlignment.strengths?.join(', ') || ''})
//         </div>
//       )}
//       {results.skillGap && (
//         <div>
//           Skill Gap: User Skills: {results.skillGap.user_skills?.join(', ') || ''}, Missing: {results.skillGap.missing_skills?.join(', ') || ''}, Recommendation: {results.skillGap.recommendation || 'Consider learning more skills'}
//         </div>
//       )}
//       {results.selectionProbability && <div>Selection Probability: {results.selectionProbability.selection_probability || 0}%</div>}
//       {results.salaryEstimate && <div>Salary Estimate: ${results.salaryEstimate.estimated_salary || 0}</div>}
//       {results.recommendedCompanies && results.recommendedCompanies.companies && results.recommendedCompanies.companies.length > 0 && (
//         <div>
//           Recommended Companies:
//           <ul>
//             {results.recommendedCompanies.companies.map((co, i) => <li key={i}>{co.name}: {co.reason}</li>)}
//           </ul>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Predict;

// import React, { useState } from 'react';
// import axios from 'axios';

// const Predict = () => {
//   const [file, setFile] = useState(null);
//   const [experienceYears, setExperienceYears] = useState('');
//   const [jobDescription, setJobDescription] = useState('');
//   const [results, setResults] = useState({});
//   const [loading, setLoading] = useState(false);

//   const handleAnalyze = async () => {
//     if (!file || !experienceYears) {
//       alert('Please upload a resume and enter experience years.');
//       return;
//     }

//     setLoading(true);
//     const formData = new FormData();
//     formData.append('resume', file);
//     formData.append('experience_years', experienceYears);
//     formData.append('job_description', jobDescription);

//     try {
//       const requests = [
//         { url: '/api/ats-score', key: 'atsScore' },
//         { url: '/api/improvement-tips', key: 'improvementTips' },
//         { url: '/api/role-alignment', key: 'roleAlignment' },
//         { url: '/api/skill-gap', key: 'skillGap' },
//         { url: '/api/predict-selection', key: 'selectionProbability' },
//         { url: '/api/salary-estimate', key: 'salaryEstimate' },
//         { url: '/api/recommend-companies', key: 'recommendedCompanies' },
//       ];

//       const newResults = {};
//       for (const req of requests) {
//         const response = await axios.post(`http://localhost:5000${req.url}`, formData, {
//           headers: { 'Content-Type': 'multipart/form-data' },
//         });

//         // Log raw response before any processing
//         console.log(`Raw response for ${req.url}:`, JSON.stringify(response.data, null, 2));

//         // Assign raw response data, with fallbacks only if specific keys are missing
//         let processedData = { ...response.data };
//         if (req.key === 'atsScore') {
//           processedData = {
//             ...processedData,
//             score: response.data.score !== undefined ? response.data.score : 80,
//             reasoning: response.data.reasoning || 'Default reasoning',
//             improvement_tips: Array.isArray(response.data.improvement_tips) ? response.data.improvement_tips : [{ tip: 'Add relevant keywords', priority: 'High' }],
//           };
//         } else if (req.key === 'improvementTips') {
//           processedData = {
//             ...processedData,
//             tips: Array.isArray(response.data.tips) ? response.data.tips : [{ category: 'General', tip: 'Failed to parse tips', priority: 'Low' }],
//           };
//         } else if (req.key === 'roleAlignment') {
//           processedData = {
//             ...processedData,
//             similarity_percentage: response.data.similarity_percentage !== undefined ? response.data.similarity_percentage : 50,
//             missing_keywords: Array.isArray(response.data.missing_keywords) ? response.data.missing_keywords : [],
//             strengths: Array.isArray(response.data.strengths) ? response.data.strengths : [],
//           };
//         } else if (req.key === 'skillGap') {
//           processedData = {
//             ...processedData,
//             user_skills: Array.isArray(response.data.user_skills) ? response.data.user_skills : [],
//             top_skills: Array.isArray(response.data.top_skills) ? response.data.top_skills : [],
//             missing_skills: Array.isArray(response.data.missing_skills) ? response.data.missing_skills : [],
//             recommendation: response.data.recommendation || 'Consider learning more skills',
//           };
//         } else if (req.key === 'selectionProbability') {
//           processedData = {
//             ...processedData,
//             selection_probability: response.data.selection_probability !== undefined ? response.data.selection_probability : 0,
//           };
//         } else if (req.key === 'salaryEstimate') {
//           processedData = {
//             ...processedData,
//             estimated_salary: response.data.estimated_salary !== undefined ? response.data.estimated_salary : 0,
//           };
//         } else if (req.key === 'recommendedCompanies') {
//           processedData = {
//             ...processedData,
//             companies: Array.isArray(response.data.companies) ? response.data.companies : [{ name: 'Default Company', reason: 'Failed to parse recommendations' }],
//           };
//         }

//         newResults[req.key] = processedData;
//       }

//       console.log('Final results object:', JSON.stringify(newResults, null, 2)); // Debug final state
//       setResults(newResults);
//     } catch (error) {
//       console.error(`Error analyzing resume: ${error.message}`, error.response?.data || 'No response data');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div>
//       <input type="file" onChange={(e) => setFile(e.target.files[0])} />
//       <input
//         type="number"
//         value={experienceYears}
//         onChange={(e) => setExperienceYears(e.target.value)}
//         placeholder="Experience Years"
//       />
//       <textarea
//         value={jobDescription}
//         onChange={(e) => setJobDescription(e.target.value)}
//         placeholder="Job Description"
//       />
//       <button onClick={handleAnalyze} disabled={loading}>
//         {loading ? 'Analyzing...' : 'Analyze Resume'}
//       </button>
//       {loading && <p>Processing...</p>}
//       {results.atsScore && (
//         <div>
//           ATS Score: {results.atsScore.score} - {results.atsScore.reasoning}
//           {Array.isArray(results.atsScore.improvement_tips) && results.atsScore.improvement_tips.length > 0 && (
//             <div>
//               Improvement Tips:
//               <ul>
//                 {results.atsScore.improvement_tips.map((tip, i) => (
//                   <li key={i}>{tip.tip} ({tip.priority})</li>
//                 ))}
//               </ul>
//             </div>
//           )}
//         </div>
//       )}
//       {results.improvementTips && Array.isArray(results.improvementTips.tips) && results.improvementTips.tips.length > 0 && (
//         <div>
//           Additional Improvement Tips:
//           <ul>
//             {results.improvementTips.tips.map((tip, i) => (
//               <li key={i}>{tip.category}: {tip.tip} ({tip.priority})</li>
//             ))}
//           </ul>
//         </div>
//       )}
//       {results.roleAlignment && (
//         <div>
//           Role Alignment: {results.roleAlignment.similarity_percentage}% (Missing: {results.roleAlignment.missing_keywords.join(', ')}, Strengths: {results.roleAlignment.strengths.join(', ')})
//         </div>
//       )}
//       {results.skillGap && (
//         <div>
//           Skill Gap: User Skills: {results.skillGap.user_skills.join(', ')}, Missing: {results.skillGap.missing_skills.join(', ')}, Recommendation: {results.skillGap.recommendation}
//         </div>
//       )}
//       {results.selectionProbability && <div>Selection Probability: {results.selectionProbability.selection_probability}%</div>}
//       {results.salaryEstimate && <div>Salary Estimate: ${results.salaryEstimate.estimated_salary || 0}</div>}
//       {results.recommendedCompanies && Array.isArray(results.recommendedCompanies.companies) && results.recommendedCompanies.companies.length > 0 && (
//         <div>
//           Recommended Companies:
//           <ul>
//             {results.recommendedCompanies.companies.map((co, i) => <li key={i}>{co.name}: {co.reason}</li>)}
//           </ul>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Predict;














//it does work=>meowwwwwwwwwwww

// import React, { useState } from 'react';
// import axios from 'axios';

// const Predict = () => {
//   const [file, setFile] = useState(null);
//   const [experienceYears, setExperienceYears] = useState('');
//   const [jobDescription, setJobDescription] = useState('');
//   const [results, setResults] = useState({});
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleAnalyze = async () => {
//     if (!file || !experienceYears) {
//       alert('Please upload a resume and enter experience years.');
//       return;
//     }

//     setLoading(true);
//     setError(null);
//     setResults({});

//     const formData = new FormData();
//     formData.append('resume', file);
//     formData.append('experience_years', experienceYears);
//     formData.append('job_description', jobDescription);

//     try {
//       const requests = [
//         { url: '/api/ats-score', key: 'atsScore' },
//         { url: '/api/improvement-tips', key: 'improvementTips' },
//         { url: '/api/role-alignment', key: 'roleAlignment' },
//         { url: '/api/skill-gap', key: 'skillGap' },
//         { url: '/api/predict-selection', key: 'selectionProbability' },
//         { url: '/api/salary-estimate', key: 'salaryEstimate' },
//         { url: '/api/recommend-companies', key: 'recommendedCompanies' },
//       ];

//       const newResults = {};
      
//       for (const req of requests) {
//         try {
//           const response = await axios.post(`http://localhost:5000${req.url}`, formData, {
//             headers: { 'Content-Type': 'multipart/form-data' },
//           });

//           console.log(`Response for ${req.key}:`, response.data);
          
//           // Store the response data directly without modification
//           newResults[req.key] = response.data;
          
//         } catch (err) {
//           console.error(`Error fetching ${req.key}:`, err.response?.data || err.message);
//           // Store error info instead of crashing
//           newResults[req.key] = { error: err.response?.data?.error || err.message };
//         }
//       }

//       console.log('Final results:', newResults);
//       setResults(newResults);
      
//     } catch (error) {
//       console.error('Error analyzing resume:', error);
//       setError(error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
//       <h2>Resume Analysis</h2>
      
//       <div style={{ marginBottom: '15px' }}>
//         <label style={{ display: 'block', marginBottom: '5px' }}>Resume (PDF):</label>
//         <input 
//           type="file" 
//           accept=".pdf"
//           onChange={(e) => setFile(e.target.files[0])} 
//         />
//       </div>

//       <div style={{ marginBottom: '15px' }}>
//         <label style={{ display: 'block', marginBottom: '5px' }}>Experience Years:</label>
//         <input
//           type="number"
//           value={experienceYears}
//           onChange={(e) => setExperienceYears(e.target.value)}
//           placeholder="e.g., 3"
//           style={{ width: '100%', padding: '8px' }}
//         />
//       </div>

//       <div style={{ marginBottom: '15px' }}>
//         <label style={{ display: 'block', marginBottom: '5px' }}>Job Description (Optional):</label>
//         <textarea
//           value={jobDescription}
//           onChange={(e) => setJobDescription(e.target.value)}
//           placeholder="Paste job description here..."
//           rows="4"
//           style={{ width: '100%', padding: '8px' }}
//         />
//       </div>

//       <button 
//         onClick={handleAnalyze} 
//         disabled={loading}
//         style={{ 
//           padding: '10px 20px', 
//           backgroundColor: loading ? '#ccc' : '#007bff',
//           color: 'white',
//           border: 'none',
//           borderRadius: '5px',
//           cursor: loading ? 'not-allowed' : 'pointer'
//         }}
//       >
//         {loading ? 'Analyzing...' : 'Analyze Resume'}
//       </button>

//       {loading && <p style={{ marginTop: '15px', color: '#007bff' }}>Processing your resume...</p>}
//       {error && <p style={{ marginTop: '15px', color: 'red' }}>Error: {error}</p>}

//       {/* Results Display */}
//       <div style={{ marginTop: '30px' }}>
//         {/* ATS Score */}
//         {results.atsScore && !results.atsScore.error && (
//           <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
//             <h3>ATS Score: {results.atsScore.score}/100</h3>
//             <p><strong>Reasoning:</strong> {results.atsScore.reasoning}</p>
//             {results.atsScore.improvement_tips && results.atsScore.improvement_tips.length > 0 && (
//               <div>
//                 <strong>Improvement Tips:</strong>
//                 <ul>
//                   {results.atsScore.improvement_tips.map((tip, i) => (
//                     <li key={i}>
//                       <strong>[{tip.priority}]</strong> {tip.tip}
//                     </li>
//                   ))}
//                 </ul>
//               </div>
//             )}
//           </div>
//         )}

//         {/* Additional Improvement Tips */}
//         {results.improvementTips && !results.improvementTips.error && results.improvementTips.tips && (
//           <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
//             <h3>Additional Improvement Tips</h3>
//             <ul>
//               {results.improvementTips.tips.map((tip, i) => (
//                 <li key={i}>
//                   <strong>{tip.category} [{tip.priority}]:</strong> {tip.tip}
//                 </li>
//               ))}
//             </ul>
//           </div>
//         )}

//         {/* Role Alignment */}
//         {results.roleAlignment && !results.roleAlignment.error && (
//           <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
//             <h3>Role Alignment: {results.roleAlignment.similarity_percentage}%</h3>
//             {results.roleAlignment.missing_keywords && results.roleAlignment.missing_keywords.length > 0 && (
//               <p><strong>Missing Keywords:</strong> {results.roleAlignment.missing_keywords.join(', ')}</p>
//             )}
//             {results.roleAlignment.strengths && results.roleAlignment.strengths.length > 0 && (
//               <p><strong>Strengths:</strong> {results.roleAlignment.strengths.join(', ')}</p>
//             )}
//           </div>
//         )}

//         {/* Skill Gap */}
//         {results.skillGap && !results.skillGap.error && (
//           <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
//             <h3>Skill Gap Analysis</h3>
//             {results.skillGap.user_skills && results.skillGap.user_skills.length > 0 && (
//               <p><strong>Your Skills:</strong> {results.skillGap.user_skills.join(', ')}</p>
//             )}
//             {results.skillGap.missing_skills && results.skillGap.missing_skills.length > 0 && (
//               <p><strong>Missing Skills:</strong> {results.skillGap.missing_skills.join(', ')}</p>
//             )}
//             {results.skillGap.recommendation && (
//               <p><strong>Recommendation:</strong> {results.skillGap.recommendation}</p>
//             )}
//           </div>
//         )}

//         {/* Selection Probability */}
//         {results.selectionProbability && !results.selectionProbability.error && (
//           <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
//             <h3>Selection Probability: {results.selectionProbability.selection_probability?.toFixed(2)}%</h3>
//           </div>
//         )}

//         {/* Salary Estimate */}
//         {results.salaryEstimate && !results.salaryEstimate.error && (
//           <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
//             <h3>Estimated Salary: ${results.salaryEstimate.estimated_salary?.toLocaleString()}</h3>
//           </div>
//         )}

//         {/* Recommended Companies */}
//         {results.recommendedCompanies && !results.recommendedCompanies.error && results.recommendedCompanies.companies && (
//           <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
//             <h3>Recommended Companies</h3>
//             <ul>
//               {results.recommendedCompanies.companies.map((company, i) => (
//                 <li key={i}>
//                   <strong>{company.name}:</strong> {company.reason}
//                 </li>
//               ))}
//             </ul>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Predict;


import React, { useState } from 'react';
import axios from 'axios';

const Predict = () => {
  const [file, setFile] = useState(null);
  const [experienceYears, setExperienceYears] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!file || !experienceYears) {
      alert('Please upload a resume and enter experience years.');
      return;
    }

    setLoading(true);
    setError(null);
    setResults({});

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('experience_years', experienceYears);
    formData.append('job_description', jobDescription);

    try {
      const requests = [
        { url: '/api/ats-score', key: 'atsScore' },
        { url: '/api/improvement-tips', key: 'improvementTips' },
        { url: '/api/role-alignment', key: 'roleAlignment' },
        { url: '/api/skill-gap', key: 'skillGap' },
        { url: '/api/recommend-companies', key: 'recommendedCompanies' },
      ];

      const newResults = {};
      
      for (const req of requests) {
        try {
          const response = await axios.post(`http://localhost:5000${req.url}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });

          console.log(`Response for ${req.key}:`, response.data);
          
          // Store the response data directly without modification
          newResults[req.key] = response.data;
          
        } catch (err) {
          console.error(`Error fetching ${req.key}:`, err.response?.data || err.message);
          // Store error info instead of crashing
          newResults[req.key] = { error: err.response?.data?.error || err.message };
        }
      }

      console.log('Final results:', newResults);
      setResults(newResults);
      
    } catch (error) {
      console.error('Error analyzing resume:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Resume Analysis</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Resume (PDF):</label>
        <input 
          type="file" 
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])} 
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Experience Years:</label>
        <input
          type="number"
          value={experienceYears}
          onChange={(e) => setExperienceYears(e.target.value)}
          placeholder="e.g., 3"
          style={{ width: '100%', padding: '8px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Job Description (Optional):</label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste job description here..."
          rows="4"
          style={{ width: '100%', padding: '8px' }}
        />
      </div>

      <button 
        onClick={handleAnalyze} 
        disabled={loading}
        style={{ 
          padding: '10px 20px', 
          backgroundColor: loading ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </button>

      {loading && <p style={{ marginTop: '15px', color: '#007bff' }}>Processing your resume...</p>}
      {error && <p style={{ marginTop: '15px', color: 'red' }}>Error: {error}</p>}

      {/* Results Display */}
      <div style={{ marginTop: '30px' }}>
        {/* ATS Score */}
        {results.atsScore && !results.atsScore.error && (
          <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h3>ATS Score: {results.atsScore.score}/100</h3>
            <p><strong>Reasoning:</strong> {results.atsScore.reasoning}</p>
            {results.atsScore.improvement_tips && results.atsScore.improvement_tips.length > 0 && (
              <div>
                <strong>Improvement Tips:</strong>
                <ul>
                  {results.atsScore.improvement_tips.map((tip, i) => (
                    <li key={i}>
                      <strong>[{tip.priority}]</strong> {tip.tip}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Additional Improvement Tips */}
        {results.improvementTips && !results.improvementTips.error && results.improvementTips.tips && (
          <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h3>Additional Improvement Tips</h3>
            <ul>
              {results.improvementTips.tips.map((tip, i) => (
                <li key={i}>
                  <strong>{tip.category} [{tip.priority}]:</strong> {tip.tip}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Role Alignment */}
        {results.roleAlignment && !results.roleAlignment.error && (
          <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h3>Role Alignment: {results.roleAlignment.similarity_percentage}%</h3>
            {results.roleAlignment.missing_keywords && results.roleAlignment.missing_keywords.length > 0 && (
              <p><strong>Missing Keywords:</strong> {results.roleAlignment.missing_keywords.join(', ')}</p>
            )}
            {results.roleAlignment.strengths && results.roleAlignment.strengths.length > 0 && (
              <p><strong>Strengths:</strong> {results.roleAlignment.strengths.join(', ')}</p>
            )}
          </div>
        )}

        {/* Skill Gap */}
        {results.skillGap && !results.skillGap.error && (
          <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h3>Skill Gap Analysis</h3>
            {results.skillGap.user_skills && results.skillGap.user_skills.length > 0 && (
              <p><strong>Your Skills:</strong> {results.skillGap.user_skills.join(', ')}</p>
            )}
            {results.skillGap.missing_skills && results.skillGap.missing_skills.length > 0 && (
              <p><strong>Missing Skills:</strong> {results.skillGap.missing_skills.join(', ')}</p>
            )}
            {results.skillGap.recommendation && (
              <p><strong>Recommendation:</strong> {results.skillGap.recommendation}</p>
            )}
          </div>
        )}

        {/* Recommended Companies */}
        {results.recommendedCompanies && !results.recommendedCompanies.error && results.recommendedCompanies.companies && (
          <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h3>Recommended Companies</h3>
            <ul>
              {results.recommendedCompanies.companies.map((company, i) => (
                <li key={i}>
                  <strong>{company.name}:</strong> {company.reason}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Predict;