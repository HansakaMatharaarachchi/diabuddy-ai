type Props = {
	size?: number;
};

const Loader = ({ size }: Props) => (
	<div
		className={`size-[${size ?? 20}px] rounded-full bg-primary animate-ping`}
	></div>
);
export default Loader;
