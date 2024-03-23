import { useEffect, useRef, useState } from "react";
import { ReactComponent as SendIcon } from "../../../assets/svg/send.svg";

type Props = {
  onSendMessage?: (message: string) => boolean;
};

const Input = ({ onSendMessage }: Props) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [inputText, setInputText] = useState("");

  const messageText = inputText.trim();

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSendMessage = () => {
    if (messageText && onSendMessage) {
      if (onSendMessage(messageText)) {
        // Clear input and focus
        setInputText("");
        inputRef.current?.focus();
      }
    }
  };

  return (
    <div className="flex gap-3 px-4 py-5 border-t rounded-t-2xl">
      <input
        ref={inputRef}
        type="text"
        className="flex-1 px-4 py-3 text-base border outline-none rounded-3xl focus:bg-primary/5"
        placeholder="Message DiaBuddy..."
        onKeyDown={(e) => {
          e.key === "Enter" && handleSendMessage();
        }}
        onChange={(e) => {
          setInputText(e.target.value);
        }}
        value={inputText}
      />
      <button
        disabled={!messageText}
        type="button"
        className={`flex justify-center p-2 rounded-full outline-none text-white *:size-10 ${
          messageText ? "hover:bg-primary/5 *:fill-primary" : "*:fill-gray-400"
        }`}
        title="Send"
        onClick={handleSendMessage}
      >
        <SendIcon className="" />
      </button>
    </div>
  );
};

export default Input;
