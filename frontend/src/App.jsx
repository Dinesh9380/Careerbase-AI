import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute';

// Public Pages
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import VerifyCertificate from './pages/VerifyCertificate';

// Student Pages
import StudentDashboard from './pages/StudentDashboard';
import ProfilePage from './pages/ProfilePage';
import AssessmentsListPage from './pages/AssessmentsListPage';
import AssessmentTakePage from './pages/AssessmentTakePage';
import AssessmentResultPage from './pages/AssessmentResultPage';
import SkillsOverviewPage from './pages/SkillsOverviewPage';
import SkillGapsPage from './pages/SkillGapsPage';
import CareersListPage from './pages/CareersListPage';
import CareerDetailPage from './pages/CareerDetailPage';
import CareerComparisonPage from './pages/CareerComparisonPage';
import RoadmapPage from './pages/RoadmapPage';
import LearningResourcesPage from './pages/LearningResourcesPage';
import ResumePage from './pages/ResumePage';
import CertificatesPage from './pages/CertificatesPage';
import CareerAIPage from './pages/CareerAIPage';

// Admin Pages
import AdminDashboard from './pages/AdminDashboard';
import AdminStudentsPage from './pages/AdminStudentsPage';
import AdminBigDataPage from './pages/AdminBigDataPage';
import AdminBlockchainPage from './pages/AdminBlockchainPage';
import AdminAuditLogsPage from './pages/AdminAuditLogsPage';

// Counselor Pages
import CounselorDashboard from './pages/CounselorDashboard';
import CounselorStudentDetailPage from './pages/CounselorStudentDetailPage';

// Shell Layout for Authenticated Views with Sidebar
const AppLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user } = useAuth();

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      <Navbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex-1 flex">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className={`flex-1 transition-all duration-200 px-4 sm:px-6 lg:px-8 py-6 ${user ? 'lg:pl-72' : ''}`}>
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  );
};

// Public Layout without Sidebar
const PublicLayout = () => (
  <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
    <Navbar onToggleSidebar={() => {}} />
    <main className="flex-1">
      <Outlet />
    </main>
    <Footer />
  </div>
);

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Routes>
            
            {/* Public Layout */}
            <Route element={<PublicLayout />}>
              <Route path="/" element={<Landing />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/verify" element={<VerifyCertificate />} />
              <Route path="/verify/:credentialId" element={<VerifyCertificate />} />
            </Route>

            {/* Student Protected Portal */}
            <Route element={<ProtectedRoute allowedRoles={['student', 'admin']} />}>
              <Route element={<AppLayout />}>
                <Route path="/dashboard" element={<StudentDashboard />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/assessments" element={<AssessmentsListPage />} />
                <Route path="/assessment/:id" element={<AssessmentTakePage />} />
                <Route path="/assessment/result/:id" element={<AssessmentResultPage />} />
                <Route path="/skills" element={<SkillsOverviewPage />} />
                <Route path="/skill-gaps" element={<SkillGapsPage />} />
                <Route path="/careers" element={<CareersListPage />} />
                <Route path="/careers/:id" element={<CareerDetailPage />} />
                <Route path="/career-comparison" element={<CareerComparisonPage />} />
                <Route path="/roadmap" element={<RoadmapPage />} />
                <Route path="/resources" element={<LearningResourcesPage />} />
                <Route path="/resume" element={<ResumePage />} />
                <Route path="/certificates" element={<CertificatesPage />} />
                <Route path="/career-ai" element={<CareerAIPage />} />
              </Route>
            </Route>

            {/* Admin Protected Portal */}
            <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
              <Route element={<AppLayout />}>
                <Route path="/admin/dashboard" element={<AdminDashboard />} />
                <Route path="/admin/students" element={<AdminStudentsPage />} />
                <Route path="/admin/bigdata" element={<AdminBigDataPage />} />
                <Route path="/admin/blockchain" element={<AdminBlockchainPage />} />
                <Route path="/admin/audit-logs" element={<AdminAuditLogsPage />} />
              </Route>
            </Route>

            {/* Counselor Protected Portal */}
            <Route element={<ProtectedRoute allowedRoles={['counselor', 'admin']} />}>
              <Route element={<AppLayout />}>
                <Route path="/counselor/dashboard" element={<CounselorDashboard />} />
                <Route path="/counselor/students" element={<CounselorDashboard />} />
                <Route path="/counselor/students/:id" element={<CounselorStudentDetailPage />} />
              </Route>
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />

          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
