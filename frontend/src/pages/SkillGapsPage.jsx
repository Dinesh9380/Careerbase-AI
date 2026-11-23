import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Layers, ArrowRight, AlertTriangle, CheckCircle, Map, Zap } from 'lucide-react';
import Badge from '../components/Badge';

const SkillGapsPage = () => {
  const [gaps, setGaps] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGaps();
  }, []);

  const fetchGaps = async () => {
    try {
      const res = await api.get('/students/me/skill-gaps');
      setGaps(res.data);
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

  const criticalCount = gaps.filter(g => g.gap_severity === 'Critical' || g.gap_severity === 'High').length;

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-amber-900/10 via-rose-900/5 to-transparent border-amber-200/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              Skill Gap Analysis
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
              Objective comparison of your current competencies against real employer job requirements. High severity gaps require prioritized upskilling.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-center shrink-0">
            <div className="text-xl font-extrabold text-rose-600">{criticalCount}</div>
            <div className="text-[11px] font-semibold text-slate-400">High Priority Gaps</div>
          </div>
        </div>
      </div>

      {/* Gaps List */}
      <div className="glass-card overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <h3 className="font-bold text-sm text-slate-900 dark:text-white">Detailed Gap Severity Matrix</h3>
          <Link to="/roadmap" className="text-xs text-primary-600 font-bold hover:underline flex items-center gap-1">
            <Map className="w-3.5 h-3.5" /> Open Learning Roadmap
          </Link>
        </div>

        <div className="divide-y divide-slate-100 dark:divide-slate-800">
          {gaps.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500">
              No critical skill gaps found! Take more assessments to stress-test your profile against advanced roles.
            </div>
          ) : (
            gaps.map((gap) => {
              const diff = Math.round(gap.gap_difference);
              const isHigh = gap.gap_severity === 'Critical' || gap.gap_severity === 'High';
              return (
                <div key={gap.id} className="p-4 sm:p-6 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-sm text-slate-900 dark:text-white">{gap.skill_name}</span>
                        <Badge variant={isHigh ? 'danger' : 'warning'} className="text-[10px]">
                          {gap.gap_severity} Gap
                        </Badge>
                      </div>
                      <p className="text-xs text-slate-500">
                        Deficit of <strong>{diff}%</strong> from market baseline. Immediate study recommended.
                      </p>
                    </div>

                    <div className="flex items-center gap-6">
                      <div className="w-40 sm:w-52">
                        <div className="flex justify-between text-xs font-bold mb-1">
                          <span className="text-slate-400">Current: {Math.round(gap.current_score)}%</span>
                          <span className="text-primary-600">Target: {Math.round(gap.required_score)}%</span>
                        </div>
                        <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${isHigh ? 'bg-rose-500' : 'bg-amber-500'}`}
                            style={{ width: `${Math.min(100, (gap.current_score / gap.required_score) * 100)}%` }}
                          ></div>
                        </div>
                      </div>

                      <Link
                        to="/roadmap"
                        className="px-3.5 py-1.5 rounded-lg bg-primary-50 dark:bg-primary-950/60 hover:bg-primary-100 text-primary-600 dark:text-primary-400 text-xs font-bold transition-colors flex items-center gap-1 shrink-0"
                      >
                        Bridge Gap <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

    </div>
  );
};

export default SkillGapsPage;
