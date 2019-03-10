import React from "react";
import MessageListItem from "./MessageListItem";
import AnimateThis from "./AnimateThis";

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
    let messages;
    if (this.props.messages && this.props.messages.length) {
      messages = this.props.messages.map(message => (
        <MessageListItem message={message} key={message.id} />
      ));
    }

    return (
      <div
        className="flex-grow-1 my-3"
        style={{ overflow: "hidden auto", minHeight: "250px" }}
        ref={this.messageList}
      >
        <AnimateThis>{messages}</AnimateThis>
      </div>
    );
  }
}

export default MessageList;
