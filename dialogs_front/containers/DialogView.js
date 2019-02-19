import { connect } from "react-redux";
import * as actions from "../actions/viewActions";
import DialogView from "../components/DialogView";

const mapStateToProps = state => ({
  dialog_id: state.dialog_id
});

export default connect(
  mapStateToProps,
  actions
)(DialogView);
