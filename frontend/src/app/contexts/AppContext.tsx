import { useAuth0 } from "@auth0/auth0-react";
import { createContext, useContext, useEffect } from "react";
import { Outlet } from "react-router-dom";
import { addAccessTokenInterceptor } from "../utils/axiosClient";

const AppContext = createContext({});

export const AppContextProvider = () => {
	const { getAccessTokenSilently } = useAuth0();

	// Set Auth0 access token to axios instance.
	useEffect(() => {
		addAccessTokenInterceptor(getAccessTokenSilently);
	}, [getAccessTokenSilently]);

	return (
		<AppContext.Provider value={{}}>
			<Outlet />
		</AppContext.Provider>
	);
};

export const useAppContext = () => useContext(AppContext);

export default AppContextProvider;
