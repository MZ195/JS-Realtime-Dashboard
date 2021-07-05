import React from "react";
import "./App.css";

import "bootstrap/dist/css/bootstrap.min.css";
import "materialize-css";

import { Spring } from "react-spring/renderprops";

import { Container } from "react-bootstrap";
import Tweets from "./Views/Tweets";
import NavBar from "./Views/NavBar";
import Summary from "./Views/Summary";
import BTPrice from "./Views/BTPrice";
import ActionButtons from "./Views/ActionButtons";
import ScoresSummary from "./Views/ScoresSummary";
import Recommendations from "./Views/Recommendations";

function App() {
  return (
    <Spring
      from={{ opacity: 0, marginTop: -500 }}
      to={{ opacity: 1, marginTop: 0 }}
    >
      {(props) => (
        <div style={props}>
          <div className="App">
            <NavBar />
            <header className="App-header">
              <Container fluid className="content">
                <div className="row">
                  <div className="col">
                    <div className="overview">
                      <Summary />
                    </div>
                  </div>
                </div>
                <div className="row">
                  <div className="col">
                    <div className="statistics2">
                      <ActionButtons />
                      <BTPrice />
                    </div>
                  </div>
                </div>
                <div className="row">
                  <div className="col-8">
                    <div className="statistics2">
                      <Tweets />
                    </div>
                  </div>
                  <div className="col">
                    <div className="row">
                      <div className="daily_summary statistics2">
                        <ScoresSummary />
                      </div>
                    </div>
                    <div className="row">
                      <div className="col">
                        <div className="row">
                          <div className="daily_summary statistics2">
                            <Recommendations />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Container>
            </header>
          </div>
        </div>
      )}
    </Spring>
  );
}

export default App;
