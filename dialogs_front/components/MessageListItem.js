import React from "react";

const MessageListItem = ({ message }) => {
  // {
  //   id: int,
  //   user: {
  //     id: int,
  //     name: str
  //   },
  //   text: str,
  //   sent_at: str,
  //   dialog: int
  // }
  const date = new Date(message.sent_at);
  return (
    <div>
      <div className="d-flex w-100 justify-content-between">
        <h5 className="mb-1">{message.user.name}</h5>
        <div>
          <span className="badge badge-info badge-pill">
            {date.toLocaleString("ru-RU")}
          </span>
        </div>
      </div>
      <p
        className="mb-1 pl-5"
        style={{ whiteSpace: "pre-wrap", overflow: "auto" }}
      >
        {message.text}
      </p>
      <hr />
    </div>
  );
};

export default MessageListItem;
