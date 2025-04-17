import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { RootState } from '../store';
import { applications } from '../services/api';
import { JobApplication } from '../types';
import {
  fetchApplicationsStart,
  fetchApplicationsSuccess,
  fetchApplicationsFailure,
} from '../store/slices/applicationsSlice';

const Applications: React.FC = () => {
  const dispatch = useDispatch();
  const { applications: applicationList, loading, error } = useSelector(
    (state: RootState) => state.applications
  );

  useEffect(() => {
    const fetchApplications = async () => {
      dispatch(fetchApplicationsStart());
      try {
        const response = await applications.list();
        dispatch(fetchApplicationsSuccess(response.data));
      } catch (err: any) {
        dispatch(fetchApplicationsFailure(err.response?.data?.message || 'Failed to fetch applications'));
      }
    };

    fetchApplications();
  }, [dispatch]);

  const getStatusColor = (status: JobApplication['status']) => {
    switch (status) {
      case 'P':
        return 'bg-yellow-100 text-yellow-800';
      case 'R':
        return 'bg-blue-100 text-blue-800';
      case 'S':
        return 'bg-green-100 text-green-800';
      case 'RJ':
        return 'bg-red-100 text-red-800';
      case 'H':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: JobApplication['status']) => {
    switch (status) {
      case 'P':
        return 'Pending';
      case 'R':
        return 'Reviewing';
      case 'S':
        return 'Shortlisted';
      case 'RJ':
        return 'Rejected';
      case 'H':
        return 'Hired';
      default:
        return 'Unknown';
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading applications...</p>
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Your Applications</h1>
        <p className="mt-2 text-sm text-gray-600">
          Track the status of your job applications
        </p>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {applicationList.map((application: JobApplication) => (
            <li key={application.id}>
              <Link
                to={`/jobs/${application.job.id}`}
                className="block hover:bg-gray-50"
              >
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-primary-600 truncate">
                        {application.job.title}
                      </p>
                      <p className="mt-1 text-sm text-gray-500">
                        {application.job.location} • {application.job.job_type}
                      </p>
                    </div>
                    <div className="ml-4 flex-shrink-0">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                          application.status
                        )}`}
                      >
                        {getStatusText(application.status)}
                      </span>
                    </div>
                  </div>
                  <div className="mt-2 sm:flex sm:justify-between">
                    <div className="sm:flex">
                      <p className="flex items-center text-sm text-gray-500">
                        Match Score: {application.match_score ? `${application.match_score}%` : 'N/A'}
                      </p>
                    </div>
                    <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                      <p>
                        Applied on{' '}
                        {new Date(application.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Applications; 