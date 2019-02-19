import React from "react";

const MessageList = props => {
  const messages = props.messages.map(message => (
    <div key={message.id} className="card bg-light mb-3">
      <h5 className="card-header">{message.user}</h5>
      <div className="card-body">{message.text}</div>
    </div>
  ));
  return <div>{messages}</div>;
};

export default MessageList;
