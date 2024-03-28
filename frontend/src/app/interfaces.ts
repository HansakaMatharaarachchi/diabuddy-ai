import { ChatMessageType, DiabetesType, Gender, Language } from "./constants";

export interface User {
	user_id: string;
	nickname?: string;
	age?: number;
	diabetes_type?: DiabetesType;
	gender?: Gender;
	preferred_language?: Language;
	is_profile_completed: boolean;
}

export interface ChatMessage {
	message_id: string;
	timestamp: string;
	content: string;
	type: ChatMessageType;
}
