import React from "react";

const DialogData = ({ dialog }) => {
  /*
  message schema
  {
    id: int,
    members: [
      {id: int, name: str, is_creator: bool},
      {id: int, name: str, is_creator: bool},
    ],
    vacancy: int,
    theme: str,
  }
  */
  let { members } = dialog;
  const creator = members.find(e => e.is_creator);
  return (
    <div>
      <b className="text-primary">{creator.name}</b>:{" "}
      <span className="font-italic">{dialog.theme}</span>
    </div>
  );
};

export default DialogData;
