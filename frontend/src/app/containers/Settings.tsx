import { useEffect } from "react";
import Swal from "sweetalert2";
import { useDeleteAuthenticatedUserMutation } from "../services/user";
import EditAuthenticatedUserProfile from "./common/EditAuthenticatedUserProfile";

const Settings = () => {
	const [
		deleteAuthenticatedUser,
		{
			isLoading: isDeletingUser,
			isSuccess: isUserDeleted,
			isError: isDeleteUserError,
		},
	] = useDeleteAuthenticatedUserMutation();

	useEffect(() => {
		(async () => {
			Swal.close();
			if (isDeletingUser) {
				Swal.fire({
					title: "Deleting Account",
					text: "Please wait while we delete your account...",
					icon: "info",
					showConfirmButton: false,
					showCancelButton: false,
					allowOutsideClick: false,
					didOpen: () => {
						Swal.showLoading();
					},
				});
			} else if (isUserDeleted) {
				await Swal.fire({
					title: "Account Deleted!",
					text: "Your account has been successfully deleted.",
					icon: "success",
					showConfirmButton: false,
					timer: 1500,
				});
			} else if (isDeleteUserError) {
				Swal.fire({
					title: "Oops..!",
					text: "Something went wrong while deleting your account, please try again later.",
					icon: "error",
				});
			}
		})();
	}, [isDeleteUserError, isDeletingUser, isUserDeleted]);

	return (
		<div className="flex flex-col items-center justify-center flex-1 gap-5 px-4 py-4">
			<div className="w-2/5">
				<span className="text-2xl font-bold">Your Information.</span>
				<EditAuthenticatedUserProfile readonly />
				<button
					type="button"
					className="text-white bg-red-500 hover:bg-red-600 focus:outline-none font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center mt-5"
					onClick={() => {
						Swal.fire({
							title: "Are you sure?",
							text: "You won't be able to revert this!",
							icon: "warning",
							showCancelButton: true,
							confirmButtonText: "Yes, delete it!",
							cancelButtonText: "No, cancel!",
						}).then((result) => {
							if (result.isConfirmed) {
								deleteAuthenticatedUser();
							}
						});
					}}
				>
					Delete Account
				</button>
			</div>
		</div>
	);
};

export default Settings;
