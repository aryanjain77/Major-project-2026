

// import React, { useState } from 'react';
// import studyAssistantData from './study_assistant';

// const StudyAssistant = () => {
//   const [activeTab, setActiveTab] = useState('popular');
//   const [selectedJob, setSelectedJob] = useState(null);

//   const popularRoles = studyAssistantData.jobs;

//   const selectJob = (job) => {
//     setSelectedJob(job);
//   };

//   const getResourceIcon = (type) => {
//     return type === 'learning' ? '📚' : '💻';
//   };

//   return (
//     <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
//       {/* Header */}
//       <div className="bg-white rounded-lg shadow-md p-6 mb-6">
//         <h1 className="text-3xl font-bold text-gray-800 mb-2">
//           🎯 AI Study Assistant for Placements
//         </h1>
//         <p className="text-gray-600">
//           Explore top job roles and their skills with curated resources
//         </p>
//       </div>

//       {/* Navigation Tabs */}
//       <div className="bg-white rounded-lg shadow-md mb-6">
//         <div className="flex border-b">
//           {[
//             { id: 'popular', label: '🔥 Popular Roles', desc: 'Trending career paths' },
//             // Add other tabs (generator, tracker) if needed
//           ].map(tab => (
//             <button
//               key={tab.id}
//               onClick={() => setActiveTab(tab.id)}
//               className={`flex-1 p-4 text-left transition-colors ${
//                 activeTab === tab.id
//                   ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                   : 'hover:bg-gray-50 text-gray-600'
//               }`}
//             >
//               <div className="font-medium">{tab.label}</div>
//               <div className="text-sm opacity-75">{tab.desc}</div>
//             </button>
//           ))}
//         </div>
//       </div>

//       {/* Popular Roles Tab */}
//       {activeTab === 'popular' && (
//         <div className="bg-white rounded-lg shadow-md p-6">
//           <h2 className="text-2xl font-bold mb-6 text-gray-800">Popular Job Roles</h2>
//           <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
//             {popularRoles.map(role => (
//               <div key={role.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
//                 <h3 className="font-semibold text-gray-800 mb-2">{role.title}</h3>
//                 <p className="text-sm text-gray-600 mb-3">{role.description}</p>
//                 <div className="space-y-2 mb-4">
//                   <div className="flex justify-between text-sm">
//                     <span className="text-gray-500">Salary:</span>
//                     <span className="font-medium text-green-600">{role.avg_salary}</span>
//                   </div>
//                   <div className="flex justify-between text-sm">
//                     <span className="text-gray-500">Demand:</span>
//                     <span
//                       className={`font-medium ${
//                         role.demand === 'Very High' ? 'text-red-600' : 'text-orange-600'
//                       }`}
//                     >
//                       {role.demand}
//                     </span>
//                   </div>
//                 </div>
//                 <div className="mb-4">
//                   <div className="text-xs text-gray-500 mb-1">Key Skills:</div>
//                   <div className="flex flex-wrap gap-1">
//                     {role.skills.map(skill => (
//                       <span key={skill.name} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
//                         {skill.name}
//                       </span>
//                     ))}
//                   </div>
//                 </div>
//                 <button
//                   onClick={() => selectJob(role)}
//                   className="w-full bg-gray-600 text-white py-2 px-4 rounded-lg text-sm hover:bg-gray-700 transition-colors"
//                 >
//                   View Skills & Resources
//                 </button>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Skills Modal */}
//       {selectedJob && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
//           <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
//             <div className="p-6 border-b">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h3 className="text-xl font-bold text-gray-800">{selectedJob.title}</h3>
//                   <p className="text-gray-600 mt-1">{selectedJob.description}</p>
//                 </div>
//                 <button
//                   onClick={() => setSelectedJob(null)}
//                   className="text-gray-500 hover:text-gray-700 text-2xl"
//                 >
//                   ×
//                 </button>
//               </div>
//             </div>
//             <div className="p-6 overflow-y-auto max-h-[70vh]">
//               <h4 className="font-semibold text-gray-800 mb-4">📚 Skills & Resources</h4>
//               <div className="space-y-6">
//                 {selectedJob.skills.map(skill => (
//                   <div key={skill.name} className="border border-gray-200 rounded-lg p-4">
//                     <h5 className="font-medium text-gray-800 mb-2">{skill.name}</h5>
//                     {skill.resources.length > 0 ? (
//                       <div className="space-y-3">
//                         {skill.resources.map(resource => (
//                           <div
//                             key={resource.url}
//                             className="flex items-start justify-between p-3 bg-gray-50 rounded-lg"
//                           >
//                             <div>
//                               <div className="flex items-center gap-2">
//                                 <span className="text-lg">{getResourceIcon(resource.type)}</span>
//                                 <a
//                                   href={resource.url}
//                                   target="_blank"
//                                   rel="noopener noreferrer"
//                                   className="text-blue-600 hover:underline"
//                                 >
//                                   {resource.title}
//                                 </a>
//                               </div>
//                               <p className="text-sm text-gray-600">{resource.description}</p>
//                               <span className="text-xs text-gray-500">
//                                 Type: {resource.type}
//                               </span>
//                             </div>
//                           </div>
//                         ))}
//                       </div>
//                     ) : (
//                       <p className="text-sm text-gray-500">No resources available.</p>
//                     )}
//                   </div>
//                 ))}
//               </div>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default StudyAssistant;

// import React, { useState, useEffect } from 'react';
// import { Upload, Loader, CheckCircle, Clock, BookOpen, Target, TrendingUp } from 'lucide-react';

// const StudyAssistant = () => {
//   const [activeTab, setActiveTab] = useState('upload');
//   const [selectedJob, setSelectedJob] = useState(null);
//   const [popularRoles, setPopularRoles] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [resumeFile, setResumeFile] = useState(null);
//   const [analysisResult, setAnalysisResult] = useState(null);
//   const [selectedRoadmap, setSelectedRoadmap] = useState(null);
//   const [error, setError] = useState(null);
//   const [backendConnected, setBackendConnected] = useState(false);

//   useEffect(() => {
//     checkBackendConnection();
//     fetchPopularRoles();
//   }, []);

//   const checkBackendConnection = async () => {
//     try {
//       const response = await fetch('http://localhost:5000/');
//       if (response.ok) {
//         setBackendConnected(true);
//       }
//     } catch (error) {
//       setBackendConnected(false);
//       console.error('Backend not connected:', error);
//     }
//   };

