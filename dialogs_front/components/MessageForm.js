import React from "react";
import api from "../utils/api";

class MessageForm extends React.Component {
  state = {
    messageText: ""
  };

  handleChange = event => {
    this.setState({ messageText: event.target.value });
  };

  handleSubmit = event => {
    event.preventDefault();
    const { dialog } = this.props;
    const { messageText } = this.state;
    api.dialogs
      .sendMessage(dialog.id, messageText)
      .then(this.props.appendMessage);
    this.setState({ messageText: "" });
  };

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="input-group">
          <textarea
            className="form-control"
            rows="8"
            value={this.state.messageText}
            onChange={this.handleChange}
          />
          <div className="input-group-append">
            <button className="btn btn-success" type="submit">
              Отправить
            </button>
          </div>
        </div>
      </form>
    );
  }
}

export default MessageForm;
