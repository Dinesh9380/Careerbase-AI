import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { FileCheck, Shield, Clock, Search } from 'lucide-react';
import Badge from '../components/Badge';

const AdminAuditLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await api.get('/admin/audit-logs?limit=100');
      setLogs(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const filtered = logs.filter(l => 
    l.action.toLowerCase().includes(search.toLowerCase()) ||
    l.user_email.toLowerCase().includes(search.toLowerCase()) ||
    l.ip_address.includes(search)
  );

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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            Security & System Audit Trail
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
            Immutable log of all user registrations, logins, assessment submissions, and administrative events.
          </p>
        </div>

        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by action, email, or IP..."
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      {/* Logs Table */}
      <div className="glass-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-900/70 text-slate-500 uppercase tracking-wider text-[10px] font-bold">
                <th className="p-4">Timestamp</th>
                <th className="p-4">Action</th>
                <th className="p-4">User</th>
                <th className="p-4">Status</th>
                <th className="p-4">IP Address</th>
                <th className="p-4">Metadata</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-mono text-[11px]">
              {filtered.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
                  <td className="p-4 whitespace-nowrap text-slate-500 font-sans">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td className="p-4 font-bold text-slate-900 dark:text-white font-sans">
                    {log.action}
                  </td>
                  <td className="p-4 text-slate-600 dark:text-slate-400 font-sans">
                    {log.user_email}
                  </td>
                  <td className="p-4">
                    <Badge variant={log.status === 'SUCCESS' ? 'success' : 'danger'} className="font-sans text-[10px]">
                      {log.status}
                    </Badge>
                  </td>
                  <td className="p-4 text-slate-500">
                    {log.ip_address}
                  </td>
                  <td className="p-4 text-slate-500 max-w-xs truncate" title={JSON.stringify(log.details)}>
                    {JSON.stringify(log.details)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};

export default AdminAuditLogsPage;
