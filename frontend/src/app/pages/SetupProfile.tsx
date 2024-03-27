import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useAppContext } from "../contexts";
import { EditUserProfileContainer } from "../containers";

const SetupProfile = () => {
	const navigate = useNavigate();
	const { authenticatedUser } = useAppContext();

	// Redirect to chat page if user profile is already completed.
	useEffect(() => {
		if (authenticatedUser?.is_profile_completed) {
			navigate("/chat", { replace: true });
		}
	}, [authenticatedUser, navigate]);

	return (
		<div className="flex flex-row p-8 w-full min-h-dvh bg-[url('/src/assets/svg/animated-bg.svg')] bg-no-repeat bg-cover items-center">
			<div className="flex flex-col w-full p-8 mx-auto rounded-xl h-fit backdrop-filter backdrop-blur-lg bg-primary/10 sm:w-5/6 md:w-3/4 lg:w-3/5 xl:w-1/3">
				<div className="flex flex-col gap-4">
					<span className="text-3xl font-semibold">Let's get started!</span>
					<p className="text-2xl font-semibold">
						Tell me a bit about yourself! so I can help you better. 🤗
					</p>
				</div>
				<EditUserProfileContainer />
			</div>
		</div>
	);
};

export default SetupProfile;
