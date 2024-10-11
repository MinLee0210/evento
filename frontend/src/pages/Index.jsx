import { useNavigate } from "react-router-dom"
export default function Index() {

  const navigate = useNavigate();

  const teamMembers = [
    { name: "Lê Đức Minh", image: "/assets/avt/Lê Đức Minh.jpg" },
    { name: "Ngọc Huyền", image: "/assets/avt/Ngọc Huyền.png" },
    { name: "Vũ Hoàng Phát", image: "/assets/avt/Vũ Hoàng Phát.png" },
    { name: "Vân Anh", image: "/assets/avt/Vân Anh.jpg" },
    { name: "Phạm Nguyễn Quốc Huy", image: "/assets/avt/Quốc Huy.jpg" },
  ]

  return (
    <div className="flex flex-col items-center min-h-screen bg-customBlue">
      <div className="relative w-full max-w-[1300px]">
        <img
          src="/assets/banner/AIC2024-Banner website.png"
          alt="AIC2024 Banner"
          width={1300}
          height={650}
          className="object-cover w-full h-auto"
        />
        
        <div className=" left-1/2 top-[500px] transform items-center justify-center -translate-y-1/2 w-full ">
          <div className="flex items-center p-2 bg-white shadow-xl">
            <div className="flex flex-shrink-0 mr-4 ">
              <img
                src="/assets/banner/Logo_PTIT_University.png"
                alt="PTIT University Logo"
                width={50}
                height={50}
                className="object-contain md:w-24 md:h-24"
              />
            </div>
            <div className="flex flex-col">
              <span className="font-semibold text-black md:text-xl">Team: AIO_Top10</span>
              <span className="text-gray-700 md:text-lg">
                Học Viện Công Nghệ Bưu Chính Viễn Thông Cơ Sở tại TP.Hồ Chí Minh
              </span>
            </div>
            <button
              className="px-4 py-2 ml-auto mr-20 w-[150px] max-w-[200px] font-semibold text-white transition 
                duration-300 ease-in-out bg-blue-500 rounded-lg shadow-md hover:bg-blue-600 hover:shadow-lg
                focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
              onClick={() => navigate("/search")} 
            >
              Bắt đầu
            </button>

          </div>
        </div>
      </div>

      <div className="w-full max-w-[1300px] bg-white">
        <div className="py-8">
          <h2 className="mb-6 text-2xl font-bold text-center">Our Team</h2>
          <div className="flex flex-wrap justify-center gap-4">
            {teamMembers.map((member, index) => (
              <div key={index} className="text-center">
                <img
                  src={member.image}
                  alt={member.name}
                  width={200}
                  height={200}
                  className="object-cover rounded-full"
                />
                <p className="mt-2 font-medium">{member.name}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}