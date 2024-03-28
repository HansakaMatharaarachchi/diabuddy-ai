export const USER_API_URL = `${process.env.REACT_APP_API_SERVER_URL}/users`;

export enum Gender {
	MALE = "Male",
	FEMALE = "Female",
}

export enum DiabetesType {
	TYPE_1 = "Type 1",
	TYPE_2 = "Type 2",
}

export enum Language {
	ENGLISH = "English",
}

export enum ChatMessageType {
	AI = "ai",
	HUMAN = "human",
}
