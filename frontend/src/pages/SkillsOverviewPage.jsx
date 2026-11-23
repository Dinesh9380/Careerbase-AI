import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Activity, Plus, CheckCircle2, ArrowRight, ShieldCheck, Award } from 'lucide-react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip
} from 'recharts';
import Badge from '../components/Badge';

const SkillsOverviewPage = () => {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSkills();
  }, []);

  const fetchSkills = async () => {
    try {
      const res = await api.get('/students/me/skills');
      setSkills(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const radarData = skills.slice(0, 8).map(s => ({
    subject: s.skill_name,
    A: s.proficiency_score,
    fullMark: 100
  }));

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
            Skill Competency Matrix
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
            Verified proficiencies synthesized from adaptive testing, technical projects, and certifications.
          </p>
        </div>

        <Link
          to="/assessments"
          className="px-4 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 transition-all flex items-center gap-1.5 self-start sm:self-auto"
        >
          <Award className="w-4 h-4" /> Benchmark a Skill
        </Link>
      </div>

      {/* Radar Section */}
      <div className="glass-card p-6">
        <h3 className="font-bold text-base text-slate-900 dark:text-white mb-2">Multidisciplinary Profile Radar</h3>
        <p className="text-xs text-slate-400 mb-4">Cross-disciplinary view of your verified competencies</p>
        
        <div className="w-full h-72">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
              <PolarGrid stroke="#94a3b8" strokeDasharray="3 3" opacity={0.3} />
              <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 11, fontWeight: 600 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#94a3b8" opacity={0.2} />
              <Radar name="Proficiency" dataKey="A" stroke="#4f46e5" fill="#6366f1" fillOpacity={0.4} />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Skills Table */}
      <div className="glass-card overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <h3 className="font-bold text-sm text-slate-900 dark:text-white">Verified Skills Inventory</h3>
          <span className="text-xs text-slate-400">{skills.length} skills recorded</span>
        </div>

        <div className="divide-y divide-slate-100 dark:divide-slate-800">
          {skills.map((s) => (
            <div key={s.id} className="p-4 sm:px-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-sm text-slate-900 dark:text-white">{s.skill_name}</span>
                  <Badge variant="default" className="text-[10px]">{s.category}</Badge>
                </div>
                <div className="text-[11px] text-slate-500 flex items-center gap-2">
                  <span>Level: <strong>{s.proficiency_level}</strong></span>
                  <span>•</span>
                  <span>Source: {s.evidence_source?.last_assessment_id ? 'Adaptive Assessment' : 'Verified Profile'}</span>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-32 sm:w-40">
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span className="text-slate-500">Proficiency</span>
                    <span className="text-primary-600">{Math.round(s.proficiency_score)}%</span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary-600 rounded-full"
                      style={{ width: `${s.proficiency_score}%` }}
                    ></div>
                  </div>
                </div>

                <Badge variant={s.proficiency_score >= 80 ? 'success' : (s.proficiency_score >= 60 ? 'primary' : 'warning')}>
                  {s.proficiency_level}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default SkillsOverviewPage;
