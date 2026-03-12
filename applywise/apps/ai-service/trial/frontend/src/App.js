import React, { useState, useRef } from 'react';
import { Route, Routes, Link } from 'react-router-dom';
import './index.css';
import NeuralNetworkBackground from './NeuralNetworkBackground';
import WhatWeDo from './WhatWeDo';
import Predict from './Predict';
import CoverLetter from './CoverLetter';
import GenerateResume from './GenerateResume';
import MarketTrends from './MarketTrends';
import StudyAssistant from './StudyAssistant';

function App() {
  const [showResumeSection, setShowResumeSection] = useState(false);
  const [showPredictSection, setShowPredictSection] = useState(false);
  const [showStudySection, setShowStudySection] = useState(false);
  const resumeSectionRef = useRef(null);
  const predictSectionRef = useRef(null);
  const studySectionRef = useRef(null);

  const handleResumeClick = () => {
    setShowResumeSection(true);
    setShowPredictSection(false);
    setShowStudySection(false);
    if (resumeSectionRef.current) {
      resumeSectionRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handlePredictClick = () => {
    setShowPredictSection(true);
    setShowResumeSection(false);
    setShowStudySection(false);
    if (predictSectionRef.current) {
      predictSectionRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleStudyClick = () => {
    setShowStudySection(true);
    setShowResumeSection(false);
    setShowPredictSection(false);
    if (studySectionRef.current) {
      studySectionRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div>
      <NeuralNetworkBackground />
      <nav className="navbar">
        <Link to="/">
          <button>Home</button>
        </Link>
        <Link to="/what-we-do">
          <button>What We Do</button>
        </Link>
        <Link to="/about-us">
          <button>About Us</button>
        </Link>
      </nav>
      <Routes>
        <Route
          path="/"
          element={
            <div className="landing-container">
              <div className="landing-content">
                <h1>Welcome to Resume Screening App</h1>
                <h2>Your Career, Optimized with AI</h2>
                <p>
                  Our AI-powered platform helps you craft the perfect resume, generate professional cover letters, and stay ahead with market trends.
                </p>
                <div className="button-container">
                  <button onClick={handleResumeClick}>Resume Assistance</button>
                  <button onClick={handlePredictClick}>Analyse resume</button>
                  <button onClick={handleStudyClick}>Study Assistant</button>
                  <Link to="/market-trends">
                    <button>Market Trends</button>
                  </Link>
                </div>
              </div>
              {showResumeSection && (
                <div className="resume-section" ref={resumeSectionRef}>
                  <h2>Resume Assistance</h2>
                  <p>
                    Upload your resume or use our tools to generate a professional resume tailored to your career goals.
                  </p>
                  <div className="section-content">
                    <h3>Generate Resume</h3>
                    <GenerateResume />
                    <h3>Create Cover Letter</h3>
                    <CoverLetter />
                  </div>
                </div>
              )}
              {showPredictSection && (
                <div className="predict-section" ref={predictSectionRef}>
                  <h2>Analyze resume</h2>
                  <p>Analyze your resume to predict your chances of success and get personalized feedback.</p>
                  <div className="section-content">
                    <Predict />
                  </div>
                </div>
              )}
              {showStudySection && (
                <div className="study-section" ref={studySectionRef}>
                  <h2>Study Assistant</h2>
                  <p>Get personalized study plans, practice questions, and learning resources to advance your career.</p>
                  <div className="section-content">
                    <StudyAssistant />
                  </div>
                </div>
              )}
            </div>
          }
        />
        <Route path="/what-we-do" element={<WhatWeDo />} />
        <Route
          path="/about-us"
          element={
            <div className="landing-container">
              <div className="landing-content">
                <h1>About Us</h1>
                <p>The core mission of Career Coach AI is to streamline career preparation for students. Specific
objectives include:
• Delivering personalised career guidance based on user profiles and aspirations.
• Enabling the generation of customized resumes and cover letters to match job requirements.
• Calculating selection chances for job applications using predictive analytics.
• Providing up-to-date insights into job market trends and emerging opportunities.
• Offering study assistance, including detailed roadmaps for career paths and curated study
materials.
These goals are achieved through a modular design that incorporates machine learning for accuracy
and React's reactivity for a smooth user experience, ensuring the platform evolves with user
feedback and technological advancements.</p>
              </div>
            </div>
          }
        />
        <Route
          path="/market-trends"
          element={
            <div className="landing-container">
              <MarketTrends />
            </div>
          }
        />
      </Routes>
    </div>
  );
}

export default App;