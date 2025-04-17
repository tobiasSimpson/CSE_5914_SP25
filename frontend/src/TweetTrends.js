import Button from "react-bootstrap/Button";
import React, { useEffect, useState } from "react";
import { Chart } from "react-google-charts";

const TweetTrends = ({chartData, chartTitle, setTweets}) => {

  const [options, setOptions] = useState(null);

  useEffect(() => {
    setOptions({
      title: `Popularity of ${chartTitle}`,
      hAxis: { 
        title: "Sentiment",
        gridlines: {color: "none"}
      },
      vAxis: { 
        title: "Number of Tweets",
        minValue: 0,
       },
      backgroundColor: "transparent",
      legend: { position: "none" },
    })
  }, [chartTitle])


  return (
    <div style={{ width: "100%", height: "400px", display: "flex", justifyContent: "center", backgroundColor: "#f8f9fa", borderRadius: "5px", boxShadow: "0px 1px 3px #999"}}>
      {chartData === null ? <div style = {{flexGrow: 1}}>Loading...</div> :
        <div style ={{flexGrow: 1}}>
          <ChartMemoized
            chartType="ColumnChart"
            width="100%"
            height="100%"
            data={chartData}
            options={options}
          />
        </div>
      }
    </div>
  );
};

// Only rerender the chart when the title has changed
// This also means that the selection wont always be immediately cleared
const ChartMemoized = React.memo(Chart, (old, current) => old.options == null || current.options.title === old.options.title);

export default TweetTrends;
