import { useState } from "react";
import { MessageBubble } from "./components/MessageBubble";
import { InputBar } from "./components/InputBar";

function App() {
  const [messages, setMessages] = useState<{ sender: "user" | "mj"; text: string }[]>([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user" as const, text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "saqlain55", // can be dynamic in future
          message: input,
        }),
      });

      const data = await res.json();

      const mjReply = {
        sender: "mj" as const,
        text: data.response || "MJ had no reply.",
      };

      setMessages((prev) => [...prev, mjReply]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          sender: "mj" as const,
          text: "⚠️ MJ server is offline or unreachable.",
        },
      ]);
    }
  };


  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="flex-grow overflow-y-auto p-4">
        
        {messages.map((msg, i) => (
          <MessageBubble key={i} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <InputBar input={input} setInput={setInput} onSend={handleSend} />
    </div>
  );

}

export default App;