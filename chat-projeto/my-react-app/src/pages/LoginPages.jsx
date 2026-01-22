import { useNavigate } from "react-router-dom";
import { useState } from "react";

function LoginPages() {
   const [nome, setNome] = useState("");
     
    const handleChange = (event) => {
      setNome(event.target.value)
    }

  const navigate = useNavigate()
  
    const handleLoginClick = () => {
    localStorage.setItem("nome", nome);
      navigate('/chat')
    }

  
  return (
    <div className=" w-screen h-screen  flex itens-center justify-center bg-sky-900 p-6">
      <div className="  w-85 h-100 bg-sky-200 rounded-md p-6  space-y-25">
        <input
        type="text"
        placeholder="coloque o seu nome"
        value={nome}
        onChange={handleChange}
        className="mr-2 bg-slate-100 p-2 rounded-md w-75 border "/>

        <button 
         onClick={()=> {
        if(!nome.trim()) {
          return alert("Digite o seu nome"); 
        } 
         handleLoginClick ();
          }}
        className="bg-slate-300 p-2 rounded-md w-75 border">Entrar</button>
        
        </div>
      
    </div>
  );
}

export default LoginPages;
