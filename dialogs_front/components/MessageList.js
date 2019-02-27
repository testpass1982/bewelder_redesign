import React from "react";
import MessageListItem from "./MessageListItem";

class MessageList extends React.Component {
  messageList = React.createRef();

  componentDidUpdate() {
    this.scrollToBottom();
  }

  scrollToBottom = () => {
    const messageList = this.messageList.current;
    const { scrollHeight, clientHeight } = messageList;
    const maxScrollTop = scrollHeight - clientHeight;
    messageList.scrollTop = maxScrollTop > 0 ? maxScrollTop : 0;
  };

  render() {
    if (this.props.messages && this.props.messages.length) {
      const messages = this.props.messages.map(message => (
        <MessageListItem message={message} key={message.id} />
      ));
      return (
        <div
          className="mb-3"
          style={{ height: "42vh", overflow: "auto" }}
          ref={this.messageList}
        >
          {messages}
        </div>
      );
    } else {
      return <div>Нет сообщений</div>;
    }
  }
}

export default MessageList;
