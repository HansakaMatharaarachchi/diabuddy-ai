import { useEffect } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./app/index.css";
import { routes } from "./app/routes";

const router = createBrowserRouter(routes);

const App = () => {
	//Set Page Title.
	useEffect(() => {
		document.title = "DiaBuddy";
	}, []);

	return <RouterProvider router={router} />;
};

export default App;
