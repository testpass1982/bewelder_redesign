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
          className="btn btn-secondary my-3"
        >
          К списку сообщений
        </button>
        {/* <h4>Dialog view</h4>
        <h5>{this.props.dialogId}</h5> */}
        <MessageList />
        <MessageForm />
      </div>
    );
  }
}

export default DialogView;
