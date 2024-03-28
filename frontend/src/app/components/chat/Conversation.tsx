import moment from "moment";
import { useEffect, useRef } from "react";
import { ChatMessageType } from "../../constants";
import { ChatMessage } from "../../interfaces";
import Message from "./Message";

type Props = {
	messages?: ChatMessage[];
};

const Conversation = ({ messages }: Props) => {
	const messagesEndRef = useRef<HTMLDivElement>(null);

	// Scroll to bottom of the chat on messages change.
	useEffect(() => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages]);

	return (
		<div className="relative flex flex-col flex-1 gap-3 px-4 py-4 overflow-y-scroll">
			{messages?.map((message: ChatMessage, index: number) => {
				const isNewDate =
					index === 0 ||
					!moment(messages?.[index - 1]?.timestamp).isSame(
						message?.timestamp,
						"day"
					);
				const isSender = message.type === ChatMessageType.HUMAN;

				return (
					<>
						{isNewDate && (
							<div
								className="sticky top-0 flex self-center justify-center p-2 text-sm font-bold rounded-lg bg-slate-200/90"
								key={`date-${message.message_id}-${message.timestamp}`}
							>
								{moment().calendar(message.timestamp, {
									sameDay: "[Today]",
									lastDay: "[Yesterday]",
									lastWeek: "dddd",
									sameElse: "DD/MM/YYYY",
								})}
							</div>
						)}
						<Message
							message={message.content}
							time={moment(message.timestamp)}
							isSender={isSender}
						/>
					</>
				);
			})}
			<div ref={messagesEndRef} />
		</div>
	);
};

export default Conversation;
