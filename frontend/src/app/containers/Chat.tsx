import { ReactComponent as ClearIcon } from "../../assets/svg/clear.svg";
import { Conversation, Input } from "../components";
import { Header } from "../layouts";

const Chat = () => {
	return (
		<>
			<Header
				title="Chat"
				options={
					<button type="button" title="Clear Chat">
						<ClearIcon className="size-10" />
					</button>
				}
			/>
			<Conversation messages={[...new Array(20)]} />
			<Input />
		</>
	);
};

export default Chat;
