import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { User, BookOpen, Cpu, Heart, FolderGit2, Award, Save, Plus, Trash2, CheckCircle2 } from 'lucide-react';
import Badge from '../components/Badge';

const ProfilePage = () => {
  const [activeTab, setActiveTab] = useState('personal');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const [formData, setFormData] = useState({
    phone: '',
    date_of_birth: '',
    location: '',
    desired_job_role: '',
    preferred_industry: '',
    preferred_location: '',
    higher_studies_preference: '',
    job_preference: '',
    academic: {
      college: '',
      degree: '',
      branch: '',
      year_of_study: '',
      cgpa: 8.5,
      graduation_year: 2026,
      academic_subjects: []
    },
    skills: [],
    soft_skills: [],
    interests: [],
    projects: [],
    certifications: []
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await api.get('/students/me');
      setFormData({
        ...res.data,
        academic: res.data.academic || { college: '', degree: '', branch: '', year_of_study: '', cgpa: 8.0, graduation_year: 2026, academic_subjects: [] },
        skills: res.data.skills || [],
        soft_skills: res.data.soft_skills || [],
        interests: res.data.interests || [],
        projects: res.data.projects || [],
        certifications: res.data.certifications || []
      });
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setSuccessMsg('');
    try {
      await api.put('/students/me', {
        phone: formData.phone,
        date_of_birth: formData.date_of_birth,
        location: formData.location,
        desired_job_role: formData.desired_job_role,
        preferred_industry: formData.preferred_industry,
        preferred_location: formData.preferred_location,
        higher_studies_preference: formData.higher_studies_preference,
        job_preference: formData.job_preference,
        academic: formData.academic,
        skills: formData.skills.map(s => ({
          skill_name: s.skill_name,
          proficiency_score: s.proficiency_score,
          proficiency_level: s.proficiency_level
        }))
      });
      setSuccessMsg('Profile updated and recommendations recalculated successfully!');
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (e) {
      alert("Failed to save profile changes.");
    } finally {
      setSaving(false);
    }
  };

  const addSkill = () => {
    const name = prompt("Enter skill name (e.g. Docker, TypeScript, PyTorch):");
    if (name) {
      setFormData(prev => ({
        ...prev,
        skills: [...prev.skills, { skill_name: name, proficiency_score: 65, proficiency_level: 'Intermediate' }]
      }));
    }
  };

  const removeSkill = (index) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.filter((_, i) => i !== index)
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const tabs = [
    { id: 'personal', label: 'Personal & Career', icon: User },
    { id: 'academic', label: 'Academics', icon: BookOpen },
    { id: 'skills', label: 'Technical Skills', icon: Cpu },
    { id: 'projects', label: 'Projects & Work', icon: FolderGit2 },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">
            Student Academic & Professional Profile
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Complete your profile to enhance AI recommendation accuracy and ATS match scores.
          </p>
        </div>

        <button
          onClick={handleSave}
          disabled={saving}
          className="px-5 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 transition-all flex items-center gap-2 self-start sm:self-auto disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          {saving ? 'Saving...' : 'Save Profile Changes'}
        </button>
      </div>

      {successMsg && (
        <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-xs font-semibold text-emerald-700 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{successMsg}</span>
        </div>
      )}

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 dark:border-slate-800 overflow-x-auto pb-1">
        {tabs.map(t => {
          const Icon = t.icon;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                activeTab === t.id
                  ? 'bg-primary-50 dark:bg-primary-950/60 text-primary-600 dark:text-primary-400 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Contents */}
      <div className="glass-card p-6 sm:p-8">
        
        {/* 1. Personal & Career */}
        {activeTab === 'personal' && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-slate-800 pb-2">
              Career Preferences & Aspiration
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Target Career Role
                </label>
                <input
                  type="text"
                  value={formData.desired_job_role || ''}
                  onChange={(e) => setFormData({ ...formData, desired_job_role: e.target.value })}
                  placeholder="e.g. Data Scientist, Full Stack Developer"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Preferred Industry
                </label>
                <input
                  type="text"
                  value={formData.preferred_industry || ''}
                  onChange={(e) => setFormData({ ...formData, preferred_industry: e.target.value })}
                  placeholder="e.g. Artificial Intelligence, Cloud Services, FinTech"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Phone Number
                </label>
                <input
                  type="text"
                  value={formData.phone || ''}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="+1 (555) 000-0000"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Location / Region
                </label>
                <input
                  type="text"
                  value={formData.location || ''}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  placeholder="e.g. San Francisco, CA / Remote"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>
            </div>
          </div>
        )}

        {/* 2. Academic Record */}
        {activeTab === 'academic' && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-slate-800 pb-2">
              University & Degree Information
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  College / University
                </label>
                <input
                  type="text"
                  value={formData.academic?.college || ''}
                  onChange={(e) => setFormData({ ...formData, academic: { ...formData.academic, college: e.target.value } })}
                  placeholder="e.g. Institute of Technology"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Degree & Major
                </label>
                <input
                  type="text"
                  value={formData.academic?.degree || ''}
                  onChange={(e) => setFormData({ ...formData, academic: { ...formData.academic, degree: e.target.value } })}
                  placeholder="e.g. Bachelor of Technology (B.Tech)"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Branch / Specialization
                </label>
                <input
                  type="text"
                  value={formData.academic?.branch || ''}
                  onChange={(e) => setFormData({ ...formData, academic: { ...formData.academic, branch: e.target.value } })}
                  placeholder="e.g. Computer Science & Engineering"
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Cumulative GPA / Percentage
                </label>
                <input
                  type="number"
                  step="0.01"
                  max="10.0"
                  value={formData.academic?.cgpa || 8.5}
                  onChange={(e) => setFormData({ ...formData, academic: { ...formData.academic, cgpa: parseFloat(e.target.value) } })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
              </div>
            </div>
          </div>
        )}

        {/* 3. Technical Skills */}
        {activeTab === 'skills' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                Technical Competencies & Proficiencies
              </h3>
              <button
                type="button"
                onClick={addSkill}
                className="px-3 py-1.5 rounded-lg bg-primary-50 dark:bg-primary-950 text-primary-600 dark:text-primary-400 font-bold text-xs flex items-center gap-1 hover:bg-primary-100"
              >
                <Plus className="w-3.5 h-3.5" /> Add Skill
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {formData.skills.map((skill, index) => (
                <div key={index} className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-slate-800 dark:text-slate-200">{skill.skill_name}</span>
                    <button
                      type="button"
                      onClick={() => removeSkill(index)}
                      className="text-slate-400 hover:text-rose-500"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <div className="flex items-center gap-3">
                    <input
                      type="range"
                      min="10"
                      max="100"
                      value={skill.proficiency_score}
                      onChange={(e) => {
                        const val = parseInt(e.target.value);
                        const newSkills = [...formData.skills];
                        newSkills[index].proficiency_score = val;
                        newSkills[index].proficiency_level = val >= 85 ? 'Expert' : (val >= 70 ? 'Advanced' : (val >= 50 ? 'Intermediate' : 'Beginner'));
                        setFormData({ ...formData, skills: newSkills });
                      }}
                      className="w-full accent-primary-600"
                    />
                    <span className="text-xs font-bold text-primary-600 w-10 text-right">
                      {Math.round(skill.proficiency_score)}%
                    </span>
                  </div>

                  <div className="text-[10px] text-slate-500 flex justify-between">
                    <span>Level: {skill.proficiency_level}</span>
                    <span className="text-slate-400">Verified by Assessment & Project</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 4. Projects */}
        {activeTab === 'projects' && (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-slate-800 pb-2">
              Demonstrated Projects & Technical Artifacts
            </h3>

            <div className="space-y-3">
              {formData.projects.map((proj, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800">
                  <h4 className="font-bold text-xs text-slate-800 dark:text-slate-200">{proj.title}</h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">{proj.description}</p>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {proj.technologies?.map((tech, tIdx) => (
                      <span key={tIdx} className="px-2 py-0.5 rounded-md bg-slate-200 dark:bg-slate-800 text-[10px] font-mono text-slate-700 dark:text-slate-300">
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>

    </div>
  );
};

export default ProfilePage;
