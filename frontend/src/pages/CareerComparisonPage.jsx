import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { GitCompare, CheckCircle2, AlertTriangle, Clock, DollarSign, ArrowRight } from 'lucide-react';
import Badge from '../components/Badge';

const CareerComparisonPage = () => {
  const [allCareers, setAllCareers] = useState([]);
  const [selectedIds, setSelectedIds] = useState([1, 3, 7]); // Full Stack, Data Scientist, Data Engineer
  const [comparison, setComparison] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCareersAndCompare();
  }, []);

  const fetchCareersAndCompare = async () => {
    try {
      const res = await api.get('/careers');
      setAllCareers(res.data);
      const initialIds = res.data.slice(0, 3).map(c => c.id);
      setSelectedIds(initialIds);
      runComparison(initialIds);
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  };

  const runComparison = async (ids) => {
    setLoading(true);
    try {
      const res = await api.post('/careers/compare', { career_ids: ids });
      setComparison(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const toggleCareer = (id) => {
    let next;
    if (selectedIds.includes(id)) {
      if (selectedIds.length <= 1) return; // Keep at least one
      next = selectedIds.filter(i => i !== id);
    } else {
      if (selectedIds.length >= 3) {
        next = [...selectedIds.slice(1), id];
      } else {
        next = [...selectedIds, id];
      }
    }
    setSelectedIds(next);
    runComparison(next);
  };

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-primary-900/10 via-indigo-900/5 to-transparent border-primary-200/40">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Multi-Career Comparative Matrix
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
          Evaluate side-by-side readiness, compensation, missing skill gaps, and learning time investment across your top choices.
        </p>

        {/* Role Selector Chips */}
        <div className="flex flex-wrap gap-2 mt-6 pt-4 border-t border-slate-200/60 dark:border-slate-800/60">
          {allCareers.slice(0, 10).map(c => {
            const isSelected = selectedIds.includes(c.id);
            return (
              <button
                key={c.id}
                onClick={() => toggleCareer(c.id)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  isSelected
                    ? 'bg-primary-600 text-white shadow-md shadow-primary-500/20'
                    : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-800 hover:bg-slate-50'
                }`}
              >
                {c.title}
              </button>
            );
          })}
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center min-h-[40vh]">
          <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : (
        /* Side-by-Side Comparison Cards Grid */
        <div className={`grid grid-cols-1 md:grid-cols-${comparison.length} gap-6`}>
          {comparison.map((item) => (
            <div key={item.career_id} className="glass-card p-6 flex flex-col justify-between border-2 border-slate-200/80 dark:border-slate-800/80 hover:border-primary-500/40 transition-all">
              
              <div className="space-y-6">
                
                {/* Title & Match */}
                <div className="pb-4 border-b border-slate-100 dark:border-slate-800">
                  <h3 className="font-extrabold text-lg text-slate-900 dark:text-white">
                    {item.title}
                  </h3>
                  <div className="flex items-center justify-between mt-3">
                    <Badge variant={item.match_score >= 75 ? 'success' : 'primary'} className="text-xs">
                      {item.readiness_level}
                    </Badge>
                    <span className="text-xl font-extrabold text-primary-600">
                      {Math.round(item.match_score)}%
                    </span>
                  </div>
                </div>

                {/* Metrics */}
                <div className="space-y-2 text-xs">
                  <div className="flex items-center justify-between py-1.5 border-b border-slate-100 dark:border-slate-800/50">
                    <span className="text-slate-400">Est. Upskilling Time</span>
                    <span className="font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-indigo-500" /> ~{item.learning_time_weeks} Weeks
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 border-b border-slate-100 dark:border-slate-800/50">
                    <span className="text-slate-400">Average Salary</span>
                    <span className="font-bold text-emerald-600">{item.average_salary.split('/')[0]}</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 border-b border-slate-100 dark:border-slate-800/50">
                    <span className="text-slate-400">Difficulty</span>
                    <span className="font-bold text-slate-700 dark:text-slate-300">{item.difficulty}</span>
                  </div>
                </div>

                {/* Missing Skills */}
                <div>
                  <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                    Priority Missing Skills
                  </span>
                  <div className="space-y-1.5">
                    {item.missing_skills?.length === 0 ? (
                      <div className="text-xs text-emerald-600 font-semibold flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" /> All core skills satisfied
                      </div>
                    ) : (
                      item.missing_skills?.map((ms, idx) => (
                        <div key={idx} className="p-2 rounded-lg bg-rose-50/50 dark:bg-rose-950/20 text-xs text-rose-700 dark:text-rose-300 flex items-center justify-between">
                          <span>{ms.skill_name}</span>
                          <span className="font-bold">{ms.gap_severity}</span>
                        </div>
                      ))
                    )}
                  </div>
                </div>

              </div>

              <div className="mt-8 pt-4 border-t border-slate-100 dark:border-slate-800">
                <button
                  onClick={() => window.location.href = `/roadmap?career_id=${item.career_id}`}
                  className="w-full py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-sm flex items-center justify-center gap-1.5"
                >
                  Generate Roadmap <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

            </div>
          ))}
        </div>
      )}

    </div>
  );
};

export default CareerComparisonPage;
