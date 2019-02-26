import { connect } from "react-redux";
import * as actions from "../actions";
import MessageList from "../components/MessageList";

const mapStateToProps = state => ({
  messages: state.dialog.message_set || []
});

export default connect(
  mapStateToProps,
  actions
)(MessageList);
