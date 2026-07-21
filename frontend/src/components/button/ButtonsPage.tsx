
 type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
   children: React.ReactNode;
   icon?: React.ReactNode;
   onClick?: () => void;
   className?: string;
   
   
  }
export const ButtonPage: React.FC<Props> = ({
  children,
  icon,
  className,
  ...props
}) => {
  return (
    <button
      className={`
        
        h-[36px]
        flex
        justify-center
        items-center
        rounded-[8px]
         border border-[#9CA3AF]
        bg-[#172554]
        text-[#FFFFFF]
        cursor-pointer
        ${className ?? ""}
      `}
      {...props}
    >
      {icon}
      {children}
    </button>
  );
};