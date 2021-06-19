import React from "react";
import "./App.css";

import "bootstrap/dist/css/bootstrap.min.css";
import { Container } from "react-bootstrap";
import AllTransactions from "./Views/AllTransactions";
import CurrentWeekBar from "./Views/CurrentWeekBar";
import CurrentWeekPie from "./Views/CurrentWeekPie";
import AllTransactionsSummery from "./Views/AllTransactionsSummery";
import PreviousMonthPie from "./Views/PreviousMonthPie";
import PreviousMonthBar from "./Views/PreviousMonthBar";
import CurrentWeekTransactionsSummery from "./Views/CurrentWeekTransactionsSummery";
import Statistics from "./Views/Statistics";
import CurrentMonthPie from "./Views/CurrentMonthPie";
import CurrentMonthBar from "./Views/CurrentMonthBar";
import AllTransactionsPerWeek from "./Views/AllTransactionsPerWeek";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Container fluid>
          <div className="row">
            <div className="col">
              <AllTransactionsSummery />
            </div>
          </div>
          <div className="row">
            <div className="col">
              <CurrentWeekTransactionsSummery />
            </div>
          </div>
          <div className="row">
            <div className="col">
              <Statistics />
            </div>
          </div>
          <div className="row">
            <div className="col">
              <div className="statistics2">
                <CurrentWeekBar />
              </div>
            </div>
            <div className="col">
              <div className="statistics2">
                <CurrentWeekPie />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <div className="statistics2">
                <CurrentMonthBar />
              </div>
            </div>
            <div className="col">
              <div className="statistics2">
                <CurrentMonthPie />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <div className="statistics2">
                <PreviousMonthBar />
              </div>
            </div>
            <div className="col">
              <div className="statistics2">
                <PreviousMonthPie />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <div className="statistics2">
                <AllTransactionsPerWeek />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <div className="statistics2">
                <AllTransactions />
              </div>
            </div>
          </div>
        </Container>
      </header>
    </div>
  );
}

export default App;
