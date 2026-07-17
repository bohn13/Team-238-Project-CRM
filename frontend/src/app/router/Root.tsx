import { HashRouter, Navigate, Route, Routes } from "react-router-dom";
import { App } from "../App";
import { LoginPage } from "../../pages/LoginPage/LoginPage";

import { ProtectedRoute } from "@/components/protectRoutes/ProtectedRoutes";
import { DoctorsPage } from "@/pages/Doctor/DoctorsPage";
import { DashboardPage } from "@/pages/Dashboard/DashboardPage";
import { ReminderPage } from "@/pages/Reminder/ReminderPage";
import { PatientsPage } from "@/pages/Patient/PatientsPage";
import { AppointmentsPage } from "@/pages/Appointments/AppointmentsPage";
import { CalendarPage } from "@/pages/Calendar/CalendarPage";
import { ROUTES } from "@/shared/config/routes";
import { ActivatePage } from "@/pages/Activation/ActivatePage";
import { DoctorDetailsPage } from "@/pages/DoctorDetails/DoctorDetailsPage";



export const Root: React.FC = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path={ROUTES.LOGIN} element={<LoginPage />} />
<Route path={ROUTES.ACTIVATE} element={<ActivatePage/>}/>
        <Route path="/" element={<App />}>
          
          <Route element={<ProtectedRoute />}>
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
            <Route path={ROUTES.REMINDER} element={<ReminderPage />} />
            <Route path={ROUTES.PATIENT} element={<PatientsPage />} />
            <Route path={ROUTES.DOCTORS} element={<DoctorsPage />} />
            <Route path={ROUTES.DETAILS} element={<DoctorDetailsPage/>}/>
            <Route path={ROUTES.APPOINTMENTS} element={<AppointmentsPage/>} />
            <Route path={ROUTES.CALENDAR} element={<CalendarPage/>} />
          </Route>
        </Route>
      </Routes>
    </HashRouter>
  );
};
