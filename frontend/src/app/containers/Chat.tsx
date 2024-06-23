import { useEffect } from "react";
import Swal from "sweetalert2";
import { ReactComponent as ClearIcon } from "../../assets/svg/clear.svg";
import { ReactComponent as RefreshIcon } from "../../assets/svg/refresh.svg";
import { Conversation, Input, Loader } from "../components";
import { useAppContext } from "../contexts";
import { Header } from "../layouts";
import {
	useDeleteAuthenticatedUserChatHistoryMutation,
	useGetAuthenticatedUserChatHistoryQuery,
	useSendMessageMutation,
} from "../services/chat";

const Chat = () => {
	const { authenticatedUser } = useAppContext();
	const {
		data: chatHistory,
		isSuccess: isChatHistorySuccess,
		isLoading: isChatHistoryLoading,
		isError: isChatHistoryError,
		refetch,
	} = useGetAuthenticatedUserChatHistoryQuery(undefined, {
		refetchOnMountOrArgChange: true,
	});

	const [sendMessage, { isLoading: isSendingMessage }] =
		useSendMessageMutation();
	const [
		deleteChatHistory,
		{
			isLoading: isDeletingChatHistory,
			isError: isDeleteChatHistoryError,
			isSuccess: isDeleteChatHistorySuccess,
		},
	] = useDeleteAuthenticatedUserChatHistoryMutation();

	useEffect(() => {
		(async () => {
			if (isDeletingChatHistory) {
				Swal.fire({
					title: "Clearing Chat",
					text: "Clearing chat history...",
					icon: "info",
					showConfirmButton: false,
					showCancelButton: false,
					allowOutsideClick: false,
					didOpen: () => {
						Swal.showLoading();
					},
				});
			} else if (isDeleteChatHistoryError) {
				Swal.fire({
					title: "Oops!",
					text: "Something went wrong while clearing chat history, please try again later.",
					icon: "error",
				});
			} else if (isDeleteChatHistorySuccess) {
				await Swal.fire({
					title: "Success",
					text: "Chat history cleared successfully",
					icon: "success",
					timer: 1500,
				});
			}
		})();
	}, [
		isDeleteChatHistoryError,
		isDeleteChatHistorySuccess,
		isDeletingChatHistory,
	]);

	const clearChatHistory = async () => {
		await Swal.fire({
			title: "Clear Chat",
			text: "Are you sure you want to clear chat history?",
			icon: "warning",
			showCancelButton: true,
			confirmButtonText: "Yes",
			cancelButtonText: "No",
		}).then(async (result) => {
			if (result.isConfirmed) {
				await deleteChatHistory();
			}
		});
	};

	const handleSendMessage = async (query: string) => {
		try {
			return await sendMessage(query).unwrap();
		} catch (error) {
			Swal.fire({
				title: "Oops!",
				text: "Something went wrong while sending your message, please try again later.",
				icon: "error",
			});
			throw error;
		}
	};

	return (
		<div className="flex flex-col h-full">
			<Header
				title="Chat"
				options={
					<>
						{!isSendingMessage && !!chatHistory?.length && (
							<button
								type="button"
								title="Clear Chat"
								onClick={clearChatHistory}
							>
								<ClearIcon className="size-8" />
							</button>
						)}
					</>
				}
			/>

			<div className="flex flex-col flex-1 overflow-y-auto xl:px-36">
				{!isChatHistorySuccess ? (
					<div className="flex flex-col items-center justify-center h-full gap-2">
						{isChatHistoryLoading && <Loader />}

						{isChatHistoryError && (
							<>
								<span className="text-lg text-center">
									Something went wrong while getting your chat history.
								</span>
								<span className="text-base">Please try again.</span>
								<button
									title="Retry"
									type="button"
									onClick={refetch}
									className="p-2 text-sm font-medium text-center text-white rounded-full bg-primary/70 hover:bg-primary/80 focus:outline-none"
								>
									<RefreshIcon className="size-8" />
								</button>
							</>
						)}
					</div>
				) : (
					<>
						{chatHistory?.length > 0 ? (
							<Conversation messages={chatHistory} />
						) : (
							<div className="flex flex-col h-full gap-2 px-4 pt-12 xl:px-0">
								<span className="text-6xl text-primary">
									Hello, {authenticatedUser?.nickname}
								</span>
								<span className="text-5xl text-black/40">
									How can I help you today?
								</span>
							</div>
						)}
					</>
				)}
				<div className={`${isChatHistoryLoading ? "animate-pulse" : ""}`}>
					<Input
						disabled={!isChatHistorySuccess || isSendingMessage}
						sendMessage={handleSendMessage}
						isLoading={isSendingMessage}
					/>
				</div>
			</div>
		</div>
	);
};

export default Chat;
