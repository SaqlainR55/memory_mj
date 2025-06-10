// src/components/InputBar.tsx
import React from "react";

type Props = {
  input: string;
  setInput: (val: string) => void;
  onSend: () => void;
};

export const InputBar: React.FC<Props> = ({ input, setInput, onSend }) => {
  return (
    <div className="flex p-4 border-t bg-white">
      <input
        className="flex-grow border border-gray-300 rounded-md px-4 py-2 mr-2 focus:outline-none"
        type="text"
        placeholder="Type a message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSend()}
      />
      <button
        onClick={onSend}
        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
      >
        Send
      </button>
    </div>
  );
};
