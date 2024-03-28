import { ReactNode, useEffect } from "react";
import { ReactComponent as MobileMenuIcon } from "../../assets/svg/menu.svg";
import { useAppContext } from "../contexts";
import useIsOnMobile from "../hooks/useIsOnMobile";

type Props = {
	title: string;
	options?: ReactNode;
};

const Header = ({ title, options }: Props) => {
	const { setIsNavBarOpen } = useAppContext();
	const isOnMobile = useIsOnMobile();

	useEffect(() => {
		document.title = `DiaBuddy | ${title}`;
	}, [title]);

	return (
		<header className="flex items-center justify-between px-4 py-5 text-3xl font-extrabold border-b shadow-sm text-primary">
			<button hidden={!isOnMobile}>
				<MobileMenuIcon
					title="Menu"
					className="w-8 h-8 text-primary"
					onClick={() => {
						setIsNavBarOpen?.((prevValue) => !prevValue);
					}}
				/>
			</button>
			{title}
			<div className="flex items-center">{options}</div>
		</header>
	);
};

export default Header;
