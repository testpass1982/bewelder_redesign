import { connect } from "react-redux";
import * as actions from "../actions";
import MessageForm from "../components/MessageForm";

const mapStateToProps = state => ({
  dialog: state.dialog
});

export default connect(
  mapStateToProps,
  actions
)(MessageForm);
