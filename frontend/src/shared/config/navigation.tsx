import { CiHome } from "react-icons/ci";
import { PiChatDotsLight } from "react-icons/pi";
import { CiUser } from "react-icons/ci";
import { ROUTES } from "./routes";
import { CiStethoscope } from "react-icons/ci";
import { PiHandshakeLight } from "react-icons/pi";
import { CiCalendar } from "react-icons/ci";
export const navigation = [
  {
    title: "Dashboard",
    path: ROUTES.DASHBOARD,
    icon: <CiHome />,
  },
  {
    title: "Reminder",
    path: ROUTES.REMINDER,
    icon: <PiChatDotsLight />,
  },
  {
    title: "Patients",
    path: ROUTES.PATIENT,
    icon: <CiUser />,
  },
  {
    title: "Doctors",
    path: ROUTES.DOCTORS,
    icon: <CiStethoscope />,
  },
  {
    title: "Appointments",
    path: ROUTES.APPOINTMENTS,
    icon: <PiHandshakeLight />,
  },
  {
    title: "Calendar",
    path: ROUTES.CALENDAR,
    icon: <CiCalendar />,
  },
];
