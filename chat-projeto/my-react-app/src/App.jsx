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

    fetch(`https://miniature-acorn-7vj9q469wgpfxx6v-5174.app.github.dev/mensagens/allMessages`)
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
  const payload = {
    user: nome,
    msg: textoDigitado
  };

  setTyping(true);

  try {
    const response = await fetch(
      "https://miniature-acorn-7vj9q469wgpfxx6v-5174.app.github.dev/mensagens/ask",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }
    );

    const data = await response.json();

    if (data.userMessage && data.botMessage) {
      setMensagens((prev) => [
        ...prev,
        data.userMessage,
        data.botMessage
      ]);
    }

  } catch (err) {
    console.error("Erro ao conversar com o bot:", err);
  } finally {
    setTyping(false);
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