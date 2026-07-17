export const RevenueChart = () => {
  return (
    <div className="w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
      <iframe
        title="Revenue Dashboard"
        src="https://public.tableau.com/views/weeklyrevenue_17836247142510/REVENUE?:showVizHome=no"
        className="h-[900px] w-full"
        frameBorder={0}
        allowFullScreen
      />
    </div>
  );
};