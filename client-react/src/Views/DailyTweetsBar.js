import React, { Component } from "react";
import { Bar } from "react-chartjs-2";

class DailyTweetsBar extends Component {
  constructor() {
    super();
    this.state = {
      myChartData: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/daily_tweets/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ myChartData: data });
        });
    }, 30000);
  }

  render() {
    const { myChartData } = this.state;

    let chartJSData = {
      labels: [],
      datasets: [
        {
          label: "Positive Tweets",
          data: [],
          backgroundColor: "rgba(0, 186, 156, 0.9)",
        },
        {
          label: "Negative Tweets",
          data: [],
          backgroundColor: "rgba(230, 73, 84, 0.9)",
        },
      ],
    };

    myChartData.forEach((item) => {
      chartJSData.labels.push(item.datetime);
      chartJSData.datasets[0].data.push(item.pos);
      chartJSData.datasets[1].data.push(item.neg);
    });

    const legend = {
      display: true,
      position: "bottom",
      labels: {
        fontColor: "#000",
      },
    };
    const options = {
      responsive: true,
      title: {
        display: true,
        text: "Today's Tweets Analysis",
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
      <div>
        <Bar data={chartJSData} options={options} legend={legend} />
      </div>
    );
  }
}

export default DailyTweetsBar;