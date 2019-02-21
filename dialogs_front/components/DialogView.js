import React from "react";
import MessageList from "../containers/MessageList";
import api from "../utils/api";

class DialogView extends React.Component {
  componentDidMount() {
    api.dialogs.get(this.props.dialogId).then(this.props.saveDialog);
  }

  handleSubmit = event => {
    event.preventDefault();
    console.log("send message");
  };

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
        <h5>{this.props.dialog_id}</h5> */}
        <MessageList />
        <div>
          <form onSubmit={this.handleSubmit}>
            <div className="input-group">
              <textarea className="form-control" rows="8" />
              <div className="input-group-append">
                <button className="btn btn-success" type="submit">
                  Отправить
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    );
  }
}

export default DialogView;
