// import React from 'react';
// import { useNavigate } from 'react-router-dom';
// import './index.css';

// const WhatWeDo = () => {
//   const navigate = useNavigate();

//   return (
//     <div>
//       <header className="navbar">
//         <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
//           Home
//         </button>
//         <button onClick={() => navigate('/what-we-do')}>
//           What We Do
//         </button>
//         <button onClick={() => {
//           navigate('/');
//           setTimeout(() => {
//             const aboutSection = document.getElementById('about-us');
//             if (aboutSection) {
//               aboutSection.scrollIntoView({ behavior: 'smooth' });
//             }
//           }, 0);
//         }}>
//           About Us
//         </button>
//       </header>
//       <div className="container">
//         <div className="card">
//           <h2>What We Do</h2>
//           <p>This section is under development. Stay tuned for more details about our services!</p>
//           <button className="button-outlined" onClick={() => navigate('/')}>
//             Back to Home
//           </button>
//         </div>
//       </div>
//       <footer>
//         <p>&copy; 2025 AI Career Assistant. All rights reserved.</p>
//       </footer>
//     </div>
//   );
// };

// export default WhatWeDo;
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './whatwedo.css'; // Make sure your CSS file is imported

const WhatWeDo = () => {
  const navigate = useNavigate();

  return (
    <div className="page-container">
      {/* Navbar */}
      {/* <header className="navbar">
        <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          Home
        </button>
        <button onClick={() => navigate('/what-we-do')}>
          What We Do
        </button>
        <button
          onClick={() => {
            navigate('/');
            setTimeout(() => {
              const aboutSection = document.getElementById('about-us');
              if (aboutSection) {
                aboutSection.scrollIntoView({ behavior: 'smooth' });
              }
            }, 0);
          }}
        >
          About Us
        </button>
      </header> */}

      {/* Card */}
      <main className="card-container">
        <div className="card">
          <h2>What We Do</h2>
          <p>The transition from academia to the professional world is fraught with obstacles, including a lack of
individualized advice, inadequate resources for document preparation, and limited insights into
employment probabilities and industry shifts. Career Coach AI addresses these pain points by
offering a suite of features tailored to student needs. Through an intuitive interface developed in
React, users can interact seamlessly with AI-powered functionalities that leverage Python-based
machine learning models for data analysis and prediction. Flask ensures efficient API handling,
while additional technologies enhance scalability and performance.</p>
          <button className="button-outlined" onClick={() => navigate('/')}>
            Back to Home
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>&copy; 2025 AI Career Assistant. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default WhatWeDo;
