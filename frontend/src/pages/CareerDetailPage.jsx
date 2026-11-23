import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { Compass, DollarSign, TrendingUp, BookOpen, FolderGit2, Award, CheckCircle2, ArrowLeft, GitCompare } from 'lucide-react';
import Badge from '../components/Badge';

const CareerDetailPage = () => {
  const { id } = useParams();
  const [career, setCareer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCareer();
  }, [id]);

  const fetchCareer = async () => {
    try {
      const res = await api.get(`/careers/${id}`);
      setCareer(res.data);
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

  if (!career) {
    return (
      <div className="p-8 text-center text-xs text-slate-500">
        Career role not found.
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      
      <Link
        to="/careers"
        className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-primary-600 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to All Careers
      </Link>

      {/* Main Header Banner */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-primary-900/15 via-indigo-900/5 to-transparent border-primary-200/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="primary">{career.industry}</Badge>
              <Badge variant="success">Demand: {career.market_demand}</Badge>
              <Badge variant="default">Level: {career.difficulty}</Badge>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              {career.title}
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 mt-2 max-w-3xl leading-relaxed">
              {career.description}
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-center shrink-0">
            <div className="text-xs text-slate-400 font-semibold mb-1">Average Compensation</div>
            <div className="text-sm font-extrabold text-emerald-600 dark:text-emerald-400">
              {career.average_salary}
            </div>
            <Link
              to="/career-comparison"
              className="mt-3 px-3 py-1.5 rounded-lg bg-primary-50 dark:bg-primary-950 text-primary-600 dark:text-primary-400 text-xs font-bold flex items-center justify-center gap-1 hover:bg-primary-100"
            >
              <GitCompare className="w-3 h-3" /> Compare Role
            </Link>
          </div>
        </div>
      </div>

      {/* Grid of details */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Required Technical Skills (7 cols) */}
        <div className="lg:col-span-7 glass-card p-6">
          <h3 className="font-bold text-base text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <Award className="w-5 h-5 text-primary-600" /> Required Technical Competencies
          </h3>

          <div className="space-y-3">
            {career.skills?.map((s, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/60">
                <div className="flex items-center justify-between text-xs font-bold mb-1.5">
                  <span className="text-slate-800 dark:text-slate-200">{s.skill_name}</span>
                  <span className="text-primary-600">Benchmark: {Math.round(s.required_level)}%</span>
                </div>
                <div className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary-600 rounded-full"
                    style={{ width: `${s.required_level}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Soft Skills & Academic Requirements (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          
          <div className="glass-card p-6">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white mb-3 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Essential Soft Skills
            </h3>
            <div className="flex flex-wrap gap-2">
              {career.soft_skills?.map((ss, idx) => (
                <Badge key={idx} variant="primary" className="text-xs px-2.5 py-1">
                  {ss}
                </Badge>
              ))}
            </div>

            <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                Education Prerequisite
              </span>
              <p className="text-xs text-slate-700 dark:text-slate-300 font-medium">
                {career.education_requirement}
              </p>
            </div>
          </div>

          <div className="glass-card p-6">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white mb-3 flex items-center gap-2">
              <FolderGit2 className="w-4 h-4 text-indigo-600" /> Recommended Capstone Projects
            </h3>
            <div className="space-y-2">
              {career.recommended_projects?.map((proj, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200/50 dark:border-slate-800/50 text-xs text-slate-700 dark:text-slate-300">
                  • {proj}
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};

export default CareerDetailPage;
