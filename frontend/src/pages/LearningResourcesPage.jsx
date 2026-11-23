import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { BookOpen, Search, ExternalLink, Star, Clock, Filter } from 'lucide-react';
import Badge from '../components/Badge';

const LearningResourcesPage = () => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState('All');

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const res = await api.get('/roadmap/resources');
      setResources(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const types = ['All', 'Course', 'Documentation', 'Tutorial', 'Certification'];

  const filtered = resources.filter(r => {
    const matchType = selectedType === 'All' || r.resource_type === selectedType;
    const matchSearch = r.title.toLowerCase().includes(searchTerm.toLowerCase()) || r.skill_name.toLowerCase().includes(searchTerm.toLowerCase());
    return matchType && matchSearch;
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
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-indigo-900/10 to-transparent border-indigo-200/40">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Curated Educational Resources
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
          High-quality educational links verified from institutions like Harvard CS50, MIT OpenCourseWare, Python Foundation, and DeepLearning.AI.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by skill or provider..."
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1">
          {types.map(t => (
            <button
              key={t}
              onClick={() => setSelectedType(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                selectedType === t
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-800 hover:bg-slate-50'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(res => (
          <div key={res.id} className="glass-card p-6 flex flex-col justify-between hover:border-primary-500/40 transition-all">
            <div>
              <div className="flex items-center justify-between gap-2 mb-3">
                <Badge variant="primary">{res.resource_type}</Badge>
                <div className="flex items-center gap-1 text-amber-500 text-xs font-bold">
                  <Star className="w-3.5 h-3.5 fill-amber-500" /> {res.rating}
                </div>
              </div>

              <h3 className="font-bold text-sm text-slate-900 dark:text-white leading-snug">
                {res.title}
              </h3>

              <div className="text-[11px] font-semibold text-primary-600 dark:text-primary-400 mt-1">
                {res.provider}
              </div>

              <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed">
                {res.description}
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
              <span className="text-xs text-slate-400 flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" /> ~{res.estimated_hours} Hours
              </span>

              <a
                href={res.url}
                target="_blank"
                rel="noreferrer"
                className="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-primary-600 hover:text-white text-slate-700 dark:text-slate-300 text-xs font-bold transition-all flex items-center gap-1.5"
              >
                Access <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
};

export default LearningResourcesPage;
