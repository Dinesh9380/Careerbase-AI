import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { FileText, UploadCloud, CheckCircle2, AlertCircle, Sparkles, ArrowRight, Eye, Layers } from 'lucide-react';
import Badge from '../components/Badge';

const ResumePage = () => {
  const [analysis, setAnalysis] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [importing, setImporting] = useState(false);
  const [importSuccess, setImportSuccess] = useState('');
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [fileError, setFileError] = useState('');

  useEffect(() => {
    // Attempt fetching latest resume analysis
    api.get('/resume/latest')
      .then(res => {
        setAnalysis(res.data);
        const newSkills = res.data.extracted_skills?.filter(s => !s.in_profile).map(s => s.skill_name) || [];
        setSelectedSkills(newSkills);
      })
      .catch(() => {});
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'jpg', 'jpeg', 'png'].includes(ext)) {
      setFileError("Supported file formats: PDF, JPG, JPEG, PNG.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setFileError("File size exceeds 10MB limit.");
      return;
    }

    setFileError('');
    setUploading(true);
    setImportSuccess('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post('/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setAnalysis(res.data);
      const newSkills = res.data.extracted_skills?.filter(s => !s.in_profile).map(s => s.skill_name) || [];
      setSelectedSkills(newSkills);
    } catch (err) {
      setFileError(err.response?.data?.detail || "Failed to analyze document. Please check format.");
    } finally {
      setUploading(false);
    }
  };

  const handleImportSkills = async () => {
    if (selectedSkills.length === 0) return;
    setImporting(true);
    try {
      const res = await api.post('/resume/accept-skills', { skills: selectedSkills });
      setImportSuccess(res.data.message);
      // Refresh
      const latest = await api.get('/resume/latest');
      setAnalysis(latest.data);
    } catch (e) {
      alert("Failed to import skills into profile.");
    } finally {
      setImporting(false);
    }
  };

  const toggleSkill = (skillName) => {
    setSelectedSkills(prev => 
      prev.includes(skillName) ? prev.filter(s => s !== skillName) : [...prev, skillName]
    );
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      
      {/* Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-amber-900/10 via-primary-900/5 to-transparent border-amber-200/40">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Resume & Document Computer Vision Intelligence
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
          Upload PDF resumes or scanned document certificates. The OCR pipeline extracts structured competencies, computes keyword density, and syncs missing skills to your profile.
        </p>
      </div>

      {/* Upload Zone */}
      <div className="glass-card p-8 text-center border-2 border-dashed border-slate-300 dark:border-slate-800 hover:border-primary-500/50 transition-colors">
        <div className="w-14 h-14 rounded-2xl bg-primary-50 dark:bg-primary-950/60 text-primary-600 flex items-center justify-center mx-auto mb-4">
          <UploadCloud className="w-7 h-7" />
        </div>

        <h3 className="font-extrabold text-base text-slate-900 dark:text-white">
          Upload Resume or Scanned Credential
        </h3>
        <p className="text-xs text-slate-500 mt-1 mb-4">
          Supports PDF, JPG, JPEG, and PNG files (Max 10MB)
        </p>

        <label className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 cursor-pointer transition-all">
          <FileText className="w-4 h-4" />
          <span>{uploading ? 'Processing OCR & NLP Extraction...' : 'Choose File to Scan'}</span>
          <input
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileUpload}
            disabled={uploading}
            className="hidden"
          />
        </label>

        {fileError && (
          <p className="mt-3 text-xs text-rose-500 font-semibold">{fileError}</p>
        )}
      </div>

      {importSuccess && (
        <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-xs font-semibold text-emerald-700 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{importSuccess}</span>
        </div>
      )}

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6">
          
          {/* Summary KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            <div className="glass-card p-5">
              <span className="text-xs font-semibold text-slate-500">Document Completeness</span>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
                {Math.round(analysis.completeness_score)}%
              </div>
              <span className="text-[11px] text-slate-400 mt-0.5 block">Structure & Sectional Depth</span>
            </div>

            <div className="glass-card p-5">
              <span className="text-xs font-semibold text-slate-500">ATS Keyword Match</span>
              <div className="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">
                {Math.round(analysis.ats_keyword_coverage)}%
              </div>
              <span className="text-[11px] text-slate-400 mt-0.5 block">Analytical Market Estimate</span>
            </div>

            <div className="glass-card p-5">
              <span className="text-xs font-semibold text-slate-500">Skills Identified</span>
              <div className="text-2xl font-extrabold text-primary-600 mt-1">
                {analysis.extracted_skills?.length || 0}
              </div>
              <span className="text-[11px] text-slate-400 mt-0.5 block">Recognized Technical Keywords</span>
            </div>
          </div>

          {/* Extracted Skills & 1-Click Sync */}
          <div className="glass-card p-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <h3 className="font-bold text-base text-slate-900 dark:text-white">
                  Extracted Technical Skills & Profile Sync
                </h3>
                <p className="text-xs text-slate-400">
                  Select identified skills below to import directly into your verified student profile.
                </p>
              </div>

              <button
                onClick={handleImportSkills}
                disabled={importing || selectedSkills.length === 0}
                className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 self-start sm:self-auto disabled:opacity-40"
              >
                <CheckCircle2 className="w-4 h-4" />
                {importing ? 'Importing...' : `Import Selected (${selectedSkills.length})`}
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              {analysis.extracted_skills?.map((s, idx) => {
                const isSelected = selectedSkills.includes(s.skill_name);
                return (
                  <div
                    key={idx}
                    onClick={() => !s.in_profile && toggleSkill(s.skill_name)}
                    className={`p-3 rounded-xl border transition-all ${
                      s.in_profile
                        ? 'border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/30 opacity-70 cursor-default'
                        : (isSelected
                            ? 'border-emerald-500 bg-emerald-50/40 dark:bg-emerald-950/30 cursor-pointer shadow-sm'
                            : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 cursor-pointer')
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-900 dark:text-white">{s.skill_name}</span>
                      {s.in_profile ? (
                        <span className="text-[10px] text-primary-600 font-semibold">In Profile</span>
                      ) : (
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => toggleSkill(s.skill_name)}
                          className="accent-emerald-600"
                        />
                      )}
                    </div>
                    <span className="text-[10px] text-slate-400 block mt-1">{s.category}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Actionable Suggested Improvements */}
          <div className="glass-card p-6">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-500" /> Actionable Resume Enhancements
            </h3>
            <div className="space-y-2">
              {analysis.suggested_improvements?.map((imp, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50 text-xs text-slate-700 dark:text-slate-300 flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0"></div>
                  <span>{imp}</span>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
};

export default ResumePage;
