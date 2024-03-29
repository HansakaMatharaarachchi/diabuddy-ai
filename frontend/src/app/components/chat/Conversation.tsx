import moment from "moment";
import { Fragment, useEffect, useRef } from "react";
import { ChatMessageType } from "../../constants";
import { ChatMessage } from "../../interfaces";
import Message from "./Message";

type Props = {
	messages?: ChatMessage[];
};

const Conversation = ({ messages }: Props) => {
	const conversationContainerRef = useRef<HTMLDivElement>(null);

	// Scroll to bottom of the chat on messages change.
	useEffect(() => {
		conversationContainerRef.current?.scrollTo({
			top: conversationContainerRef.current.scrollHeight,
			behavior: "smooth",
		});
	}, [messages]);

	return (
		<div
			className="relative flex flex-col flex-1 gap-3 px-4 py-4 overflow-y-scroll scroll-smooth"
			ref={conversationContainerRef}
		>
			{messages?.map((message: ChatMessage, index: number) => {
				const isNewDate =
					index === 0 ||
					!moment(messages?.[index - 1]?.timestamp).isSame(
						message?.timestamp,
						"day"
					);
				const isSender = message.type === ChatMessageType.HUMAN;
				const messageTimeStampMoment = moment(message.timestamp);

				return (
					<Fragment key={message.message_id}>
						{isNewDate && messageTimeStampMoment.isValid() && (
							<div className="sticky top-0 z-40 flex self-center justify-center p-2 m-1 text-sm font-bold rounded-lg bg-slate-200 min-w-36">
								{messageTimeStampMoment.calendar(null, {
									sameDay: "[Today]",
									lastDay: "[Yesterday]",
									lastWeek: "dddd",
									sameElse: "DD/MM/YYYY",
								})}
							</div>
						)}
						<Message
							message={message.content}
							time={messageTimeStampMoment}
							isSender={isSender}
						/>
					</Fragment>
				);
			})}
		</div>
	);
};

export default Conversation;
