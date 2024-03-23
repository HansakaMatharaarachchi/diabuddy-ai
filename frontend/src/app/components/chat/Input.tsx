import { useEffect, useRef } from "react";
import { ReactComponent as SendIcon } from "../../../assets/svg/send.svg";

type Props = {
  onSendMessage?: (message: string) => boolean;
};

const Input = ({ onSendMessage }: Props) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSendMessage = () => {
    if (inputRef.current) {
      const newMessage = inputRef.current.value?.trim();

      if (onSendMessage && newMessage) {
        if (onSendMessage(newMessage)) {
          // Clear input and focus
          inputRef.current.value = "";
          inputRef.current.focus();
        }
      }
    }
  };

  return (
    <div className="flex gap-3 px-4 py-5 border-t rounded-t-2xl">
      <input
        type="text"
        className="flex-1 px-4 py-3 text-base border outline-none rounded-3xl focus:bg-primary/5"
        placeholder="Message DiaBuddy..."
        ref={inputRef}
        onKeyDown={(e) => {
          e.key === "Enter" && handleSendMessage();
        }}
      />
      <button
        type="button"
        className="flex justify-center p-2 rounded-full outline-none hover:bg-primary/5"
        title="Send"
        onClick={handleSendMessage}
      >
        <SendIcon className="text-white fill-primary size-10 " />
      </button>
    </div>
  );
};

export default Input;
