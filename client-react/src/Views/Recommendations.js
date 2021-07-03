import React, { Component } from "react";

class Recommendations extends Component {
  constructor() {
    super();
    this.state = {
      data: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/btc/profit/details")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ data: data });
        });
    }, 15000);
  }

  render() {
    const { data } = this.state;
    var content = [];

    //profit/loss

    data.forEach((recom) => {
      content.push(
        <tr>
          <td className="column1">{recom.datetime}</td>
          <td className="column2">{recom.recommendation}</td>
          <td className="column3">
            {Number(recom["profit/loss"]).toLocaleString()}
          </td>
          <td className="column4">{Number(recom.price).toLocaleString()}</td>
        </tr>
      );
    });

    const table_content = <tbody>{content}</tbody>;

    return (
      <div className="row">
        <div className="col">
          <div className="container-table100">
            <div className="table-responsive">
              <table>
                <thead>
                  <tr className="table100-head">
                    <th className="column1">Time</th>
                    <th className="column2">Recommendation</th>
                    <th className="column3">Profit/Loss</th>
                    <th className="column4">Price</th>
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

export default Recommendations;
