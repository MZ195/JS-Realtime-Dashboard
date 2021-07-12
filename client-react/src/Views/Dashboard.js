import React, { Component } from "react";
import { Container } from "react-bootstrap";
import Tweets from "./Tweets";
import NavBar from "./NavBar";
import Summary from "./Summary";
import BTPrice from "./BTPrice";
import ActionButtons from "./ActionButtons";
import ScoresSummary from "./ScoresSummary";
import Recommendations from "./Recommendations";

class Dashboard extends Component {
  constructor() {
    super();
    this.state = {
      isLoading: false,
    };
  }

  render() {
    return this.state.isLoading ? (
      <div className="row loading-view">
        <p>Loading...</p>
      </div>
    ) : (
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
                      <div className="daily_summary statistics2 recommendations">
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
    );
  }
}

export default Dashboard;
