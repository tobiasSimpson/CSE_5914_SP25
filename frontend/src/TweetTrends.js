import React, { useState } from "react";
import { Chart } from "react-google-charts";

const TweetTrends = () => {
  // Example Data: Date vs Tweet Mentions
  const data = [
    ["Date", "Mentions", "Sentiment"],
    ["2024-01-20", 200, 0],
    ["2024-01-21", 250, 0.7],
    ["2024-01-22", 400, 0.2],
    ["2024-01-23", 350, 0.6],
    ["2024-01-24", 500, 0.5],
  ];


  const [options] = useState({
    title: "Popularity Over Time",
    curveType: "function",
    hAxis: { title: "Date" },
    vAxis: { title: "Mentions" },
    backgroundColor: "#f8f9fa",
    legend: { position: "bottom" },

    // Hide the sentiment data
    series: {
      1: { 
        visibleInLegend: false,
        lineWidth: 0

       },
    },


  });

  const eventListeners = [{
      eventName: "select",
      callback({ chartWrapper }) {
        const selection = chartWrapper.getChart().getSelection()
        if (selection.length === 0)
          setSelectedDate(new Date(0))
        else {
          const num = selection[0].row;
          setSelectedDate(new Date(data[num + 1][0] + "T00:00:00.000Z"))
        }
        
      },
    }]

  const [selectedDate, setSelectedDate] = useState(new Date(0));

  const dateToString = (date) => {
    if (date.getTime() === 0) return "No date selected"
    return date.getUTCFullYear() + "-" + (date.getUTCMonth() + 1) + "-" + date.getUTCDate()
  }

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

      <div style={{width:"100px", fontSize:"1.1rem"}}>
        <div style = {{fontWeight: 600, width: "100%", borderBottom: "1px solid #1e90ff", marginBottom: 10}}>Selection</div> 
        <span>{dateToString(selectedDate)}</span>
      </div>
    </div>
  );
};

export default TweetTrends;
