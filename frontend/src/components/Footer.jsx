import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ShieldCheck, Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-slate-950/60 backdrop-blur-sm mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-lg bg-primary-600 text-white flex items-center justify-center font-bold text-xs">
              <Sparkles className="w-3.5 h-3.5" />
            </div>
            <span className="font-bold text-sm text-slate-800 dark:text-slate-200">
              EduCareer AI
            </span>
            <span className="text-xs text-slate-400">
              © {new Date().getFullYear()} — Empowering students via AI & Quality Education (SDG 4)
            </span>
          </div>

          <div className="flex items-center gap-6 text-xs text-slate-500 dark:text-slate-400">
            <Link to="/verify" className="hover:text-primary-600 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> Verify Credential
            </Link>
            <a href="#privacy" className="hover:text-primary-600">Privacy Policy</a>
            <a href="#terms" className="hover:text-primary-600">Terms of Service</a>
            <a href="#audit" className="hover:text-primary-600">Security Audit</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
