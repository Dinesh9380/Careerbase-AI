import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Users, BookOpen, Compass, ChevronRight, MessageSquare, Award } from 'lucide-react';
import Badge from '../components/Badge';

const CounselorDashboard = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAssignedStudents();
  }, []);

  const fetchAssignedStudents = async () => {
    try {
      const res = await api.get('/counselor/students');
      setStudents(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-teal-900/10 via-primary-900/5 to-transparent border-teal-200/40">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Career Counselor Guidance Portal
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
          Review your assigned student cohorts, analyze their skill assessments and identified gaps, and formulate personalized guidance intervention notes.
        </p>
      </div>

      {/* Student List */}
      <div className="glass-card overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <h3 className="font-bold text-sm text-slate-900 dark:text-white">Assigned Student Cohort</h3>
          <span className="text-xs text-slate-400">{students.length} scholars assigned</span>
        </div>

        <div className="divide-y divide-slate-100 dark:divide-slate-800">
          {students.map((student) => (
            <div key={student.id} className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
              <div className="flex items-center gap-3.5">
                <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-teal-600 to-primary-600 text-white flex items-center justify-center font-bold text-sm shadow-md shadow-teal-500/20">
                  {student.student_name.charAt(0)}
                </div>
                <div>
                  <h4 className="font-bold text-sm text-slate-900 dark:text-white">{student.student_name}</h4>
                  <p className="text-xs text-slate-500">{student.email}</p>
                </div>
              </div>

              <div className="flex items-center gap-6">
                <div className="text-right">
                  <span className="text-[11px] text-slate-400 block font-semibold uppercase">Target Career</span>
                  <span className="text-xs font-bold text-primary-600">{student.target_career}</span>
                </div>

                <div className="text-right">
                  <span className="text-[11px] text-slate-400 block font-semibold uppercase">Notes Logged</span>
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300">{student.notes_count} Notes</span>
                </div>

                <Link
                  to={`/counselor/students/${student.id}`}
                  className="px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-sm flex items-center gap-1.5"
                >
                  Review Dossier <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default CounselorDashboard;
