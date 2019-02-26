import React from "react";
import MessageListItem from "./MessageListItem";

const MessageList = props => {
  if (props.messages && props.messages.length) {
    const messages = props.messages.map(message => (
      <MessageListItem message={message} key={message.id} />
    ));
    return (
      <div className="mb-3" style={{ height: "42vh", overflow: "auto" }}>
        {messages}
      </div>
    );
  } else {
    return <div>Нет сообщений</div>;
  }
};

export default MessageList;
