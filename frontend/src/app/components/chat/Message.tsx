import { Moment } from "moment";

type Props = {
  message: string;
  time: Moment;
  isSender: boolean;
  showDate?: boolean;
};

const Message = ({ message, time, isSender, showDate }: Props) => {
  return (
    <>
      <div className="flex justify-center ">{time?.format("MMMM Do YYYY")}</div>
      <div
        className={`flex items-end gap-2 ${isSender ? "flex-row-reverse" : ""}`}
      >
        <div
          className={`px-4 py-2 text-base border  rounded-t-2xl max-w-[90%] ${
            isSender ? "rounded-bl-2xl" : "rounded-br-2xl"
          }`}
        >
          {message}
        </div>
        <span className="text-sm">{time?.format("hh.mm a")}</span>
      </div>
    </>
  );
};

export default Message;
