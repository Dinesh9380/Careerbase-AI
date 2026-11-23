import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard, User, Award, CheckSquare, Compass, GitCompare,
  Map, BookOpen, FileText, ShieldCheck, MessageSquare, Database,
  Activity, Users, FileCheck, Layers, X
} from 'lucide-react';

const Sidebar = ({ isOpen, onClose }) => {
  const { user } = useAuth();
  if (!user) return null;

  const studentLinks = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/profile', label: 'My Profile', icon: User },
    { to: '/assessments', label: 'Skill Assessments', icon: CheckSquare },
    { to: '/skills', label: 'Skill Profile', icon: Activity },
    { to: '/skill-gaps', label: 'Skill Gaps', icon: Layers },
    { to: '/careers', label: 'Career Matches', icon: Compass },
    { to: '/career-comparison', label: 'Compare Careers', icon: GitCompare },
    { to: '/roadmap', label: 'Learning Roadmap', icon: Map },
    { to: '/resources', label: 'Resources', icon: BookOpen },
    { to: '/resume', label: 'Resume Vision AI', icon: FileText },
    { to: '/certificates', label: 'Blockchain Vault', icon: ShieldCheck },
    { to: '/career-ai', label: 'CareerAI Chat', icon: MessageSquare },
  ];

  const adminLinks = [
    { to: '/admin/dashboard', label: 'Admin Overview', icon: LayoutDashboard },
    { to: '/admin/students', label: 'Students Roster', icon: Users },
    { to: '/admin/bigdata', label: 'Big Data Pipeline', icon: Database },
    { to: '/admin/blockchain', label: 'Blockchain Explorer', icon: ShieldCheck },
    { to: '/admin/audit-logs', label: 'Audit Trail Logs', icon: FileCheck },
  ];

  const counselorLinks = [
    { to: '/counselor/dashboard', label: 'Counselor Portal', icon: LayoutDashboard },
    { to: '/counselor/students', label: 'Assigned Students', icon: Users },
  ];

  let activeLinks = studentLinks;
  if (user.role === 'admin') activeLinks = adminLinks;
  else if (user.role === 'counselor') activeLinks = counselorLinks;

  const baseItemClass = "flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all";
  const activeClass = "bg-primary-50 dark:bg-primary-950/60 text-primary-600 dark:text-primary-400 font-bold shadow-sm";
  const inactiveClass = "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-white";

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 lg:hidden"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-16 bottom-0 left-0 z-50 w-64 border-r border-slate-200/80 dark:border-slate-800/80 bg-white/95 dark:bg-slate-950/95 backdrop-blur-md overflow-y-auto px-4 py-4 transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between lg:hidden mb-4 pb-2 border-b border-slate-100 dark:border-slate-800">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Navigation</span>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-slate-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mb-3 px-3">
          <span className="text-[11px] font-extrabold uppercase tracking-wider text-slate-400 dark:text-slate-500">
            {user.role === 'admin' ? 'Administration' : (user.role === 'counselor' ? 'Counseling' : 'Student Portal')}
          </span>
        </div>

        <nav className="space-y-1">
          {activeLinks.map(link => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                onClick={() => onClose && onClose()}
                className={({ isActive }) => `${baseItemClass} ${isActive ? activeClass : inactiveClass}`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{link.label}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* SDG 4 Impact Callout in Sidebar Footer */}
        <div className="mt-8 p-3.5 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50/50 dark:from-slate-900 dark:to-slate-800/60 border border-blue-100 dark:border-slate-700/60">
          <div className="flex items-center gap-2 text-blue-700 dark:text-blue-400 font-bold text-xs mb-1">
            <Award className="w-4 h-4" /> UN SDG 4 Certified
          </div>
          <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
            Personalized guidance bridging education with industry readiness.
          </p>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
