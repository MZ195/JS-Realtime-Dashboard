import React from "react";
import "./App.css";

import "bootstrap/dist/css/bootstrap.min.css";
import "materialize-css";

import { Spring } from "react-spring/renderprops";

import Dashboard from "./Views/Dashboard";

function App() {
  return (
    <Spring
      from={{ opacity: 0, marginTop: -500 }}
      to={{ opacity: 1, marginTop: 0 }}
    >
      {(props) => (
        <div style={props}>
          <Dashboard />
        </div>
      )}
    </Spring>
  );
}

export default App;
