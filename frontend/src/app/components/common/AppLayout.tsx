import React from "react";
import NavBar from "./NavBar";
import Header from "./Header";

type Props = {
  children?: React.ReactNode;
};

const AppLayout = ({ children }: Props) => {
  return (
    <div className="flex w-full h-dvh">
      <aside className="flex w-4/5 min-h-screen border border-r shadow-2xl sm:w-2/5 md:w-1/3 xl:w-1/5 sm:shadow-none rounded-2xl">
        <NavBar />
      </aside>
      <div className="flex flex-col w-full">
        <Header title="Chat" options={<div>ok</div>} />
        <main>{children}</main>
      </div>
    </div>
  );
};

export default AppLayout;
