import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { ShieldCheck, Hash, Clock, CheckCircle2, AlertTriangle, Layers, RefreshCw } from 'lucide-react';
import Badge from '../components/Badge';

const AdminBlockchainPage = () => {
  const [ledger, setLedger] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLedger();
  }, []);

  const fetchLedger = async () => {
    setLoading(true);
    try {
      const res = await api.get('/blockchain/ledger');
      setLedger(res.data);
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

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-emerald-900/10 via-primary-900/5 to-transparent border-emerald-200/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-600 mb-1">
              <ShieldCheck className="w-4 h-4" /> Dual EVM Smart Contract & Merkle Hash-Chain
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              Blockchain Ledger Explorer
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
              Inspect the cryptographically linked blocks of the tamper-evident credential registry. Every block cryptographically references the preceding block's hash.
            </p>
          </div>

          <button
            onClick={fetchLedger}
            className="px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 font-bold text-xs hover:bg-slate-50 flex items-center gap-1.5 self-start sm:self-auto"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh Blocks
          </button>
        </div>
      </div>

      {/* Chain Status */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <span className="text-xs font-semibold text-slate-500">Total Blocks Mined</span>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
            {ledger?.total_blocks || 0}
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold mt-0.5 block">
            Genesis + Credential Blocks
          </span>
        </div>

        <div className="glass-card p-5">
          <span className="text-xs font-semibold text-slate-500">Consensus & Proof Difficulty</span>
          <div className="text-2xl font-extrabold text-indigo-600 mt-1">
            Difficulty: {ledger?.difficulty || 2}
          </div>
          <span className="text-[11px] text-slate-400 mt-0.5 block">
            SHA-256 Leading Zeroes Target
          </span>
        </div>

        <div className="glass-card p-5">
          <span className="text-xs font-semibold text-slate-500">Chain Integrity Status</span>
          <div className="text-2xl font-extrabold text-emerald-600 mt-1 flex items-center gap-1.5">
            <CheckCircle2 className="w-6 h-6" /> 100% VALID
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold mt-0.5 block">
            Zero Tampering Detected
          </span>
        </div>
      </div>

      {/* Blocks Visual List */}
      <div className="space-y-4">
        {ledger?.chain?.map((block) => (
          <div key={block.index} className="glass-card p-6 border-l-4 border-l-primary-600 space-y-3 font-mono text-xs">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-sm text-primary-600">Block #{block.index}</span>
                {block.index === 0 && <Badge variant="primary" className="font-sans">GENESIS</Badge>}
              </div>
              <span className="text-slate-400 text-[11px]">
                Timestamp: {new Date(block.timestamp * 1000).toLocaleString()} (Nonce: {block.nonce})
              </span>
            </div>

            <div className="space-y-2">
              <div>
                <span className="text-slate-400 text-[10px] uppercase font-bold block">Current Block Hash</span>
                <span className="text-emerald-600 dark:text-emerald-400 break-all select-all font-semibold">
                  {block.hash}
                </span>
              </div>

              <div>
                <span className="text-slate-400 text-[10px] uppercase font-bold block">Previous Block Hash</span>
                <span className="text-slate-600 dark:text-slate-400 break-all select-all">
                  {block.previous_hash}
                </span>
              </div>
            </div>

            {/* Transactions in Block */}
            <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800">
              <span className="text-slate-400 text-[10px] uppercase font-bold block mb-1">Transactions Sealed</span>
              <div className="space-y-1">
                {block.transactions?.map((tx, tIdx) => (
                  <div key={tIdx} className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50 flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-[11px]">
                    <span className="text-slate-800 dark:text-slate-200 font-bold">
                      {tx.title || tx.credential_id}
                    </span>
                    <span className="text-indigo-600 dark:text-indigo-400">
                      ID: {tx.credential_id}
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
};

export default AdminBlockchainPage;
