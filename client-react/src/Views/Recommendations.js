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

    data.forEach((recom) => {
      content.push(
        <tr>
          <td className="column11">{recom.datetime}</td>
          <td className="column22">{recom.recommendation}</td>
          <td className="column5">{Number(recom.price).toLocaleString()}</td>
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
                    <th className="column11">Time</th>
                    <th className="column22">Recommendation</th>
                    <th className="column5">Price</th>
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
