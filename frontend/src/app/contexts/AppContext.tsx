import { useAuth0 } from "@auth0/auth0-react";
import { createContext, useContext, useEffect } from "react";
import { Outlet } from "react-router-dom";

const AppContext = createContext({});

export const AppContextProvider = () => {
	const { isAuthenticated, user } = useAuth0();

	useEffect(() => {
		if (isAuthenticated && user) {
			console.log(user);
		}
	}, [isAuthenticated, user]);

	return (
		<AppContext.Provider value={{}}>
			<Outlet />
		</AppContext.Provider>
	);
};

export const useAppContext = () => useContext(AppContext);

export default AppContextProvider;
