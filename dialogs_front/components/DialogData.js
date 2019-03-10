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
  const creatorIndex = members.findIndex(e => e.is_creator);
  const creator = members[creatorIndex];
  const opponent = members[1 - creatorIndex];
  return (
    <div>
      <b className="text-primary">{creator.name}</b>
      <br />
      {opponent ? (
        <span>
          {opponent.name}
          <br />
        </span>
      ) : null}
      <strong>Тема:</strong> <span className="font-italic">{dialog.theme}</span>
    </div>
  );
};

export default DialogData;
