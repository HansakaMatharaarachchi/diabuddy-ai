import { useLayoutEffect, useState } from "react";
import debounce from "lodash/debounce";

// Hook to determine if the user is on a mobile device.
const useIsOnMobile = (): boolean => {
	const [isMobile, setIsMobile] = useState(false);

	useLayoutEffect(() => {
		const updateSize = (): void => {
			setIsMobile(window.innerWidth < 768);
		};

		updateSize();
		window.addEventListener("resize", debounce(updateSize, 250));
		return (): void => window.removeEventListener("resize", updateSize);
	}, []);

	return isMobile;
};

export default useIsOnMobile;
