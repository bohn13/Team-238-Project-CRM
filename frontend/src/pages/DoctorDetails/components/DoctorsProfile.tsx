import type { Doctor } from "@/types/doctor"

type Props = {
  selectedDoctor:Doctor
}
export const DoctorsProfile:React.FC<Props> = ({ selectedDoctor }) => {
  return (<>  <div className="flex items-center gap-5">
            <img
              src={selectedDoctor.avatarUrl ?? undefined}
              alt="Doctor"
              className="h-20 w-20 rounded-full bg-amber-300 object-cover"
            />

            <div>
              <div className="mb-2 flex items-center gap-3">
                <h1 className="text-2xl font-semibold">
                  Dr. {selectedDoctor?.firstName} {selectedDoctor?.lastName}
                </h1>

                <span className="rounded-md bg-teal-100 px-3 py-1 text-sm font-medium text-teal-700">
                  {selectedDoctor?.employmentType}
                </span>
              </div>

              <p className="mb-3 text-gray-600">
                {selectedDoctor?.specialization}
              </p>

              <div className="flex gap-8 text-sm text-gray-500">
                <span>{selectedDoctor?.phoneNumber}</span>

                <span>{selectedDoctor?.email}</span>
              </div>
            </div>
          </div>

          

          <div className="w-[320px]">
            <div className="mb-2 flex justify-between text-sm">
              <span className="font-medium">Workload</span>

              <span>80%</span>
            </div>

            <div className="h-2 overflow-hidden rounded-full bg-gray-200">
              <div className="h-full w-[80%] rounded-full bg-[#EF4444]"></div>
            </div>
          </div></>)
}