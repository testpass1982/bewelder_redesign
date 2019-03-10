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
      <div className="d-flex flex-column" style={{ maxHeight: "80vh" }}>
        <div>
          <button
            onClick={this.props.toDialogList}
            className="btn btn-secondary my-1"
          >
            К списку сообщений
          </button>
        </div>
        <MessageList />
        <MessageForm />
      </div>
    );
  }
}

export default DialogView;
