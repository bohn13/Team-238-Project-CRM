import type { Patient } from "@/types/patient";
import { createSlice } from "@reduxjs/toolkit";
import { createPatientThunk } from "./thunk/createPatientThunk";
import { getAllPatientThunk } from "./thunk/getAllPacientThunk";

interface PatientsState {
  patients: Patient[];
  selectedPatient: Patient | null;

  loading: boolean;
  error: string | null;

  total: number;

  
}
const initialState: PatientsState = {
  patients: [],
  selectedPatient: null,
  total: 0,
  loading: false,
  error:null,
  
}

const patientsSlice = createSlice({
  name: "patient",
  initialState,
  reducers: {

    
  },
  extraReducers: (builder) => {
    builder
      .addCase(createPatientThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(createPatientThunk.fulfilled, state => {
        state.loading = false;
      })
      .addCase(createPatientThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? 'failed to create patient'
      })
      .addCase(getAllPatientThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(getAllPatientThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.patients = action.payload
      })
      .addCase(getAllPatientThunk.rejected, (state) => {
        state.loading = false;
    })
    
  }
})
export default patientsSlice.reducer;