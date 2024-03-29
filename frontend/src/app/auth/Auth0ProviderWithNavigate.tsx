import { AppState, Auth0Provider } from "@auth0/auth0-react";
import { Outlet, useNavigate } from "react-router-dom";

export const Auth0ProviderWithNavigate = () => {
	const navigate = useNavigate();

	const domain = process.env.REACT_APP_AUTH0_DOMAIN;
	const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID;
	const redirectUri = process.env.REACT_APP_AUTH0_REDIRECT_URI;
	const audience = process.env.REACT_APP_AUTH0_AUDIENCE;

	const onRedirectCallback = (appState?: AppState) => {
		navigate(appState?.returnTo ?? window.location.pathname);
	};

	if (!(domain && clientId && redirectUri && audience)) {
		return null;
	}

	return (
		<Auth0Provider
			domain={domain}
			clientId={clientId}
			authorizationParams={{
				audience: audience,
				redirect_uri: redirectUri,
			}}
			useRefreshTokens
			useRefreshTokensFallback
			cacheLocation="localstorage"
			onRedirectCallback={onRedirectCallback}
		>
			<Outlet />
		</Auth0Provider>
	);
};

export default Auth0ProviderWithNavigate;
