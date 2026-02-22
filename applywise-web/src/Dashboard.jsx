// src/Dashboard.jsx
import { addDoc } from 'firebase/firestore';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth, db } from './firebase';
import { collection, query, where, getDocs, deleteDoc, doc} from 'firebase/firestore';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import ChartDataLabels from 'chartjs-plugin-datalabels';
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ChartDataLabels);

function Dashboard() {
  const navigate = useNavigate();
  console.log("Your UID:", auth.currentUser?.uid);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);


useEffect(() => {
  const fetchJobs = async () => {
    if (!auth.currentUser?.email) return;

    setLoading(true);
    try {
      const userEmail = auth.currentUser.email;

      const q = query(
        collection(db, 'jobs'),
        where('email', '==', userEmail)  // ← filter by logged-in user's email
      );

      const querySnapshot = await getDocs(q);
      const userJobs = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));

      setJobs(userJobs);
    } catch (error) {
      console.error("Error fetching jobs:", error);
      alert("Could not load your jobs. Check console.");
    } finally {
      setLoading(false);
    }
  };

  fetchJobs();
}, [auth.currentUser?.email]);  // re-run when email changes (e.g. logout/login)


// Funnel chart data (exact match, no normalization)
const statusOrder = ['Applied', 'OA', 'Technical', 'HR', 'Offer']; // fixed order

const statusCounts = jobs.reduce((acc, job) => {
  const status = job.status?.trim() || 'Applied'; // fallback if missing
  acc[status] = (acc[status] || 0) + 1;
  return acc;
}, {});

// Force all stages to have a count (even 0)
const chartData = statusOrder.map(status => statusCounts[status] || 0);

const total = chartData.reduce((sum, val) => sum + val, 0) || 1; // avoid division by zero

const funnelData = {
  labels: statusOrder,
  datasets: [{
    label: 'Applications',
    data: chartData,
    backgroundColor: [
      '#2563eb', // Applied
      '#3b82f6', // OA
      '#60a5fa', // Technical
      '#93c5fd', // HR
      '#10b981', // Offer
    ],
    borderWidth: 1,
  }],
};

const funnelOptions = {
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Your Application Funnel',
      font: { size: 18 },
      padding: { top: 10, bottom: 20 }
    },
    tooltip: {
      enabled: true, // force tooltips on
      callbacks: {
        label: function(context) {
          const value = context.raw;
          const percentage = total > 0 ? ((value / total) * 100).toFixed(0) : 0;
          return `${context.label}: ${value} applications (${percentage}%)`;
        }
      }
    },
    datalabels: {
      anchor: 'end',
      align: 'end',
      color: '#333',
      font: { weight: 'bold', size: 12 },
      formatter: (value) => value > 0 ? value : ''
    }
  },
  scales: {
    x: {
      beginAtZero: true,
      min: 0,
      suggestedMax: Math.max(...chartData, 1) + 2, // give room for labels
      title: { display: true, text: 'Number of Applications' },
      ticks: { stepSize: 1 }
    },
    y: {
      title: { display: true, text: 'Stage' },
      ticks: {
        autoSkip: false, // force every label to show
        maxRotation: 0,
        minRotation: 0
      }
    }
  },
  animation: {
    duration: 800 // smooth
  }
};



return (
  <div className="dashboard">
    <h2>Your Dashboard</h2>
    <p>Track your applications and see where you're at.</p>

    {/* Job List Table */}
    <div className="card">
      <h3>Recent Applications</h3>
      {loading ? (
        <p>Loading your jobs...</p>
      ) : jobs.length === 0 ? (
        <p>No applications yet. Add one below!</p>
      ) : (
        <table className="job-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Company</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map(job => (
  <tr key={job.id}>
    <td>{job.dateApplied || 'N/A'}</td>
    <td>{job.company || 'N/A'}</td>
    <td>{job.role || 'N/A'}</td>
    <td className={`status ${job.status?.toLowerCase() || 'applied'}`}>
      {job.status || 'Applied'}
    </td>
    <td>
      <button
        onClick={async () => {
          if (!window.confirm(`Delete ${job.company} - ${job.role}?`)) return;
          try {
            await deleteDoc(doc(db, 'jobs', job.id));
            setJobs(jobs.filter(j => j.id !== job.id));
          } catch (err) {
            alert('Delete failed: ' + err.message);
          }
        }}
        style={{
          background: 'none', border: '1px solid #fca5a5',
          color: '#dc2626', borderRadius: '5px',
          padding: '3px 10px', cursor: 'pointer', fontSize: '12px'
        }}
      >
        Delete
      </button>
    </td>
  </tr>
))}
          </tbody>
        </table>
      )}
    </div>

    {/* Funnel Chart */}
    <div className="card">
      <Bar data={funnelData} options={funnelOptions} />
    </div>

    {/* New: Add Job Form */}
    <div className="card">
      <h3>Add New Job</h3>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          const newJob = {
            userId: auth.currentUser.uid,
            email: auth.currentUser.email,
            dateApplied: formData.get('dateApplied') || new Date().toISOString().split('T')[0],
            company: formData.get('company')?.trim(),
            role: formData.get('role')?.trim(),
            status: formData.get('status'),
            stipend: formData.get('stipend')?.trim() || '',
            description: formData.get('description')?.trim() || '',
            link: formData.get('link')?.trim() || '',
            notes: formData.get('notes')?.trim() || '',
            timestamp: new Date().toISOString()
          };

          // Basic validation
          if (!newJob.company || !newJob.role || !newJob.status) {
            alert('Please fill Company, Role, and Status');
            return;
          }

          try {
            await addDoc(collection(db, 'jobs'), newJob);
            alert('Job added successfully!');
            // Refresh job list
            const updatedJobs = [...jobs, { id: 'temp-' + Date.now(), ...newJob }];
            setJobs(updatedJobs);
            e.target.reset(); // clear form
          } catch (error) {
            console.error("Add job error:", error);
            alert('Failed to add job. Check console.');
          }
        }}
        className="add-job-form"
      >
        <div className="form-group">
          <label>Date Applied</label>
          <input type="date" name="dateApplied" defaultValue={new Date().toISOString().split('T')[0]} />
        </div>

        <div className="form-group">
          <label>Company</label>
          <input type="text" name="company" placeholder="e.g. Google" required />
        </div>

        <div className="form-group">
          <label>Role</label>
          <input type="text" name="role" placeholder="e.g. Software Engineer" required />
        </div>

        <div className="form-group">
          <label>Status</label>
          <select name="status" required>
            <option value="">Select status</option>
            <option value="Applied">Applied</option>
            <option value="OA">OA</option>
            <option value="Technical">Technical</option>
            <option value="HR">HR</option>
            <option value="Offer">Offer</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>

        <div className="form-group">
          <label>Stipend/Package</label>
          <input type="text" name="stipend" placeholder="e.g. 20-30 LPA" />
        </div>

        <div className="form-group">
          <label>Link</label>
          <input type="url" name="link" placeholder="https://..." />
        </div>

        <div className="form-group">
          <label>Notes</label>
          <textarea name="notes" placeholder="Any extra notes..." rows="3" />
        </div>

        <button type="submit" className="btn btn-primary">
          Add Job
        </button>
      </form>
    </div>

    <button
      className="btn btn-primary"
      onClick={() => navigate('/')}
    >
      Back to Home
    </button>
  </div>
);
}

export default Dashboard;