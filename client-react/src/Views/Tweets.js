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
          borderColor: "rgba(68, 168, 184, 0.9)",
          fill: false,
        },
        {
          label: "Negative Tweets",
          data: [],
          pointBackgroundColor: [],
          borderColor: "rgba(139, 68, 246, 0.9)",
          fill: false,
        },
      ],
    };

    PositiveTweetsData.forEach((item) => {
      chartJSData.labels.push(item.datetime);
      chartJSData.datasets[0].data.push(item.count);
      chartJSData.datasets[0].pointBackgroundColor.push(
        "rgba(68, 168, 184, 0.9)"
      );
    });

    NegativeTweetsData.forEach((item) => {
      chartJSData.datasets[1].data.push(item.count);
      chartJSData.datasets[1].pointBackgroundColor.push(
        "rgba(139, 68, 246, 0.9)"
      );
    });

    const legend = {
      labels: {
        usePointStyle: true,
        fontColor: "rgba(255, 255, 255, 0.7)",
      },
      position: "right",
    };
    const options = {
      maintainAspectRatio: false,
      responsive: true,
      title: {
        display: true,
        text: "Tweets",
        fontColor: "rgba(255, 255, 255, 0.7)",
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
              color: "rgba(255, 255, 255, 0.034)",
            },
            ticks: {
              fontColor: "rgba(255, 255, 255, 0.7)", // this here
            },
            scaleLabel: {
              display: true,
              labelString: "Time",
              fontColor: "rgba(255, 255, 255, 0.7)",
            },
          },
        ],
        yAxes: [
          {
            display: true,
            gridLines: {
              display: true,
              color: "rgba(255, 255, 255, 0.034)",
            },
            ticks: {
              fontColor: "rgba(255, 255, 255, 0.7)", // this here
            },
            scaleLabel: {
              display: true,
              labelString: "Count",
              fontColor: "rgba(255, 255, 255, 0.7)",
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
