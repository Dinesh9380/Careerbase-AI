import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { CheckSquare, Clock, HelpCircle, ArrowRight, Award, Search, Filter, Briefcase } from 'lucide-react';
import Badge from '../components/Badge';

const AssessmentsListPage = () => {
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRole, setSelectedRole] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    fetchAssessments();
  }, []);

  const fetchAssessments = async () => {
    try {
      const res = await api.get('/assessments');
      setAssessments(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const ROLE_OPTIONS = [
    { label: 'All Roles', slug: 'All' },
    { label: 'Full Stack Developer', slug: 'full-stack-developer' },
    { label: 'AI Engineer', slug: 'ai-engineer' },
    { label: 'Data Scientist', slug: 'data-scientist' },
    { label: 'Machine Learning Engineer', slug: 'machine-learning-engineer' },
    { label: 'Data Analyst', slug: 'data-analyst' },
    { label: 'Data Engineer', slug: 'data-engineer' },
    { label: 'Cloud Engineer', slug: 'cloud-engineer' },
    { label: 'DevOps Engineer', slug: 'devops-engineer' },
    { label: 'Cybersecurity Analyst', slug: 'cybersecurity-analyst' },
    { label: 'Blockchain Developer', slug: 'blockchain-developer' },
    { label: 'Computer Vision Engineer', slug: 'computer-vision-engineer' },
    { label: 'NLP Engineer', slug: 'nlp-engineer' },
    { label: 'QA Automation Engineer', slug: 'qa-automation-engineer' },
    { label: 'Systems Architect', slug: 'systems-architect' },
    { label: 'CS Fundamentals', slug: 'cs-fundamentals' },
    { label: 'Python Programming', slug: 'python-programming' },
    { label: 'Problem Solving', slug: 'problem-solving' },
  ];

  const categories = ['All', ...new Set(assessments.map(a => a.category).filter(Boolean))];

  const formatRoleLabel = (slug) => {
    if (!slug) return null;
    const found = ROLE_OPTIONS.find(r => r.slug === slug);
    if (found) return found.label;
    return slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  };

  const filtered = assessments.filter(a => {
    const matchRole = selectedRole === 'All' || a.role_slug === selectedRole;
    const matchCat = selectedCategory === 'All' || a.category === selectedCategory;
    const matchSearch =
      a.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (a.category && a.category.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (a.role_slug && a.role_slug.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchRole && matchCat && matchSearch;
  });

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
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-indigo-900/10 via-primary-900/5 to-transparent border-indigo-200/40">
        <div className="flex items-center gap-2 text-primary-600 dark:text-primary-400 text-xs font-bold uppercase tracking-wider mb-2">
          <CheckSquare className="w-4 h-4" /> Role-Aligned Assessment Engine
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Adaptive Skill Assessments
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
          Select your target career role or technical domain to test your competency. Every assessment contains calibrated questions with real-time scoring, live timers, and instant skill profile updating.
        </p>
      </div>

      {/* Role Filter Bar */}
      <div className="glass-card p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-700 dark:text-slate-300">
            <Briefcase className="w-4 h-4 text-primary-600" />
            <span>Filter by Target Career Role:</span>
          </div>
          <span className="text-[11px] text-slate-400 font-medium">
            Showing {filtered.length} assessment{filtered.length === 1 ? '' : 's'}
          </span>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1.5 scrollbar-thin">
          {ROLE_OPTIONS.map(role => (
            <button
              key={role.slug}
              onClick={() => {
                setSelectedRole(role.slug);
                setSelectedCategory('All');
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                selectedRole === role.slug
                  ? 'bg-primary-600 text-white shadow-sm shadow-primary-500/20'
                  : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              {role.label}
            </button>
          ))}
        </div>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by assessment title, skill, or role..."
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Category pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                selectedCategory === cat
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-800 hover:bg-slate-50'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Assessment Grid */}
      {filtered.length === 0 ? (
        <div className="glass-card p-12 text-center max-w-md mx-auto space-y-3">
          <HelpCircle className="w-10 h-10 text-slate-400 mx-auto" />
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">No assessments found</h3>
          <p className="text-xs text-slate-500">
            No assessments match your active filter. Try resetting your search or selecting "All Roles".
          </p>
          <button
            onClick={() => { setSelectedRole('All'); setSelectedCategory('All'); setSearchTerm(''); }}
            className="px-4 py-2 rounded-xl bg-primary-600 text-white text-xs font-bold"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map(ass => (
            <div key={ass.id} className="glass-card p-6 flex flex-col justify-between hover:border-primary-500/40 transition-all group">
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <Badge variant="primary">{ass.category}</Badge>
                  <div className="flex items-center gap-1 text-slate-400 text-xs">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{ass.time_limit_minutes} mins</span>
                  </div>
                </div>

                <h3 className="font-bold text-base text-slate-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                  {ass.title}
                </h3>

                {ass.role_slug && (
                  <div className="mt-2">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 text-[11px] font-semibold border border-indigo-200/50 dark:border-indigo-900/50">
                      <Briefcase className="w-3 h-3" /> Target Role: {formatRoleLabel(ass.role_slug)}
                    </span>
                  </div>
                )}

                <p className="text-xs text-slate-600 dark:text-slate-400 mt-2.5 leading-relaxed">
                  {ass.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-3 text-xs text-slate-500">
                  <span className="flex items-center gap-1 font-semibold text-emerald-600 dark:text-emerald-400">
                    <HelpCircle className="w-3.5 h-3.5" /> {ass.total_questions} Questions
                  </span>
                  <span>Pass: {ass.passing_percentage}%</span>
                </div>

                <Link
                  to={`/assessment/${ass.id}`}
                  className="px-3.5 py-1.5 rounded-lg bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-sm shadow-primary-500/20 transition-all flex items-center gap-1.5"
                >
                  Start Test <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
};

export default AssessmentsListPage;
