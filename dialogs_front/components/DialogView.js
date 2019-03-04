import React from "react";
import MessageList from "../containers/MessageList";
import MessageForm from "../containers/MessageForm";
import api from "../utils/api";

class DialogView extends React.Component {
  componentDidMount() {
    api.dialogs.get(this.props.dialog.id).then(this.props.saveDialog);
  }

  render() {
    return (
      <div>
        <button
          onClick={this.props.toDialogList}
          className="btn btn-secondary my-1"
        >
          К списку сообщений
        </button>
        <MessageList />
        <MessageForm />
      </div>
    );
  }
}

export default DialogView;
