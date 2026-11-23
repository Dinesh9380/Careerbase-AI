import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { ShieldCheck, ShieldAlert, Search, CheckCircle2, AlertTriangle, Hash, Clock, Award } from 'lucide-react';
import Badge from '../components/Badge';

const VerifyCertificate = () => {
  const { credentialId: paramId } = useParams();
  const [credentialId, setCredentialId] = useState(paramId || 'CRED-2026-EDU-8492');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleVerify = async (idToVerify) => {
    const target = idToVerify || credentialId;
    if (!target.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await api.get(`/blockchain/verify/${encodeURIComponent(target.trim())}`);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to query blockchain ledger.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (paramId) {
      setCredentialId(paramId);
      handleVerify(paramId);
    } else {
      // Auto-verify sample credential
      handleVerify('CRED-2026-EDU-8492');
    }
  }, [paramId]);

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 text-xs font-bold mb-4 shadow-sm">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Public Cryptographic Ledger Verification</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Verify Academic & Skill Credentials
        </h1>
        <p className="mt-3 text-xs sm:text-sm text-slate-600 dark:text-slate-400">
          Validate the authenticity and tamper-evident integrity of student certifications directly against the blockchain registry.
        </p>
      </div>

      {/* Verification Search Bar */}
      <div className="glass-card p-4 sm:p-6 mb-8 max-w-2xl mx-auto">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleVerify();
          }}
          className="flex flex-col sm:flex-row gap-2.5"
        >
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={credentialId}
              onChange={(e) => setCredentialId(e.target.value)}
              placeholder="Enter Credential ID (e.g. CRED-2026-EDU-8492)"
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-emerald-500 font-mono"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Verify on Ledger'}
          </button>
        </form>
      </div>

      {/* Result Display */}
      {result && (
        <div className={`glass-card p-6 sm:p-8 border-2 transition-all ${
          result.is_valid
            ? 'border-emerald-500/40 bg-gradient-to-b from-emerald-50/20 to-white/40 dark:from-emerald-950/20 dark:to-slate-900'
            : 'border-rose-500/40 bg-gradient-to-b from-rose-50/20 to-white/40 dark:from-rose-950/20 dark:to-slate-900'
        }`}>
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200 dark:border-slate-800">
            <div className="flex items-center gap-3">
              <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${
                result.is_valid ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-400' : 'bg-rose-100 text-rose-600 dark:bg-rose-950 dark:text-rose-400'
              }`}>
                {result.is_valid ? <ShieldCheck className="w-7 h-7" /> : <ShieldAlert className="w-7 h-7" />}
              </div>
              <div>
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                  Blockchain Status
                </span>
                <span className={`text-xl font-extrabold ${result.is_valid ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                  {result.verification_status}
                </span>
              </div>
            </div>

            <Badge variant={result.is_valid ? 'success' : 'danger'} className="text-xs px-3 py-1 self-start sm:self-auto">
              {result.is_valid ? 'Cryptographically Sealed' : 'Tampering Detected'}
            </Badge>
          </div>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <div className="space-y-4">
              <div>
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Credential Title
                </span>
                <p className="text-sm font-bold text-slate-800 dark:text-slate-100">
                  {result.title || 'Technical Competency Certificate'}
                </p>
              </div>

              <div>
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Student Scholar
                </span>
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  {result.student_name || 'Verified Scholar'}
                </p>
              </div>

              <div>
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Verification Detail
                </span>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  {result.details}
                </p>
              </div>
            </div>

            <div className="space-y-3 p-4 rounded-xl bg-slate-50 dark:bg-slate-950/60 border border-slate-200/60 dark:border-slate-800/60 font-mono text-[11px]">
              <div>
                <span className="text-slate-400 font-bold block mb-0.5">Credential ID</span>
                <span className="text-slate-800 dark:text-slate-200 select-all">{result.credential_id}</span>
              </div>
              <div>
                <span className="text-slate-400 font-bold block mb-0.5">SHA-256 Content Hash</span>
                <span className="text-indigo-600 dark:text-indigo-400 break-all select-all">{result.credential_hash}</span>
              </div>
              <div>
                <span className="text-slate-400 font-bold block mb-0.5">Transaction Hash</span>
                <span className="text-emerald-600 dark:text-emerald-400 break-all select-all">{result.blockchain_tx_hash}</span>
              </div>
              <div className="flex justify-between pt-2 border-t border-slate-200 dark:border-slate-800 text-[10px]">
                <span className="text-slate-500">Block #{result.block_number}</span>
                <span className="text-slate-500">Dual EVM / Merkle Anchor</span>
              </div>
            </div>

          </div>

        </div>
      )}

      {error && (
        <div className="glass-card p-6 border-rose-200 dark:border-rose-900 text-center max-w-md mx-auto">
          <AlertTriangle className="w-8 h-8 text-rose-500 mx-auto mb-2" />
          <p className="text-xs text-rose-600 font-medium">{error}</p>
        </div>
      )}

    </div>
  );
};

export default VerifyCertificate;
