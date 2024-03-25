import logo from "../../assets/images/logo.png";
import { ReactComponent as EnterSVG } from "../../assets/svg/enter.svg";
import { ReactComponent as AddUserSVG } from "../../assets/svg/user-plus.svg";
import { useAuth0 } from "@auth0/auth0-react";

const GetStarted = () => {
	const { loginWithRedirect } = useAuth0();
	return (
		<div className="flex flex-col sm:flex-row w-full min-h-dvh text-primary bg-[url('/src/assets/svg/animated-bg.svg')] bg-no-repeat bg-cover">
			<aside className="flex w-full border-r sm:min-h-screen sm:border sm:bg-white sm:w-2/5 md:w-1/3 xl:w-1/4 2xl:w-1/5 rounded-2xl">
				<nav className="flex flex-col gap-2.5 p-6 ">
					<img
						src={logo}
						className="place-self-center size-56 sm:size-auto"
						alt="logo"
					/>

					<div className="flex flex-col sm:justify-between flex-1 gap-4 sm:gap-2.5 *:flex *:flex-col *:gap-2  ">
						<div className="text-4xl font-bold ">
							<span>Welcome</span>
							<span>to DiaBuddy 👋</span>
						</div>
						<span className="text-2xl font-bold opacity-90 sm:text-3xl">
							Take control of your diabetes. Get the support you need.
						</span>
					</div>
				</nav>
			</aside>
			<div className="flex flex-col items-center flex-1 w-full p-6 sm:items-end gap-y-8">
				<main className="flex flex-col justify-center flex-1 w-full h-full gap-10">
					<div className="hidden sm:flex flex-col text-3xl max-w-[985px] font-semibold">
						<span>DiaBuddy is always ready to listen.</span>
						<span>
							Get answers, find support, and learn about managing your condition
							with ease.
						</span>
					</div>
					<div className="flex flex-col items-center justify-center gap-2.5">
						<span className="text-4xl font-bold">Get started</span>
						<div className="flex gap-2.5 *:flex *:gap-3 *:px-4 *:py-5 *:text-white *:transition-colors *:border *:rounded-xl *:border-black/20 *:bg-primary *:shadow">
							<button
								onClick={() =>
									loginWithRedirect({
										appState: {
											returnTo: "/chat",
										},
									})
								}
								className="hover:ring-4 hover:ring-primary/30"
							>
								<EnterSVG className="size-6" />
								Log In
							</button>
							<button
								onClick={() =>
									loginWithRedirect({
										appState: {
											returnTo: "/chat",
										},
										authorizationParams: {
											screen_hint: "signup",
										},
									})
								}
								className="hover:ring-4 hover:ring-primary/30"
							>
								<AddUserSVG className="size-6" />
								Sign Up
							</button>
						</div>
					</div>
				</main>
				<footer className="text-xl font-bold text-center">
					<a href="https://github.com/HansakaMatharaarachchi">
						© 2024 Hansaka Matharaarchchi
					</a>
				</footer>
			</div>
		</div>
	);
};

export default GetStarted;
