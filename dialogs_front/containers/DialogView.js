import { connect } from "react-redux";
import * as actions from "../actions";
import DialogView from "../components/DialogView";

const mapStateToProps = state => ({
  dialog: state.dialog
});

export default connect(
  mapStateToProps,
  actions
)(DialogView);
