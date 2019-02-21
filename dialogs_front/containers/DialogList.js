import { connect } from "react-redux";
import * as actions from "../actions";
import DialogList from "../components/DialogList";

const mapStateToProps = state => ({
  dialogs: state.dialogs
});

export default connect(
  mapStateToProps,
  actions
)(DialogList);
