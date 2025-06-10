// src/components/MessageBubble.tsx
import React from "react";

type Props = {
  sender: "user" | "mj";
  text: string;
};

export const MessageBubble: React.FC<Props> = ({ sender, text }) => {
  return (
    <div className={`flex ${sender === "user" ? "justify-end" : "justify-start"} mb-2`}>
      <div
        className={`px-4 py-2 rounded-lg max-w-xs ${
          sender === "user" ? "bg-blue-600 text-white" : "bg-gray-300 text-black"
        }`}
      >
        {text}
      </div>
    </div>
  );
};