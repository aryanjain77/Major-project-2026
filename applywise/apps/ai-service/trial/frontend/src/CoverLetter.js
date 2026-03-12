import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

const CoverLetter = () => {
  const [jobDesc, setJobDesc] = useState('');
  const [hrName, setHrName] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [coverLetter, setCoverLetter] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('job_desc', jobDesc);
      formData.append('hr_name', hrName);
      formData.append('resume_file', resumeFile);

      const res = await axios.post(
        'http://localhost:5000/generate_cover_letter',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      setCoverLetter(res.data.cover_letter);
      setError(null);
    } catch (err) {
      setError('Failed to generate cover letter. Please try again.');
      console.error(err);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Job Description</label>
          <textarea
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            placeholder="Enter job description"
            required
          />
        </div>
        <div>
          <label>HR Name</label>
          <input
            value={hrName}
            style={{color: "black"}}
            onChange={(e) => setHrName(e.target.value)}
            placeholder="Enter HR name"
            required
          />
        </div>
        <div>
          <label>Upload Resume (PDF)</label>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setResumeFile(e.target.files[0])}
            required
          />
        </div>
        <button type="submit" className="button-primary">
          Generate Cover Letter
        </button>
      </form>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {coverLetter && (
        <div className="card">
          <h2>Generated Cover Letter</h2>
          <p style={{ whiteSpace: 'pre-wrap', color: 'white', lineHeight: 1.6 }}>
            {coverLetter}
          </p>
        </div>
      )}
    </div>
  );
};

export default CoverLetter;