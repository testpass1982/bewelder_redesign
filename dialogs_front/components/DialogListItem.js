import React from "react";

const DialogListItem = ({ dialog }) => {
  /*
  {
    id: int,
    members: [
      {id: int, name: str},
      {id: int, name: str},
    ],
    vacancy: int,
    theme: str,
  }
  */
  return <span>{dialog.theme}</span>;
};

export default DialogListItem;
