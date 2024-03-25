import { createApi } from "@reduxjs/toolkit/query/react";
import axiosBaseQuery from "../utils/axiosBaseQuery";
import { USER_API_URL } from "../constants";

export const userApi = createApi({
	reducerPath: "userAPI",
	baseQuery: axiosBaseQuery({
		baseUrl: USER_API_URL,
	}),
	endpoints(build) {
		return {};
	},
});

export const {} = userApi;
