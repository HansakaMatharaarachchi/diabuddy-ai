import { useAuth0 } from "@auth0/auth0-react";
import { NavLink } from "react-router-dom";
import logo from "../../assets/images/logo.png";
import { ReactComponent as ChatSvg } from "../../assets/svg/chat.svg";
import { ReactComponent as ExitSvg } from "../../assets/svg/exit.svg";
import { ReactComponent as SettingsSvg } from "../../assets/svg/settings.svg";

interface NavItemProps {
	Icon: React.FC<React.SVGProps<SVGSVGElement>>;
	text: string;
	isActive?: boolean;
	onClick?: () => void;
}

const NavItem = ({ Icon, text, isActive, onClick }: NavItemProps) => (
	<button
		className={`flex gap-3 px-4 py-5 w-full border rounded-lg border-black/20 text-primary transition-colors hover:bg-primary hover:text-white ${
			isActive ? "bg-primary text-white" : ""
		}`}
		onClick={onClick}
	>
		<Icon className="size-6" />
		{text}
	</button>
);

const NavBar = () => {
	const { logout } = useAuth0();

	return (
		<nav className="flex flex-col gap-2.5 p-4 ">
			<img src={logo} alt="logo" />

			<div className="flex flex-col justify-between flex-1 gap-2.5 text-xl font-bold *:flex *:flex-col *:gap-2">
				<div>
					<NavLink to="/chat">
						{({ isActive }) => (
							<NavItem
								Icon={ChatSvg}
								text="Chat"
								isActive={isActive}
								aria-label="Chat Navigation"
							/>
						)}
					</NavLink>
				</div>

				<div>
					<NavLink to="/settings">
						{({ isActive }) => (
							<NavItem
								Icon={SettingsSvg}
								text="Settings"
								isActive={isActive}
								aria-label="Settings Navigation"
							/>
						)}
					</NavLink>
					<NavItem
						Icon={ExitSvg}
						text="Log Out"
						aria-label="Log Out Navigation"
						onClick={() =>
							logout({
								logoutParams: {
									returnTo: window.location.origin,
								},
							})
						}
					/>
				</div>
			</div>
		</nav>
	);
};
export default NavBar;
