import React from "react";
import { CSSTransitionGroup } from "react-transition-group";
import MessageListItem from "./MessageListItem";
import "./animation.css";

class MessageList extends React.Component {
  messageList = React.createRef();

  componentDidUpdate() {
    this.scrollToBottom();
  }

  scrollToBottom = () => {
    const messageList = this.messageList.current;
    const { scrollHeight, clientHeight } = messageList;
    const maxScrollTop = scrollHeight - clientHeight;
    messageList.scrollTop = maxScrollTop > 0 ? maxScrollTop : 0;
  };

  render() {
    let messages = <div key="No messages">Нет сообщений</div>;
    if (this.props.messages && this.props.messages.length) {
      messages = this.props.messages.map(message => (
        <MessageListItem message={message} key={message.id} />
      ));
    }

    return (
      <div
        className="mb-3"
        style={{ height: "40vh", overflow: "auto" }}
        ref={this.messageList}
      >
        <CSSTransitionGroup
          transitionName="slide"
          transitionAppear={false}
          transitionAppearTimeout={1000}
          transitionEnterTimeout={1000}
          transitionLeave={false}
        >
          {messages}
        </CSSTransitionGroup>
      </div>
    );
  }
}

export default MessageList;
