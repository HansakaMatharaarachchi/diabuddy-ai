import { ReactComponent as ClearIcon } from "../../assets/svg/clear.svg";
import Header from "../components/common/Header";

import Conversation from "../components/chat/Conversation";
import Input from "../components/chat/Input";

const Chat = () => {
  return (
    <>
      <Header
        title="Chat"
        options={
          <button type="button" title="Clear Chat">
            <ClearIcon className="size-10" />
          </button>
        }
      />
      <Conversation messages={[...new Array(20)]} />
      <Input />
    </>
  );
};

export default Chat;
