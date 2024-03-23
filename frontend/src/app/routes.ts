import { RouteObject } from "react-router-dom";
import Chat from "./pages/Chat";
import GetStarted from "./pages/GetStarted";

export const routes: RouteObject[] = [
  {
    path: "/",
    Component: GetStarted,
  },
  {
    path: "/chat",
    Component: Chat,
  },
];
