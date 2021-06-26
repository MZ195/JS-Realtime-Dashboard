import React, { Component } from "react";

class DailySummary extends Component {
  constructor() {
    super();
    this.state = {
      data: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/daily_summary/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ data: data });
        });
    }, 30000);
  }

  render() {
    const { data } = this.state;
    var content = [];

    for (var i = 0; i < data.length; i++) {
      const current_element = data[i];
      var date_time = current_element.datetime;
      var positive_tweets = current_element.pos;
      var price = Number(current_element.price).toLocaleString();
      var negative_tweets = current_element.neg;
      content.push(
        <tr>
          <td className="column1">{date_time}</td>
          <td className="column2">{positive_tweets}</td>
          <td className="column3">{negative_tweets}</td>
          <td className="column4">{price}</td>
        </tr>
      );
    }

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
                    <th className="column2">Pos+</th>
                    <th className="column3">Neg-</th>
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

export default DailySummary;
