import { useAuth0 } from "@auth0/auth0-react";
import { createContext, useContext, useEffect, useMemo } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useGetAuthenticatedUserQuery } from "../services/user";
import { addAccessTokenInterceptor } from "../utils/axiosClient";
import { User } from "../interfaces";
import { Loader, ErrorPage } from "../components";

type AppContextType = {
	authenticatedUser?: User;
};

const AppContext = createContext<AppContextType>({});

export const AppContextProvider = () => {
	const navigate = useNavigate();

	const {
		isAuthenticated,
		isLoading: isAuthLoading,
		error: authError,
		getAccessTokenSilently,
		logout,
	} = useAuth0();

	// Set Auth0 access token to axios instance.
	useEffect(() => {
		if (isAuthenticated) {
			addAccessTokenInterceptor(getAccessTokenSilently);
		}
	}, [getAccessTokenSilently, isAuthenticated]);

	const {
		data: authenticatedUser,
		isSuccess: isGettingAuthenticatedUserSuccess,
		isLoading: isGettingAuthenticatedUserLoading,
		error: getAuthenticatedUserError,
	} = useGetAuthenticatedUserQuery(undefined, {
		skip: !isAuthenticated,
	});

	const contextValue = useMemo(
		() => ({
			authenticatedUser,
		}),
		[authenticatedUser]
	);

	// Redirect to setup profile page,
	// if user is authenticated but profile is not completed.
	useEffect(() => {
		if (
			isGettingAuthenticatedUserSuccess &&
			!authenticatedUser.is_profile_completed
		) {
			navigate("/setup-profile", { replace: true });
		}
	}, [
		authenticatedUser?.is_profile_completed,
		isGettingAuthenticatedUserSuccess,
		navigate,
	]);

	// If the user is already deleted, but still authenticated, logout the user.
	useEffect(() => {
		if (isAuthenticated && (getAuthenticatedUserError as any)?.status === 404) {
			logout();
		}
	}, [getAuthenticatedUserError, isAuthenticated, logout]);

	if (isAuthLoading || isGettingAuthenticatedUserLoading) {
		return (
			<div className="flex items-center justify-center w-full h-svh">
				<Loader />
			</div>
		);
	} else if (
		authError ||
		(getAuthenticatedUserError &&
			(getAuthenticatedUserError as any).status !== 404)
	) {
		return <ErrorPage />;
	} else {
		return (
			<AppContext.Provider value={contextValue}>
				<Outlet />
			</AppContext.Provider>
		);
	}
};

export const useAppContext = () => useContext(AppContext);

export default AppContextProvider;
