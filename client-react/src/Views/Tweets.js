import React, { Component } from "react";
import { Line } from "react-chartjs-2";

class Tweets extends Component {
  constructor() {
    super();
    this.state = {
      PositiveTweetsData: [],
      NegativeTweetsData: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/pos/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ PositiveTweetsData: data });
        });

      fetch("http://localhost:9000/neg/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ NegativeTweetsData: data });
        });
    }, 30000);
  }

  render() {
    const { PositiveTweetsData } = this.state;
    const { NegativeTweetsData } = this.state;

    // var canvas = document.getElementById("lineChart");
    // var ctx = canvas.getContext("2d");

    // var gradientFill = ctx.createLinearGradient(0, 0, 0, 290);
    // gradientFill.addColorStop(0, "rgba(173, 53, 186, 1)");
    // gradientFill.addColorStop(1, "rgba(173, 53, 186, 0.1)");

    let chartJSData = {
      labels: [],
      datasets: [
        {
          label: "Positive Tweets",
          data: [],
          pointBackgroundColor: [],
          borderColor: "rgba(0, 186, 156, 0.9)",
          fill: false,
        },
        {
          label: "Negative Tweets",
          data: [],
          pointBackgroundColor: [],
          borderColor: "rgba(230, 73, 84, 0.9)",
          fill: false,
        },
      ],
    };

    PositiveTweetsData.forEach((item) => {
      chartJSData.labels.push(item.datetime);
      chartJSData.datasets[0].data.push(item.count);
      chartJSData.datasets[0].pointBackgroundColor.push(
        "rgba(0, 186, 156, 0.9)"
      );
    });

    NegativeTweetsData.forEach((item) => {
      chartJSData.datasets[1].data.push(item.count);
      chartJSData.datasets[1].pointBackgroundColor.push(
        "rgba(230, 73, 84, 0.9)"
      );
    });

    const legend = {
      labels: {
        usePointStyle: true,
      },
      position: "right",
    };
    const options = {
      maintainAspectRatio: false,
      responsive: true,
      title: {
        display: true,
        text: "Tweets",
      },
      tooltips: {
        mode: "label",
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      scales: {
        xAxes: [
          {
            display: true,
            gridLines: {
              display: true,
            },
            scaleLabel: {
              display: true,
              labelString: "Time",
            },
          },
        ],
        yAxes: [
          {
            display: true,
            gridLines: {
              display: true,
            },
            scaleLabel: {
              display: true,
              labelString: "Count",
            },
          },
        ],
      },
    };
    return (
      <div className="chartLine">
        <Line data={chartJSData} options={options} legend={legend} />
      </div>
    );
  }
}

export default Tweets;