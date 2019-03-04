import React from "react";
import api from "../utils/api";

class DialogCreate extends React.Component {
  state = {
    theme: "",
    text: ""
  };

  handleSubmit = event => {
    event.preventDefault();
    const { theme, text } = this.state;
    api.dialogs
      .create(this.props.opponentId, null, theme, text)
      .then(dialog => this.props.toDialogView(dialog.id));
  };

  handleChange = event => {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  };

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <label htmlFor="themeInputId">Тема сообщения</label>
            <input
              type="text"
              className="form-control"
              id="themeInputId"
              name="theme"
              onChange={this.handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="textMessageInputId">Текст сообщения:</label>
            <textarea
              className="form-control"
              id="textMessageInputId"
              rows="8"
              name="text"
              onChange={this.handleChange}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary btn-block">
            Отправить
          </button>
        </form>
      </div>
    );
  }
}

export default DialogCreate;
