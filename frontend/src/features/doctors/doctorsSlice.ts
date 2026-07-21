import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { Doctor } from "@/types/doctor";
import type { DoctorQuery } from "./model/DoctorQuery";

import { updateDoctorThunk } from "./thunk/updateDoctorThunk";
import { createDoctorThunk } from "./thunk/createDoctorThunk";
import { getAllDoctorsThunk } from "./thunk/getAllDoctorsThunk";
import { getDoctorByIdThunk } from "./thunk/getDoctorByIdThunk";
import { removeDoctorThunk } from "./thunk/removeDoctorThunk";

interface DoctorsState {
  doctors: Doctor[];
  selectedDoctor: Doctor | null;

  loading: boolean;
  error: string | null;

  total: number;

  query: DoctorQuery;
}

const initialState: DoctorsState = {
  doctors: [],
  selectedDoctor: null,

  loading: false,
  error: null,

  total: 0,

  query: {
    search: "",
    specialization: "",
    employmentType: "",
    sortBy: "name",
    sortOrder: "asc",
    page: 1,
    pageSize: 5,
  },
};

const doctorSlice = createSlice({
  name: "doctor",
  initialState,

  reducers: {
    setQuery(state, action: PayloadAction<Partial<DoctorQuery>>) {
      state.query = {
        ...state.query,
        ...action.payload,
      };
    },

    resetQuery(state) {
      state.query = initialState.query;
    },

    setSelectedDoctor(state, action: PayloadAction<Doctor | null>) {
      state.selectedDoctor = action.payload;
    },
  },

  extraReducers: (builder) => {
    builder

      .addCase(createDoctorThunk.pending, (state) => {
        state.loading = true;
        state.error = null;
      })

      .addCase(createDoctorThunk.fulfilled, (state) => {
        state.loading = false;
      })

      .addCase(createDoctorThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to create doctor";
      })

      .addCase(getAllDoctorsThunk.pending, (state) => {
        state.loading = true;
        state.error = null;
      })

      .addCase(getAllDoctorsThunk.fulfilled, (state, action) => {
        state.loading = false;

        state.doctors = action.payload.items;
        state.total = action.payload.total;
      })

      .addCase(getAllDoctorsThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to load doctors";
      });
    builder
      .addCase(getDoctorByIdThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(getDoctorByIdThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedDoctor = action.payload;
      })
      .addCase(getDoctorByIdThunk.rejected, (state) => {
        state.loading = false;
      })
      .addCase(updateDoctorThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateDoctorThunk.fulfilled, (state, action) => {
        state.loading = false;
        
        state.selectedDoctor = action.payload;
      })
      .addCase(updateDoctorThunk.rejected, (state) => {
        state.loading = false;
      })
      .addCase(removeDoctorThunk.pending, state => {
        state.loading = true;
      })
    .addCase(removeDoctorThunk.fulfilled, (state, action) => {
       state.loading = false;

        state.doctors = state.doctors.filter(
        doctor => doctor.id !== action.payload
  );

  if (state.selectedDoctor?.id === action.payload) {
      state.selectedDoctor = null;
  }
    })
      .addCase(removeDoctorThunk.rejected, state => {
        state.loading = false;
      });
  },
});

export const { setQuery, resetQuery, setSelectedDoctor } = doctorSlice.actions;

export default doctorSlice.reducer;
