import { useEffect, useRef, useState } from "react";
import { ReactComponent as MessageLoadingIcon } from "../../../assets/svg/message-loading.svg";
import { ReactComponent as SendIcon } from "../../../assets/svg/send.svg";

type Props = {
	sendMessage?: (message: string) => Promise<unknown>;
	disabled?: boolean;
	isLoading?: boolean;
};

const Input = ({ sendMessage, disabled, isLoading }: Props) => {
	const inputRef = useRef<HTMLInputElement>(null);
	const [inputText, setInputText] = useState("");

	const messageText = inputText.trim();

	useEffect(() => {
		inputRef.current?.focus();
	}, []);

	const handleSendMessage = async () => {
		if (messageText && sendMessage) {
			try {
				setInputText("");
				await sendMessage(messageText);
				inputRef.current?.focus();
			} catch (error) {
				setInputText(messageText);
			}
		}
	};

	return (
		<div className="flex gap-3 px-4 py-5 border-t">
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
				disabled={disabled}
			/>
			<button
				disabled={disabled || !messageText}
				type="button"
				className={`flex justify-center p-2 rounded-full outline-none text-white *:size-10 ${
					messageText ? "hover:bg-primary/5 *:fill-primary" : "*:fill-gray-400"
				}`}
				title={isLoading ? "Loading" : "Send Message"}
				onClick={handleSendMessage}
			>
				{isLoading ? (
					<MessageLoadingIcon className="text-primary" />
				) : (
					<SendIcon />
				)}
			</button>
		</div>
	);
};

export default Input;
