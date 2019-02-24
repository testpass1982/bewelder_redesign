import React from "react";

const MessageList = props => {
  /*
  [
    {
      id: int,
      user: {
        id: int,
        name: str
      },
      text: str,
      sent_at: str,
      dialog: int
    }
  ]
  */
  if (props.messages && props.messages.length) {
    const messages = props.messages.map(message => (
      <div key={message.id} className="card bg-light mb-3">
        <h5 className="card-header">{message.user.name}</h5>
        <div className="card-body">{message.text}</div>
      </div>
    ));
    return <div>{messages}</div>;
  } else {
    return <div>Нет сообщений</div>;
  }
};

export default MessageList;
