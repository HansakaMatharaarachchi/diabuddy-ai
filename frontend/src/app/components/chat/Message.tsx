import moment, { Moment } from "moment";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Props = {
	message: string;
	time: Moment;
	isSender: boolean;
};

const Message = ({ message, time, isSender }: Props) => {
	return (
		<>
			{message && (
				<div
					className={`flex flex-col ${isSender ? "items-end" : "items-start"}`}
				>
					<div
						className={`flex gap-2 ${
							isSender ? "flex-row-reverse" : ""
						} items-end`}
					>
						<Markdown
							className={`px-4 py-2 text-base border rounded-t-2xl prose overflow-scroll ${
								isSender ? "rounded-bl-2xl" : "rounded-br-2xl"
							}`}
							remarkPlugins={[remarkGfm]}
						>
							{message}
						</Markdown>
						{moment.isMoment(time) && (
							<span className="text-sm min-w-fit">{time.fromNow()}</span>
						)}
					</div>
				</div>
			)}
		</>
	);
};

export default Message;
