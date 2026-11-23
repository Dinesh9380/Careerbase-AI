import React, { useState } from 'react';
import api from '../services/api';
import { Database, Play, Clock, Zap, BarChart3, TrendingUp, Layers, CheckCircle2 } from 'lucide-react';
import Badge from '../components/Badge';

const AdminBigDataPage = () => {
  const [recordCount, setRecordCount] = useState(10000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunPipeline = async () => {
    setLoading(true);
    try {
      const res = await api.post('/admin/bigdata/generate', { record_count: recordCount });
      setResult(res.data);
    } catch (e) {
      alert("Failed to run Big Data batch pipeline.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-rose-900/10 via-primary-900/5 to-transparent border-rose-200/40">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Big Data Analytics Pipeline
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
          Simulate enterprise-scale institutional telemetry. Process 1,000 to 100,000 student assessment logs on-demand using PySpark and high-speed vectorized analytical computation.
        </p>
      </div>

      {/* Runner Controls */}
      <div className="glass-card p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
            Telemetry Dataset Size
          </span>
          <div className="flex flex-wrap gap-2">
            {[1000, 10000, 50000, 100000].map(count => (
              <button
                key={count}
                onClick={() => setRecordCount(count)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  recordCount === count
                    ? 'bg-rose-600 text-white shadow-md shadow-rose-500/20'
                    : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50'
                }`}
              >
                {count.toLocaleString()} Records
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleRunPipeline}
          disabled={loading}
          className="px-6 py-3 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow-lg shadow-rose-500/25 transition-all flex items-center justify-center gap-2 self-start sm:self-auto disabled:opacity-50"
        >
          <Play className="w-4 h-4 fill-white" />
          {loading ? 'Executing Distributed Aggregation...' : `Process ${recordCount.toLocaleString()} Records`}
        </button>
      </div>

      {/* Execution Results */}
      {result && (
        <div className="space-y-6">
          
          {/* Execution Benchmark Telemetry */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <div className="glass-card p-5">
              <span className="text-xs font-semibold text-slate-500">Records Processed</span>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
                {result.records_processed.toLocaleString()}
              </div>
              <span className="text-[11px] text-emerald-600 font-semibold mt-0.5 block">
                100% Ingestion Complete
              </span>
            </div>

            <div className="glass-card p-5">
              <span className="text-xs font-semibold text-slate-500">Execution Time</span>
              <div className="text-2xl font-extrabold text-rose-600 mt-1">
                {result.execution_time_seconds}s
              </div>
              <span className="text-[11px] text-slate-400 mt-0.5 block">
                Vectorized In-Memory Engine
              </span>
            </div>

            <div className="glass-card p-5">
              <span className="text-xs font-semibold text-slate-500">Processing Throughput</span>
              <div className="text-2xl font-extrabold text-primary-600 mt-1">
                {result.records_per_second.toLocaleString()}
              </div>
              <span className="text-[11px] text-slate-400 mt-0.5 block">Records per second</span>
            </div>

            <div className="glass-card p-5">
              <span className="text-xs font-semibold text-slate-500">Pipeline Engine</span>
              <div className="text-sm font-extrabold text-slate-800 dark:text-slate-100 mt-2">
                PySpark / Vectorized
              </div>
              <span className="text-[11px] text-emerald-600 font-semibold mt-0.5 block">
                Zero Memory Leak
              </span>
            </div>
          </div>

          {/* Aggregations Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Skill Popularity Table */}
            <div className="glass-card p-6">
              <h3 className="font-bold text-base text-slate-900 dark:text-white mb-3 flex items-center justify-between">
                <span>Skill Assessment Volume & Mean Proficiency</span>
                <Badge variant="primary">Top 10</Badge>
              </h3>

              <div className="space-y-2">
                {result.skill_popularity?.map((s, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50 text-xs">
                    <span className="font-bold text-slate-800 dark:text-slate-200">{s.skill}</span>
                    <div className="flex items-center gap-4">
                      <span className="text-slate-400">{s.assessments_count} logs</span>
                      <span className="font-extrabold text-emerald-600">{s.average_score}% Avg</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Common Skill Gaps */}
            <div className="glass-card p-6">
              <h3 className="font-bold text-base text-slate-900 dark:text-white mb-3 flex items-center justify-between">
                <span>Identified Population Skill Gaps (&lt;60%)</span>
                <Badge variant="danger">Critical</Badge>
              </h3>

              <div className="space-y-2">
                {result.common_skill_gaps?.map((g, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2.5 rounded-xl bg-rose-50/40 dark:bg-rose-950/20 border border-rose-200/40 dark:border-rose-900/40 text-xs">
                    <span className="font-bold text-rose-700 dark:text-rose-300">{g.skill}</span>
                    <span className="font-extrabold text-rose-600">{g.gap_count} students affected</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Career Trends */}
            <div className="glass-card p-6">
              <h3 className="font-bold text-base text-slate-900 dark:text-white mb-3 flex items-center justify-between">
                <span>Desired Career Role Distribution</span>
                <Badge variant="primary">Trends</Badge>
              </h3>

              <div className="space-y-2">
                {result.career_interest_trends?.map((c, idx) => (
                  <div key={idx} className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50 text-xs">
                    <div className="flex justify-between font-bold mb-1">
                      <span>{c.desired_career}</span>
                      <span className="text-primary-600">{c.percentage}% ({c.student_count})</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-primary-600 rounded-full" style={{ width: `${c.percentage * 3}%` }}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Department Performance */}
            <div className="glass-card p-6">
              <h3 className="font-bold text-base text-slate-900 dark:text-white mb-3 flex items-center justify-between">
                <span>Academic Department Aggregations</span>
                <Badge variant="success">Institutional</Badge>
              </h3>

              <div className="space-y-2">
                {result.department_performance?.map((d, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50 text-xs">
                    <span className="font-bold text-slate-800 dark:text-slate-200">{d.department}</span>
                    <div className="flex items-center gap-4">
                      <span className="text-slate-400">{d.total_records} records</span>
                      <span className="font-extrabold text-indigo-600">{d.mean_score}% Score</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  );
};

export default AdminBigDataPage;
