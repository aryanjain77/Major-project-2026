import React, { useState } from 'react';
import axios from 'axios';
import jsPDF from 'jspdf';
import './generateresume.css';

function GenerateResume() {
  const [formData, setFormData] = useState({
    // Personal Information
    fullName: '',
    phoneNumber: '',
    email: '',
    linkedinUrl: '',
    githubPortfolioUrl: '',
    location: '',

    // Resume Headline/Summary
    jobTitle: '',
    professionalSummary: '',

    // Skills
    technicalSkills: '',
    softSkills: '',

    // Work Experience
    workExperience: [{
      jobTitle: '',
      companyName: '',
      location: '',
      startDate: '',
      endDate: '',
      responsibilities: '',
      achievements: ''
    }],

    // Education
    education: [{
      degree: '',
      universityName: '',
      location: '',
      startDate: '',
      endDate: '',
      gpa: '',
      relevantCoursework: ''
    }],

    // Projects
    projects: [{
      projectTitle: '',
      description: '',
      technologiesUsed: '',
      impact: '',
      projectLink: ''
    }],

    // Certifications
    certifications: [{
      certificationName: '',
      issuingAuthority: '',
      date: ''
    }],

    // Achievements
    achievements: [{
      title: '',
      organization: '',
      date: '',
      description: ''
    }],

    // Additional Sections
    languages: '',
    publications: '',
    volunteering: '',
    hobbies: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e, index = null, field = null, section = null) => {
    if (section && index !== null && field) {
      const updatedSection = [...formData[section]];
      updatedSection[index] = { ...updatedSection[index], [field]: e.target.value };
      setFormData({ ...formData, [section]: updatedSection });
    } else {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const addItem = (section) => {
    const newItem = {
      workExperience: {
        jobTitle: '', companyName: '', location: '', startDate: '', endDate: '', responsibilities: '', achievements: ''
      },
      education: {
        degree: '', universityName: '', location: '', startDate: '', endDate: '', gpa: '', relevantCoursework: ''
      },
      projects: {
        projectTitle: '', description: '', technologiesUsed: '', impact: '', projectLink: ''
      },
      certifications: {
        certificationName: '', issuingAuthority: '', date: ''
      },
      achievements: {
        title: '', organization: '', date: '', description: ''
      }
    };

    setFormData({
      ...formData,
      [section]: [...formData[section], newItem[section]]
    });
  };

  const removeItem = (section, index) => {
    setFormData({
      ...formData,
      [section]: formData[section].filter((_, i) => i !== index)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Clean up empty entries before sending
      const cleanedData = {
        ...formData,
        workExperience: formData.workExperience.filter(exp =>
          exp.jobTitle.trim() || exp.companyName.trim()
        ),
        education: formData.education.filter(edu =>
          edu.degree.trim() || edu.universityName.trim()
        ),
        projects: formData.projects.filter(proj =>
          proj.projectTitle.trim()
        ),
        certifications: formData.certifications.filter(cert =>
          cert.certificationName.trim()
        ),
        achievements: formData.achievements.filter(ach =>
          ach.title.trim()
        )
      };

      const form = new FormData();

      // Add simple fields
      Object.keys(cleanedData).forEach(key => {
        if (Array.isArray(cleanedData[key])) {
          // Only stringify non-empty arrays
          if (cleanedData[key].length > 0) {
            form.append(key, JSON.stringify(cleanedData[key]));
          }
        } else if (cleanedData[key] && cleanedData[key].trim() !== '') {
          form.append(key, cleanedData[key].trim());
        }
      });

      console.log('Sending data to backend:', Object.fromEntries(form));

      const response = await axios.post("http://localhost:5000/api/resume/create", form, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
        timeout: 30000,
      });

      const pdfBlob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${cleanedData.fullName || 'resume'}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      console.log("Resume generated successfully!");

    } catch (err) {
      console.error("Failed to generate resume from backend:", err);
      setError('Backend generation failed. Generating client-side PDF as fallback.');

      try {
        generateClientSidePDF();
      } catch (clientErr) {
        setError(`Both backend and client-side generation failed: ${clientErr.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const generateClientSidePDF = () => {
    const doc = new jsPDF();
    let yOffset = 20;
    const pageHeight = doc.internal.pageSize.height;
    const margin = 20;

    const checkPageBreak = (requiredSpace = 20) => {
      if (yOffset + requiredSpace > pageHeight - margin) {
        doc.addPage();
        yOffset = margin;
      }
    };

    const addText = (text, fontSize = 10, isBold = false, maxWidth = 170) => {
      if (!text || text.trim() === '') return;

      doc.setFontSize(fontSize);
      doc.setFont("helvetica", isBold ? "bold" : "normal");

      const lines = doc.splitTextToSize(text, maxWidth);
      const requiredSpace = lines.length * (fontSize * 0.6) + 5;
      checkPageBreak(requiredSpace);

      lines.forEach(line => {
        doc.text(line, margin, yOffset);
        yOffset += fontSize * 0.6;
      });
      yOffset += 5;
    };

    // Header - Name and Contact Info
    addText(formData.fullName || "N/A", 18, true);

    const contactInfo = [];
    if (formData.phoneNumber) contactInfo.push(formData.phoneNumber);
    if (formData.email) contactInfo.push(formData.email);
    if (formData.location) contactInfo.push(formData.location);
    if (contactInfo.length > 0) addText(contactInfo.join(" | "), 10);

    const profileLinks = [];
    if (formData.linkedinUrl) profileLinks.push(`LinkedIn: ${formData.linkedinUrl}`);
    if (formData.githubPortfolioUrl) profileLinks.push(`Portfolio: ${formData.githubPortfolioUrl}`);
    if (profileLinks.length > 0) addText(profileLinks.join(" | "), 10);

    yOffset += 5;

    // Professional Summary
    if (formData.jobTitle) {
      addText(formData.jobTitle, 14, true);
    }
    if (formData.professionalSummary) {
      addText(formData.professionalSummary, 10);
    }

    // Skills
    if (formData.technicalSkills || formData.softSkills) {
      addText("SKILLS", 12, true);
      if (formData.technicalSkills) {
        addText(`Technical Skills: ${formData.technicalSkills}`, 10);
      }
      if (formData.softSkills) {
        addText(`Soft Skills: ${formData.softSkills}`, 10);
      }
    }

    // Work Experience
    if (formData.workExperience && formData.workExperience.some(exp => exp.jobTitle || exp.companyName)) {
      addText("WORK EXPERIENCE", 12, true);
      formData.workExperience.forEach(exp => {
        if (exp.jobTitle || exp.companyName) {
          const jobHeader = `${exp.jobTitle || 'N/A'} - ${exp.companyName || 'N/A'}`;
          addText(jobHeader, 11, true);

          const dateLocation = [];
          if (exp.startDate || exp.endDate) {
            dateLocation.push(`${exp.startDate || 'N/A'} - ${exp.endDate || 'Present'}`);
          }
          if (exp.location) dateLocation.push(exp.location);
          if (dateLocation.length > 0) addText(dateLocation.join(" | "), 9);

          if (exp.responsibilities) addText(`• ${exp.responsibilities}`, 10);
          if (exp.achievements) addText(`• ${exp.achievements}`, 10);
          yOffset += 5;
        }
      });
    }

    // Education
    if (formData.education && formData.education.some(edu => edu.degree || edu.universityName)) {
      addText("EDUCATION", 12, true);
      formData.education.forEach(edu => {
        if (edu.degree || edu.universityName) {
          const eduHeader = `${edu.degree || 'N/A'} - ${edu.universityName || 'N/A'}`;
          addText(eduHeader, 11, true);

          const eduDetails = [];
          if (edu.location) eduDetails.push(edu.location);
          if (edu.startDate || edu.endDate) {
            eduDetails.push(`${edu.startDate || 'N/A'} - ${edu.endDate || 'N/A'}`);
          }
          if (edu.gpa) eduDetails.push(`GPA: ${edu.gpa}`);
          if (eduDetails.length > 0) addText(eduDetails.join(" | "), 9);

          if (edu.relevantCoursework) addText(`Relevant Coursework: ${edu.relevantCoursework}`, 10);
          yOffset += 5;
        }
      });
    }

    // Projects
    if (formData.projects && formData.projects.some(proj => proj.projectTitle)) {
      addText("PROJECTS", 12, true);
      formData.projects.forEach(proj => {
        if (proj.projectTitle) {
          addText(proj.projectTitle, 11, true);
          if (proj.description) addText(proj.description, 10);
          if (proj.technologiesUsed) addText(`Technologies: ${proj.technologiesUsed}`, 10);
          if (proj.impact) addText(`Impact: ${proj.impact}`, 10);
          if (proj.projectLink) addText(`Link: ${proj.projectLink}`, 10);
          yOffset += 5;
        }
      });
    }

    // Certifications
    if (formData.certifications && formData.certifications.some(cert => cert.certificationName)) {
      addText("CERTIFICATIONS", 12, true);
      formData.certifications.forEach(cert => {
        if (cert.certificationName) {
          const certText = `${cert.certificationName} - ${cert.issuingAuthority || 'N/A'} (${cert.date || 'N/A'})`;
          addText(certText, 10);
        }
      });
    }

    // Achievements
    if (formData.achievements && formData.achievements.some(ach => ach.title)) {
      addText("ACHIEVEMENTS", 12, true);
      formData.achievements.forEach(ach => {
        if (ach.title) {
          const achText = `${ach.title} - ${ach.organization || 'N/A'} (${ach.date || 'N/A'})`;
          addText(achText, 10, true);
          if (ach.description) addText(ach.description, 10);
        }
      });
    }

    // Additional sections
    if (formData.languages) {
      addText("LANGUAGES", 12, true);
      addText(formData.languages, 10);
    }

    if (formData.publications) {
      addText("PUBLICATIONS", 12, true);
      addText(formData.publications, 10);
    }

    if (formData.volunteering) {
      addText("VOLUNTEERING", 12, true);
      addText(formData.volunteering, 10);
    }

    if (formData.hobbies) {
      addText("HOBBIES & INTERESTS", 12, true);
      addText(formData.hobbies, 10);
    }

    doc.save(`${formData.fullName || 'resume'}.pdf`);
  };

  return (
    <div className="max-w-4xl bg-white shadow-lg rounded-lg">
      <div className="text-center mb-8">
        <h1 className="text-3xl mb-2">Professional Resume Builder</h1>
        <p className="text-gray-600">Create an ATS-friendly resume with professional formatting</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">

        {/* Personal Information Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>📌</span> Personal Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label>
                Full Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleInputChange}
                required
                placeholder="Enter your full name"
              />
            </div>
            <div>
              <label>
                Phone Number <span className="text-red-500">*</span>
              </label>
              <input
                type="tel"
                name="phoneNumber"
                value={formData.phoneNumber}
                onChange={handleInputChange}
                required
                placeholder="+1 (555) 123-4567"
              />
            </div>
            <div>
              <label>
                Email <span className="text-red-500">*</span>
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                placeholder="professional.email@domain.com"
              />
            </div>
            <div>
              <label>LinkedIn URL</label>
              <input
                type="url"
                name="linkedinUrl"
                value={formData.linkedinUrl}
                onChange={handleInputChange}
                placeholder="https://linkedin.com/in/yourprofile"
              />
            </div>
            <div>
              <label>GitHub/Portfolio/Website</label>
              <input
                type="url"
                name="githubPortfolioUrl"
                value={formData.githubPortfolioUrl}
                onChange={handleInputChange}
                placeholder="https://github.com/yourusername or your portfolio URL"
              />
            </div>
            <div>
              <label>Location</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                placeholder="City, State, Country"
              />
            </div>
          </div>
        </div>

        {/* Resume Headline/Summary Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>📌</span> Resume Headline / Summary
          </h2>
          <div className="space-y-4">
            <div>
              <label>Job Title / Headline</label>
              <input
                type="text"
                name="jobTitle"
                value={formData.jobTitle}
                onChange={handleInputChange}
                placeholder="e.g., Software Engineer | React & Python Developer"
              />
            </div>
            <div>
              <label>Professional Summary (3-4 sentences)</label>
              <textarea
                name="professionalSummary"
                value={formData.professionalSummary}
                onChange={handleInputChange}
                rows="4"
                placeholder="Write a compelling summary highlighting your key achievements and skills with relevant keywords..."
              />
            </div>
          </div>
        </div>

        {/* Skills Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>📌</span> Skills Section
          </h2>
          <div className="space-y-4">
            <div>
              <label>Technical Skills</label>
              <textarea
                name="technicalSkills"
                value={formData.technicalSkills}
                onChange={handleInputChange}
                rows="3"
                placeholder="Python, JavaScript, React, Node.js, AWS, Docker, MySQL, Git (comma-separated for ATS)"
              />
            </div>
            <div>
              <label>Soft Skills</label>
              <textarea
                name="softSkills"
                value={formData.softSkills}
                onChange={handleInputChange}
                rows="2"
                placeholder="Leadership, Communication, Problem Solving, Team Collaboration (comma-separated)"
              />
            </div>
          </div>
        </div>

        {/* Work Experience Section */}
        <div className="bg-orange-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>🔹</span> Work Experience
          </h2>
          {formData.workExperience.map((exp, index) => (
            <div key={index} className="mb-6 p-4 bg-gray rounded-lg border">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label>Job Title</label>
                  <input
                    type="text"
                    value={exp.jobTitle}
                    onChange={(e) => handleInputChange(e, index, "jobTitle", "workExperience")}
                    placeholder="Software Engineer"
                  />
                </div>
                <div>
                  <label>Company Name</label>
                  <input
                    type="text"
                    value={exp.companyName}
                    onChange={(e) => handleInputChange(e, index, "companyName", "workExperience")}
                    placeholder="Tech Company Inc."
                  />
                </div>
                <div>
                  <label>Location</label>
                  <input
                    type="text"
                    value={exp.location}
                    onChange={(e) => handleInputChange(e, index, "location", "workExperience")}
                    placeholder="San Francisco, CA"
                  />
                </div>
                <div>
                  <label>Start Date - End Date</label>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={exp.startDate}
                      onChange={(e) => handleInputChange(e, index, "startDate", "workExperience")}
                      className="w-1/2"
                      placeholder="MM/YYYY"
                    />
                    <input
                      type="text"
                      value={exp.endDate}
                      onChange={(e) => handleInputChange(e, index, "endDate", "workExperience")}
                      className="w-1/2"
                      placeholder="MM/YYYY or Present"
                    />
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <label>Key Responsibilities</label>
                  <textarea
                    value={exp.responsibilities}
                    onChange={(e) => handleInputChange(e, index, "responsibilities", "workExperience")}
                    rows="3"
                    placeholder="• Developed and maintained web applications using React and Node.js&#10;• Collaborated with cross-functional teams to deliver features&#10;• Implemented responsive design and optimized performance"
                  />
                </div>
                <div>
                  <label>Achievements / Impact (with metrics)</label>
                  <textarea
                    value={exp.achievements}
                    onChange={(e) => handleInputChange(e, index, "achievements", "workExperience")}
                    rows="3"
                    placeholder="• Increased application performance by 40% through code optimization&#10;• Led a team of 5 developers to deliver project 2 weeks ahead of schedule&#10;• Reduced bug reports by 30% through implementation of automated testing"
                  />
                </div>
              </div>
              {formData.workExperience.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeItem("workExperience", index)}
                  className="mt-4 text-red-600 font-medium"
                >
                  Remove Experience
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => addItem("workExperience")}
            className="w-full bg-gray-100 font-medium py-2 px-4 rounded-md transition"
          >
            + Add Another Work Experience
          </button>
        </div>

        {/* Education Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>🔹</span> Education
          </h2>
          {formData.education.map((edu, index) => (
            <div key={index} className="mb-6 p-4 bg-gray rounded-lg border">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label>Degree</label>
                  <input
                    type="text"
                    value={edu.degree}
                    onChange={(e) => handleInputChange(e, index, "degree", "education")}
                    placeholder="Bachelor of Science in Computer Science"
                  />
                </div>
                <div>
                  <label>University/College Name</label>
                  <input
                    type="text"
                    value={edu.universityName}
                    onChange={(e) => handleInputChange(e, index, "universityName", "education")}
                    placeholder="University of Technology"
                  />
                </div>
                <div>
                  <label>Location</label>
                  <input
                    type="text"
                    value={edu.location}
                    onChange={(e) => handleInputChange(e, index, "location", "education")}
                    placeholder="Boston, MA"
                  />
                </div>
                <div>
                  <label>Start Date - End Date</label>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={edu.startDate}
                      onChange={(e) => handleInputChange(e, index, "startDate", "education")}
                      className="w-1/2"
                      placeholder="MM/YYYY"
                    />
                    <input
                      type="text"
                      value={edu.endDate}
                      onChange={(e) => handleInputChange(e, index, "endDate", "education")}
                      className="w-1/2"
                      placeholder="MM/YYYY"
                    />
                  </div>
                </div>
                <div>
                  <label>GPA (Optional)</label>
                  <input
                    type="text"
                    value={edu.gpa}
                    onChange={(e) => handleInputChange(e, index, "gpa", "education")}
                    placeholder="3.8/4.0"
                  />
                </div>
                <div>
                  <label>Relevant Coursework (Optional)</label>
                  <input
                    type="text"
                    value={edu.relevantCoursework}
                    onChange={(e) => handleInputChange(e, index, "relevantCoursework", "education")}
                    placeholder="Data Structures, Algorithms, Machine Learning"
                  />
                </div>
              </div>
              {formData.education.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeItem("education", index)}
                  className="mt-4 text-red-600 font-medium"
                >
                  Remove Education
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => addItem("education")}
            className="w-full bg-blue-100 font-medium py-2 px-4 rounded-md transition"
          >
            + Add Another Education
          </button>
        </div>

        {/* Projects Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>📌</span> Projects
          </h2>
          {formData.projects.map((proj, index) => (
            <div key={index} className="mb-6 p-4 bg-gray rounded-lg border">
              <div className="space-y-4">
                <div>
                  <label>Project Title</label>
                  <input
                    type="text"
                    value={proj.projectTitle}
                    onChange={(e) => handleInputChange(e, index, "projectTitle", "projects")}
                    placeholder="E-commerce Web Application"
                  />
                </div>
                <div>
                  <label>Brief Description (problem + solution)</label>
                  <textarea
                    value={proj.description}
                    onChange={(e) => handleInputChange(e, index, "description", "projects")}
                    rows="3"
                    placeholder="Developed a full-stack e-commerce platform to solve inventory management issues for small businesses. Implemented real-time inventory tracking and automated order processing."
                  />
                </div>
                <div>
                  <label>Technologies/Tools Used</label>
                  <input
                    type="text"
                    value={proj.technologiesUsed}
                    onChange={(e) => handleInputChange(e, index, "technologiesUsed", "projects")}
                    placeholder="React, Node.js, MongoDB, AWS, Docker"
                  />
                </div>
                <div>
                  <label>Impact (with metrics if possible)</label>
                  <input
                    type="text"
                    value={proj.impact}
                    onChange={(e) => handleInputChange(e, index, "impact", "projects")}
                    placeholder="Reduced load time by 40%, increased user engagement by 25%"
                  />
                </div>
                <div>
                  <label>Project Link</label>
                  <input
                    type="url"
                    value={proj.projectLink}
                    onChange={(e) => handleInputChange(e, index, "projectLink", "projects")}
                    placeholder="https://github.com/username/project or live demo URL"
                  />
                </div>
              </div>
              {formData.projects.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeItem("projects", index)}
                  className="mt-4 text-red-600 font-medium"
                >
                  Remove Project
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => addItem("projects")}
            className="w-full bg-blue-100 font-medium py-2 px-4 rounded-md transition"
          >
            + Add Another Project
          </button>
        </div>

        {/* Certifications Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>📌</span> Certifications & Training
          </h2>
          {formData.certifications.map((cert, index) => (
            <div key={index} className="mb-6 p-4 bg-gray rounded-lg border">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label>Certification Name</label>
                  <input
                    type="text"
                    value={cert.certificationName}
                    onChange={(e) => handleInputChange(e, index, "certificationName", "certifications")}
                    placeholder="AWS Certified Solutions Architect"
                  />
                </div>
                <div>
                  <label>Issuing Authority</label>
                  <input
                    type="text"
                    value={cert.issuingAuthority}
                    onChange={(e) => handleInputChange(e, index, "issuingAuthority", "certifications")}
                    placeholder="Amazon Web Services"
                  />
                </div>
                <div>
                  <label>Date</label>
                  <input
                    type="text"
                    value={cert.date}
                    onChange={(e) => handleInputChange(e, index, "date", "certifications")}
                    placeholder="MM/YYYY or 'In Progress'"
                  />
                </div>
              </div>
              {formData.certifications.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeItem("certifications", index)}
                  className="mt-4 text-red-600 font-medium"
                >
                  Remove Certification
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => addItem("certifications")}
            className="w-full bg-blue-100 font-medium py-2 px-4 rounded-md transition"
          >
            + Add Another Certification
          </button>
        </div>

        {/* Achievements Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>📌</span> Achievements / Awards
          </h2>
          {formData.achievements.map((ach, index) => (
            <div key={index} className="mb-6 p-4 bg-gray rounded-lg border">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label>Award/Recognition Title</label>
                  <input
                    type="text"
                    value={ach.title}
                    onChange={(e) => handleInputChange(e, index, "title", "achievements")}
                    placeholder="Employee of the Month"
                  />
                </div>
                <div>
                  <label>Organization/Institution</label>
                  <input
                    type="text"
                    value={ach.organization}
                    onChange={(e) => handleInputChange(e, index, "organization", "achievements")}
                    placeholder="Tech Company Inc."
                  />
                </div>
                <div>
                  <label>Date</label>
                  <input
                    type="text"
                    value={ach.date}
                    onChange={(e) => handleInputChange(e, index, "date", "achievements")}
                    placeholder="MM/YYYY"
                  />
                </div>
              </div>
              <div>
                <label>Description</label>
                <textarea
                  value={ach.description}
                  onChange={(e) => handleInputChange(e, index, "description", "achievements")}
                  rows="2"
                  placeholder="Recognized for outstanding performance and leadership in project delivery"
                />
              </div>
              {formData.achievements.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeItem("achievements", index)}
                  className="mt-4 text-red-600 font-medium"
                >
                  Remove Achievement
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => addItem("achievements")}
            className="w-full bg-blue-100 font-medium py-2 px-4 rounded-md transition"
          >
            + Add Another Achievement
          </button>
        </div>

        {/* Additional Sections */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl border-b-2 pb-2">
            <span>📌</span> Additional Sections (Optional)
          </h2>
          <div className="space-y-4">
            <div>
              <label>Languages</label>
              <textarea
                name="languages"
                value={formData.languages}
                onChange={handleInputChange}
                rows="2"
                placeholder="English (Native), Spanish (Fluent), French (Conversational)"
              />
            </div>
            <div>
              <label>Publications / Blogs / Research Papers</label>
              <textarea
                name="publications"
                value={formData.publications}
                onChange={handleInputChange}
                rows="3"
                placeholder="List any publications, blog posts, or research papers with titles and links"
              />
            </div>
            <div>
              <label>Volunteering / Extracurriculars</label>
              <textarea
                name="volunteering"
                value={formData.volunteering}
                onChange={handleInputChange}
                rows="3"
                placeholder="Volunteer work, leadership roles, community involvement"
              />
            </div>
            <div>
              <label>Hobbies & Interests (only if relevant to role)</label>
              <textarea
                name="hobbies"
                value={formData.hobbies}
                onChange={handleInputChange}
                rows="2"
                placeholder="Photography, Open Source Contributing, Marathon Running"
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-center pt-6">
          <button
            type="submit"
            disabled={loading}
            className="bg-gradient-to-r px-8 py-3 font-semibold rounded-lg shadow-lg transform hover:scale-105"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Generating Resume...
              </div>
            ) : (
              "Generate Professional Resume"
            )}
          </button>
        </div>

        {error && (
          <div className="mt-4 bg-red-50 rounded-md">
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* ATS Tips */}
        <div className="mt-8 bg-orange-50 rounded-lg">
          <h3 className="text-lg mb-3">✅ ATS Optimization Tips:</h3>
          <ul className="text-sm space-y-1">
            <li>• Keep formatting simple with standard section headers</li>
            <li>• Use keywords from job descriptions (customize per role)</li>
            <li>• List skills in comma-separated format for better parsing</li>
            <li>• Include metrics and achievements with numbers (%, $, growth)</li>
            <li>• Use reverse chronological format (most recent first)</li>
            <li>• Avoid tables, columns, graphics, and fancy formatting</li>
            <li>• Save as PDF to preserve formatting when submitting</li>
          </ul>
        </div>
      </form>
    </div>
  );
}

export default GenerateResume;