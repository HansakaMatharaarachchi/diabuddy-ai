import { createApi } from "@reduxjs/toolkit/query/react";
import { USER_API_URL } from "../constants";
import { ChatMessage } from "../interfaces";
import axiosBaseQuery from "../utils/axiosBaseQuery";

export const chatApi = createApi({
	reducerPath: "chatAPI",
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
			}),
			deleteAuthenticatedUserChatHistory: build.mutation<void, void>({
				query: () => ({
					url: "/me/chat",
					method: "DELETE",
				}),
			}),
		};
	},
});

export const {
	useGetAuthenticatedUserChatHistoryQuery,
	useDeleteAuthenticatedUserChatHistoryMutation,
} = chatApi;
