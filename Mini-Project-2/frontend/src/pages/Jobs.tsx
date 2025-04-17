import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { RootState } from '../store';
import { fetchJobsStart, fetchJobsSuccess, fetchJobsFailure, setFilters } from '../store/slices/jobsSlice';
import { jobs } from '../services/api';
import { Job } from '../types';

const Jobs: React.FC = () => {
  const dispatch = useDispatch();
  const { jobs: jobList, loading, error, filters } = useSelector((state: RootState) => state.jobs);
  const [searchParams, setSearchParams] = useState({
    title: '',
    location: '',
    job_type: '',
    experience_level: '',
    skills: [] as string[],
  });

  useEffect(() => {
    const fetchJobs = async () => {
      dispatch(fetchJobsStart());
      try {
        const response = await jobs.list(filters);
        dispatch(fetchJobsSuccess(response.data));
      } catch (err: any) {
        dispatch(fetchJobsFailure(err.response?.data?.message || 'Failed to fetch jobs'));
      }
    };

    fetchJobs();
  }, [dispatch, filters]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(setFilters(searchParams));
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSkillsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    const skills = value.split(',').map((skill) => skill.trim());
    setSearchParams((prev) => ({ ...prev, skills }));
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Find Your Next Job</h1>
        <p className="mt-2 text-sm text-gray-600">
          Browse through our latest job opportunities
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Job Title
              </label>
              <input
                type="text"
                name="title"
                id="title"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={searchParams.title}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                Location
              </label>
              <input
                type="text"
                name="location"
                id="location"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={searchParams.location}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="job_type" className="block text-sm font-medium text-gray-700">
                Job Type
              </label>
              <select
                name="job_type"
                id="job_type"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={searchParams.job_type}
                onChange={handleInputChange}
              >
                <option value="">All Types</option>
                <option value="FT">Full Time</option>
                <option value="PT">Part Time</option>
                <option value="CT">Contract</option>
                <option value="IN">Internship</option>
                <option value="RM">Remote</option>
              </select>
            </div>
            <div>
              <label htmlFor="experience_level" className="block text-sm font-medium text-gray-700">
                Experience Level
              </label>
              <select
                name="experience_level"
                id="experience_level"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={searchParams.experience_level}
                onChange={handleInputChange}
              >
                <option value="">All Levels</option>
                <option value="EN">Entry Level</option>
                <option value="JR">Junior</option>
                <option value="MD">Mid Level</option>
                <option value="SR">Senior</option>
                <option value="LD">Lead</option>
                <option value="MG">Manager</option>
              </select>
            </div>
            <div>
              <label htmlFor="skills" className="block text-sm font-medium text-gray-700">
                Skills (comma separated)
              </label>
              <input
                type="text"
                name="skills"
                id="skills"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={searchParams.skills.join(', ')}
                onChange={handleSkillsChange}
              />
            </div>
          </div>
          <div className="flex justify-end">
            <button
              type="submit"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Search Jobs
            </button>
          </div>
        </form>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading jobs...</p>
        </div>
      ) : error ? (
        <div className="text-center py-12">
          <p className="text-red-600">{error}</p>
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {jobList.map((job: Job) => (
            <Link
              key={job.id}
              to={`/jobs/${job.id}`}
              className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300"
            >
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg font-medium text-gray-900">{job.title}</h3>
                <p className="mt-1 text-sm text-gray-500">{job.location}</p>
                <div className="mt-2 flex items-center text-sm text-gray-500">
                  <span className="mr-2">{job.job_type}</span>
                  <span>•</span>
                  <span className="ml-2">{job.experience_level}</span>
                </div>
                <div className="mt-4">
                  <div className="flex flex-wrap gap-2">
                    {job.skills_required.map((skill, index) => (
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
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default Jobs; 