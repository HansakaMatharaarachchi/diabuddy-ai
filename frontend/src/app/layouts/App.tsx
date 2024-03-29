import { useAuth0 } from "@auth0/auth0-react";
import { animated, config, useSpring } from "@react-spring/web";
import { ComponentType, ReactNode } from "react";
import { ReactComponent as MobileMenuIcon } from "../../assets/svg/menu.svg";
import { useAppContext } from "../contexts";
import useIsOnMobile from "../hooks/useIsOnMobile";
import NavBar from "./NavBar";
import Swal from "sweetalert2";

type Props = {
	children?: ReactNode;
};

const AppLayout = ({ children }: Props) => {
	const { isNavBarOpen, setIsNavBarOpen } = useAppContext();

	const isOnMobile = useIsOnMobile();
	const { logout } = useAuth0();

	const asideAnimation = useSpring({
		transform: isNavBarOpen ? "translateX(0%)" : "translateX(-100%)",
		config: config.stiff,
	});

	const logoutHandler = () => {
		Swal.fire({
			title: "Are you sure?",
			text: "You are about to logout from DiaBuddy",
			icon: "warning",
			showCancelButton: true,
			confirmButtonText: "Yes, logout",
		}).then((result) => {
			if (result.isConfirmed) {
				logout({
					logoutParams: {
						returnTo: window.location.origin,
					},
				});
			}
		});
	};

	return (
		<div className="relative flex w-full h-dvh">
			<animated.aside
				className="absolute z-50 flex w-full h-full border border-r md:relative backdrop-blur-sm md:backdrop-blur-0 md:w-3/5 lg:w-2/5 xl:w-2/5 2xl:w-1/5"
				style={isOnMobile ? asideAnimation : undefined}
			>
				<div className="flex flex-col w-4/5 bg-white shadow-2xl md:shadow-none md:w-full sm:w-2/4">
					<button hidden={!isOnMobile} className="self-end">
						<MobileMenuIcon
							title="Menu"
							className="w-8 h-8 m-4 text-primary"
							onClick={() => {
								setIsNavBarOpen?.((prevValue) => !prevValue);
							}}
						/>
					</button>
					<NavBar
						logout={logoutHandler}
						onNavLinkClick={() => setIsNavBarOpen?.(false)}
					/>
				</div>
			</animated.aside>
			<div className="flex flex-col w-full">{children}</div>
		</div>
	);
};

const withLayout = <P extends object>(WrappedComponent: ComponentType<P>) => {
	return (props: P) => {
		return (
			<AppLayout>
				<WrappedComponent {...props} />
			</AppLayout>
		);
	};
};

export default withLayout;
