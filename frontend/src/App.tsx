import { RouterProvider, createBrowserRouter } from "react-router-dom";
import "./app/index.css";
import { routes } from "./app/routes";

const router = createBrowserRouter(routes);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
