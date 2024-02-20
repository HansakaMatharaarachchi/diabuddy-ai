import { RouteObject } from "react-router-dom";
import Chat from "./pages/chat";

export const routes: RouteObject[] = [
  {
    path: "/",
    Component: Chat
  }
];