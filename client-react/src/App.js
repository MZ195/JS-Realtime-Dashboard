import React from "react";
import "./App.css";

import "bootstrap/dist/css/bootstrap.min.css";
import "materialize-css";

import { Container } from "react-bootstrap";
import Tweets from "./Views/Tweets";
import NavBar from "./Views/NavBar";
import Summary from "./Views/Summary";
import BTPrice from "./Views/BTPrice";
import DailyTweetsBar from "./Views/DailyTweetsBar";
import DailySummary from "./Views/DailySummary";

function App() {
  return (
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
            <div className="col-8">
              <div className="statistics2">
                <Tweets />
              </div>
            </div>
            <div className="col-4">
              <div className="row">
                <div className="col">
                  <div className="daily_summary">
                    <DailySummary />
                  </div>
                </div>
              </div>
              <div className="row">
                <div className="col">
                  <div className="statistics2">
                    <DailyTweetsBar />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <div className="statistics2">
                <BTPrice />
              </div>
            </div>
          </div>
        </Container>
      </header>
    </div>
  );
}

export default App;