//   const fetchPopularRoles = async () => {
//     try {
//       const response = await fetch('http://localhost:5000/api/roadmap/popular-roles');
//       if (!response.ok) {
//         throw new Error(`Server error: ${response.status}`);
//       }
//       const data = await response.json();
//       setPopularRoles(data.roles || []);
//     } catch (error) {
//       console.error('Error fetching popular roles:', error);
//       setError(`Backend connection failed. Make sure server is running on port 5000. Error: ${error.message}`);
//     }
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (file && file.type === 'application/pdf') {
//       setResumeFile(file);
//       setError(null);
//     } else {
//       setError('Please upload a PDF file');
//     }
//   };

//   const handleResumeUpload = async () => {
//     if (!resumeFile) {
//       setError('Please select a resume file');
//       return;
//     }

//     setLoading(true);
//     setError(null);

//     try {
//       const formData = new FormData();
//       formData.append('resume', resumeFile);

//       console.log('Uploading resume to backend...');
      
//       const response = await fetch('http://localhost:5000/api/roadmap/analyze-resume', {
//         method: 'POST',
//         body: formData,
//       });

//       console.log('Response status:', response.status);

//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.error || `Server error: ${response.status}`);
//       }

//       const data = await response.json();
//       console.log('Analysis result:', data);
      
//       setAnalysisResult(data);
//       setSelectedRoadmap(data.personalized_roadmap);
//       setActiveTab('roadmap');
//     } catch (error) {
//       const errorMessage = error.message || 'Failed to analyze resume';
//       setError(`${errorMessage}. Make sure the backend server is running on http://localhost:5000`);
//       console.error('Error analyzing resume:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleGenerateRoadmapForRole = async (role) => {
//     if (!analysisResult) return;

//     setLoading(true);
//     setError(null);

//     try {
//       const response = await fetch('http://localhost:5000/api/roadmap/generate-for-role', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           job_role: role,
//           career_info: analysisResult.career_analysis,
//         }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to generate roadmap');
//       }

//       const data = await response.json();
//       setSelectedRoadmap(data.roadmap);
//       setActiveTab('roadmap');
//     } catch (error) {
//       setError(error.message || 'Failed to generate roadmap');
//       console.error('Error generating roadmap:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const renderUploadTab = () => (
//     <div className="bg-white rounded-lg shadow-md p-8">
//       <div className="max-w-2xl mx-auto">
//         <div className="text-center mb-8">
//           <Upload className="w-16 h-16 mx-auto mb-4 text-blue-500" />
//           <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Your Resume</h2>
//           <p className="text-gray-600">
//             Get a personalized career roadmap based on your skills and experience
//           </p>
//         </div>

//         <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
//           <input
//             type="file"
//             accept=".pdf"
//             onChange={handleFileChange}
//             className="hidden"
//             id="resume-upload"
//           />
//           <label htmlFor="resume-upload" className="cursor-pointer">
//             <div className="space-y-2">
//               <div className="text-4xl">📄</div>
//               <div className="text-gray-600">
//                 {resumeFile ? resumeFile.name : 'Click to upload or drag and drop'}
//               </div>
//               <div className="text-sm text-gray-500">PDF files only</div>
//             </div>
//           </label>
//         </div>

//         {error && (
//           <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
//             {error}
//           </div>
//         )}

//         <button
//           onClick={handleResumeUpload}
//           disabled={!resumeFile || loading}
//           className="w-full mt-6 bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
//         >
//           {loading ? (
//             <>
//               <Loader className="w-5 h-5 animate-spin" />
//               Analyzing Resume...
//             </>
//           ) : (
//             <>
//               <Target className="w-5 h-5" />
//               Generate My Career Roadmap
//             </>
//           )}
//         </button>

//         <div className="mt-8 text-center">
//           <p className="text-gray-600 mb-4">Or explore popular career paths</p>
//           <button
//             onClick={() => setActiveTab('popular')}
//             className="text-blue-600 hover:text-blue-700 font-medium"
//           >
//             View Popular Roles →
//           </button>
//         </div>
//       </div>
//     </div>
//   );

//   const renderRoadmapTab = () => {
//     if (!selectedRoadmap) return null;

//     return (
//       <div className="space-y-6">
//         {analysisResult && (
//           <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-md p-6">
//             <h2 className="text-2xl font-bold text-gray-800 mb-4">
//               Your Personalized Career Path
//             </h2>
//             <div className="grid md:grid-cols-3 gap-4">
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <Target className="w-5 h-5 text-blue-600" />
//                   <h3 className="font-semibold text-gray-700">Primary Role</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900">
//                   {analysisResult.career_analysis.primary_role}
//                 </p>
//               </div>
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <TrendingUp className="w-5 h-5 text-green-600" />
//                   <h3 className="font-semibold text-gray-700">Experience Level</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900 capitalize">
//                   {analysisResult.career_analysis.experience_level}
//                 </p>
//               </div>
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <Clock className="w-5 h-5 text-purple-600" />
//                   <h3 className="font-semibold text-gray-700">Timeline</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900">
//                   {selectedRoadmap.total_estimated_weeks} weeks
//                 </p>
//               </div>
//             </div>

//             {analysisResult.career_analysis.skill_gaps && analysisResult.career_analysis.skill_gaps.length > 0 && (
//               <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
//                 <h4 className="font-semibold text-gray-700 mb-2">Skills to Develop:</h4>
//                 <div className="flex flex-wrap gap-2">
//                   {analysisResult.career_analysis.skill_gaps.map((skill, idx) => (
//                     <span
//                       key={idx}
//                       className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm"
//                     >
//                       {skill}
//                     </span>
//                   ))}
//                 </div>
//               </div>
//             )}
//           </div>
//         )}

//         {selectedRoadmap.personalized_intro && (
//           <div className="bg-white rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-3">Your Journey Begins</h3>
//             <p className="text-gray-700 leading-relaxed">{selectedRoadmap.personalized_intro}</p>
//           </div>
//         )}

//         <div className="bg-white rounded-lg shadow-md p-6">
//           <h3 className="text-xl font-bold text-gray-800 mb-6">Learning Roadmap</h3>
//           <div className="space-y-6">
//             {selectedRoadmap.phases && selectedRoadmap.phases.map((phase, phaseIdx) => (
//               <div key={phaseIdx} className="border border-gray-200 rounded-lg p-5">
//                 <div className="flex items-start justify-between mb-4">
//                   <div>
//                     <h4 className="text-lg font-semibold text-gray-800">
//                       Phase {phase.phase_number}: {phase.phase_name}
//                     </h4>
//                     <p className="text-gray-600 mt-1">{phase.description}</p>
//                     <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
//                       <span className="flex items-center gap-1">
//                         <Clock className="w-4 h-4" />
//                         {phase.duration_weeks} weeks
//                       </span>
//                     </div>
//                   </div>
//                 </div>

//                 <div className="space-y-3 mt-4">
//                   {phase.steps && phase.steps.map((step, stepIdx) => (
//                     <div key={stepIdx} className="bg-gray-50 rounded-lg p-4">
//                       <div className="flex items-start gap-3">
//                         <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
//                           {stepIdx + 1}
//                         </div>
//                         <div className="flex-1">
//                           <h5 className="font-medium text-gray-800">{step.title}</h5>
//                           <p className="text-sm text-gray-600 mt-1">{step.description}</p>
                          
//                           {step.key_topics && step.key_topics.length > 0 && (
//                             <div className="mt-2">
//                               <span className="text-xs text-gray-500">Key Topics:</span>
//                               <div className="flex flex-wrap gap-1 mt-1">
//                                 {step.key_topics.map((topic, idx) => (
//                                   <span
//                                     key={idx}
//                                     className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded"
//                                   >
//                                     {topic}
//                                   </span>
//                                 ))}
//                               </div>
//                             </div>
//                           )}

//                           <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
//                             <span>⏱️ {step.estimated_hours}h</span>
//                             <span className={`px-2 py-1 rounded ${
//                               step.priority === 'high' ? 'bg-red-100 text-red-700' :
//                               step.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
//                               'bg-green-100 text-green-700'
//                             }`}>
//                               {step.priority} priority
//                             </span>
//                           </div>
//                         </div>
//                       </div>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>

//         {analysisResult && analysisResult.alternative_careers && analysisResult.alternative_careers.length > 0 && (
//           <div className="bg-white rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-4">More Career Paths For You</h3>
//             <p className="text-gray-600 mb-6">Based on your skills and experience, you might also consider:</p>
//             <div className="grid md:grid-cols-2 gap-4">
//               {analysisResult.alternative_careers.map((career, idx) => (
//                 <div
//                   key={idx}
//                   className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors cursor-pointer"
//                   onClick={() => handleGenerateRoadmapForRole(career.role)}
//                 >
//                   <div className="flex items-start justify-between">
//                     <div className="flex-1">
//                       <h4 className="font-semibold text-gray-800">{career.role}</h4>
//                       <p className="text-sm text-gray-600 mt-1">{career.reason}</p>
//                     </div>
//                     <div className="flex-shrink-0 ml-4">
//                       <div className="text-2xl font-bold text-blue-600">
//                         {career.match_percentage}%
//                       </div>
//                       <div className="text-xs text-gray-500 text-center">match</div>
//                     </div>
//                   </div>
//                   <button className="mt-3 w-full text-sm text-blue-600 hover:text-blue-700 font-medium">
//                     Generate Roadmap →
//                   </button>
//                 </div>
//               ))}
//             </div>
//           </div>
//         )}

//         {selectedRoadmap.career_tips && selectedRoadmap.career_tips.length > 0 && (
//           <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-4">💡 Personalized Tips</h3>
//             <ul className="space-y-2">
//               {selectedRoadmap.career_tips.map((tip, idx) => (
//                 <li key={idx} className="flex items-start gap-2 text-gray-700">
//                   <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
//                   <span>{tip}</span>
//                 </li>
//               ))}
//             </ul>
//           </div>
//         )}
//       </div>
//     );
//   };

//   const renderPopularRolesTab = () => (
//     <div className="bg-white rounded-lg shadow-md p-6">
//       <h2 className="text-2xl font-bold mb-6 text-gray-800">More Career Roadmaps</h2>
//       <p className="text-gray-600 mb-6">
//         Explore these popular career paths to find the one that suits you best
//       </p>
//       <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
//         {popularRoles.map((role) => (
//           <div
//             key={role.id}
//             className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
//           >
//             <h3 className="font-semibold text-gray-800 mb-2">{role.title}</h3>
//             <p className="text-sm text-gray-600 mb-3">{role.description}</p>
//             <div className="space-y-2 mb-4">
//               <div className="flex justify-between text-sm">
//                 <span className="text-gray-500">Salary:</span>
//                 <span className="font-medium text-green-600">{role.avg_salary}</span>
//               </div>
//               <div className="flex justify-between text-sm">
//                 <span className="text-gray-500">Demand:</span>
//                 <span className={`font-medium ${
//                   role.demand === 'Very High' ? 'text-red-600' : 'text-orange-600'
//                 }`}>
//                   {role.demand}
//                 </span>
//               </div>
//             </div>
//             <div className="mb-4">
//               <div className="text-xs text-gray-500 mb-1">Key Skills:</div>
//               <div className="flex flex-wrap gap-1">
//                 {role.skills.map((skill, idx) => (
//                   <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
//                     {skill}
//                   </span>
//                 ))}
//               </div>
//             </div>
//             <button
//               onClick={() => setSelectedJob(role)}
//               className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg text-sm hover:bg-blue-700 transition-colors"
//             >
//               View Details
//             </button>
//           </div>
//         ))}
//       </div>
//     </div>
//   );

//   return (
//     <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
//       <div className="bg-white rounded-lg shadow-md p-6 mb-6">
//         <h1 className="text-3xl font-bold text-gray-800 mb-2">
//           🎯 AI Career Roadmap Generator
//         </h1>
//         <p className="text-gray-600">
//           Upload your resume for a personalized career path or explore popular roles
//         </p>
//       </div>

//       <div className="bg-white rounded-lg shadow-md mb-6">
//         <div className="flex border-b">
//           <button
//             onClick={() => setActiveTab('upload')}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'upload'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             }`}
//           >
//             <div className="font-medium">📤 Upload Resume</div>
//             <div className="text-sm opacity-75">Get personalized roadmap</div>
//           </button>
//           <button
//             onClick={() => setActiveTab('roadmap')}
//             disabled={!selectedRoadmap}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'roadmap'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             } ${!selectedRoadmap ? 'opacity-50 cursor-not-allowed' : ''}`}
//           >
//             <div className="font-medium">🗺️ Your Roadmap</div>
//             <div className="text-sm opacity-75">View your career path</div>
//           </button>
//           <button
//             onClick={() => setActiveTab('popular')}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'popular'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             }`}
//           >
//             <div className="font-medium">🔥 Popular Roles</div>
//             <div className="text-sm opacity-75">Explore career options</div>
//           </button>
//         </div>
//       </div>

//       {activeTab === 'upload' && renderUploadTab()}
//       {activeTab === 'roadmap' && renderRoadmapTab()}
//       {activeTab === 'popular' && renderPopularRolesTab()}

//       {selectedJob && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
//           <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
//             <div className="p-6 border-b">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h3 className="text-xl font-bold text-gray-800">{selectedJob.title}</h3>
//                   <p className="text-gray-600 mt-1">{selectedJob.description}</p>
//                 </div>
//                 <button
//                   onClick={() => setSelectedJob(null)}
//                   className="text-gray-500 hover:text-gray-700 text-2xl"
//                 >
//                   ×
//                 </button>
//               </div>
//             </div>
//             <div className="p-6 overflow-y-auto max-h-[70vh]">
//               <div className="space-y-4">
//                 <div>
//                   <h4 className="font-semibold text-gray-800 mb-2">Salary Range</h4>
//                   <p className="text-green-600 font-medium">{selectedJob.avg_salary}</p>
//                 </div>
//                 <div>
//                   <h4 className="font-semibold text-gray-800 mb-2">Market Demand</h4>
//                   <p className="text-orange-600 font-medium">{selectedJob.demand}</p>
//                 </div>
//                 <div>
//                   <h4 className="font-semibold text-gray-800 mb-2">Key Skills Required</h4>
//                   <div className="flex flex-wrap gap-2">
//                     {selectedJob.skills.map((skill, idx) => (
//                       <span
//                         key={idx}
//                         className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm"
//                       >
//                         {skill}
//                       </span>
//                     ))}
//                   </div>
//                 </div>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default StudyAssistant;

// import React, { useState, useEffect } from 'react';

// const StudyAssistant = () => {
//   const [activeTab, setActiveTab] = useState('upload');
//   const [selectedJob, setSelectedJob] = useState(null);
//   const [popularRoles, setPopularRoles] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [resumeFile, setResumeFile] = useState(null);
//   const [analysisResult, setAnalysisResult] = useState(null);
//   const [selectedRoadmap, setSelectedRoadmap] = useState(null);
//   const [error, setError] = useState(null);
//   const [backendConnected, setBackendConnected] = useState(false);

//   useEffect(() => {
//     checkBackendConnection();
//     fetchPopularRoles();
//   }, []);

//   const checkBackendConnection = async () => {
//     try {
//       const response = await fetch('http://localhost:5000/');
//       if (response.ok) {
//         setBackendConnected(true);
//       }
//     } catch (error) {
//       setBackendConnected(false);
//       console.error('Backend not connected:', error);
//     }
//   };

//   const fetchPopularRoles = async () => {
//     try {
//       const response = await fetch('http://localhost:5000/api/roadmap/popular-roles');
//       if (!response.ok) {
//         throw new Error(`Server error: ${response.status}`);
//       }
//       const data = await response.json();
//       setPopularRoles(data.roles || []);
//     } catch (error) {
//       console.error('Error fetching popular roles:', error);
//       setError(`Backend connection failed. Make sure server is running on port 5000. Error: ${error.message}`);
//     }
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (file && file.type === 'application/pdf') {
//       setResumeFile(file);
//       setError(null);
//     } else {
//       setError('Please upload a PDF file');
//     }
//   };

//   const handleResumeUpload = async () => {
//     if (!resumeFile) {
//       setError('Please select a resume file');
//       return;
//     }

//     setLoading(true);
//     setError(null);

//     try {
//       const formData = new FormData();
//       formData.append('resume', resumeFile);

//       console.log('Uploading resume to backend...');
      
//       const response = await fetch('http://localhost:5000/api/roadmap/analyze-resume', {
//         method: 'POST',
//         body: formData,
//       });

//       console.log('Response status:', response.status);

//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.error || `Server error: ${response.status}`);
//       }

//       const data = await response.json();
//       console.log('Analysis result:', data);
      
//       setAnalysisResult(data);
//       setSelectedRoadmap(data.personalized_roadmap);
//       setActiveTab('roadmap');
//     } catch (error) {
//       const errorMessage = error.message || 'Failed to analyze resume';
//       setError(`${errorMessage}. Make sure the backend server is running on http://localhost:5000`);
//       console.error('Error analyzing resume:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleGenerateRoadmapForRole = async (role) => {
//     if (!analysisResult) return;

//     setLoading(true);
//     setError(null);

//     try {
//       const response = await fetch('http://localhost:5000/api/roadmap/generate-for-role', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           job_role: role,
//           career_info: analysisResult.career_analysis,
//         }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to generate roadmap');
//       }

//       const data = await response.json();
//       setSelectedRoadmap(data.roadmap);
//       setActiveTab('roadmap');
//     } catch (error) {
//       setError(error.message || 'Failed to generate roadmap');
//       console.error('Error generating roadmap:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const renderUploadTab = () => (
//     <div className="bg-white rounded-lg shadow-md p-8">
//       <div className="max-w-2xl mx-auto">
//         <div className="text-center mb-8">
//           <div className="text-6xl mb-4">📤</div>
//           <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Your Resume</h2>
//           <p className="text-gray-600">
//             Get a personalized career roadmap based on your skills and experience
//           </p>
//         </div>

//         <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
//           <input
//             type="file"
//             accept=".pdf"
//             onChange={handleFileChange}
//             className="hidden"
//             id="resume-upload"
//           />
//           <label htmlFor="resume-upload" className="cursor-pointer">
//             <div className="space-y-2">
//               <div className="text-4xl">📄</div>
//               <div className="text-gray-600">
//                 {resumeFile ? resumeFile.name : 'Click to upload or drag and drop'}
//               </div>
//               <div className="text-sm text-gray-500">PDF files only</div>
//             </div>
//           </label>
//         </div>

//         {error && (
//           <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
//             {error}
//           </div>
//         )}

//         <button
//           onClick={handleResumeUpload}
//           disabled={!resumeFile || loading}
//           className="w-full mt-6 bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
//         >
//           {loading ? (
//             <>
//               <span className="inline-block animate-spin">⏳</span>
//               Analyzing Resume...
//             </>
//           ) : (
//             <>
//               <span>🎯</span>
//               Generate My Career Roadmap
//             </>
//           )}
//         </button>

//         <div className="mt-8 text-center">
//           <p className="text-gray-600 mb-4">Or explore popular career paths</p>
//           <button
//             onClick={() => setActiveTab('popular')}
//             className="text-blue-600 hover:text-blue-700 font-medium"
//           >
//             View Popular Roles →
//           </button>
//         </div>
//       </div>
//     </div>
//   );

//   const renderRoadmapTab = () => {
//     if (!selectedRoadmap) return null;

//     return (
//       <div className="space-y-6">
//         {analysisResult && (
//           <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-md p-6">
//             <h2 className="text-2xl font-bold text-gray-800 mb-4">
//               Your Personalized Career Path
//             </h2>
//             <div className="grid md:grid-cols-3 gap-4">
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <span className="text-xl">🎯</span>
//                   <h3 className="font-semibold text-gray-700">Primary Role</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900">
//                   {analysisResult.career_analysis.primary_role}
//                 </p>
//               </div>
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <span className="text-xl">📈</span>
//                   <h3 className="font-semibold text-gray-700">Experience Level</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900 capitalize">
//                   {analysisResult.career_analysis.experience_level}
//                 </p>
//               </div>
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <span className="text-xl">⏰</span>
//                   <h3 className="font-semibold text-gray-700">Timeline</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900">
//                   {selectedRoadmap.total_estimated_weeks} weeks
//                 </p>
//               </div>
//             </div>

//             {analysisResult.career_analysis.skill_gaps && analysisResult.career_analysis.skill_gaps.length > 0 && (
//               <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
//                 <h4 className="font-semibold text-gray-700 mb-2">Skills to Develop:</h4>
//                 <div className="flex flex-wrap gap-2">
//                   {analysisResult.career_analysis.skill_gaps.map((skill, idx) => (
//                     <span
//                       key={idx}
//                       className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm"
//                     >
//                       {skill}
//                     </span>
//                   ))}
//                 </div>
//               </div>
//             )}
//           </div>
//         )}

//         {selectedRoadmap.personalized_intro && (
//           <div className="bg-white rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-3">🚀 Your Journey Begins</h3>
//             <p className="text-gray-700 leading-relaxed">{selectedRoadmap.personalized_intro}</p>
//           </div>
//         )}

//         <div className="bg-white rounded-lg shadow-md p-6">
//           <h3 className="text-xl font-bold text-gray-800 mb-6">📚 Learning Roadmap</h3>
//           <div className="space-y-6">
//             {selectedRoadmap.phases && selectedRoadmap.phases.map((phase, phaseIdx) => (
//               <div key={phaseIdx} className="border border-gray-200 rounded-lg p-5">
//                 <div className="flex items-start justify-between mb-4">
//                   <div>
//                     <h4 className="text-lg font-semibold text-gray-800">
//                       Phase {phase.phase_number}: {phase.phase_name}
//                     </h4>
//                     <p className="text-gray-600 mt-1">{phase.description}</p>
//                     <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
//                       <span className="flex items-center gap-1">
//                         <span>⏰</span>
//                         {phase.duration_weeks} weeks
//                       </span>
//                     </div>
//                   </div>
//                 </div>

//                 <div className="space-y-3 mt-4">
//                   {phase.steps && phase.steps.map((step, stepIdx) => (
//                     <div key={stepIdx} className="bg-gray-50 rounded-lg p-4">
//                       <div className="flex items-start gap-3">
//                         <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
//                           {stepIdx + 1}
//                         </div>
//                         <div className="flex-1">
//                           <h5 className="font-medium text-gray-800">{step.title}</h5>
//                           <p className="text-sm text-gray-600 mt-1">{step.description}</p>
                          
//                           {step.key_topics && step.key_topics.length > 0 && (
//                             <div className="mt-2">
//                               <span className="text-xs text-gray-500">Key Topics:</span>
//                               <div className="flex flex-wrap gap-1 mt-1">
//                                 {step.key_topics.map((topic, idx) => (
//                                   <span
//                                     key={idx}
//                                     className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded"
//                                   >
//                                     {topic}
//                                   </span>
//                                 ))}
//                               </div>
//                             </div>
//                           )}

//                           <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
//                             <span>⏱️ {step.estimated_hours}h</span>
//                             <span className={`px-2 py-1 rounded ${
//                               step.priority === 'high' ? 'bg-red-100 text-red-700' :
//                               step.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
//                               'bg-green-100 text-green-700'
//                             }`}>
//                               {step.priority} priority
//                             </span>
//                           </div>
//                         </div>
//                       </div>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>

//         {analysisResult && analysisResult.alternative_careers && analysisResult.alternative_careers.length > 0 && (
//           <div className="bg-white rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-4">🎯 More Career Paths For You</h3>
//             <p className="text-gray-600 mb-6">Based on your skills and experience, you might also consider:</p>
//             <div className="grid md:grid-cols-2 gap-4">
//               {analysisResult.alternative_careers.map((career, idx) => (
//                 <div
//                   key={idx}
//                   className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors cursor-pointer"
//                   onClick={() => handleGenerateRoadmapForRole(career.role)}
//                 >
//                   <div className="flex items-start justify-between">
//                     <div className="flex-1">
//                       <h4 className="font-semibold text-gray-800">{career.role}</h4>
//                       <p className="text-sm text-gray-600 mt-1">{career.reason}</p>
//                     </div>
//                     <div className="flex-shrink-0 ml-4">
//                       <div className="text-2xl font-bold text-blue-600">
//                         {career.match_percentage}%
//                       </div>
//                       <div className="text-xs text-gray-500 text-center">match</div>
//                     </div>
//                   </div>
//                   <button className="mt-3 w-full text-sm text-blue-600 hover:text-blue-700 font-medium">
//                     Generate Roadmap →
//                   </button>
//                 </div>
//               ))}
//             </div>
//           </div>
//         )}

//         {selectedRoadmap.career_tips && selectedRoadmap.career_tips.length > 0 && (
//           <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-4">💡 Personalized Tips</h3>
//             <ul className="space-y-2">
//               {selectedRoadmap.career_tips.map((tip, idx) => (
//                 <li key={idx} className="flex items-start gap-2 text-gray-700">
//                   <span className="text-green-600 flex-shrink-0">✓</span>
//                   <span>{tip}</span>
//                 </li>
//               ))}
//             </ul>
//           </div>
//         )}
//       </div>
//     );
//   };

//   const renderPopularRolesTab = () => (
//     <div className="bg-white rounded-lg shadow-md p-6">
//       <h2 className="text-2xl font-bold mb-6 text-gray-800">🔥 More Career Roadmaps</h2>
//       <p className="text-gray-600 mb-6">
//         Explore these popular career paths to find the one that suits you best
//       </p>
//       <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
//         {popularRoles.map((role) => (
//           <div
//             key={role.id}
//             className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
//           >
//             <h3 className="font-semibold text-gray-800 mb-2">{role.title}</h3>
//             <p className="text-sm text-gray-600 mb-3">{role.description}</p>
//             <div className="space-y-2 mb-4">
//               <div className="flex justify-between text-sm">
//                 <span className="text-gray-500">Salary:</span>
//                 <span className="font-medium text-green-600">{role.avg_salary}</span>
//               </div>
//               <div className="flex justify-between text-sm">
//                 <span className="text-gray-500">Demand:</span>
//                 <span className={`font-medium ${
//                   role.demand === 'Very High' ? 'text-red-600' : 'text-orange-600'
//                 }`}>
//                   {role.demand}
//                 </span>
//               </div>
//             </div>
//             <div className="mb-4">
//               <div className="text-xs text-gray-500 mb-1">Key Skills:</div>
//               <div className="flex flex-wrap gap-1">
//                 {role.skills.map((skill, idx) => (
//                   <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
//                     {typeof skill === 'string' ? skill : skill.name}
//                   </span>
//                 ))}
//               </div>
//             </div>
//             <button
//               onClick={() => setSelectedJob(role)}
//               className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg text-sm hover:bg-blue-700 transition-colors"
//             >
//               View Skills & Resources
//             </button>
//           </div>
//         ))}
//       </div>
//     </div>
//   );

//   return (
//     <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
//       <div className="bg-white rounded-lg shadow-md p-6 mb-6">
//         <div className="flex items-center justify-between">
//           <div>
//             <h1 className="text-3xl font-bold text-gray-800 mb-2">
//               🎯 AI Career Roadmap Generator
//             </h1>
//             <p className="text-gray-600">
//               Upload your resume for a personalized career path or explore popular roles
//             </p>
//           </div>
//           <div className="flex items-center gap-2">
//             <div className={`w-3 h-3 rounded-full ${backendConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
//             <span className="text-sm text-gray-600">
//               {backendConnected ? 'Connected' : 'Disconnected'}
//             </span>
//           </div>
//         </div>
//         {!backendConnected && (
//           <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
//             ⚠️ Backend server is not running. Please start the Flask server on port 5000.
//           </div>
//         )}
//       </div>

//       <div className="bg-white rounded-lg shadow-md mb-6">
//         <div className="flex border-b">
//           <button
//             onClick={() => setActiveTab('upload')}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'upload'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             }`}
//           >
//             <div className="font-medium">📤 Upload Resume</div>
//             <div className="text-sm opacity-75">Get personalized roadmap</div>
//           </button>
//           <button
//             onClick={() => setActiveTab('roadmap')}
//             disabled={!selectedRoadmap}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'roadmap'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             } ${!selectedRoadmap ? 'opacity-50 cursor-not-allowed' : ''}`}
//           >
//             <div className="font-medium">🗺️ Your Roadmap</div>
//             <div className="text-sm opacity-75">View your career path</div>
//           </button>
//           <button
//             onClick={() => setActiveTab('popular')}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'popular'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             }`}
//           >
//             <div className="font-medium">🔥 Popular Roles</div>
//             <div className="text-sm opacity-75">Explore career options</div>
//           </button>
//         </div>
//       </div>

//       {activeTab === 'upload' && renderUploadTab()}
//       {activeTab === 'roadmap' && renderRoadmapTab()}
//       {activeTab === 'popular' && renderPopularRolesTab()}

//       {selectedJob && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
//           <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
//             <div className="p-6 border-b">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h3 className="text-xl font-bold text-gray-800">{selectedJob.title}</h3>
//                   <p className="text-gray-600 mt-1">{selectedJob.description}</p>
//                 </div>
//                 <button
//                   onClick={() => setSelectedJob(null)}
//                   className="text-gray-500 hover:text-gray-700 text-2xl"
//                 >
//                   ×
//                 </button>
//               </div>
//             </div>
//             <div className="p-6 overflow-y-auto max-h-[70vh]">
//               <div className="space-y-4">
//                 <div>
//                   <h4 className="font-semibold text-gray-800 mb-2">💰 Salary Range</h4>
//                   <p className="text-green-600 font-medium">{selectedJob.avg_salary}</p>
//                 </div>
//                 <div>
//                   <h4 className="font-semibold text-gray-800 mb-2">📊 Market Demand</h4>
//                   <p className="text-orange-600 font-medium">{selectedJob.demand}</p>
//                 </div>
//                 <div>
//                   <h4 className="font-semibold text-gray-800 mb-2">🎯 Key Skills Required</h4>
//                   <div className="flex flex-wrap gap-2">
//                     {selectedJob.skills.map((skill, idx) => (
//                       <span
//                         key={idx}
//                         className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm"
//                       >
//                         {skill}
//                       </span>
//                     ))}
//                   </div>
//                 </div>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default StudyAssistant;

// import React, { useState, useEffect } from 'react';

// const StudyAssistant = () => {
//   const [activeTab, setActiveTab] = useState('upload');
//   const [selectedJob, setSelectedJob] = useState(null);
//   const [popularRoles, setPopularRoles] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [resumeFile, setResumeFile] = useState(null);
//   const [analysisResult, setAnalysisResult] = useState(null);
//   const [selectedRoadmap, setSelectedRoadmap] = useState(null);
//   const [error, setError] = useState(null);
//   const [backendConnected, setBackendConnected] = useState(false);

//   useEffect(() => {
//     checkBackendConnection();
//     fetchPopularRoles();
//   }, []);

//   const checkBackendConnection = async () => {
//     try {
//       const controller = new AbortController();
//       const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
      
//       const response = await fetch('http://localhost:5000/', {
//         signal: controller.signal
//       });
      
//       clearTimeout(timeoutId);
      
//       if (response.ok) {
//         setBackendConnected(true);
//         console.log('✅ Backend connected successfully');
//       } else {
//         setBackendConnected(false);
//         console.error('❌ Backend returned error:', response.status);
//       }
//     } catch (error) {
//       setBackendConnected(false);
//       console.error('❌ Backend connection failed:', error.message);
      
//       // Retry after 3 seconds
//       setTimeout(() => {
//         console.log('🔄 Retrying backend connection...');
//         checkBackendConnection();
//       }, 3000);
//     }
//   };

//   const fetchPopularRoles = async () => {
//     try {
//       const response = await fetch('http://localhost:5000/api/roadmap/popular-roles');
//       if (!response.ok) {
//         throw new Error(`Server error: ${response.status}`);
//       }
//       const data = await response.json();
//       setPopularRoles(data.roles || []);
//     } catch (error) {
//       console.error('Error fetching popular roles:', error);
//       setError(`Backend connection failed. Make sure server is running on port 5000. Error: ${error.message}`);
//     }
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (file && file.type === 'application/pdf') {
//       setResumeFile(file);
//       setError(null);
//     } else {
//       setError('Please upload a PDF file');
//     }
//   };

//   const handleResumeUpload = async () => {
//     if (!resumeFile) {
//       setError('Please select a resume file');
//       return;
//     }

//     setLoading(true);
//     setError(null);

//     try {
//       const formData = new FormData();
//       formData.append('resume', resumeFile);

//       console.log('Uploading resume to backend...');
      
//       const response = await fetch('http://localhost:5000/api/roadmap/analyze-resume', {
//         method: 'POST',
//         body: formData,
//       });

//       console.log('Response status:', response.status);

//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.error || `Server error: ${response.status}`);
//       }

//       const data = await response.json();
//       console.log('Analysis result:', data);
      
//       setAnalysisResult(data);
//       setSelectedRoadmap(data.personalized_roadmap);
//       setActiveTab('roadmap');
//     } catch (error) {
//       const errorMessage = error.message || 'Failed to analyze resume';
//       setError(`${errorMessage}. Make sure the backend server is running on http://localhost:5000`);
//       console.error('Error analyzing resume:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleGenerateRoadmapForRole = async (role) => {
//     if (!analysisResult) return;

//     setLoading(true);
//     setError(null);

//     try {
//       const response = await fetch('http://localhost:5000/api/roadmap/generate-for-role', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           job_role: role,
//           career_info: analysisResult.career_analysis,
//         }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to generate roadmap');
//       }

//       const data = await response.json();
//       setSelectedRoadmap(data.roadmap);
//       setActiveTab('roadmap');
//     } catch (error) {
//       setError(error.message || 'Failed to generate roadmap');
//       console.error('Error generating roadmap:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const renderUploadTab = () => (
//     <div className="bg-white rounded-lg shadow-md p-8">
//       <div className="max-w-2xl mx-auto">
//         <div className="text-center mb-8">
//           <div className="text-6xl mb-4">📤</div>
//           <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Your Resume</h2>
//           <p className="text-gray-600">
//             Get a personalized career roadmap based on your skills and experience
//           </p>
//         </div>

//         <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
//           <input
//             type="file"
//             accept=".pdf"
//             onChange={handleFileChange}
//             className="hidden"
//             id="resume-upload"
//           />
//           <label htmlFor="resume-upload" className="cursor-pointer">
//             <div className="space-y-2">
//               <div className="text-4xl">📄</div>
//               <div className="text-gray-600">
//                 {resumeFile ? resumeFile.name : 'Click to upload or drag and drop'}
//               </div>
//               <div className="text-sm text-gray-500">PDF files only</div>
//             </div>
//           </label>
//         </div>

//         {error && (
//           <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
//             {error}
//           </div>
//         )}

//         <button
//           onClick={handleResumeUpload}
//           disabled={!resumeFile || loading}
//           className="w-full mt-6 bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
//         >
//           {loading ? (
//             <>
//               <span className="inline-block animate-spin">⏳</span>
//               Analyzing Resume...
//             </>
//           ) : (
//             <>
//               <span>🎯</span>
//               Generate My Career Roadmap
//             </>
//           )}
//         </button>

//         <div className="mt-8 text-center">
//           <p className="text-gray-600 mb-4">Or explore popular career paths</p>
//           <button
//             onClick={() => setActiveTab('popular')}
//             className="text-blue-600 hover:text-blue-700 font-medium"
//           >
//             View Popular Roles →
//           </button>
//         </div>
//       </div>
//     </div>
//   );

//   const renderRoadmapTab = () => {
//     if (!selectedRoadmap) return null;

//     return (
//       <div className="space-y-6">
//         {analysisResult && (
//           <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-md p-6">
//             <h2 className="text-2xl font-bold text-gray-800 mb-4">
//               Your Personalized Career Path
//             </h2>
//             <div className="grid md:grid-cols-3 gap-4">
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <span className="text-xl">🎯</span>
//                   <h3 className="font-semibold text-gray-700">Primary Role</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900">
//                   {analysisResult.career_analysis.primary_role}
//                 </p>
//               </div>
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <span className="text-xl">📈</span>
//                   <h3 className="font-semibold text-gray-700">Experience Level</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900 capitalize">
//                   {analysisResult.career_analysis.experience_level}
//                 </p>
//               </div>
//               <div className="bg-white rounded-lg p-4">
//                 <div className="flex items-center gap-2 mb-2">
//                   <span className="text-xl">⏰</span>
//                   <h3 className="font-semibold text-gray-700">Timeline</h3>
//                 </div>
//                 <p className="text-lg font-medium text-gray-900">
//                   {selectedRoadmap.total_estimated_weeks} weeks
//                 </p>
//               </div>
//             </div>

//             {analysisResult.career_analysis.skill_gaps && analysisResult.career_analysis.skill_gaps.length > 0 && (
//               <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
//                 <h4 className="font-semibold text-gray-700 mb-2">Skills to Develop:</h4>
//                 <div className="flex flex-wrap gap-2">
//                   {analysisResult.career_analysis.skill_gaps.map((skill, idx) => (
//                     <span
//                       key={idx}
//                       className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm"
//                     >
//                       {skill}
//                     </span>
//                   ))}
//                 </div>
//               </div>
//             )}
//           </div>
//         )}

//         {selectedRoadmap.personalized_intro && (
//           <div className="bg-white rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-3">🚀 Your Journey Begins</h3>
//             <p className="text-gray-700 leading-relaxed">{selectedRoadmap.personalized_intro}</p>
//           </div>
//         )}

//         <div className="bg-white rounded-lg shadow-md p-6">
//           <h3 className="text-xl font-bold text-gray-800 mb-6">📚 Learning Roadmap</h3>
//           <div className="space-y-6">
//             {selectedRoadmap.phases && selectedRoadmap.phases.map((phase, phaseIdx) => (
//               <div key={phaseIdx} className="border border-gray-200 rounded-lg p-5">
//                 <div className="flex items-start justify-between mb-4">
//                   <div>
//                     <h4 className="text-lg font-semibold text-gray-800">
//                       Phase {phase.phase_number}: {phase.phase_name}
//                     </h4>
//                     <p className="text-gray-600 mt-1">{phase.description}</p>
//                     <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
//                       <span className="flex items-center gap-1">
//                         <span>⏰</span>
//                         {phase.duration_weeks} weeks
//                       </span>
//                     </div>
//                   </div>
//                 </div>

//                 <div className="space-y-3 mt-4">
//                   {phase.steps && phase.steps.map((step, stepIdx) => (
//                     <div key={stepIdx} className="bg-gray-50 rounded-lg p-4">
//                       <div className="flex items-start gap-3">
//                         <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
//                           {stepIdx + 1}
//                         </div>
//                         <div className="flex-1">
//                           <h5 className="font-medium text-gray-800">{step.title}</h5>
//                           <p className="text-sm text-gray-600 mt-1">{step.description}</p>
                          
//                           {step.key_topics && step.key_topics.length > 0 && (
//                             <div className="mt-2">
//                               <span className="text-xs text-gray-500">Key Topics:</span>
//                               <div className="flex flex-wrap gap-1 mt-1">
//                                 {step.key_topics.map((topic, idx) => (
//                                   <span
//                                     key={idx}
//                                     className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded"
//                                   >
//                                     {topic}
//                                   </span>
//                                 ))}
//                               </div>
//                             </div>
//                           )}

//                           <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
//                             <span>⏱️ {step.estimated_hours}h</span>
//                             <span className={`px-2 py-1 rounded ${
//                               step.priority === 'high' ? 'bg-red-100 text-red-700' :
//                               step.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
//                               'bg-green-100 text-green-700'
//                             }`}>
//                               {step.priority} priority
//                             </span>
//                           </div>
//                         </div>
//                       </div>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>

//         {analysisResult && analysisResult.alternative_careers && analysisResult.alternative_careers.length > 0 && (
//           <div className="bg-white rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-4">🎯 More Career Paths For You</h3>
//             <p className="text-gray-600 mb-6">Based on your skills and experience, you might also consider:</p>
//             <div className="grid md:grid-cols-2 gap-4">
//               {analysisResult.alternative_careers.map((career, idx) => (
//                 <div
//                   key={idx}
//                   className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors cursor-pointer"
//                   onClick={() => handleGenerateRoadmapForRole(career.role)}
//                 >
//                   <div className="flex items-start justify-between">
//                     <div className="flex-1">
//                       <h4 className="font-semibold text-gray-800">{career.role}</h4>
//                       <p className="text-sm text-gray-600 mt-1">{career.reason}</p>
//                     </div>
//                     <div className="flex-shrink-0 ml-4">
//                       <div className="text-2xl font-bold text-blue-600">
//                         {career.match_percentage}%
//                       </div>
//                       <div className="text-xs text-gray-500 text-center">match</div>
//                     </div>
//                   </div>
//                   <button className="mt-3 w-full text-sm text-blue-600 hover:text-blue-700 font-medium">
//                     Generate Roadmap →
//                   </button>
//                 </div>
//               ))}
//             </div>
//           </div>
//         )}

//         {selectedRoadmap.career_tips && selectedRoadmap.career_tips.length > 0 && (
//           <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg shadow-md p-6">
//             <h3 className="text-xl font-bold text-gray-800 mb-4">💡 Personalized Tips</h3>
//             <ul className="space-y-2">
//               {selectedRoadmap.career_tips.map((tip, idx) => (
//                 <li key={idx} className="flex items-start gap-2 text-gray-700">
//                   <span className="text-green-600 flex-shrink-0">✓</span>
//                   <span>{tip}</span>
//                 </li>
//               ))}
//             </ul>
//           </div>
//         )}
//       </div>
//     );
//   };

//   const renderPopularRolesTab = () => (
//     <div className="bg-white rounded-lg shadow-md p-6">
//       <h2 className="text-2xl font-bold mb-6 text-gray-800">🔥 More Career Roadmaps</h2>
//       <p className="text-gray-600 mb-6">
//         Explore these popular career paths to find the one that suits you best
//       </p>
//       <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
//         {popularRoles.map((role) => (
//           <div
//             key={role.id}
//             className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
//           >
//             <h3 className="font-semibold text-gray-800 mb-2">{role.title}</h3>
//             <p className="text-sm text-gray-600 mb-3">{role.description}</p>
//             <div className="space-y-2 mb-4">
//               <div className="flex justify-between text-sm">
//                 <span className="text-gray-500">Salary:</span>
//                 <span className="font-medium text-green-600">{role.avg_salary}</span>
//               </div>
//               <div className="flex justify-between text-sm">
//                 <span className="text-gray-500">Demand:</span>
//                 <span className={`font-medium ${
//                   role.demand === 'Very High' ? 'text-red-600' : 'text-orange-600'
//                 }`}>
//                   {role.demand}
//                 </span>
//               </div>
//             </div>
//             <div className="mb-4">
//               <div className="text-xs text-gray-500 mb-1">Key Skills:</div>
//               <div className="flex flex-wrap gap-1">
//                 {role.skills.map((skill, idx) => (
//                   <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
//                     {typeof skill === 'string' ? skill : skill.name}
//                   </span>
//                 ))}
//               </div>
//             </div>
//             <button
//               onClick={() => setSelectedJob(role)}
//               className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg text-sm hover:bg-blue-700 transition-colors"
//             >
//               View Skills & Resources
//             </button>
//           </div>
//         ))}
//       </div>
//     </div>
//   );

//   return (
//     <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
//       <div className="bg-white rounded-lg shadow-md p-6 mb-6">
//         <div className="flex items-center justify-between">
//           <div>
//             <h1 className="text-3xl font-bold text-gray-800 mb-2">
//               🎯 AI Career Roadmap Generator
//             </h1>
//             <p className="text-gray-600">
//               Upload your resume for a personalized career path or explore popular roles
//             </p>
//           </div>
//           <div className="flex items-center gap-2">
//             <div className={`w-3 h-3 rounded-full ${backendConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
//             <span className="text-sm text-gray-600">
//               {backendConnected ? 'Connected' : 'Disconnected'}
//             </span>
//           </div>
//         </div>
//         {!backendConnected && (
//           <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
//             <div className="flex items-center justify-between">
//               <span className="text-red-700 text-sm">
//                 ⚠️ Backend server is not responding. Please check if it's running on port 5000.
//               </span>
//               <button
//                 onClick={checkBackendConnection}
//                 className="ml-4 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
//               >
//                 Retry
//               </button>
//             </div>
//           </div>
//         )}
//       </div>

//       <div className="bg-white rounded-lg shadow-md mb-6">
//         <div className="flex border-b">
//           <button
//             onClick={() => setActiveTab('upload')}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'upload'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             }`}
//           >
//             <div className="font-medium">📤 Upload Resume</div>
//             <div className="text-sm opacity-75">Get personalized roadmap</div>
//           </button>
//           <button
//             onClick={() => setActiveTab('roadmap')}
//             disabled={!selectedRoadmap}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'roadmap'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             } ${!selectedRoadmap ? 'opacity-50 cursor-not-allowed' : ''}`}
//           >
//             <div className="font-medium">🗺️ Your Roadmap</div>
//             <div className="text-sm opacity-75">View your career path</div>
//           </button>
//           <button
//             onClick={() => setActiveTab('popular')}
//             className={`flex-1 p-4 text-left transition-colors ${
//               activeTab === 'popular'
//                 ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
//                 : 'hover:bg-gray-50 text-gray-600'
//             }`}
//           >
//             <div className="font-medium">🔥 Popular Roles</div>
//             <div className="text-sm opacity-75">Explore career options</div>
//           </button>
//         </div>
//       </div>

//       {activeTab === 'upload' && renderUploadTab()}
//       {activeTab === 'roadmap' && renderRoadmapTab()}
//       {activeTab === 'popular' && renderPopularRolesTab()}

//       {selectedJob && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
//           <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
//             <div className="p-6 border-b">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h3 className="text-xl font-bold text-gray-800">{selectedJob.title}</h3>
//                   <p className="text-gray-600 mt-1">{selectedJob.description}</p>
//                 </div>
//                 <button
//                   onClick={() => setSelectedJob(null)}
//                   className="text-gray-500 hover:text-gray-700 text-2xl"
//                 >
//                   ×
//                 </button>
//               </div>
//             </div>
//             <div className="p-6 overflow-y-auto max-h-[70vh]">
//               <div className="space-y-6">
//                 <div className="grid md:grid-cols-2 gap-4">
//                   <div>
//                     <h4 className="font-semibold text-gray-800 mb-2">💰 Salary Range</h4>
//                     <p className="text-green-600 font-medium">{selectedJob.avg_salary}</p>
//                   </div>
//                   <div>
//                     <h4 className="font-semibold text-gray-800 mb-2">📊 Market Demand</h4>
//                     <p className="text-orange-600 font-medium">{selectedJob.demand}</p>
//                   </div>
//                 </div>

//                 <div>
//                   <h4 className="font-semibold text-gray-800 mb-4">📚 Skills & Learning Resources</h4>
//                   <div className="space-y-4">
//                     {selectedJob.skills.map((skill, idx) => {
//                       const skillName = typeof skill === 'string' ? skill : skill.name;
//                       const resources = typeof skill === 'object' ? skill.resources : [];
                      
//                       return (
//                         <div key={idx} className="border border-gray-200 rounded-lg p-4">
//                           <h5 className="font-medium text-gray-800 mb-3">{skillName}</h5>
//                           {resources && resources.length > 0 ? (
//                             <div className="space-y-2">
//                               {resources.map((resource, resIdx) => (
//                                 <div key={resIdx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
//                                   <span className="text-xl flex-shrink-0">
//                                     {resource.type === 'learning' ? '📚' : '💻'}
//                                   </span>
//                                   <div className="flex-1">
//                                     <a
//                                       href={resource.url}
//                                       target="_blank"
//                                       rel="noopener noreferrer"
//                                       className="text-blue-600 hover:underline font-medium"
//                                     >
//                                       {resource.title}
//                                     </a>
//                                     <p className="text-sm text-gray-600 mt-1">{resource.description}</p>
//                                     <span className="text-xs text-gray-500 mt-1 inline-block">
//                                       {resource.type === 'learning' ? '📖 Learning' : '⚡ Practice'}
//                                     </span>
//                                   </div>
//                                 </div>
//                               ))}
//                             </div>
//                           ) : (
//                             <p className="text-sm text-gray-500 italic">Resources coming soon...</p>
//                           )}
//                         </div>
//                       );
//                     })}
//                   </div>
//                 </div>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default StudyAssistant;



import React, { useState, useEffect } from 'react';

const StudyAssistant = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedJob, setSelectedJob] = useState(null);
  const [popularRoles, setPopularRoles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [resumeFile, setResumeFile] = useState(null);
  const [experienceYears, setExperienceYears] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [selectedRoadmap, setSelectedRoadmap] = useState(null);
  const [error, setError] = useState(null);
  const [backendConnected, setBackendConnected] = useState(false);

  useEffect(() => {
    checkBackendConnection();
    fetchPopularRoles();
  }, []);

  const checkBackendConnection = async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
      
      const response = await fetch('http://localhost:5000/', {
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        setBackendConnected(true);
        console.log('✅ Backend connected successfully');
      } else {
        setBackendConnected(false);
        console.error('❌ Backend returned error:', response.status);
      }
    } catch (error) {
      setBackendConnected(false);
      console.error('❌ Backend connection failed:', error.message);
      
      // Retry after 3 seconds
      setTimeout(() => {
        console.log('🔄 Retrying backend connection...');
        checkBackendConnection();
      }, 3000);
    }
  };

  const fetchPopularRoles = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/roadmap/popular-roles');
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      const data = await response.json();
      setPopularRoles(data.popular_roles || []);
    } catch (error) {
      console.error('Error fetching popular roles:', error);
      setError(`Backend connection failed. Make sure server is running on port 5000. Error: ${error.message}`);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setError(null);
    } else {
      setError('Please upload a PDF file');
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile || !experienceYears) {
      setError('Please select a resume file and enter experience years');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('resume', resumeFile);
      formData.append('experience_years', experienceYears);
      formData.append('job_description', jobDescription || ''); // Optional, defaults to empty if not provided

      console.log('Uploading resume to backend...');

      // Fetch data from multiple endpoints concurrently
      const requests = [
        { url: '/api/ats-score', key: 'atsScore' },
        { url: '/api/improvement-tips', key: 'improvementTips' },
        { url: '/api/role-alignment', key: 'roleAlignment' },
        { url: '/api/skill-gap', key: 'skillGap' },
        { url: '/api/predict-selection', key: 'selectionProbability' },
        { url: '/api/salary-estimate', key: 'salaryEstimate' },
        { url: '/api/recommend-companies', key: 'recommendedCompanies' },
      ];

      const responses = await Promise.all(
        requests.map(req =>
          fetch(`http://localhost:5000${req.url}`, {
            method: 'POST',
            body: formData,
          }).then(res => {
            if (!res.ok) throw new Error(`Failed to fetch ${req.url}: ${res.status}`);
            return res.json().then(data => ({ [req.key]: data }));
          })
        )
      );

      // Aggregate results
      const analysisData = responses.reduce((acc, curr) => ({ ...acc, ...curr }), {});
      console.log('Analysis result:', analysisData);

      // Extract skill gaps for display
      const skillGaps = analysisData.skillGap?.missing_skills || [];
      const careerAnalysis = {
        primary_role: analysisData.roleAlignment?.strengths?.includes('Data Scientist') ? 'Data Scientist' : 'Software Engineer', // Derive from strengths
        experience_level: experienceYears <= 2 ? 'Entry Level' : 'Mid Level', // Derive from experience_years
        skill_gaps: skillGaps,
      };

      setAnalysisResult({
        ...analysisData,
        career_analysis: careerAnalysis,
      });
      setSelectedRoadmap({ phases: [] }); // Placeholder, to be enhanced with roadmap logic
      setActiveTab('roadmap');
    } catch (error) {
      const errorMessage = error.message || 'Failed to analyze resume';
      setError(`${errorMessage}. Make sure the backend server is running on http://localhost:5000`);
      console.error('Error analyzing resume:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRoadmapForRole = async (role) => {
    if (!analysisResult) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/roadmap/generate-for-role', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_role: role,
          career_info: analysisResult.career_analysis,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate roadmap');
      }

      const data = await response.json();
      setSelectedRoadmap(data.roadmap);
      setActiveTab('roadmap');
    } catch (error) {
      setError(error.message || 'Failed to generate roadmap');
      console.error('Error generating roadmap:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderUploadTab = () => (
    <div className="bg-white rounded-lg shadow-md p-8">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">📤</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Your Resume</h2>
          <p className="text-gray-600">
            Get a personalized career roadmap based on your skills and experience
          </p>
        </div>

        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
            id="resume-upload"
          />
          <label htmlFor="resume-upload" className="cursor-pointer">
            <div className="space-y-2">
              <div className="text-4xl">📄</div>
              <div className="text-gray-600">
                {resumeFile ? resumeFile.name : 'Click to upload or drag and drop'}
              </div>
              <div className="text-sm text-gray-500">PDF files only</div>
            </div>
          </label>
        </div>

        <div className="mt-4">
          <input
            type="number"
            value={experienceYears}
            onChange={(e) => setExperienceYears(e.target.value)}
            placeholder="Experience Years"
            className="w-full p-2 border rounded-lg mb-4"
          />
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Job Description (optional)"
            className="w-full p-2 border rounded-lg mb-4"
            rows="3"
          />
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        <button
          onClick={handleResumeUpload}
          disabled={!resumeFile || !experienceYears || loading}
          className="w-full mt-6 bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <span className="inline-block animate-spin">⏳</span>
              Analyzing Resume...
            </>
          ) : (
            <>
              <span>🎯</span>
              Generate My Career Roadmap
            </>
          )}
        </button>

        <div className="mt-8 text-center">
          <p className="text-gray-600 mb-4">Or explore popular career paths</p>
          <button
            onClick={() => setActiveTab('popular')}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            View Popular Roles →
          </button>
        </div>
      </div>
    </div>
  );

  // [Rest of the renderRoadmapTab, renderPopularRolesTab, and return remain unchanged]
  // Copy the unchanged parts from the previous version to maintain consistency

  const renderRoadmapTab = () => {
    if (!selectedRoadmap) return null;

    return (
      <div className="space-y-6">
        {analysisResult && (
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Your Personalized Career Path
            </h2>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">🎯</span>
                  <h3 className="font-semibold text-gray-700">Primary Role</h3>
                </div>
                <p className="text-lg font-medium text-gray-900">
                  {analysisResult.career_analysis.primary_role}
                </p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">📈</span>
                  <h3 className="font-semibold text-gray-700">Experience Level</h3>
                </div>
                <p className="text-lg font-medium text-gray-900 capitalize">
                  {analysisResult.career_analysis.experience_level}
                </p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">⏰</span>
                  <h3 className="font-semibold text-gray-700">Timeline</h3>
                </div>
                <p className="text-lg font-medium text-gray-900">
                  {selectedRoadmap.total_estimated_weeks || 'N/A'} weeks
                </p>
              </div>
            </div>

            {analysisResult.career_analysis.skill_gaps && analysisResult.career_analysis.skill_gaps.length > 0 && (
              <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 className="font-semibold text-gray-700 mb-2">Skills to Develop:</h4>
                <div className="flex flex-wrap gap-2">
                  {analysisResult.career_analysis.skill_gaps.map((skill, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {selectedRoadmap.personalized_intro && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-3">🚀 Your Journey Begins</h3>
            <p className="text-gray-700 leading-relaxed">{selectedRoadmap.personalized_intro}</p>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-6">📚 Learning Roadmap</h3>
          <div className="space-y-6">
            {selectedRoadmap.phases && selectedRoadmap.phases.map((phase, phaseIdx) => (
              <div key={phaseIdx} className="border border-gray-200 rounded-lg p-5">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800">
                      Phase {phase.phase_number}: {phase.phase_name}
                    </h4>
                    <p className="text-gray-600 mt-1">{phase.description}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span className="flex items-center gap-1">
                        <span>⏰</span>
                        {phase.duration_weeks} weeks
                      </span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3 mt-4">
                  {phase.steps && phase.steps.map((step, stepIdx) => (
                    <div key={stepIdx} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-start gap-3">
                        <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                          {stepIdx + 1}
                        </div>
                        <div className="flex-1">
                          <h5 className="font-medium text-gray-800">{step.title}</h5>
                          <p className="text-sm text-gray-600 mt-1">{step.description}</p>
                          
                          {step.key_topics && step.key_topics.length > 0 && (
                            <div className="mt-2">
                              <span className="text-xs text-gray-500">Key Topics:</span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {step.key_topics.map((topic, idx) => (
                                  <span
                                    key={idx}
                                    className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded"
                                  >
                                    {topic}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                            <span>⏱️ {step.estimated_hours}h</span>
                            <span className={`px-2 py-1 rounded ${
                              step.priority === 'high' ? 'bg-red-100 text-red-700' :
                              step.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {step.priority} priority
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {analysisResult && analysisResult.recommendedCompanies && analysisResult.recommendedCompanies.companies.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">🎯 More Career Paths For You</h3>
            <p className="text-gray-600 mb-6">Based on your skills and experience, you might also consider:</p>
            <div className="grid md:grid-cols-2 gap-4">
              {analysisResult.recommendedCompanies.companies.map((company, idx) => (
                <div
                  key={idx}
                  className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors cursor-pointer"
                  onClick={() => handleGenerateRoadmapForRole(company.name)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-800">{company.name}</h4>
                      <p className="text-sm text-gray-600 mt-1">{company.reason}</p>
                    </div>
                    <div className="flex-shrink-0 ml-4">
                      <div className="text-2xl font-bold text-blue-600">
                        {analysisResult.roleAlignment?.similarity_percentage || 0}%
                      </div>
                      <div className="text-xs text-gray-500 text-center">match</div>
                    </div>
                  </div>
                  <button className="mt-3 w-full text-sm text-blue-600 hover:text-blue-700 font-medium">
                    Generate Roadmap →
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedRoadmap.career_tips && selectedRoadmap.career_tips.length > 0 && (
          <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">💡 Personalized Tips</h3>
            <ul className="space-y-2">
              {selectedRoadmap.career_tips.map((tip, idx) => (
                <li key={idx} className="flex items-start gap-2 text-gray-700">
                  <span className="text-green-600 flex-shrink-0">✓</span>
                  <span>{tip}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderPopularRolesTab = () => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">🔥 More Career Roadmaps</h2>
      <p className="text-gray-600 mb-6">
        Explore these popular career paths to find the one that suits you best
      </p>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {popularRoles.map((role) => (
          <div
            key={role.id}
            className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
          >
            <h3 className="font-semibold text-gray-800 mb-2">{role.role}</h3>
            <p className="text-sm text-gray-600 mb-3">{role.description || 'No description available'}</p>
            <div className="space-y-2 mb-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Salary:</span>
                <span className="font-medium text-green-600">{role.avg_salary || 'N/A'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Demand:</span>
                <span className={`font-medium ${
                  role.demand === 'High' || role.demand === 'Very High' ? 'text-red-600' : 'text-orange-600'
                }`}>
                  {role.demand || 'N/A'}
                </span>
              </div>
            </div>
            <div className="mb-4">
              <div className="text-xs text-gray-500 mb-1">Key Skills:</div>
              <div className="flex flex-wrap gap-1">
                {role.skills && role.skills.map((skill, idx) => (
                  <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                    {skill}
                  </span>
                )) || <span className="text-xs text-gray-500">No skills listed</span>}
              </div>
            </div>
            <button
              onClick={() => setSelectedJob(role)}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg text-sm hover:bg-blue-700 transition-colors"
            >
              View Skills & Resources
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              🎯 AI Career Roadmap Generator
            </h1>
            <p className="text-gray-600">
              Upload your resume for a personalized career path or explore popular roles
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${backendConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600">
              {backendConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
        {!backendConnected && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="text-red-700 text-sm">
                ⚠️ Backend server is not responding. Please check if it's running on port 5000.
              </span>
              <button
                onClick={checkBackendConnection}
                className="ml-4 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
              >
                Retry
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="flex border-b">
          <button
            onClick={() => setActiveTab('upload')}
            className={`flex-1 p-4 text-left transition-colors ${
              activeTab === 'upload'
                ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
                : 'hover:bg-gray-50 text-gray-600'
            }`}
          >
            <div className="font-medium">📤 Upload Resume</div>
            <div className="text-sm opacity-75">Get personalized roadmap</div>
          </button>
          <button
            onClick={() => setActiveTab('roadmap')}
            disabled={!selectedRoadmap}
            className={`flex-1 p-4 text-left transition-colors ${
              activeTab === 'roadmap'
                ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
                : 'hover:bg-gray-50 text-gray-600'
            } ${!selectedRoadmap ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <div className="font-medium">🗺️ Your Roadmap</div>
            <div className="text-sm opacity-75">View your career path</div>
          </button>
          <button
            onClick={() => setActiveTab('popular')}
            className={`flex-1 p-4 text-left transition-colors ${
              activeTab === 'popular'
                ? 'bg-blue-50 border-b-2 border-blue-500 text-blue-700'
                : 'hover:bg-gray-50 text-gray-600'
            }`}
          >
            <div className="font-medium">🔥 Popular Roles</div>
            <div className="text-sm opacity-75">Explore career options</div>
          </button>
        </div>
      </div>

      {activeTab === 'upload' && renderUploadTab()}
      {activeTab === 'roadmap' && renderRoadmapTab()}
      {activeTab === 'popular' && renderPopularRolesTab()}

      {selectedJob && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-xl font-bold text-gray-800">{selectedJob.role}</h3>
                  <p className="text-gray-600 mt-1">{selectedJob.description || 'No description available'}</p>
                </div>
                <button
                  onClick={() => setSelectedJob(null)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ×
                </button>
              </div>
            </div>
            <div className="p-6 overflow-y-auto max-h-[70vh]">
              <div className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold text-gray-800 mb-2">💰 Salary Range</h4>
                    <p className="text-green-600 font-medium">{selectedJob.avg_salary || 'N/A'}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-800 mb-2">📊 Market Demand</h4>
                    <p className="text-orange-600 font-medium">{selectedJob.demand || 'N/A'}</p>
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-800 mb-4">📚 Skills & Learning Resources</h4>
                  <div className="space-y-4">
                    {selectedJob.skills && selectedJob.skills.map((skill, idx) => {
                      const skillName = typeof skill === 'string' ? skill : skill.name || skill;
                      const resources = typeof skill === 'object' && skill.resources ? skill.resources : [];
                      
                      return (
                        <div key={idx} className="border border-gray-200 rounded-lg p-4">
                          <h5 className="font-medium text-gray-800 mb-3">{skillName}</h5>
                          {resources.length > 0 ? (
                            <div className="space-y-2">
                              {resources.map((resource, resIdx) => (
                                <div key={resIdx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                  <span className="text-xl flex-shrink-0">
                                    {resource.type === 'learning' ? '📚' : '💻'}
                                  </span>
                                  <div className="flex-1">
                                    <a
                                      href={resource.url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-blue-600 hover:underline font-medium"
                                    >
                                      {resource.title}
                                    </a>
                                    <p className="text-sm text-gray-600 mt-1">{resource.description}</p>
                                    <span className="text-xs text-gray-500 mt-1 inline-block">
                                      {resource.type === 'learning' ? '📖 Learning' : '⚡ Practice'}
                                    </span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <p className="text-sm text-gray-500 italic">Resources coming soon...</p>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudyAssistant;