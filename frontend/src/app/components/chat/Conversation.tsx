import moment from "moment";
import Message from "./Message";

type Props = {
  messages: any;
};

const Conversation = ({ messages }: Props) => {
  // TODO change data accordingly.
  return (
    <div className="flex flex-col flex-1 gap-2.5 px-4 py-4 overflow-y-scroll ">
      {messages?.map((message: any, index: number) => {
        const isNewDate =
          index === 0 ||
          !moment(messages?.[index - 1]?.time).isSame(message?.date, "day");
        return (
          <Message
            key={index}
            showDate={isNewDate}
            message="Hello there!!!!!!!!!"
            time={moment()}
            isSender={false}
          />
        );
      })}
    </div>
  );
};

export default Conversation;
