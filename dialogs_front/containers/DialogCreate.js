import { connect } from "react-redux";
import * as actions from "../actions";
import DialogCreate from "../components/DialogCreate";

const mapStateToProps = state => ({
  opponentId: state.opponentId
});

export default connect(
  mapStateToProps,
  actions
)(DialogCreate);
