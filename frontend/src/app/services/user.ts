import { createApi } from "@reduxjs/toolkit/query/react";
import { USER_API_URL } from "../constants";
import { User } from "../interfaces";
import axiosBaseQuery from "../utils/axiosBaseQuery";

export const userApi = createApi({
	reducerPath: "userAPI",
	tagTypes: ["AuthenticatedUser"],
	baseQuery: axiosBaseQuery({
		baseUrl: USER_API_URL,
	}),
	endpoints(build) {
		return {
			getAuthenticatedUser: build.query<User, void>({
				query: () => ({ url: "/me", method: "GET" }),
				providesTags: ["AuthenticatedUser"],
			}),
			updateAuthenticatedUser: build.mutation<User, Partial<User>>({
				query: (userData) => ({ url: "/me", method: "PATCH", data: userData }),
				invalidatesTags: ["AuthenticatedUser"],
			}),
			deleteAuthenticatedUser: build.mutation<void, void>({
				query: () => ({ url: "/me", method: "DELETE" }),
				invalidatesTags: ["AuthenticatedUser"],
			}),
		};
	},
});

export const {
	useGetAuthenticatedUserQuery,
	useUpdateAuthenticatedUserMutation,
	useDeleteAuthenticatedUserMutation,
} = userApi;
