import React, { Component } from "react";
import { Line } from "react-chartjs-2";
import { BigNumber } from "bignumber.js";

class BTPrice extends Component {
  constructor() {
    super();
    this.state = {
      BTC_Data: [],
      BTC_Prediction_ARIMA: [],
      BTC_Prediction_VARMAX: [],
      BTC_Prediction_SES: [],
      BTC_Prediction_RF: [],
      BTC_Prediction_overall: [],
      BTC_last_operation: {},
    };
  }

  componentDidMount() {
    setInterval(async () => {
      var v = new Date();
      if (
        v.getSeconds() === 33 ||
        v.getSeconds() === 3 ||
        v.getSeconds() === 13 ||
        v.getSeconds() === 43
      ) {
        fetch("http://localhost:9000/btc/price")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Data: data });
          });

        fetch("http://localhost:9000/predict/ARIMA")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_ARIMA: data });
          });

        fetch("http://localhost:9000/predict/VARMAX")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_VARMAX: data });
          });

        fetch("http://localhost:9000/predict/SES")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_SES: data });
          });

        fetch("http://localhost:9000/predict/RF")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_RF: data });
          });

        fetch("http://localhost:9000/predict/overall")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_overall: data });
          });

        fetch("http://localhost:9000/btc/profit/details/lastOperation")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_last_operation: data });
          });
      }
    }, 60);
  }

  render() {
    const { BTC_Data } = this.state;
    const { BTC_Prediction_ARIMA } = this.state;
    const { BTC_Prediction_VARMAX } = this.state;
    const { BTC_Prediction_SES } = this.state;
    const { BTC_Prediction_RF } = this.state;
    const { BTC_Prediction_overall } = this.state;
    const { BTC_last_operation } = this.state;

    let chartJSData = {
      labels: [],
      datasets: [
        {
          label: "BTC Price",
          data: [],
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(88, 216, 163, 0.9)",
          // fill: true,
          backgroundColor: "rgba(88, 216, 163, 0.03)",
        },
        {
          label: "BTC Price ARIMA",
          data: [],
          hidden: true,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(139, 68, 246, 0.9)",
          // fill: true,
          backgroundColor: "rgba(139, 68, 246, 0.03)",
        },
        {
          label: "BTC Price VARMAX",
          data: [],
          hidden: true,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(87, 199, 212, 0.9)",
          // fill: true,
          backgroundColor: "rgba(87, 199, 212, 0.03)",
        },
        {
          label: "BTC Price SES",
          data: [],
          hidden: true,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(33, 150, 243, 0.9)",
          // fill: true,
          backgroundColor: "rgba(33, 150, 243, 0.03)",
        },
        {
          label: "BTC Price RF",
          data: [],
          hidden: true,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(255, 121, 198, 0.9)",
          // fill: true,
          backgroundColor: "rgba(255, 121, 198, 0.03)",
        },
        {
          label: "BTC Price Overall",
          data: [],
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(233, 30, 99, 0.9)",
          // fill: true,
          backgroundColor: "rgba(233, 30, 99, 0.03)",
        },
        {
          label: "Buying Price",
          data: [],
          hidden: false,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(255, 175, 0, 0.9)",
          fill: false,
        },
      ],
    };

    BTC_Data.forEach((item) => {
      chartJSData.labels.push(item.datetime);
      chartJSData.datasets[0].data.push(item.price);
      chartJSData.datasets[0].pointBackgroundColor.push(
        "rgba(88, 216, 163, 0.9)"
      );
    });

    BTC_Prediction_ARIMA.forEach((item) => {
      if (!chartJSData.labels.includes(item.datetime)) {
        var currentHour = item.datetime.substring(0, 2);
        var currentMinutes = item.datetime.substring(3, 5);
        var currentSeconds = item.datetime.substring(6, 8);
        var dateLimit = new Date(new Date() - 28 * 60000);
        var v = new Date();

        if (currentHour === "23") {
          v.setDate(v.getDate() - 1);
          v.setMinutes(currentMinutes);
          v.setSeconds(currentSeconds);
          v.setHours(currentHour);
        } else {
          v.setMinutes(currentMinutes);
          v.setSeconds(currentSeconds);
          v.setHours(currentHour);
        }

        let limit_num = BigNumber(dateLimit.getTime());
        let item_num = BigNumber(v.getTime());

        let diff = Number(limit_num.minus(item_num));

        if (diff < 0) {
          chartJSData.labels.push(item.datetime);
        }
      }

      if (BTC_last_operation.datetime !== undefined) {
        var currentHour2 = BTC_last_operation.datetime.substring(0, 2);
        var currentMinutes2 = BTC_last_operation.datetime.substring(3, 5);
        var currentSeconds2 = BTC_last_operation.datetime.substring(6, 8);

        var currentHour1 = item.datetime.substring(0, 2);
        var currentMinutes1 = item.datetime.substring(3, 5);
        var currentSeconds1 = item.datetime.substring(6, 8);

        var last_operation = new Date();
        var current_item = new Date();

        if (currentHour2 === "23") {
          last_operation.setDate(last_operation.getDate() - 1);
          last_operation.setMinutes(currentMinutes2);
          last_operation.setSeconds(currentSeconds2);
          last_operation.setHours(currentHour2);

          current_item.setDate(current_item.getDate() - 1);
          current_item.setMinutes(currentMinutes1);
          current_item.setSeconds(currentSeconds1);
          current_item.setHours(currentHour1);
        } else {
          last_operation.setMinutes(currentMinutes2);
          last_operation.setSeconds(currentSeconds2);
          last_operation.setHours(currentHour2);

          current_item.setMinutes(currentMinutes1);
          current_item.setSeconds(currentSeconds1);
          current_item.setHours(currentHour1);
        }

        let last_operation_num = BigNumber(last_operation.getTime());
        let current_item_num = BigNumber(current_item.getTime());

        let diff = Number(last_operation_num.minus(current_item_num));

        if (BTC_last_operation.price !== 0.0) {
          chartJSData.datasets[6].data.push(BTC_last_operation.price);
          if (diff >= 0) {
            console.log(diff);
            chartJSData.datasets[6].pointBackgroundColor.push(
              "rgba(255, 123, 0, 0.9)"
            );
          } else {
            chartJSData.datasets[6].pointBackgroundColor.push(
              "rgba(255, 175, 0, 0.9)"
            );
          }
        }
      }

      chartJSData.datasets[1].data.push(item.price);
      chartJSData.datasets[1].pointBackgroundColor.push(
        "rgba(139, 68, 246, 0.9)"
      );
    });

    BTC_Prediction_VARMAX.forEach((item) => {
      chartJSData.datasets[2].data.push(item.price);
      chartJSData.datasets[2].pointBackgroundColor.push(
        "rgba(87, 199, 212, 0.9)"
      );
    });

    BTC_Prediction_SES.forEach((item) => {
      chartJSData.datasets[3].data.push(item.price);
      chartJSData.datasets[3].pointBackgroundColor.push(
        "rgba(33, 150, 243, 0.9)"
      );
    });

    BTC_Prediction_RF.forEach((item) => {
      chartJSData.datasets[4].data.push(item.price);
      chartJSData.datasets[4].pointBackgroundColor.push(
        "rgba(255, 121, 198, 0.9)"
      );
    });

    BTC_Prediction_overall.forEach((item) => {
      chartJSData.datasets[5].data.push(item.price);
      chartJSData.datasets[5].pointBackgroundColor.push(
        "rgba(233, 30, 99, 0.9)"
      );
    });

    const legend = {
      labels: {
        usePointStyle: true,
        fontColor: "rgba(255, 255, 255, 0.7)",
      },
      position: "bottom",
    };
    const options = {
      maintainAspectRatio: false,
      responsive: true,
      title: {
        display: true,
        text: "Bitcoin Price",
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
              labelString: "Time (30 min Window)",
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
              labelString: "Price (USD)",
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

export default BTPrice;
