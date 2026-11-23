import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sparkles, Lock, Mail, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogin = async (e) => {
    e?.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      const user = await login(email, password);
      const from = location.state?.from?.pathname;
      if (from) {
        navigate(from, { replace: true });
      } else {
        if (user.role === 'admin') navigate('/admin/dashboard');
        else if (user.role === 'counselor') navigate('/counselor/dashboard');
        else navigate('/dashboard');
      }
    } catch (err) {
      if (!err.response || err.response.status >= 500) {
        setError('Backend server is not running on port 8000. Please start the backend server using start.bat or uvicorn.');
      } else {
        setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const fillCredentials = (demoEmail) => {
    setEmail(demoEmail);
    setPassword('Demo@123456');
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 glass-card p-8 sm:p-10 relative">
        
        <div className="text-center">
          <div className="mx-auto w-12 h-12 rounded-2xl bg-gradient-to-tr from-primary-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-primary-500/30 mb-4">
            <Sparkles className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 dark:text-white">
            Welcome back
          </h2>
          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
            Sign in to access your skills, roadmaps, and career intelligence.
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 text-xs text-rose-700 dark:text-rose-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form className="mt-6 space-y-4" onSubmit={handleLogin}>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@university.edu"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500 outline-none transition-all"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                Password
              </label>
              <span className="text-[11px] text-primary-600 dark:text-primary-400 cursor-pointer">
                Forgot password?
              </span>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white focus:ring-2 focus:ring-primary-500 outline-none transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isSubmitting ? 'Signing in...' : 'Sign In'} <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Demo Credentials Quick-Fill */}
        <div className="pt-4 border-t border-slate-100 dark:border-slate-800 text-center">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
            Quick Fill Demo Credentials
          </span>
          <div className="flex flex-wrap gap-2 justify-center">
            <button
              type="button"
              onClick={() => fillCredentials('student@demo.com')}
              className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-[11px] font-medium text-slate-700 dark:text-slate-300"
            >
              Student
            </button>
            <button
              type="button"
              onClick={() => fillCredentials('admin@demo.com')}
              className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-[11px] font-medium text-slate-700 dark:text-slate-300"
            >
              Admin
            </button>
            <button
              type="button"
              onClick={() => fillCredentials('counselor@demo.com')}
              className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-[11px] font-medium text-slate-700 dark:text-slate-300"
            >
              Counselor
            </button>
          </div>
        </div>

        <div className="text-center text-xs text-slate-500 dark:text-slate-400">
          Don't have an account yet?{' '}
          <Link to="/register" className="font-bold text-primary-600 dark:text-primary-400 hover:underline">
            Register now
          </Link>
        </div>

      </div>
    </div>
  );
};

export default Login;
