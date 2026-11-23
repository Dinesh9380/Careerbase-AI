import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Compass, Search, ArrowRight, DollarSign, TrendingUp, GitCompare, Layers } from 'lucide-react';
import Badge from '../components/Badge';

const CareersListPage = () => {
  const [careers, setCareers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedIndustry, setSelectedIndustry] = useState('All');

  useEffect(() => {
    fetchCareers();
  }, []);

  const fetchCareers = async () => {
    try {
      const res = await api.get('/careers');
      setCareers(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const industries = ['All', ...new Set(careers.map(c => c.industry))];

  const filtered = careers.filter(c => {
    const matchInd = selectedIndustry === 'All' || c.industry === selectedIndustry;
    const matchSearch = c.title.toLowerCase().includes(searchTerm.toLowerCase()) || c.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchInd && matchSearch;
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
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-primary-900/10 to-transparent border-primary-200/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              Career Roles & Industry Blueprints
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
              Explore 20 premier technology roles mapped to actual industry competency frameworks, salary benchmarks, and prerequisite skills.
            </p>
          </div>

          <Link
            to="/career-comparison"
            className="px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 font-bold text-xs hover:bg-slate-50 dark:hover:bg-slate-800 transition-all shadow-sm flex items-center gap-2 self-start sm:self-auto shrink-0"
          >
            <GitCompare className="w-4 h-4 text-primary-600" /> Compare 2-3 Careers
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search roles, frameworks, or skills..."
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1">
          {industries.map(ind => (
            <button
              key={ind}
              onClick={() => setSelectedIndustry(ind)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                selectedIndustry === ind
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-800 hover:bg-slate-50'
              }`}
            >
              {ind}
            </button>
          ))}
        </div>
      </div>

      {/* Career Roles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(c => (
          <div key={c.id} className="glass-card p-6 flex flex-col justify-between hover:border-primary-500/40 transition-all group">
            <div>
              <div className="flex items-center justify-between gap-2 mb-3">
                <Badge variant="primary">{c.industry}</Badge>
                <span className="text-[11px] font-semibold text-emerald-600 flex items-center gap-1">
                  <TrendingUp className="w-3.5 h-3.5" /> {c.market_demand}
                </span>
              </div>

              <h3 className="font-bold text-base text-slate-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                {c.title}
              </h3>

              <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed line-clamp-3">
                {c.description}
              </p>

              {/* Skills badges preview */}
              <div className="flex flex-wrap gap-1.5 mt-4">
                {c.skills?.slice(0, 4).map((s, idx) => (
                  <span key={idx} className="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-[10px] font-medium text-slate-700 dark:text-slate-300">
                    {s.skill_name}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800">
              <div className="flex items-center justify-between text-xs text-slate-500 mb-3">
                <span className="flex items-center gap-1 font-semibold text-slate-700 dark:text-slate-300">
                  <DollarSign className="w-3.5 h-3.5 text-emerald-600" /> {c.average_salary.split('/')[0]}
                </span>
                <span>{c.difficulty} Level</span>
              </div>

              <Link
                to={`/careers/${c.id}`}
                className="w-full py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-primary-600 hover:text-white text-slate-700 dark:text-slate-300 text-xs font-bold transition-all flex items-center justify-center gap-1.5"
              >
                Inspect Blueprint <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
};

export default CareersListPage;
