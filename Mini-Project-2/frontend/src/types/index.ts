export interface User {
  id: number;
  username: string;
  email: string;
  role: 'applicant' | 'recruiter';
  first_name?: string;
  last_name?: string;
}

export interface Job {
  id: number;
  title: string;
  description: string;
  requirements: string;
  location: string;
  salary_min?: number;
  salary_max?: number;
  job_type: 'FT' | 'PT' | 'CT' | 'IN' | 'RM';
  experience_level: 'EN' | 'JR' | 'MD' | 'SR' | 'LD' | 'MG';
  skills_required: string[];
  is_active: boolean;
  recruiter: User;
  created_at: string;
  updated_at: string;
}

export interface JobApplication {
  id: number;
  job: Job;
  applicant: User;
  resume: Resume;
  cover_letter: string;
  status: 'P' | 'R' | 'S' | 'RJ' | 'H';
  match_score?: number;
  created_at: string;
  updated_at: string;
}

export interface JobMatch {
  id: number;
  job: Job;
  resume: Resume;
  match_score: number;
  skills_match: string[];
  experience_match: boolean;
  education_match: boolean;
  created_at: string;
  updated_at: string;
}

export interface Resume {
  id: number;
  user: User;
  title: string;
  file: string;
  created_at: string;
  updated_at: string;
}

export interface ResumeAnalysis {
  id: number;
  resume: Resume;
  skills: string[];
  experience: string[];
  education: string[];
  overall_score: number;
  created_at: string;
  updated_at: string;
}

export interface ResumeFeedback {
  id: number;
  resume: Resume;
  feedback_type: 'skill_gap' | 'formatting' | 'ats';
  message: string;
  severity: 'low' | 'medium' | 'high';
  created_at: string;
}

export interface SavedJob {
  id: number;
  user: User;
  job: Job;
  created_at: string;
} 