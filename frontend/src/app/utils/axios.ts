// https://stackoverflow.com/questions/69011315/how-to-get-auth0-token-from-outside-react-components
import axios from "axios";

const axiosClient = axios.create();

// adds access tokens in all api requests
// this interceptor is only added when the auth0 instance is ready and exports the getAccessTokenSilently method
export const addAccessTokenInterceptor = (getAccessTokenSilently: any) => {
	axiosClient.interceptors.request.use(async (config) => {
		const token = await getAccessTokenSilently();
		config.headers.Authorization = `Bearer ${token}`;
		return config;
	});
};

export default axiosClient;
