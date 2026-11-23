import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Clock, AlertCircle, ArrowLeft, ArrowRight, CheckCircle2, Flag, Send } from 'lucide-react';
import Badge from '../components/Badge';

const AssessmentTakePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [testData, setTestData] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // question_id => [option_id]
  const [timeLeft, setTimeLeft] = useState(1200); // 20 mins default
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const startTimeRef = useRef(Date.now());
  const timerRef = useRef(null);

  useEffect(() => {
    startTest();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [id]);

  const startTest = async () => {
    try {
      const res = await api.post(`/assessments/${id}/start`);
      setTestData(res.data);
      const totalSecs = (res.data.time_limit_minutes || 20) * 60;
      setTimeLeft(totalSecs);
      startTimeRef.current = Date.now();

      // Countdown timer
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timerRef.current);
            handleAutoSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

    } catch (e) {
      setError(e.response?.data?.detail || "Failed to start assessment. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (questionId, optionId) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: [optionId]
    }));
  };

  const handleAutoSubmit = () => {
    alert("Time limit expired! Your answers are being automatically submitted.");
    submitTest();
  };

  const submitTest = async () => {
    if (submitting) return;
    setSubmitting(true);
    if (timerRef.current) clearInterval(timerRef.current);

    const timeSpent = Math.round((Date.now() - startTimeRef.current) / 1000);
    const answersPayload = Object.entries(selectedAnswers).map(([qId, opts]) => ({
      question_id: parseInt(qId),
      selected_options: opts
    }));

    try {
      const res = await api.post(`/assessments/${testData.attempt_id}/submit`, {
        time_spent_seconds: timeSpent,
        answers: answersPayload
      });
      // Navigate to results
      navigate(`/assessment/result/${testData.attempt_id}`, { state: { result: res.data } });
    } catch (e) {
      alert("Error submitting answers. Please try again.");
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-md mx-auto my-12 glass-card p-6 text-center">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <p className="text-xs text-rose-600 font-semibold mb-4">{error}</p>
        <button
          onClick={() => navigate('/assessments')}
          className="px-4 py-2 rounded-xl bg-primary-600 text-white text-xs font-bold"
        >
          Back to Assessments
        </button>
      </div>
    );
  }

  const questions = testData?.questions || [];
  if (questions.length === 0) {
    return (
      <div className="max-w-md mx-auto my-16 glass-card p-8 text-center space-y-4">
        <AlertCircle className="w-12 h-12 text-amber-500 mx-auto" />
        <h3 className="font-bold text-base text-slate-900 dark:text-white">
          No Questions Available Yet
        </h3>
        <p className="text-xs text-slate-500">
          This assessment does not have any questions registered at the moment. Please select another assessment.
        </p>
        <button
          onClick={() => navigate('/assessments')}
          className="px-4 py-2 rounded-xl bg-primary-600 text-white text-xs font-bold shadow-md shadow-primary-500/20"
        >
          Back to Assessments
        </button>
      </div>
    );
  }
  const currentQ = questions[currentIndex];
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const isTimeWarning = timeLeft < 120; // less than 2 mins

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-16">
      
      {/* Test Control Bar */}
      <div className="glass-card p-4 sm:p-5 flex items-center justify-between sticky top-20 z-30 shadow-md">
        <div>
          <span className="text-[11px] font-bold text-primary-600 uppercase tracking-wider block">
            {testData.category}
          </span>
          <h2 className="font-extrabold text-sm sm:text-base text-slate-900 dark:text-white">
            {testData.title}
          </h2>
        </div>

        <div className="flex items-center gap-3">
          <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-mono text-xs font-bold ${
            isTimeWarning ? 'bg-rose-500 text-white animate-pulse' : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
          }`}>
            <Clock className="w-4 h-4" />
            <span>{String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}</span>
          </div>

          <button
            onClick={submitTest}
            disabled={submitting}
            className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-sm shadow-emerald-500/20 transition-all flex items-center gap-1.5"
          >
            <Send className="w-3.5 h-3.5" />
            {submitting ? 'Submitting...' : 'Submit Test'}
          </button>
        </div>
      </div>

      {/* Question Progress Tracker */}
      <div className="glass-card p-4">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500 mb-2">
          <span>Question {currentIndex + 1} of {questions.length}</span>
          <span className="text-primary-600">
            {Math.round(((currentIndex + 1) / questions.length) * 100)}% Complete
          </span>
        </div>
        <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-primary-600 rounded-full transition-all duration-300"
            style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
          ></div>
        </div>

        {/* Quick jump bubbles */}
        <div className="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800">
          {questions.map((q, idx) => {
            const isAnswered = selectedAnswers[q.id]?.length > 0;
            const isCurrent = idx === currentIndex;
            return (
              <button
                key={q.id}
                onClick={() => setCurrentIndex(idx)}
                className={`w-7 h-7 rounded-lg text-xs font-bold transition-all ${
                  isCurrent
                    ? 'bg-primary-600 text-white ring-2 ring-primary-500/40'
                    : (isAnswered ? 'bg-emerald-500 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400')
                }`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>
      </div>

      {/* Active Question Card */}
      {currentQ && (
        <div className="glass-card p-6 sm:p-8 space-y-6">
          
          <div className="flex items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
            <Badge variant="primary" className="text-xs">
              Difficulty: {currentQ.difficulty}
            </Badge>
            <span className="text-xs font-semibold text-slate-400">
              {currentQ.marks} Mark{currentQ.marks > 1 ? 's' : ''}
            </span>
          </div>

          <div>
            <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-relaxed">
              {currentQ.question_text}
            </h3>

            {/* Optional code snippet */}
            {currentQ.code_snippet && (
              <div className="mt-4 p-4 rounded-xl bg-slate-950 text-emerald-400 font-mono text-xs overflow-x-auto border border-slate-800">
                <pre>{currentQ.code_snippet}</pre>
              </div>
            )}
          </div>

          {/* Options */}
          <div className="space-y-3 pt-2">
            {currentQ.options?.map((opt) => {
              const isSelected = selectedAnswers[currentQ.id]?.includes(opt.id);
              return (
                <div
                  key={opt.id}
                  onClick={() => handleSelectOption(currentQ.id, opt.id)}
                  className={`p-4 rounded-xl border-2 transition-all cursor-pointer flex items-start gap-3 ${
                    isSelected
                      ? 'border-primary-600 bg-primary-50/50 dark:bg-primary-950/40 text-primary-900 dark:text-primary-100'
                      : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white/40 dark:bg-slate-900/40'
                  }`}
                >
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 mt-0.5 ${
                    isSelected ? 'border-primary-600 bg-primary-600 text-white' : 'border-slate-400'
                  }`}>
                    {isSelected && <div className="w-2 h-2 rounded-full bg-white"></div>}
                  </div>
                  <span className="text-xs sm:text-sm font-medium leading-snug">
                    {opt.option_text}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Navigation Buttons */}
          <div className="pt-6 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <button
              onClick={() => setCurrentIndex(prev => Math.max(0, prev - 1))}
              disabled={currentIndex === 0}
              className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40 flex items-center gap-1.5"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Previous
            </button>

            {currentIndex < questions.length - 1 ? (
              <button
                onClick={() => setCurrentIndex(prev => Math.min(questions.length - 1, prev + 1))}
                className="px-5 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white text-xs font-bold shadow-sm flex items-center gap-1.5"
              >
                Next Question <ArrowRight className="w-3.5 h-3.5" />
              </button>
            ) : (
              <button
                onClick={submitTest}
                disabled={submitting}
                className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-sm shadow-emerald-500/20 flex items-center gap-1.5"
              >
                Finish & Submit <Send className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

        </div>
      )}

    </div>
  );
};

export default AssessmentTakePage;
