import React from "react";
import { CSSTransitionGroup } from "react-transition-group";
import "./animation.css";

const AnimateThis = props => {
  const timeout = props.timeout || 1000;
  const useDiv = !!props.useDiv;
  const transitionLeave = !!props.transitionLeave;
  return (
    <CSSTransitionGroup
      transitionName="slide"
      transitionAppear={true}
      transitionAppearTimeout={timeout}
      transitionEnterTimeout={timeout}
      transitionLeaveTimeout={timeout}
      transitionLeave={transitionLeave}
      {...(useDiv
        ? {
            component: "div",
            className: "anim-container"
          }
        : {})}
    >
      {props.children}
    </CSSTransitionGroup>
  );
};

export default AnimateThis;
