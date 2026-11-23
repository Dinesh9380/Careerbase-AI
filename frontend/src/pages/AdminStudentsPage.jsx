import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Users, Search, Award, CheckCircle2, ChevronRight, Mail } from 'lucide-react';
import Badge from '../components/Badge';

const AdminStudentsPage = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchStudents();
  }, [search]);

  const fetchStudents = async () => {
    try {
      const url = search ? `/admin/students?search=${encodeURIComponent(search)}` : '/admin/students';
      const res = await api.get(url);
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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            Student Roster & Cohort Management
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
            Directory of all registered students, their degree, academic standing, and targeted career paths.
          </p>
        </div>

        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by student name or email..."
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      {/* Table */}
      <div className="glass-card overflow-hidden">
        <div className="divide-y divide-slate-100 dark:divide-slate-800">
          {students.map((student) => (
            <div key={student.id} className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
              <div className="flex items-center gap-3.5">
                <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-primary-600 to-indigo-500 text-white flex items-center justify-center font-bold text-sm shadow-md shadow-primary-500/20">
                  {student.full_name.charAt(0)}
                </div>
                <div>
                  <h3 className="font-bold text-sm text-slate-900 dark:text-white">{student.full_name}</h3>
                  <div className="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
                    <span className="flex items-center gap-1">
                      <Mail className="w-3 h-3" /> {student.email}
                    </span>
                    <span>•</span>
                    <span>{student.degree} (CGPA: {student.cgpa})</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-6">
                <div className="text-right">
                  <span className="text-[11px] text-slate-400 block font-semibold uppercase">Target Career</span>
                  <span className="text-xs font-bold text-primary-600 dark:text-primary-400">
                    {student.desired_job_role}
                  </span>
                </div>

                <div className="w-28 text-right">
                  <span className="text-[11px] text-slate-400 block font-semibold uppercase">Completeness</span>
                  <span className="text-xs font-bold text-emerald-600">
                    {Math.round(student.profile_completeness)}%
                  </span>
                </div>

                <Badge variant="primary" className="text-xs">
                  {student.points} XP
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default AdminStudentsPage;
