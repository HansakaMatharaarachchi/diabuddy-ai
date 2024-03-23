import { NavLink, NavLinkProps } from "react-router-dom";
import logo from "../../../assets/images/logo.png";
import { ReactComponent as ChatSvg } from "../../../assets/svg/chat.svg";
import { ReactComponent as ClockSvg } from "../../../assets/svg/clock.svg";
import { ReactComponent as ExitSvg } from "../../../assets/svg/exit.svg";
import { ReactComponent as SettingsSvg } from "../../../assets/svg/settings.svg";

interface NavItemProps extends NavLinkProps {
  Icon: React.FC<React.SVGProps<SVGSVGElement>>;
  text: string;
}

const NavItem = ({ to, Icon, text, ...rest }: NavItemProps) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      `flex gap-3 px-4 py-5 border rounded-lg border-black/20 text-primary transition-colors hover:bg-primary hover:text-white ${
        isActive ? "bg-primary text-white" : ""
      }`
    }
    {...rest}
  >
    <Icon className="size-6" />
    {text}
  </NavLink>
);

const NavBar = () => (
  <nav className="flex flex-col gap-2.5 p-4 ">
    <img src={logo} alt="logo" />

    <div className="flex flex-col justify-between flex-1 gap-2.5 text-xl font-bold *:flex *:flex-col *:gap-2">
      <div>
        <NavItem
          to="/chat"
          Icon={ChatSvg}
          text="Chat"
          aria-label="Chat Navigation"
        />
        <NavItem
          to="/reminders"
          Icon={ClockSvg}
          text="Reminders"
          aria-label="Reminders Navigation"
        />
      </div>

      <div>
        <NavItem
          to="/settings"
          Icon={SettingsSvg}
          text="Settings"
          aria-label="Settings Navigation"
        />
        <NavItem
          to="/logout"
          Icon={ExitSvg}
          text="Log Out"
          aria-label="Log Out Navigation"
        />
      </div>
    </div>
  </nav>
);

export default NavBar;
