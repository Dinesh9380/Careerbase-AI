import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Sparkles, ArrowRight, CheckCircle2, ShieldCheck, Database,
  Brain, FileText, Map, Award, Users, ChevronRight, Lock, Target, TrendingUp
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Badge from '../components/Badge';

const Landing = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleQuickDemo = async (email) => {
    try {
      await login(email, "Demo@123456");
      if (email === "admin@demo.com") navigate('/admin/dashboard');
      else if (email === "counselor@demo.com") navigate('/counselor/dashboard');
      else navigate('/dashboard');
    } catch (e) {
      navigate('/login');
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28">
        {/* Glow ambient background */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-primary-500/15 dark:bg-primary-500/10 blur-[100px] rounded-full pointer-events-none -z-10" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 dark:bg-blue-950/60 border border-blue-200/60 dark:border-blue-800/60 text-blue-700 dark:text-blue-300 text-xs font-semibold mb-6 shadow-sm">
            <Award className="w-4 h-4 text-blue-600" />
            <span>Advancing UN Sustainable Development Goal 4: Quality Education</span>
          </div>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-[1.1] max-w-4xl mx-auto">
            Discover Your Skills. <br />
            <span className="bg-gradient-to-r from-primary-600 via-indigo-600 to-blue-500 bg-clip-text text-transparent">
              Find Your Career.
            </span> <br />
            Build Your Future.
          </h1>

          <p className="mt-6 text-base sm:text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
            The next-generation student career intelligence platform combining adaptive skill assessments, 
            explainable AI recommendations, resume computer vision, personalized learning roadmaps, 
            and blockchain-verified credentials.
          </p>

          {/* Call to Actions */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              to="/register"
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-sm shadow-lg shadow-primary-500/25 transition-all flex items-center justify-center gap-2"
            >
              Start Free Assessment <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/verify"
              className="w-full sm:w-auto px-5 py-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 font-semibold text-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition-all flex items-center justify-center gap-2"
            >
              <ShieldCheck className="w-4 h-4 text-emerald-600" /> Verify Blockchain Credential
            </Link>
          </div>

          {/* Quick Demo Logins Bar */}
          <div className="mt-10 p-4 rounded-2xl bg-white/70 dark:bg-slate-900/70 border border-slate-200/80 dark:border-slate-800/80 max-w-2xl mx-auto backdrop-blur-md shadow-sm">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-2.5">
              1-Click Instant Evaluation Demo Logins
            </span>
            <div className="flex flex-wrap items-center justify-center gap-2">
              <button
                onClick={() => handleQuickDemo("student@demo.com")}
                className="px-3.5 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 hover:bg-indigo-100 text-indigo-700 dark:text-indigo-300 text-xs font-bold transition-colors flex items-center gap-1.5"
              >
                <Users className="w-3.5 h-3.5" /> Demo Student
              </button>
              <button
                onClick={() => handleQuickDemo("admin@demo.com")}
                className="px-3.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-950/60 hover:bg-amber-100 text-amber-700 dark:text-amber-300 text-xs font-bold transition-colors flex items-center gap-1.5"
              >
                <Database className="w-3.5 h-3.5" /> Demo Admin & Big Data
              </button>
              <button
                onClick={() => handleQuickDemo("counselor@demo.com")}
                className="px-3.5 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 hover:bg-emerald-100 text-emerald-700 dark:text-emerald-300 text-xs font-bold transition-colors flex items-center gap-1.5"
              >
                <Target className="w-3.5 h-3.5" /> Demo Counselor
              </button>
            </div>
            <p className="text-[11px] text-slate-400 mt-2">Password: <code className="text-primary-600 font-mono">Demo@123456</code> (Pre-seeded with assessments, roadmaps & verified credentials)</p>
          </div>

        </div>
      </section>

      {/* Metrics Banner */}
      <section className="border-y border-slate-200/80 dark:border-slate-800/80 bg-white/40 dark:bg-slate-900/40 backdrop-blur-sm py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl font-extrabold text-primary-600 dark:text-primary-400">20+</div>
              <div className="text-xs font-medium text-slate-500 mt-1">Target Career Roles</div>
            </div>
            <div>
              <div className="text-3xl font-extrabold text-indigo-600 dark:text-indigo-400">100+</div>
              <div className="text-xs font-medium text-slate-500 mt-1">Categorized Skills</div>
            </div>
            <div>
              <div className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400">96.4%</div>
              <div className="text-xs font-medium text-slate-500 mt-1">ML Model F1-Score</div>
            </div>
            <div>
              <div className="text-3xl font-extrabold text-blue-600 dark:text-blue-400">100%</div>
              <div className="text-xs font-medium text-slate-500 mt-1">On-Chain Verifiable</div>
            </div>
          </div>
        </div>
      </section>

      {/* 8 Core Innovations Grid */}
      <section id="features" className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs font-extrabold uppercase tracking-widest text-primary-600 dark:text-primary-400">
            Integrated Architecture
          </h2>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white mt-2">
            Eight Pillars of Student Career Intelligence
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-3">
            Every feature is production-ready, fully interactive, and designed to eliminate guesswork from career planning.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950 text-blue-600 flex items-center justify-center mb-4">
                <Brain className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">1. AI/ML Career Engine</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Trained scikit-learn classifier combined with transparent rule-matching explaining precisely WHY each role is recommended.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-blue-600 font-semibold">
              Explainable AI Decisions
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950 text-indigo-600 flex items-center justify-center mb-4">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">2. Adaptive Testing</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Dynamic skill evaluations across 16 domains. Questions adapt difficulty in real-time based on your consecutive responses.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-indigo-600 font-semibold">
              Real-Time Dynamic Scoring
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 flex items-center justify-center mb-4">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">3. Blockchain Registry</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Dual Solidity smart contract & cryptographic SHA-256 Merkle ledger providing tamper-evident certificate verification without exposing PII.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-emerald-600 font-semibold">
              Public Proof & Hash Check
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950 text-amber-600 flex items-center justify-center mb-4">
                <FileText className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">4. Resume Vision AI</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Upload PDF or scanned resumes. Optical character recognition extracts skills, computes ATS coverage, and syncs directly into your profile.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-amber-600 font-semibold">
              1-Click Profile Sync
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-purple-50 dark:bg-purple-950 text-purple-600 flex items-center justify-center mb-4">
                <Map className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">5. 5-Tier Roadmaps</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Progressive milestones from Foundation to Professional, linked to genuine learning resources, mini-projects, and progress tracking.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-purple-600 font-semibold">
              Actionable Gap Bridging
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-950 text-rose-600 flex items-center justify-center mb-4">
                <Database className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">6. Big Data Analytics</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                PySpark batch jobs and high-speed vectorized engines analyzing 1,000 to 100,000 student telemetry records in seconds.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-rose-600 font-semibold">
              Sub-Second Batch Profiling
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-cyan-50 dark:bg-cyan-950 text-cyan-600 flex items-center justify-center mb-4">
                <Lock className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">7. Enterprise Security</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Strict JWT auth, bcrypt password hashing, Role-Based Access Control (Student, Admin, Counselor), and immutable audit logs.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-cyan-600 font-semibold">
              Defense-In-Depth Protocol
            </div>
          </div>

          <div className="glass-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-xl bg-teal-50 dark:bg-teal-950 text-teal-600 flex items-center justify-center mb-4">
                <Sparkles className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-base text-slate-900 dark:text-white mb-2">8. CareerAI Chatbot</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Personalized RAG advisor with direct awareness of your actual test scores, gaps, target careers, and resume points.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-teal-600 font-semibold">
              Student-Context Aware
            </div>
          </div>

        </div>
      </section>

      {/* UN SDG 4 Impact Section */}
      <section id="sdg4" className="py-20 bg-gradient-to-b from-blue-50/50 via-white to-slate-50 dark:from-slate-900/50 dark:via-slate-950 dark:to-slate-950 border-t border-slate-200/80 dark:border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 text-xs font-bold mb-4">
                United Nations SDG 4 Alignment
              </div>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
                Democratizing Equitable, Data-Driven Quality Education
              </h2>
              <p className="mt-4 text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                Target 4.4 of SDG 4 calls for substantially increasing the number of youth and adults who have relevant technical and vocational skills for employment, decent jobs, and entrepreneurship.
              </p>

              <div className="mt-6 space-y-3.5">
                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-600 flex items-center justify-center shrink-0 mt-0.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                  <p className="text-xs text-slate-700 dark:text-slate-300">
                    <strong className="text-slate-900 dark:text-white">Fair & Objective Evaluation:</strong> Removes socio-economic bias through standardized, evidence-based skill testing.
                  </p>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-600 flex items-center justify-center shrink-0 mt-0.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                  <p className="text-xs text-slate-700 dark:text-slate-300">
                    <strong className="text-slate-900 dark:text-white">Bridge Higher Education & Industry:</strong> Maps curriculum performance to real industry role requirements.
                  </p>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-600 flex items-center justify-center shrink-0 mt-0.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                  <p className="text-xs text-slate-700 dark:text-slate-300">
                    <strong className="text-slate-900 dark:text-white">Universal Portability:</strong> Blockchain-secured certificates prove competencies worldwide without centralized gatekeepers.
                  </p>
                </div>
              </div>

              <div className="mt-8">
                <Link
                  to="/register"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all shadow-md shadow-blue-500/20"
                >
                  Join the Mission <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>

            <div className="glass-card p-8 bg-gradient-to-br from-white to-blue-50/30 dark:from-slate-900 dark:to-slate-800/40 border border-blue-200/60 dark:border-blue-900/40">
              <h3 className="font-bold text-base text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-blue-600" /> Platform SDG 4 Impact Indicators
              </h3>

              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span className="text-slate-600 dark:text-slate-400">Target 4.4: Employability Skill Alignment</span>
                    <span className="text-blue-600 dark:text-blue-400">92%</span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-600 rounded-full" style={{ width: '92%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span className="text-slate-600 dark:text-slate-400">Personalized Learning Paths Generated</span>
                    <span className="text-emerald-600 dark:text-emerald-400">100% Tailored</span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-600 rounded-full" style={{ width: '100%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span className="text-slate-600 dark:text-slate-400">Cryptographic Credential Tamper Defense</span>
                    <span className="text-indigo-600 dark:text-indigo-400">100% Immutable</span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-indigo-600 rounded-full" style={{ width: '100%' }}></div>
                  </div>
                </div>
              </div>

              <div className="mt-6 p-4 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-[11px] text-blue-800 dark:text-blue-300 leading-relaxed border border-blue-100 dark:border-blue-900/50">
                "Education is the most powerful weapon which you can use to change the world." Providing students transparent visibility into their skills ensures no learner is left behind.
              </div>
            </div>

          </div>

        </div>
      </section>

    </div>
  );
};

export default Landing;
