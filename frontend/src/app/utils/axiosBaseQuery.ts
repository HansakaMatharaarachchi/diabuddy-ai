import type { BaseQueryFn } from "@reduxjs/toolkit/query";
import type { AxiosError, AxiosRequestConfig } from "axios";
import axiosClient from "./axiosClient";

const axiosBaseQuery =
	(
		{ baseUrl }: { baseUrl: string } = { baseUrl: "" }
	): BaseQueryFn<
		{
			url: string;
			method?: AxiosRequestConfig["method"];
			data?: AxiosRequestConfig["data"];
			params?: AxiosRequestConfig["params"];
			headers?: AxiosRequestConfig["headers"];
			responseType?: AxiosRequestConfig["responseType"];
			adapter?: AxiosRequestConfig["adapter"];
		},
		unknown,
		unknown
	> =>
	async ({ url, method, data, params, headers, responseType, adapter }) => {
		try {
			const result = await axiosClient({
				url: baseUrl + url,
				method,
				data,
				params,
				headers,
				responseType,
				adapter,
			});
			return { data: result.data };
		} catch (axiosError) {
			const err = axiosError as AxiosError;
			return {
				error: {
					status: err.response?.status,
					data: err.response?.data || err.message,
				},
			};
		}
	};

export default axiosBaseQuery;
