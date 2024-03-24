import { withAuthenticationRequired } from "@auth0/auth0-react";
import { Loader } from "../components";

const withAuthGuard = (component: any) => {
	const guardedComponent = withAuthenticationRequired(component, {
		onRedirecting: () => (
			<div className="flex items-center justify-center w-full h-svh">
				<Loader size={64} />
			</div>
		),
	});

	return guardedComponent;
};

export default withAuthGuard;
