import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, CheckCircle2, MessageSquare, Send, Award, Compass, Layers, User } from 'lucide-react';
import Badge from '../components/Badge';

const CounselorStudentDetailPage = () => {
  const { id } = useParams();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [noteText, setNoteText] = useState('');
  const [actionInput, setActionInput] = useState('');
  const [guidanceActions, setGuidanceActions] = useState([]);
  const [savingNote, setSavingNote] = useState(false);
  const [noteSuccess, setNoteSuccess] = useState('');

  useEffect(() => {
    fetchStudentDetail();
  }, [id]);

  const fetchStudentDetail = async () => {
    try {
      const res = await api.get(`/counselor/students/${id}`);
      setStudent(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleAddAction = (e) => {
    e.preventDefault();
    if (actionInput.trim()) {
      setGuidanceActions(prev => [...prev, actionInput.trim()]);
      setActionInput('');
    }
  };

  const handleSubmitNote = async (e) => {
    e.preventDefault();
    if (!noteText.trim()) return;

    setSavingNote(true);
    setNoteSuccess('');
    try {
      await api.post(`/counselor/students/${id}/notes`, {
        note_text: noteText,
        guidance_actions: guidanceActions
      });
      setNoteSuccess('Guidance note recorded and notification dispatched to student.');
      setNoteText('');
      setGuidanceActions([]);
      fetchStudentDetail();
    } catch (e) {
      alert("Failed to submit counselor note.");
    } finally {
      setSavingNote(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!student) {
    return <div className="p-8 text-center text-xs text-slate-500">Student not found.</div>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      
      <Link
        to="/counselor/dashboard"
        className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-primary-600 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Counselor Roster
      </Link>

      {/* Student Overview Header */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-teal-900/15 via-primary-900/5 to-transparent border-teal-200/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-teal-600 mb-1">
              <User className="w-4 h-4" /> Academic & Skill Evaluation
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              {student.full_name}
            </h1>
            <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
              {student.email} • {student.academic?.degree} (CGPA: {student.academic?.cgpa}) • Target: <strong className="text-teal-600">{student.desired_career}</strong>
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Skills & Top Recommendations (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Skills Grid */}
          <div className="glass-card p-6">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white mb-3 flex items-center gap-2">
              <Award className="w-4 h-4 text-primary-600" /> Verified Skill Competencies
            </h3>
            <div className="grid grid-cols-2 gap-3">
              {student.skills?.map((s, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/50 dark:border-slate-800/50">
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span>{s.skill_name}</span>
                    <span className="text-primary-600">{Math.round(s.proficiency_score)}%</span>
                  </div>
                  <span className="text-[10px] text-slate-400">Level: {s.proficiency_level}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Past Counselor Guidance Notes */}
          <div className="glass-card p-6">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-teal-600" /> Previous Counselor Intervention Notes
            </h3>

            <div className="space-y-3">
              {student.notes?.length === 0 ? (
                <p className="text-xs text-slate-400">No previous counselor notes logged for this student.</p>
              ) : (
                student.notes?.map((n) => (
                  <div key={n.id} className="p-4 rounded-xl bg-slate-50 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/60 space-y-2">
                    <div className="flex items-center justify-between text-xs font-semibold">
                      <span className="text-teal-700 dark:text-teal-400 font-bold">{n.counselor_name}</span>
                      <span className="text-slate-400 text-[10px]">{new Date(n.created_at).toLocaleDateString()}</span>
                    </div>
                    <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                      {n.note_text}
                    </p>
                    {n.guidance_actions?.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-slate-200/50 dark:border-slate-800/50 space-y-1">
                        <span className="text-[10px] font-bold text-slate-400 uppercase">Assigned Actions:</span>
                        {n.guidance_actions.map((act, aIdx) => (
                          <div key={aIdx} className="flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-400">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                            <span>{act}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>

        </div>

        {/* Right: Add Note Form (5 cols) */}
        <div className="lg:col-span-5 glass-card p-6 h-fit sticky top-20">
          <h3 className="font-bold text-sm text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <Send className="w-4 h-4 text-primary-600" /> Add Personalized Guidance Note
          </h3>

          {noteSuccess && (
            <div className="p-3 mb-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 text-xs font-semibold text-emerald-700">
              {noteSuccess}
            </div>
          )}

          <form onSubmit={handleSubmitNote} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Guidance & Feedback Remarks
              </label>
              <textarea
                rows={4}
                required
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
                placeholder="Write specific recommendations, interview coaching tips, or capstone feedback..."
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Prescribe Actionable Next Steps
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={actionInput}
                  onChange={(e) => setActionInput(e.target.value)}
                  placeholder="e.g. Complete Docker advanced quiz"
                  className="flex-1 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 text-xs text-slate-900 dark:text-white"
                />
                <button
                  type="button"
                  onClick={handleAddAction}
                  className="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-200"
                >
                  Add
                </button>
              </div>

              {guidanceActions.length > 0 && (
                <div className="mt-2 space-y-1">
                  {guidanceActions.map((act, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs">
                      <span>• {act}</span>
                      <button
                        type="button"
                        onClick={() => setGuidanceActions(guidanceActions.filter((_, i) => i !== idx))}
                        className="text-rose-500 text-xs font-bold ml-2"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={savingNote}
              className="w-full py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-md shadow-teal-500/20 transition-all flex items-center justify-center gap-1.5 disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
              {savingNote ? 'Recording Note...' : 'Dispatch Counselor Guidance'}
            </button>
          </form>
        </div>

      </div>

    </div>
  );
};

export default CounselorStudentDetailPage;
