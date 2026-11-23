import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { ShieldCheck, Plus, FileDown, ExternalLink, Hash, Award, CheckCircle2, Copy } from 'lucide-react';
import Badge from '../components/Badge';

const CertificatesPage = () => {
  const [credentials, setCredentials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isMinting, setIsMinting] = useState(false);
  const [copiedId, setCopiedId] = useState('');

  useEffect(() => {
    fetchCredentials();
  }, []);

  const fetchCredentials = async () => {
    try {
      const res = await api.get('/credentials');
      setCredentials(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleMintCertificate = async () => {
    const title = prompt("Enter Credential Title:", "Advanced Python & Machine Learning Competency");
    if (!title) return;

    setIsMinting(true);
    try {
      await api.post('/credentials/create', {
        title,
        credential_type: "Skill Assessment Certificate",
        metadata: { score: 92.5, honors: "Magna Cum Laude", issued_by: "EduCareer AI Authority" }
      });
      fetchCredentials();
    } catch (e) {
      alert("Failed to mint certificate onto blockchain ledger.");
    } finally {
      setIsMinting(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(''), 2500);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-emerald-900/10 via-primary-900/5 to-transparent border-emerald-200/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-600 mb-1">
              <ShieldCheck className="w-4 h-4" /> Cryptographic Proof & Privacy
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              Blockchain Credential Vault
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
              Immutable academic and skill certificates registered on the blockchain ledger. Employers can verify authenticity instantly without exposing sensitive student PII.
            </p>
          </div>

          <button
            onClick={handleMintCertificate}
            disabled={isMinting}
            className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5 self-start sm:self-auto shrink-0 disabled:opacity-50"
          >
            <Plus className="w-4 h-4" />
            {isMinting ? 'Mining Block...' : 'Mint New Credential'}
          </button>
        </div>
      </div>

      {/* Credentials List */}
      <div className="space-y-4">
        {credentials.length === 0 ? (
          <div className="glass-card p-10 text-center text-xs text-slate-500">
            No credentials issued yet. Complete an assessment or click 'Mint New Credential' to anchor your first certificate on the blockchain.
          </div>
        ) : (
          credentials.map((cred) => (
            <div key={cred.id} className="glass-card p-6 border-l-4 border-l-emerald-500 space-y-4">
              
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 flex items-center justify-center font-bold">
                    <Award className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-extrabold text-base text-slate-900 dark:text-white">
                      {cred.title}
                    </h3>
                    <div className="flex items-center gap-2 mt-0.5">
                      <Badge variant="primary" className="text-[10px]">{cred.credential_type}</Badge>
                      <span className="text-[11px] text-slate-400">
                        Issued: {new Date(cred.issued_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Badge variant="success" className="text-xs px-2.5 py-1">
                    VERIFIED ON-CHAIN
                  </Badge>
                </div>
              </div>

              {/* Hashes & Ledger Telemetry */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/50 border border-slate-200/50 dark:border-slate-800/50">
                  <span className="text-slate-400 font-bold block text-[10px] uppercase mb-0.5">Credential ID</span>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-800 dark:text-slate-200 select-all font-semibold">{cred.credential_id}</span>
                    <button
                      onClick={() => copyToClipboard(cred.credential_id, cred.credential_id)}
                      className="text-slate-400 hover:text-slate-700 dark:hover:text-white p-1"
                      title="Copy ID"
                    >
                      <Copy className="w-3.5 h-3.5" />
                    </button>
                  </div>
                  {copiedId === cred.credential_id && (
                    <span className="text-[10px] text-emerald-600 block mt-0.5">Copied to clipboard!</span>
                  )}
                </div>

                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/50 border border-slate-200/50 dark:border-slate-800/50">
                  <span className="text-slate-400 font-bold block text-[10px] uppercase mb-0.5">Block Number & Issuer</span>
                  <div className="flex items-center justify-between text-slate-800 dark:text-slate-200 font-semibold">
                    <span>Block #{cred.block_number}</span>
                    <span className="text-[11px] text-slate-400">{cred.issuer_address}</span>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/50 border border-slate-200/50 dark:border-slate-800/50 md:col-span-2">
                  <span className="text-slate-400 font-bold block text-[10px] uppercase mb-0.5">Cryptographic SHA-256 Hash</span>
                  <span className="text-indigo-600 dark:text-indigo-400 select-all break-all text-[11px]">{cred.credential_hash}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-2 flex flex-wrap items-center justify-between gap-3 text-xs">
                <Link
                  to={`/verify/${cred.credential_id}`}
                  className="font-bold text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1"
                >
                  <ExternalLink className="w-3.5 h-3.5" /> Open Public Verification Link
                </Link>

                <button
                  onClick={async () => {
                    const res = await api.get('/reports/download-pdf', { responseType: 'blob' });
                    const blob = new Blob([res.data], { type: 'application/pdf' });
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', `${cred.credential_id}.pdf`);
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                  }}
                  className="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-semibold hover:bg-slate-100 dark:hover:bg-slate-800 flex items-center gap-1.5"
                >
                  <FileDown className="w-3.5 h-3.5 text-primary-600" /> Download Certified PDF
                </button>
              </div>

            </div>
          ))
        )}
      </div>

    </div>
  );
};

export default CertificatesPage;
