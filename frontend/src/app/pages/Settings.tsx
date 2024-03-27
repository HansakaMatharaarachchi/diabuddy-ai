import { SettingsContainer } from "../containers";
import { Header, withLayout } from "../layouts";

const Settings = () => {
	return (
		<>
			<Header title="Settings" />
			<SettingsContainer />
		</>
	);
};

export default withLayout(Settings);
