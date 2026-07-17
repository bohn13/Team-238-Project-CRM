
type Props = {
bgColor?:string,
  rotate?: string,
  width: string,
  height: string,
  ml?: string,
  mb?:string,
  radiusTL: string,
  radiusTR: string,
  radiusBR: string,
  radiusBL: string,
  image?:string,

}

export const Rectangle: React.FC<Props> = ({
  width, height,rotate,mb,ml,radiusBL,radiusBR,radiusTL,radiusTR, image, bgColor
}) => {
  return (
    <div className=" bg-cover bg-center bg-no-repeat "
      style={{
        width: width,
        height: height,
        marginBottom: mb,
        marginLeft: ml,
        backgroundColor:bgColor,
        borderTopLeftRadius: radiusTL,
        borderTopRightRadius: radiusTR,
        borderBottomRightRadius: radiusBR,
        borderBottomLeftRadius: radiusBL,
        ...(image && {
    backgroundImage: `url(${image})`,
  }),
        transform: rotate ? `rotate(-${rotate})` : undefined,
       
    }}></div>
  )
}