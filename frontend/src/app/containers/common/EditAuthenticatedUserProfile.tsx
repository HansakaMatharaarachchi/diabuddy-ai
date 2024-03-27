import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import { Gender, DiabetesType, Language } from "../../constants";
import { useUpdateAuthenticatedUserMutation } from "../../services/user";
import { User } from "../../interfaces";
import Swal from "sweetalert2";
import { useAppContext } from "../../contexts";
type EditAuthenticatedUserProfileProps = {
	readonly?: boolean;
};

type UserFormData = Omit<User, "user_id" | "is_profile_completed">;

const EditAuthenticatedUserProfile = ({
	readonly,
}: EditAuthenticatedUserProfileProps) => {
	const { authenticatedUser } = useAppContext();

	const [formData, setFormData] = useState<UserFormData>({
		nickname: authenticatedUser?.nickname,
		age: authenticatedUser?.age,
		gender: authenticatedUser?.gender ?? Gender.MALE,
		diabetes_type: authenticatedUser?.diabetes_type ?? DiabetesType.TYPE_1,
		preferred_language:
			authenticatedUser?.preferred_language ?? Language.ENGLISH,
	});

	const [
		updateUser,
		{
			isSuccess: isUserUpdated,
			isLoading: isUpdatingUser,
			isError: updateUserError,
		},
	] = useUpdateAuthenticatedUserMutation();

	useEffect(() => {
		Swal.close();
		if (isUserUpdated) {
			Swal.fire({
				title: "Success",
				text: "Profile updated successfully",
				icon: "success",
				timer: 1000,
			});
		} else if (isUpdatingUser) {
			Swal.fire({
				title: "Updating",
				text: "Updating your profile...",
				icon: "info",
				showConfirmButton: false,
				showCancelButton: false,
				allowOutsideClick: false,
				didOpen: () => {
					Swal.showLoading();
				},
			});
		} else if (updateUserError) {
			Swal.fire({
				title: "Oops..!",
				text: "Something went wrong. Please try again later",
				icon: "error",
			});
		}
	}, [isUpdatingUser, isUserUpdated, updateUserError]);

	const handleChange = (
		e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
	) => {
		const { name, value } = e.target;
		setFormData({
			...formData,
			[name]: value,
		});
	};

	const submitForm = (e: FormEvent) => {
		e.preventDefault();

		if (formData) updateUser(formData);
	};

	return (
		<form onSubmit={submitForm}>
			<fieldset
				className="flex flex-col gap-4 mt-5 text-base"
				disabled={readonly}
			>
				<div>
					<label htmlFor="nickname">Nickname</label>
					<input
						type="text"
						name="nickname"
						id="nickname"
						required
						className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary/50 focus:border-primary/50 block w-full p-2.5 outline-none"
						placeholder="Nickname"
						value={formData.nickname}
						onChange={handleChange}
					/>
				</div>
				<div>
					<label htmlFor="age">Age</label>
					<input
						type="number"
						name="age"
						id="age"
						required
						min={18}
						max={100}
						step="1"
						placeholder="Select your age"
						className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary/50 focus:border-primary/50 block w-full p-2.5 outline-none"
						value={formData.age}
						onChange={handleChange}
					/>
				</div>
				<div>
					<label htmlFor="gender">Gender</label>
					<select
						name="gender"
						id="gender"
						required
						className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary/50 focus:border-primary/50 block w-full p-2.5"
						value={formData.gender ?? undefined}
						onChange={handleChange}
					>
						{Object.values(Gender).map((gender) => (
							<option key={gender} value={gender}>
								{gender}
							</option>
						))}
					</select>
				</div>
				<div>
					<label htmlFor="diabetes_type">Diabetes type</label>
					<select
						name="diabetes_type"
						id="diabetes_type"
						required
						className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary/50 focus:border-primary/50 block w-full p-2.5"
						value={formData.diabetes_type ?? undefined}
						onChange={handleChange}
					>
						{Object.values(DiabetesType).map((type) => (
							<option key={type} value={type}>
								{type}
							</option>
						))}
					</select>
				</div>
				<div>
					<label htmlFor="preferred_language">Preferred language</label>
					<select
						name="preferred_language"
						id="preferred_language"
						className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary/50 focus:border-primary/50 block w-full p-2.5"
						disabled
						required
						value={formData.preferred_language ?? undefined}
						onChange={handleChange}
					>
						{Object.values(Language).map((language) => (
							<option key={language} value={language}>
								{language}
							</option>
						))}
					</select>
				</div>
				{!readonly && (
					<button
						type="submit"
						className={`text-white bg-primary/70 hover:bg-primary/80 focus:outline-none font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center self-end ${
							isUpdatingUser ? "cursor-not-allowed" : ""
						}`}
						disabled={isUpdatingUser}
					>
						{isUpdatingUser ? "Updating..." : "Update"}
					</button>
				)}
			</fieldset>
		</form>
	);
};

export default EditAuthenticatedUserProfile;
