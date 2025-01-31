import React from "react";
import { Chart } from "react-google-charts";

const TweetTrends = () => {
  // Example Data: Date vs Tweet Mentions
  const data = [
    ["Date", "Sentiment"],
    ["2024-01-20", 200],
    ["2024-01-21", 250],
    ["2024-01-22", 400],
    ["2024-01-23", 350],
    ["2024-01-24", 500],
  ];

  const options = {
    title: "Twitter Sentiments Over Time",
    curveType: "function",
    legend: { position: "bottom" },
    hAxis: { title: "Date" },
    vAxis: { title: "Mentions" },
    backgroundColor: "#f8f9fa",
  };

  const eventListeners = [{
      eventName: "select",
      callback({ chartWrapper }) {
        console.log("Selected ", chartWrapper.getChart().getSelection());
      },
    }]

  return (
    <div style={{ width: "100%", height: "400px", display: "flex", justifyContent: "center" }}>
      <Chart
        chartType="LineChart"
        width="90%"
        height="100%"
        data={data}
        options={options}
        chartEvents={eventListeners}
      />
    </div>
  );
};

export default TweetTrends;
