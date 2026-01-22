import { useEffect, useState, useRef } from "react";
import ChatBox from "./components/ChatBox";
import ChatInput from "./components/ChatInput";
import { useMediaQuery } from "@mui/material";
import "./App.css";

function App() {
  const scrollMensagemRef = useRef(null);
  const [typing, setTyping] = useState(false);
  const [mensagens, setMensagens] = useState([]);
  const [nome, setNome] = useState("");

  const isMobile = useMediaQuery("(max-width:500px)");

  // Carrega só o nome do localStorage
  useEffect(() => {
    const nomeSalvo = localStorage.getItem("nome");
    if (nomeSalvo) {
      setNome(nomeSalvo);
    }
  }, []);

  // Busca histórico REAL no backend (1 vez ao entrar)
  useEffect(() => {
    if (!nome) return;

    fetch(`http://localhost:5000/mensagens/allMesages`)
      .then((res) => res.json())
      .then((data) => {
        const msgsDoUsuario = data.filter(
          (msg) => msg.user === nome || msg.to === nome
        );
      setMensagens(
        msgsDoUsuario.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt))
      );
      })
      .catch((err) => console.error("Erro ao carregar histórico:", err));
  }, [nome]);

  // Scroll automático
  useEffect(() => {
    scrollMensagemRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [mensagens]);

  // ENVIA MENSAGEM
  async function onclickbutton(textoDigitado) {
    const novaMensagem = {
      user: nome,
      msg: textoDigitado,
      to: "atendente",
    };

    // Adiciona no frontend imediatamente
    setMensagens((prev) => [...prev, novaMensagem]);

    try {
      // Salva no backend
      await fetch("http://localhost:5000/mensagens/allMesages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(novaMensagem),
      });

      // BOT só responde na primeira mensagem
      if (mensagens.length === 0) {
        setTyping(true);

        setTimeout(async () => {
          const botMsg = {
            user: "atendente",
            msg: `Oi ${nome}, como posso te ajudar?`,
            to: nome,
          };

          // Adiciona no frontend
          setMensagens((prev) => [...prev, botMsg]);

          // Salva no backend
          await fetch("http://localhost:5000/mensagens/allMesages", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(botMsg),
          });

          setTyping(false);
        }, 1000);
      }
    } catch (err) {
      console.error("Erro ao enviar mensagem:", err);
    }
  }

  return (
    <div
      className={`w-screen h-screen flex flex-col bg-sky-100 ${
        isMobile ? "p-2" : "p-6"
      }`}
    >
      <ChatBox
        mensagens={mensagens}
        nome={nome}
        typing={typing}
        scrollMensagemRef={scrollMensagemRef}
         isMobile={isMobile}
      />

      <ChatInput onSend={onclickbutton} />
    </div>
  );
}

export default App;