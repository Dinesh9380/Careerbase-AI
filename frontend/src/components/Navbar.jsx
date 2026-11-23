import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import {
  Sparkles, Bell, Sun, Moon, LogOut, User as UserIcon,
  ShieldCheck, BookOpen, Layers, Menu, X, Award
} from 'lucide-react';
import api from '../services/api';

const Navbar = ({ onToggleSidebar }) => {
  const { user, logout, isStudent } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const [notifications, setNotifications] = useState([]);
  const [showNotifs, setShowNotifs] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (user) {
      api.get('/notifications')
        .then(res => {
          setNotifications(res.data);
          setUnreadCount(res.data.filter(n => !n.is_read).length);
        })
        .catch(() => {});
    }
  }, [user]);

  const markRead = async (id) => {
    try {
      await api.post(`/notifications/${id}/read`);
      setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (e) {}
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 dark:border-slate-800/80 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Left: Mobile Toggle & Brand */}
        <div className="flex items-center gap-4">
          {user && (
            <button
              onClick={onToggleSidebar}
              className="lg:hidden p-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
              aria-label="Toggle Navigation Menu"
            >
              <Menu className="w-5 h-5" />
            </button>
          )}

          <Link to={user ? (user.role === 'admin' ? '/admin/dashboard' : (user.role === 'counselor' ? '/counselor/dashboard' : '/dashboard')) : '/'} className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-primary-600 to-indigo-500 flex items-center justify-center shadow-md shadow-primary-500/20 text-white font-bold text-lg">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-slate-900 to-slate-700 dark:from-white dark:to-slate-300 bg-clip-text text-transparent">
                EduCareer<span className="text-primary-600 dark:text-primary-400">AI</span>
              </span>
              <div className="hidden sm:flex items-center gap-1.5 -mt-1">
                <span className="text-[10px] uppercase font-bold tracking-wider text-blue-600 dark:text-blue-400">
                  UN SDG 4: Quality Education
                </span>
              </div>
            </div>
          </Link>
        </div>

        {/* Center: Public Links when logged out */}
        {!user && (
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600 dark:text-slate-300">
            <Link to="/#features" className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Features</Link>
            <Link to="/#sdg4" className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">SDG 4 Impact</Link>
            <Link to="/#how-it-works" className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">How It Works</Link>
            <Link to="/verify" className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors flex items-center gap-1">
              <ShieldCheck className="w-4 h-4 text-emerald-600" /> Verify Certificate
            </Link>
          </nav>
        )}

        {/* Right Actions */}
        <div className="flex items-center gap-2.5 sm:gap-3">
          
          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
          </button>

          {user ? (
            <>
              {/* Notifications Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifs(!showNotifs)}
                  className="relative p-2 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  title="Notifications"
                >
                  <Bell className="w-4 h-4" />
                  {unreadCount > 0 && (
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500 ring-2 ring-white dark:ring-slate-950"></span>
                  )}
                </button>

                {showNotifs && (
                  <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl py-2 z-50 animate-in fade-in zoom-in-95 duration-100">
                    <div className="px-4 py-2 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
                      <span className="font-semibold text-sm text-slate-800 dark:text-slate-200">Notifications</span>
                      <span className="text-xs text-slate-400">{unreadCount} unread</span>
                    </div>
                    <div className="max-h-80 overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800/60">
                      {notifications.length === 0 ? (
                        <p className="py-6 text-center text-xs text-slate-400">No notifications yet.</p>
                      ) : (
                        notifications.map(n => (
                          <div
                            key={n.id}
                            onClick={() => markRead(n.id)}
                            className={`p-3.5 hover:bg-slate-50 dark:hover:bg-slate-800/40 cursor-pointer transition-colors ${!n.is_read ? 'bg-primary-50/40 dark:bg-primary-950/20' : ''}`}
                          >
                            <div className="flex items-start justify-between gap-2">
                              <h4 className="text-xs font-semibold text-slate-800 dark:text-slate-200">{n.title}</h4>
                              <span className="text-[10px] text-slate-400 shrink-0">
                                {new Date(n.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                              </span>
                            </div>
                            <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">{n.message}</p>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* User Pill / Profile */}
              <div className="flex items-center gap-3 pl-2 border-l border-slate-200 dark:border-slate-800">
                <div className="hidden md:block text-right">
                  <div className="text-xs font-bold text-slate-800 dark:text-slate-200 leading-tight">{user.full_name}</div>
                  <div className="text-[10px] capitalize text-primary-600 dark:text-primary-400 font-medium">{user.role}</div>
                </div>

                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-600 to-indigo-500 text-white flex items-center justify-center font-bold text-xs shadow-inner">
                  {user.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
                </div>

                <button
                  onClick={logout}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-colors"
                  title="Log out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="px-3.5 py-1.5 rounded-xl text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="px-4 py-1.5 rounded-xl text-sm font-semibold bg-primary-600 hover:bg-primary-500 text-white shadow-sm shadow-primary-500/20 transition-all"
              >
                Get Started
              </Link>
            </div>
          )}

        </div>
      </div>
    </header>
  );
};

export default Navbar;
