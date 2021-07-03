import React, { Component } from "react";

class ScoresSummary extends Component {
  constructor() {
    super();
    this.state = {
      arima_score: [],
      varmax_score: [],
      ses_score: [],
      rf_score: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/score/ARIMA")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ arima_score: data });
        });

      fetch("http://localhost:9000/score/VARMAX")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ varmax_score: data });
        });

      fetch("http://localhost:9000/score/SES")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ ses_score: data });
        });

      fetch("http://localhost:9000/score/RF")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ rf_score: data });
        });
    }, 30000);
  }

  render() {
    const { arima_score } = this.state;
    const { varmax_score } = this.state;
    const { ses_score } = this.state;
    const { rf_score } = this.state;

    var content = [];

    content.push(
      <tr>
        <td className="column1">Random Forest</td>
        <td className="column2">{Number(rf_score.RMSE).toLocaleString()}</td>
        <td className="column3">{Number(rf_score.MAE).toLocaleString()}</td>
        <td className="column4">{Number(rf_score.MSE).toLocaleString()}</td>
      </tr>,
      <tr>
        <td className="column1">VARMAX</td>
        <td className="column2">
          {Number(varmax_score.RMSE).toLocaleString()}
        </td>
        <td className="column3">{Number(varmax_score.MAE).toLocaleString()}</td>
        <td className="column4">{Number(varmax_score.MSE).toLocaleString()}</td>
      </tr>,
      <tr>
        <td className="column1">ARIMA</td>
        <td className="column2">{Number(arima_score.RMSE).toLocaleString()}</td>
        <td className="column3">{Number(arima_score.MAE).toLocaleString()}</td>
        <td className="column4">{Number(arima_score.MSE).toLocaleString()}</td>
      </tr>,
      <tr>
        <td className="column1">SES</td>
        <td className="column2">{Number(ses_score.RMSE).toLocaleString()}</td>
        <td className="column3">{Number(ses_score.MAE).toLocaleString()}</td>
        <td className="column4">{Number(ses_score.MSE).toLocaleString()}</td>
      </tr>
    );

    const table_content = <tbody>{content}</tbody>;

    return (
      <div className="row">
        <div className="col">
          <div className="container-table100">
            <div className="table-responsive">
              <table>
                <thead>
                  <tr className="table100-head">
                    <th className="column1">Model</th>
                    <th className="column2">RMSE</th>
                    <th className="column3">MAE</th>
                    <th className="column4">MSE</th>
                  </tr>
                </thead>
                {table_content}
              </table>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ScoresSummary;
