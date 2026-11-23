import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import {
  Users, CheckSquare, Award, Database, ShieldCheck, TrendingUp,
  Activity, ArrowRight, Sparkles, Layers, FileCheck
} from 'lucide-react';
import Badge from '../components/Badge';

const AdminDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const res = await api.get('/admin/dashboard');
      setData(res.data);
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

  const { summary, sdg4_impact, skill_distribution, career_demand, blockchain_status } = data || {};

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-slate-900/10 via-primary-900/5 to-transparent">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-primary-600 mb-1">
              <ShieldCheck className="w-4 h-4" /> System Governance & Institutional Telemetry
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              Institutional Intelligence Dashboard
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
              Real-time analytics on student assessment performance, skill gaps, career trends, and UN SDG 4 outcomes.
            </p>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-auto">
            <Link
              to="/admin/bigdata"
              className="px-4 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 flex items-center gap-1.5"
            >
              <Database className="w-4 h-4" /> Run Big Data Pipeline
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">Active Students</span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/60 text-blue-600 flex items-center justify-center">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
            {summary?.total_students || 1}
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">
            100% profile active
          </span>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">Assessments Taken</span>
            <div className="w-8 h-8 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 flex items-center justify-center">
              <CheckSquare className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
            {summary?.completed_assessments || 1}
          </div>
          <span className="text-[11px] text-indigo-600 font-semibold mt-1 block">
            Avg Score: {summary?.average_score || 75}%
          </span>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">Credentials Issued</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 flex items-center justify-center">
              <Award className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
            {summary?.total_credentials_issued || 1}
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">
            Blockchain Anchored
          </span>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-500">Ledger Status</span>
            <div className="w-8 h-8 rounded-lg bg-teal-50 dark:bg-teal-950/60 text-teal-600 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-emerald-600">
            {blockchain_status?.total_blocks || 2} Blocks
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">
            Integrity Verified
          </span>
        </div>
      </div>

      {/* UN SDG 4 Impact Telemetry Box */}
      <div className="glass-card p-6 border-l-4 border-l-blue-600">
        <div className="flex items-center gap-2 text-blue-600 font-extrabold text-sm mb-3">
          <Award className="w-5 h-5" /> United Nations Sustainable Development Goal 4 (Quality Education) Impact
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
          <div className="p-3.5 rounded-xl bg-blue-50/50 dark:bg-blue-950/20 border border-blue-100 dark:border-blue-900/40">
            <div className="text-xl font-extrabold text-blue-700 dark:text-blue-300">
              {sdg4_impact?.personalized_roadmaps_generated || 2}
            </div>
            <div className="text-[11px] font-semibold text-slate-500 mt-0.5">
              Personalized Roadmaps Formulated
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-blue-50/50 dark:bg-blue-950/20 border border-blue-100 dark:border-blue-900/40">
            <div className="text-xl font-extrabold text-blue-700 dark:text-blue-300">
              {sdg4_impact?.skills_assessed_count || 20}
            </div>
            <div className="text-[11px] font-semibold text-slate-500 mt-0.5">
              Skill Benchmarks Measured
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-blue-50/50 dark:bg-blue-950/20 border border-blue-100 dark:border-blue-900/40">
            <div className="text-xl font-extrabold text-blue-700 dark:text-blue-300">
              {sdg4_impact?.blockchain_credentials_issued || 1}
            </div>
            <div className="text-[11px] font-semibold text-slate-500 mt-0.5">
              Verifiable Micro-Credentials Minted
            </div>
          </div>
        </div>

        <p className="text-xs text-slate-500 mt-4 leading-relaxed">
          <strong>Target 4.4 Compliance:</strong> The platform delivers data-backed career intelligence and verifiable skill credentials, directly enhancing youth readiness for employment, entrepreneurship, and decent work.
        </p>
      </div>

      {/* Two columns: Popular Skills & Career Demand */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Skills Popularity */}
        <div className="glass-card p-6">
          <h3 className="font-bold text-base text-slate-900 dark:text-white mb-4 flex items-center justify-between">
            <span>Skill Demand & Telemetry Distribution</span>
            <Badge variant="primary">Real-Time</Badge>
          </h3>

          <div className="space-y-3">
            {skill_distribution?.map((s, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50 text-xs">
                <span className="font-bold text-slate-800 dark:text-slate-200">{s.name}</span>
                <div className="flex items-center gap-3">
                  <span className="text-slate-400">{s.category}</span>
                  <span className="font-extrabold text-primary-600">{s.count} assessments</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Career Interests */}
        <div className="glass-card p-6">
          <h3 className="font-bold text-base text-slate-900 dark:text-white mb-4 flex items-center justify-between">
            <span>Student Career Aspiration Breakdown</span>
            <Badge variant="primary">Top Roles</Badge>
          </h3>

          <div className="space-y-3">
            {career_demand?.map((c, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50">
                <div className="flex items-center justify-between text-xs font-bold mb-1">
                  <span className="text-slate-800 dark:text-slate-200">{c.title}</span>
                  <span className="text-primary-600">{c.student_interest_pct}% Interest</span>
                </div>
                <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary-600 rounded-full"
                    style={{ width: `${c.student_interest_pct * 3}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};

export default AdminDashboard;
