import axios from 'axios';
import { User, Job, JobApplication, Resume, ResumeAnalysis, ResumeFeedback } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const auth = {
  login: (credentials: { username: string; password: string }) =>
    api.post<{ user: User; token: string }>('/auth/login/', credentials),
  register: (data: {
    username: string;
    email: string;
    password: string;
    role: User['role'];
  }) => api.post<{ user: User; token: string }>('/auth/register/', data),
};

// Job endpoints
export const jobs = {
  list: (params?: {
    job_type?: string;
    experience_level?: string;
    location?: string;
    skills?: string[];
  }) => api.get<Job[]>('/jobs/', { params }),
  create: (data: Omit<Job, 'id' | 'recruiter' | 'created_at' | 'updated_at'>) =>
    api.post<Job>('/jobs/', data),
  retrieve: (id: number) => api.get<Job>(`/jobs/${id}/`),
  update: (id: number, data: Partial<Job>) =>
    api.patch<Job>(`/jobs/${id}/`, data),
  delete: (id: number) => api.delete(`/jobs/${id}/`),
  search: (params: {
    title?: string;
    location?: string;
    job_type?: string;
    experience_level?: string;
    skills?: string[];
    salary_min?: number;
    salary_max?: number;
  }) => api.post<Job[]>('/jobs/search/', params),
};

// Application endpoints
export const applications = {
  list: () => api.get<JobApplication[]>('/applications/'),
  create: (data: {
    job: number;
    resume: number;
    cover_letter: string;
  }) => api.post<JobApplication>('/applications/', data),
  retrieve: (id: number) => api.get<JobApplication>(`/applications/${id}/`),
  update: (id: number, data: { status: JobApplication['status'] }) =>
    api.patch<JobApplication>(`/applications/${id}/`, data),
};

// Resume endpoints
export const resumes = {
  list: () => api.get<Resume[]>('/resumes/'),
  create: (data: FormData) =>
    api.post<Resume>('/resumes/', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  retrieve: (id: number) => api.get<Resume>(`/resumes/${id}/`),
  delete: (id: number) => api.delete(`/resumes/${id}/`),
  analysis: (id: number) => api.get<ResumeAnalysis>(`/resumes/${id}/analysis/`),
  feedback: (id: number) => api.get<ResumeFeedback[]>(`/resumes/${id}/feedback/`),
};

// Saved jobs endpoints
export const savedJobs = {
  list: () => api.get<Job[]>('/saved-jobs/'),
  create: (jobId: number) => api.post('/saved-jobs/', { job: jobId }),
  delete: (jobId: number) => api.delete(`/saved-jobs/${jobId}/`),
};

export default api; 