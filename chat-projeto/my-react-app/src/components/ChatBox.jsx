import { ChevronLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import foto from "../img/fotoDePerfil.jpg";
import robo from "../img/fotorobo.jpg";
import {useMediaQuery} from '@mui/material'

 

function ChatBox({ mensagens = [], nome = "", typing = false, scrollMensagemRef }) {
   const navigate = useNavigate();
   const isMobile = useMediaQuery("(max-width: 600px)");
  const mensagensOrdenadas = [...mensagens].sort(
  (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
);
  return (
    
    <div className="flex-1 overflow-y-auto">
      <header 
     
      className= {`flex justify-between  items-center fixed top-0 w-full  left-0 bg-sky-600 ${isMobile ?  "p-2" : "p-6"

      }`}>
        <div className="flex items-center gap-2">
          <img
           src={foto} 
           alt="um foto que o usuario irá poder colocar caso ele queira" 
           title="sua foto" 
           className="w-10 h-10 rounded-full object-cover"/>

          <h1 className="">{nome}</h1>

        </div>

        <button onClick={() => navigate("/")}>
          <ChevronLeft />
        </button>
        
      </header>

      <main className= {` space-y-4 ${isMobile ? "pt-15 " : "pt-20  p-4"

      } `}>
        {/*pega as listas de mensagens*/}{" "}

        {mensagensOrdenadas.map((msg, index) => (
          msg.user && (
            
          <div
           key={index} 
           className={`flex flex-col ${
              msg.user ==="atendente" ? "items-start": "items-end"
           }`}
           >
           
           <div className="flex items-center space-x-4"> 
            {msg.user === "atendente" && (
            <img 
            src={robo} 
            alt="uma imagem de um robo" 
            className="w-10 h-10 rounded-xl object-cover"
            />
            )}
               
              
           <p
  className={`p-4 rounded-xl whitespace-pre-wrap break-words break-all text-left
    max-w-full overflow-hidden ${
      isMobile ? "text-sm max-w-[90%]" : "text-base max-w-[50%]"
    } ${
      msg.user === "atendente"
        ? "bg-slate-300 text-black"
        : "bg-blue-900 text-white"
    }`}
>
  {msg.msg}
</p>
            </div>
          </div>
          )
        ))}

         {typing && (
                <div>
                  <p className=" w-10 h-8 text-sm text-center animate-pulse bg-slate-300 p-3 m-2 rounded-xl ">
                     ...
                  </p>
                  </div>
               )}

               <div className={`${isMobile ? "h-15" : "h-8"} outline-none focus:outline-none`} 
               style={{backgroundColor: "transparent"}}
               ></div> {/*faz aparecer a ultima mensagem que ficaria escondida atras do input e button*/}

        <div ref={scrollMensagemRef}></div> {/*rebece a lista do App*/}

        
      </main>
    </div>
  );
}

export default ChatBox;
