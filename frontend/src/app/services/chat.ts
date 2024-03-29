import { createApi } from "@reduxjs/toolkit/query/react";
import {
	ParsedEvent,
	ReconnectInterval,
	createParser,
} from "eventsource-parser";
import { USER_API_URL } from "../constants";
import { ChatMessage } from "../interfaces";
import axiosBaseQuery from "../utils/axiosBaseQuery";

export const chatApi = createApi({
	reducerPath: "chatAPI",
	tagTypes: ["ChatMessage"],
	baseQuery: axiosBaseQuery({
		baseUrl: USER_API_URL,
	}),
	endpoints(build) {
		return {
			getAuthenticatedUserChatHistory: build.query<ChatMessage[], void>({
				query: () => ({
					url: "/me/chat",
					method: "GET",
				}),
				providesTags: ["ChatMessage"],
			}),
			deleteAuthenticatedUserChatHistory: build.mutation<void, void>({
				query: () => ({
					url: "/me/chat",
					method: "DELETE",
				}),
				invalidatesTags: ["ChatMessage"],
			}),
			sendMessage: build.mutation<Record<string, ChatMessage>, string>({
				async queryFn(arg, api, _extraOptions, baseQuery) {
					try {
						const { data: readableStream } = await baseQuery({
							url: "/me/chat/stream",
							method: "POST",
							data: { query: arg },
							responseType: "stream",
							adapter: "fetch",
						});

						if (!(readableStream instanceof ReadableStream)) {
							throw new Error(
								"Unexpected server response: Not a readable stream."
							);
						}

						const streamedResponse: Record<string, ChatMessage> = {};
						let isChunkingStarted = false;

						const parser = createParser(
							(event: ParsedEvent | ReconnectInterval) => {
								if (event.type === "event") {
									const parsedData = JSON.parse(event.data).data;

									switch (event.event) {
										case "user_message":
											streamedResponse.userMessage = parsedData;
											api.dispatch(
												chatApi.util.updateQueryData(
													"getAuthenticatedUserChatHistory",
													undefined,
													(existingChatHistory = []) => {
														existingChatHistory.push(
															streamedResponse.userMessage
														);
													}
												)
											);
											break;
										case "ai_response_start":
											streamedResponse.aiMessage = parsedData;
											api.dispatch(
												chatApi.util.updateQueryData(
													"getAuthenticatedUserChatHistory",
													undefined,
													(existingChatHistory = []) => {
														existingChatHistory.push(
															streamedResponse.aiMessage
														);
													}
												)
											);
											break;
										case "ai_message_chunk":
											if (!streamedResponse.aiMessage) {
												throw new Error(
													"Unexpected server response: Missing AI message."
												);
											}

											if (!isChunkingStarted) {
												isChunkingStarted = true;
												streamedResponse.aiMessage = {
													...streamedResponse.aiMessage,
													content: "",
												};
											}

											// Update the AI message content with the new chunk.
											api.dispatch(
												chatApi.util.updateQueryData(
													"getAuthenticatedUserChatHistory",
													undefined,
													(existingChatHistory = []) => {
														const lastMessage = existingChatHistory.at(-1);
														if (
															lastMessage &&
															lastMessage.message_id ===
																streamedResponse.aiMessage?.message_id
														) {
															const aiMessageContent =
																streamedResponse.aiMessage.content +
																parsedData.chunk;

															streamedResponse.aiMessage = {
																...streamedResponse.aiMessage,
																content: aiMessageContent,
															};

															lastMessage.content = aiMessageContent;
														}
													}
												)
											);
											break;
										case "error":
											throw new Error(`Server error: ${parsedData.message}`);
										default:
											break;
									}
								}
							}
						);

						const reader = readableStream.getReader();

						try {
							while (true) {
								const { done, value } = await reader.read();
								if (done) break;
								const chunk = new TextDecoder().decode(value);
								parser.feed(chunk);
							}

							return { data: streamedResponse };
						} finally {
							reader.releaseLock();
						}
					} catch (error) {
						// Invalidate the chat history query to force a refetch to prevent desync.
						api.dispatch(chatApi.util.invalidateTags(["ChatMessage"]));
						const err = error as any;
						return {
							error: {
								status: err.status,
								data: err.data || err.message || "Unknown error occurred",
							},
						};
					}
				},
			}),
		};
	},
});

export const {
	useSendMessageMutation,
	useGetAuthenticatedUserChatHistoryQuery,
	useDeleteAuthenticatedUserChatHistoryMutation,
} = chatApi;
