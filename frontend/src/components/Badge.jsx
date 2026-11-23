import React from 'react';

const Badge = ({ variant = 'default', children, className = '' }) => {
  const styles = {
    default: 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200',
    primary: 'bg-primary-50 text-primary-700 dark:bg-primary-950/60 dark:text-primary-300 border border-primary-200/50 dark:border-primary-800/50',
    success: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200/50 dark:border-emerald-800/50',
    warning: 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200/50 dark:border-amber-800/50',
    danger: 'bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200/50 dark:border-rose-800/50',
    sdg: 'bg-blue-600 text-white font-semibold shadow-sm shadow-blue-500/20'
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[variant] || styles.default} ${className}`}>
      {children}
    </span>
  );
};

export default Badge;
