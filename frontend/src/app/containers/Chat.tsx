import Header from "../components/common/Header";
import { ReactComponent as ClearIcon } from "../../assets/svg/clear.svg";

const Chat = () => {
  return (
    <>
      <Header
        title="Chat"
        options={
          <button type="button">
            <ClearIcon className="size-10" />
          </button>
        }
      />
      <main>
        <div>yello</div>
      </main>
    </>
  );
};

export default Chat;
