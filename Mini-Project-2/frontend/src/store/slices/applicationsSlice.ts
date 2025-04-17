import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { JobApplication } from '../../types';

interface ApplicationsState {
  applications: JobApplication[];
  selectedApplication: JobApplication | null;
  loading: boolean;
  error: string | null;
}

const initialState: ApplicationsState = {
  applications: [],
  selectedApplication: null,
  loading: false,
  error: null,
};

const applicationsSlice = createSlice({
  name: 'applications',
  initialState,
  reducers: {
    fetchApplicationsStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchApplicationsSuccess: (state, action: PayloadAction<JobApplication[]>) => {
      state.loading = false;
      state.applications = action.payload;
      state.error = null;
    },
    fetchApplicationsFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    setSelectedApplication: (state, action: PayloadAction<JobApplication>) => {
      state.selectedApplication = action.payload;
    },
    updateApplicationStatus: (state, action: PayloadAction<{ id: number; status: JobApplication['status'] }>) => {
      const application = state.applications.find(app => app.id === action.payload.id);
      if (application) {
        application.status = action.payload.status;
      }
      if (state.selectedApplication?.id === action.payload.id) {
        state.selectedApplication.status = action.payload.status;
      }
    },
  },
});

export const {
  fetchApplicationsStart,
  fetchApplicationsSuccess,
  fetchApplicationsFailure,
  setSelectedApplication,
  updateApplicationStatus,
} = applicationsSlice.actions;

export default applicationsSlice.reducer; 