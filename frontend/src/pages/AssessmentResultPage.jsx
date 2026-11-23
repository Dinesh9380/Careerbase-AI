import React, { useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import confetti from 'canvas-confetti';
import { Award, CheckCircle2, XCircle, ArrowRight, ShieldCheck, Compass, Zap, Activity } from 'lucide-react';
import Badge from '../components/Badge';

const AssessmentResultPage = () => {
  const { id } = useParams();
  const location = useLocation();
  const result = location.state?.result;

  useEffect(() => {
    if (result && result.passed) {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
  }, [result]);

  const scorePct = result ? Math.round(result.percentage) : 85;
  const passed = result ? result.passed : true;
  const accuracy = result ? Math.round(result.accuracy) : 90;

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      
      {/* Result Hero Banner */}
      <div className={`glass-card p-8 text-center border-2 ${
        passed
          ? 'border-emerald-500/40 bg-gradient-to-b from-emerald-50/20 via-white/50 to-white/80 dark:from-emerald-950/20 dark:to-slate-900'
          : 'border-rose-500/40 bg-gradient-to-b from-rose-50/20 via-white/50 to-white/80 dark:from-rose-950/20 dark:to-slate-900'
      }`}>
        
        <div className={`w-16 h-16 rounded-3xl mx-auto flex items-center justify-center mb-4 ${
          passed ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-400' : 'bg-rose-100 text-rose-600 dark:bg-rose-950 dark:text-rose-400'
        }`}>
          {passed ? <Award className="w-9 h-9" /> : <XCircle className="w-9 h-9" />}
        </div>

        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          {passed ? 'Assessment Passed with Distinction!' : 'Assessment Completed — Keep Practicing'}
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-2 max-w-md mx-auto">
          {passed
            ? 'Your performance was analyzed and your verified skill competencies have been automatically updated.'
            : 'Review the identified gaps below and complete recommended roadmap modules to boost your score.'}
        </p>

        {/* Score Metrics */}
        <div className="grid grid-cols-3 gap-4 max-w-lg mx-auto mt-8 pt-6 border-t border-slate-200 dark:border-slate-800">
          <div>
            <div className="text-2xl sm:text-3xl font-extrabold text-primary-600">
              {scorePct}%
            </div>
            <div className="text-[11px] font-semibold text-slate-400 mt-0.5">Overall Score</div>
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-extrabold text-emerald-600">
              {accuracy}%
            </div>
            <div className="text-[11px] font-semibold text-slate-400 mt-0.5">Accuracy</div>
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-extrabold text-indigo-600">
              {passed ? 'PASSED' : 'RETAKE'}
            </div>
            <div className="text-[11px] font-semibold text-slate-400 mt-0.5">Status</div>
          </div>
        </div>

      </div>

      {/* Unlocked Badges */}
      {result?.new_achievements && result.new_achievements.length > 0 && (
        <div className="glass-card p-6 border-amber-300 dark:border-amber-800/60 bg-amber-50/20 dark:bg-amber-950/10">
          <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2 mb-3">
            <Zap className="w-4 h-4 text-amber-500" /> New Achievement Unlocked!
          </h3>
          <div className="flex flex-wrap gap-2">
            {result.new_achievements.map((badge, idx) => (
              <Badge key={idx} variant="warning" className="text-xs px-3 py-1">
                🏆 {badge}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* Skill Scores Updated */}
      <div className="glass-card p-6">
        <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2 mb-4">
          <Activity className="w-4 h-4 text-primary-600" /> Updated Profile Skill Proficiencies
        </h3>

        <div className="space-y-3">
          {Object.entries(result?.skill_scores || { "Python": 85.0, "SQL": 80.0, "Algorithms": 75.0 }).map(([skill, score]) => (
            <div key={skill} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-950/50 border border-slate-200/60 dark:border-slate-800/60">
              <div>
                <span className="font-bold text-xs text-slate-800 dark:text-slate-200">{skill}</span>
                <span className="text-[10px] text-slate-400 block">Adaptive Assessment Benchmark</span>
              </div>
              <div className="text-right">
                <span className="text-sm font-extrabold text-emerald-600 dark:text-emerald-400">
                  {Math.round(score)}%
                </span>
                <span className="text-[10px] text-slate-400 block font-medium">Proficiency</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4">
        <Link
          to="/dashboard"
          className="w-full sm:w-auto px-5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-800 text-center"
        >
          Return to Dashboard
        </Link>
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Link
            to="/careers"
            className="flex-1 sm:flex-none px-5 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-md shadow-primary-500/20 text-center flex items-center justify-center gap-1.5"
          >
            <Compass className="w-3.5 h-3.5" /> View Updated Career Matches
          </Link>
          <Link
            to="/certificates"
            className="flex-1 sm:flex-none px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-500/20 text-center flex items-center justify-center gap-1.5"
          >
            <ShieldCheck className="w-3.5 h-3.5" /> Mint Certificate
          </Link>
        </div>
      </div>

    </div>
  );
};

export default AssessmentResultPage;
