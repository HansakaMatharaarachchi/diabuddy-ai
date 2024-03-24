import { RouteObject } from "react-router-dom";

import { Auth0ProviderWithNavigate, withAuthGuard } from "./auth";
import { Chat, GetStarted, NotFound, Settings } from "./pages";
import { AppContextProvider } from "./contexts";

export const routes: RouteObject[] = [
	{
		Component: Auth0ProviderWithNavigate,
		children: [
			{
				Component: AppContextProvider,
				children: [
					{
						path: "/",
						Component: GetStarted,
					},
					{
						path: "/chat",
						Component: withAuthGuard(Chat),
					},
					{
						path: "/settings",
						Component: withAuthGuard(Settings),
					},
					{
						path: "*",
						Component: NotFound,
					},
				],
			},
		],
	},
];
