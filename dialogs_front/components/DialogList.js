import React from "react";
import DialogListItem from "./DialogListItem";
import api from "../utils/api";

class DialogList extends React.Component {
  componentDidMount() {
    api.dialogs.get().then(dialogs => {
      if (JSON.stringify(dialogs) !== JSON.stringify(this.props.dialogs)) {
        this.props.saveDialogList(dialogs);
      }
    });
  }

  render() {
    const dialogs = this.props.dialogs.map(dialog => (
      <a
        href="#"
        className="list-group-item list-group-item-action"
        key={dialog.id}
        onClick={() => {
          this.props.toDialogView(dialog.id);
        }}
      >
        <DialogListItem dialog={dialog} />
      </a>
    ));
    return (
      <div className="my-3">
        <div className="list-group">{dialogs}</div>
      </div>
    );
  }
}

export default DialogList;
