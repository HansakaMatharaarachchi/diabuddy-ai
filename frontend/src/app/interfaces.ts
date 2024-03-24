import { DiabetesType, Gender, Language } from "./constants";

export interface User {
	user_id: string;
	nickname: string;
	user_metadata: {
		age: number;
		diabetes_type: DiabetesType;
		gender: Gender;
		preferred_language: Language;
	};
}
