type Props = {
  title: string,
  description:string,
}

export const LoginTitle:React.FC<Props> = ({title, description}) => {
  return <div className="mb-[24px]">
    <h1 className="font-[Inter] font-medium text-[36px] text-[#000000] tracking-[0.5%]">{title}</h1>
    <p className="text-[#6B7280] text-[16px] font-medium">{description}</p>
  </div>
}