import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { resumes } from '../services/api';
import { Resume, ResumeAnalysis, ResumeFeedback } from '../types';

const ResumeAnalysis: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [resume, setResume] = useState<Resume | null>(null);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [feedbacks, setFeedbacks] = useState<ResumeFeedback[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resumeResponse, analysisResponse, feedbacksResponse] = await Promise.all([
          resumes.retrieve(Number(id)),
          resumes.analysis(Number(id)),
          resumes.feedback(Number(id))
        ]);
        setResume(resumeResponse.data);
        setAnalysis(analysisResponse.data);
        setFeedbacks(feedbacksResponse.data);
        setLoading(false);
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to fetch resume analysis');
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">{resume?.title}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold mb-2">Overall Score</h3>
            <div className="text-4xl font-bold text-primary-600">
              {analysis?.overall_score.toFixed(1)}%
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Skills</h3>
            <div className="flex flex-wrap gap-2">
              {analysis?.skills.map((skill, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Feedback</h3>
        <div className="space-y-4">
          {feedbacks.map((feedback) => (
            <div
              key={feedback.id}
              className={`p-4 rounded-lg ${
                feedback.severity === 'high'
                  ? 'bg-red-50 border border-red-200'
                  : feedback.severity === 'medium'
                  ? 'bg-yellow-50 border border-yellow-200'
                  : 'bg-blue-50 border border-blue-200'
              }`}
            >
              <div className="flex items-center mb-2">
                <span
                  className={`text-sm font-medium ${
                    feedback.severity === 'high'
                      ? 'text-red-800'
                      : feedback.severity === 'medium'
                      ? 'text-yellow-800'
                      : 'text-blue-800'
                  }`}
                >
                  {feedback.feedback_type === 'skill_gap'
                    ? 'Skill Gap'
                    : feedback.feedback_type === 'formatting'
                    ? 'Formatting'
                    : 'ATS Optimization'}
                </span>
                <span
                  className={`ml-2 px-2 py-1 text-xs font-medium rounded-full ${
                    feedback.severity === 'high'
                      ? 'bg-red-100 text-red-800'
                      : feedback.severity === 'medium'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-blue-100 text-blue-800'
                  }`}
                >
                  {feedback.severity.charAt(0).toUpperCase() + feedback.severity.slice(1)}
                </span>
              </div>
              <p className="text-sm text-gray-700">{feedback.message}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ResumeAnalysis; 