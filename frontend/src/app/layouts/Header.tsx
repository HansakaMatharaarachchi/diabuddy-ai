import React, { useEffect } from "react";

type Props = {
	title: string;
	options?: React.ReactNode;
};

const Header = ({ title, options }: Props) => {
	useEffect(() => {
		document.title = `DiaBuddy | ${title}`;
	}, [title]);

	return (
		<header className="flex items-center justify-between px-4 py-5 text-3xl font-extrabold border-b shadow-sm rounded-bl-2xl text-primary">
			{title}
			{options}
		</header>
	);
};

export default Header;
