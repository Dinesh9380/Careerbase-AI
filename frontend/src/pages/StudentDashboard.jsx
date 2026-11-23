import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import {
  Sparkles, Award, ArrowRight, CheckCircle2, ChevronRight, FileDown,
  Layers, Compass, Activity, Flame, ShieldCheck, Zap
} from 'lucide-react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip
} from 'recharts';
import Badge from '../components/Badge';

const StudentDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const res = await api.get('/students/me/dashboard');
      setData(res.data);
    } catch (e) {
      console.error("Dashboard error:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    setDownloading(true);
    try {
      const res = await api.get('/reports/download-pdf', { responseType: 'blob' });
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Career_Intelligence_Report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (e) {
      alert("Failed to download PDF report. Ensure assessment results exist.");
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const { metrics, radar_skills, top_recommendations, critical_gaps, recent_assessments, achievements } = data || {};

  return (
    <div className="space-y-6 pb-12">
      
      {/* Welcome & Quick Action Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-primary-900/10 via-indigo-900/5 to-transparent border border-primary-200/40 dark:border-primary-900/40 relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-primary-600 dark:text-primary-400 mb-1">
              <Sparkles className="w-4 h-4" /> AI-Driven Student Career Intelligence
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              Welcome back, {data?.student_name || 'Scholar'}!
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
              Your target career path is <strong className="text-primary-600 dark:text-primary-400">{data?.desired_career}</strong>.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={handleDownloadReport}
              disabled={downloading}
              className="px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 font-bold text-xs hover:bg-slate-50 dark:hover:bg-slate-800 transition-all shadow-sm flex items-center gap-2"
            >
              <FileDown className="w-4 h-4 text-primary-600" />
              {downloading ? 'Exporting PDF...' : 'Download PDF Dossier'}
            </button>
            <Link
              to="/assessments"
              className="px-4 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 transition-all flex items-center gap-2"
            >
              Take Assessment <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        
        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">Overall Skill Score</span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/60 text-blue-600 flex items-center justify-center">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
            {metrics?.overall_skill_score || 72}%
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">
            Verified across multi-skills
          </span>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">Assessment Average</span>
            <div className="w-8 h-8 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 flex items-center justify-center">
              <Award className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
            {metrics?.assessment_score || 78}%
          </div>
          <span className="text-[11px] text-indigo-600 font-semibold mt-1 block">
            Adaptive testing accuracy
          </span>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">Career Readiness</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 flex items-center justify-center">
              <Compass className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
            {metrics?.career_readiness || 84}%
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">
            ML profile match
          </span>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">XP Points & Streak</span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-950/60 text-amber-600 flex items-center justify-center">
              <Flame className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
            {metrics?.points || 120} XP
          </div>
          <span className="text-[11px] text-amber-600 font-semibold mt-1 block flex items-center gap-1">
            <Flame className="w-3 h-3" /> {metrics?.streak_days || 1}-day active streak
          </span>
        </div>

      </div>

      {/* Main Row: Skill Radar & Top Career Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Radar Chart (5 cols) */}
        <div className="lg:col-span-5 glass-card p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h2 className="font-bold text-base text-slate-900 dark:text-white">Skill Competency Radar</h2>
              <p className="text-xs text-slate-400">Holistic proficiency across core engineering disciplines</p>
            </div>
            <Link to="/skills" className="text-xs text-primary-600 font-bold hover:underline">
              Details
            </Link>
          </div>

          <div className="w-full h-64 sm:h-72">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radar_skills || []}>
                <PolarGrid stroke="#94a3b8" strokeDasharray="3 3" opacity={0.3} />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 11, fontWeight: 600 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#94a3b8" opacity={0.2} />
                <Radar name="Proficiency" dataKey="A" stroke="#4f46e5" fill="#6366f1" fillOpacity={0.45} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-center pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-500">
            Assessed through adaptive benchmarks and project evidence.
          </div>
        </div>

        {/* Top Career Recommendations (7 cols) */}
        <div className="lg:col-span-7 glass-card p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-bold text-base text-slate-900 dark:text-white">AI Career Matches & Explainability</h2>
              <p className="text-xs text-slate-400">Transparent AI match scores with verifiable evidence</p>
            </div>
            <Link to="/careers" className="text-xs text-primary-600 font-bold hover:underline">
              View All 20 Roles
            </Link>
          </div>

          <div className="space-y-3">
            {top_recommendations?.map((rec) => (
              <div
                key={rec.career_id}
                className="p-4 rounded-xl bg-slate-50/70 dark:bg-slate-950/50 border border-slate-200/60 dark:border-slate-800/60 hover:border-primary-500/40 transition-all"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-extrabold text-primary-600">#{rec.rank}</span>
                      <h3 className="font-bold text-sm text-slate-900 dark:text-white">{rec.title}</h3>
                      <Badge variant="primary" className="text-[10px]">{rec.industry}</Badge>
                    </div>

                    <div className="mt-2 space-y-1">
                      {rec.reasons?.map((reason, idx) => (
                        <div key={idx} className="flex items-start gap-1.5 text-[11px] text-slate-600 dark:text-slate-300">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                          <span>{reason}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="text-xl font-extrabold text-emerald-600 dark:text-emerald-400">
                      {Math.round(rec.match_score)}%
                    </div>
                    <span className="text-[10px] text-slate-400 font-medium">Match</span>
                  </div>
                </div>

                <div className="mt-3 pt-2.5 border-t border-slate-200/50 dark:border-slate-800/50 flex items-center justify-between">
                  <Link
                    to={`/careers/${rec.career_id}`}
                    className="text-[11px] font-bold text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1"
                  >
                    View Career Blueprint & Required Skills <ChevronRight className="w-3 h-3" />
                  </Link>
                  <Link
                    to="/career-comparison"
                    className="text-[11px] text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
                  >
                    Compare Role
                  </Link>
                </div>
              </div>
            ))}
          </div>

        </div>

      </div>

      {/* Second Row: Critical Skill Gaps & Gamification Achievements */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Critical Gaps (7 cols) */}
        <div className="lg:col-span-7 glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-bold text-base text-slate-900 dark:text-white">Identified Skill Gaps</h2>
              <p className="text-xs text-slate-400">Bridge these gaps to maximize placement readiness</p>
            </div>
            <Link to="/roadmap" className="text-xs text-primary-600 font-bold hover:underline">
              Open Roadmap
            </Link>
          </div>

          <div className="space-y-3">
            {critical_gaps?.map((gap, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/60">
                <div className="flex items-center justify-between text-xs font-bold mb-1.5">
                  <span className="text-slate-800 dark:text-slate-200">{gap.skill_name}</span>
                  <Badge variant={gap.severity === 'Critical' ? 'danger' : (gap.severity === 'High' ? 'warning' : 'default')}>
                    {gap.severity} Gap
                  </Badge>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500 mb-1">
                  <span>Current: {Math.round(gap.current_score)}%</span>
                  <span>Required: {Math.round(gap.required_score)}%</span>
                </div>

                <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${gap.severity === 'Critical' ? 'bg-rose-500' : (gap.severity === 'High' ? 'bg-amber-500' : 'bg-primary-500')}`}
                    style={{ width: `${Math.min(100, (gap.current_score / gap.required_score) * 100)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Gamification Badges (5 cols) */}
        <div className="lg:col-span-5 glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-bold text-base text-slate-900 dark:text-white">Achievements & Badges</h2>
              <p className="text-xs text-slate-400">Milestones earned on your learning journey</p>
            </div>
            <span className="text-xs font-extrabold text-amber-500">{achievements?.length || 1} Unlocked</span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {achievements?.map((ach) => (
              <div key={ach.id} className="p-3 rounded-xl bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200/40 dark:border-amber-900/40 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold shadow-md shadow-amber-500/20 shrink-0">
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-900 dark:text-white leading-snug">{ach.title}</h4>
                  <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-tight mt-0.5">{ach.description}</p>
                </div>
              </div>
            ))}

            <div className="p-3 rounded-xl border border-dashed border-slate-300 dark:border-slate-800 flex items-center gap-3 opacity-60">
              <div className="w-10 h-10 rounded-xl bg-slate-200 dark:bg-slate-800 text-slate-400 flex items-center justify-center font-bold shrink-0">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300">Roadmap Finisher</h4>
                <p className="text-[10px] text-slate-400">Complete all stage modules</p>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};

export default StudentDashboard;
