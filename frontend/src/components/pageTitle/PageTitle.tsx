
type Props = {
  text: string;
  description?: string |  null;
}

export const PageTitle: React.FC<Props> = ({ text, description }) => {
  return <div >
    <h1 className="font-[Inter] font-semibold text-[24px] text-[#1F2937] tracking-[0.5%]">{text}</h1>
    <p className="text-[#6B7280] text-[16px] font-medium">{description}</p>
  </div>
}