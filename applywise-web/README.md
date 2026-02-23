# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


# 🚀 ApplyWise: Job Application Tracker

**ApplyWise** is a full-stack React application designed to help job seekers organize their recruitment journey. It eliminates "spreadsheet fatigue" by providing a centralized dashboard to track applications, visualize progress through an interview funnel, and manage interview notes in real-time.

---

## 🛠️ Tech Stack

* **Frontend:** React (Vite)
* **Styling:** CSS3 (Custom Design System with Flexbox & Grid)
* **Database & Auth:** Firebase (Firestore & Google Auth)
* **Data Viz:** Chart.js (Application Funnel)
* **Routing:** React Router v6

---

## 🧠 Architectural Mechanics

### 1. The Data Flow (End-to-End)

Use npm run dev to start the frontend application. When you run "npm run dev" the following happens=>

Vite starts a local server: It identifies your vite.config.js and creates a lightning-fast development environment (usually at http://localhost:5173).

The browser loads index.html: Unlike traditional apps, the HTML is almost empty, containing only a <div id="root"></div>.

index.html calls src/main.jsx: The browser sees the script tag <script type="module" src="/src/main.jsx"></script> and fetches the JavaScript entry point.

main.jsx tells React to take over: The ReactDOM.createRoot function finds the #root div and "hydrates" it with your React components.

React looks at App.jsx: It checks the user state. If the state is null (because no one is logged in yet), it triggers the Public Route.

Style Injection: The browser simultaneously parses index.css and App.css. It applies the .app-container rules to center the view and the .card rules to draw the white login box.

DOM Rendering: React injects the <h2>Sign in to start tracking jobs</h2> and the <button> into the DOM.

Event Listening: The "Sign in with Google" button sits "armed." When clicked, it invokes handleLogin, which triggers the Firebase Handshake defined in firebase.js.

The application follows a strict **unidirectional data flow**.

* **Authentication:** `App.jsx` uses a listener (`onAuthStateChanged`) to monitor the user's session.
* **Storage:** Data is scoped to the individual user’s email via Firestore queries, ensuring privacy and data integrity.
* **Visualization:** Raw data from Firestore is reduced into status counts and mapped to a fixed "Funnel Order" (Applied → OA → Technical → HR → Offer) before being rendered by Chart.js.

### 2. Styling Strategy

We utilize a **dual-layer CSS architecture**:

* **`index.css` (The Global Laws):** Defines the "World" of ApplyWise. This includes the global Flexbox layout, the semantic color system for job statuses, and the mobile-responsive Grid rules.
* **`App.css` (The Local Decoration):** Handles component-specific animations and the high-level `#root` container constraints.

---

## 🎨 Design System & UI Components

### Semantic Status Colors

To provide instant visual feedback, the application uses a color-coded system defined in `index.css`:

* 🔵 **Applied:** Standard blue
* 🟠 **OA:** Online Assessment orange
* 🟣 **Technical:** Interview purple
* 🟢 **Offer:** Success green
* 🔴 **Rejected:** Termination red

### Responsive Layout

The UI utilizes a "Mobile-First" mindset. The `add-job-form` uses **CSS Grid** to switch from a 2-column layout on desktop to a single-stack layout on mobile devices via `@media` queries.

### User Experience (UX)

"The application pre-fills the 'Date Applied' field with the current system date. This reduces the number of clicks required to log a new application, as most users log their jobs on the same day they apply."

---

## 🚀 Getting Started

### 1. Prerequisites

* Node.js (v18+)
* A Firebase Project (Firestore + Google Auth enabled)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/applywise.git

# Install dependencies
npm install

# Start the development server
npm run dev

```

### 3. Configuration

Create a `src/firebase.js` file and populate it with your Firebase SDK configuration:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_ID",
  appId: "YOUR_APP_ID"
};
