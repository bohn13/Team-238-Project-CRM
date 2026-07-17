

export interface DoctorQuery {
  search: string;
  specialization: string;
  employmentType:"full_time" | "part_time";

  sortBy: "name" | "specialization" | "years_experience" | "created_at";

  sortOrder: "asc" | "desc";

  page: number;
  pageSize: number;
}