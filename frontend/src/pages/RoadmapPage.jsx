import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../services/api';
import { Map, CheckCircle2, Circle, Clock, ExternalLink, Sparkles, FolderGit2, ArrowRight } from 'lucide-react';
import Badge from '../components/Badge';

const STAGE_COLORS = {
  Foundation: 'border-blue-500 bg-blue-50/20 dark:bg-blue-950/20 text-blue-600',
  Beginner: 'border-indigo-500 bg-indigo-50/20 dark:bg-indigo-950/20 text-indigo-600',
  Intermediate: 'border-purple-500 bg-purple-50/20 dark:bg-purple-950/20 text-purple-600',
  Advanced: 'border-amber-500 bg-amber-50/20 dark:bg-amber-950/20 text-amber-600',
  Professional: 'border-emerald-500 bg-emerald-50/20 dark:bg-emerald-950/20 text-emerald-600'
};

const RoadmapPage = () => {
  const [searchParams] = useSearchParams();
  const careerId = searchParams.get('career_id');

  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRoadmap();
  }, [careerId]);

  const fetchRoadmap = async () => {
    try {
      const url = careerId ? `/roadmap?career_id=${careerId}` : '/roadmap';
      const res = await api.get(url);
      setRoadmap(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const toggleItem = async (itemId) => {
    try {
      const res = await api.post(`/roadmap/items/${itemId}/complete`);
      setRoadmap(prev => ({
        ...prev,
        completed_items: res.data.completed_items,
        progress_percentage: res.data.progress_percentage,
        items: prev.items.map(it => it.id === itemId ? { ...it, is_completed: res.data.is_completed } : it)
      }));
    } catch (e) {
      alert("Failed to toggle roadmap milestone.");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const stages = ['Foundation', 'Beginner', 'Intermediate', 'Advanced', 'Professional'];

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-16">
      
      {/* Roadmap Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-primary-900/10 via-purple-900/5 to-transparent border-primary-200/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-[11px] font-bold text-primary-600 uppercase tracking-wider block">
              Personalized Learning Pathway
            </span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white mt-0.5">
              {roadmap?.career_title} Mastery Roadmap
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
              Engineered across five evolutionary tiers to systematically bridge your verified skill gaps.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-center shrink-0 w-36">
            <div className="text-2xl font-extrabold text-primary-600">
              {Math.round(roadmap?.progress_percentage || 0)}%
            </div>
            <div className="text-[11px] font-semibold text-slate-400">Roadmap Progress</div>
            <div className="text-[10px] text-slate-500 mt-0.5">
              {roadmap?.completed_items}/{roadmap?.total_items} Complete
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full h-2.5 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden mt-6">
          <div
            className="h-full bg-gradient-to-r from-primary-600 to-emerald-500 rounded-full transition-all duration-500"
            style={{ width: `${roadmap?.progress_percentage || 0}%` }}
          ></div>
        </div>
      </div>

      {/* Stages Iteration */}
      <div className="space-y-8">
        {stages.map((stageName, stageIdx) => {
          const stageItems = roadmap?.items?.filter(it => it.stage === stageName) || [];
          if (stageItems.length === 0) return null;

          return (
            <div key={stageName} className="space-y-4">
              
              {/* Stage Title */}
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center font-extrabold text-xs border ${STAGE_COLORS[stageName]}`}>
                  {stageIdx + 1}
                </div>
                <div>
                  <h3 className="font-extrabold text-base text-slate-900 dark:text-white">
                    STAGE {stageIdx + 1}: {stageName.toUpperCase()}
                  </h3>
                  <span className="text-[11px] text-slate-400">
                    {stageName === 'Foundation' ? 'Prerequisites, syntax & computational basics' : (
                      stageName === 'Beginner' ? 'Core tools, frameworks & schema architecture' : (
                        stageName === 'Intermediate' ? 'Distributed design, API mechanics & validation' : (
                          stageName === 'Advanced' ? 'System scalability & deep algorithmic optimization' : 'Production deployment & capstone delivery'
                        )
                      )
                    )}
                  </span>
                </div>
              </div>

              {/* Stage Items */}
              <div className="space-y-3 pl-4 border-l-2 border-slate-200 dark:border-slate-800 ml-4">
                {stageItems.map((item) => (
                  <div
                    key={item.id}
                    className={`glass-card p-5 transition-all ${
                      item.is_completed ? 'opacity-80 bg-slate-50/50 dark:bg-slate-900/30' : 'hover:border-primary-500/40'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      
                      <div className="flex items-start gap-3">
                        <button
                          onClick={() => toggleItem(item.id)}
                          className={`mt-0.5 text-slate-400 hover:text-emerald-500 transition-colors ${
                            item.is_completed ? 'text-emerald-600 dark:text-emerald-400' : ''
                          }`}
                        >
                          {item.is_completed ? (
                            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                          ) : (
                            <Circle className="w-5 h-5" />
                          )}
                        </button>

                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <h4 className={`font-bold text-sm ${item.is_completed ? 'line-through text-slate-400' : 'text-slate-900 dark:text-white'}`}>
                              {item.title}
                            </h4>
                            <Badge variant="default" className="text-[10px]">{item.skill_name}</Badge>
                          </div>

                          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                            {item.description}
                          </p>

                          {item.project_prompt && (
                            <div className="mt-2 p-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50 text-[11px] text-slate-600 dark:text-slate-300 flex items-start gap-2">
                              <FolderGit2 className="w-3.5 h-3.5 text-primary-600 shrink-0 mt-0.5" />
                              <span><strong>Capstone Task:</strong> {item.project_prompt}</span>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="text-right shrink-0 flex flex-col items-end gap-2">
                        <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5" /> {item.estimated_hours}h
                        </span>

                        {item.resource_link && (
                          <a
                            href={item.resource_link}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 text-xs font-bold text-primary-600 hover:underline"
                          >
                            Study <ExternalLink className="w-3 h-3" />
                          </a>
                        )}
                      </div>

                    </div>
                  </div>
                ))}
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};

export default RoadmapPage;
