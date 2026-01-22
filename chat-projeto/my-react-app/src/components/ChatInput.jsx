import { SendHorizontal } from "lucide-react";
import { useState } from "react";
import {useMediaQuery} from '@mui/material';


function ChatInput(props) {
  const [mensagens, setMensagens] = useState(""); // cria um estato no ChatInput

  const onciclkbutton = () => {
    props.onSend(mensagens); // manda as mensagens para o app
    setMensagens(""); 
  };

  const handleChange = (event) => {
    setMensagens(event.target.value);
   };  // ele recebe o evento do input e atualiza as mensagens

   const isMobile = useMediaQuery('(max-width:500px)');
   

   
  return (
    <div className="fixed bottom-0 left-0 w-full p-6 bg-sky-100 rounded-md shadow flex items-center gap-2  ">
      <input
        type="text"
        value={mensagens}
       onChange={handleChange}
        placeholder="Digite a sua mensagem "
        className={` bg-blue-300 p-2 rounded-md text-white w-full ${isMobile ? "mr-1" : "mr-2"}` }
      />
      <button
        onClick={()=> {
        if(!mensagens.trim()) {
          return alert("Por favor, coloque uma mensagem"); 

        }
        onciclkbutton();
      }}
        className="bg-blue-300 p-1 rounded-md text-white  items-center justify-center flex "
      >
        <SendHorizontal size={30} />
      </button>
    </div>
  );

}

export default ChatInput;
