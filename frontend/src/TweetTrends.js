import Button from "react-bootstrap/Button";
import React, { useEffect, useState } from "react";
import { Chart } from "react-google-charts";

const TweetTrends = ({chartData, chartTitle}) => {
  
  const chartBackgroundColor = "#f8f9fa";

  const [options, setOptions] = useState(null);

  useEffect(() => {
    setOptions({
      title: `Popularity of ${chartTitle} Over Time`,
      // curveType: "function",
      hAxis: { 
        title: "Date",
        // Don't show every date
        maxAlterations: 1,
        minTextSpacing: 20,
        format: "MMM yyyy",
        gridlines: {color: "none"}

      },
      vAxis: { 
        title: "Mentions",
        minValue: 0,
       },
      backgroundColor: chartBackgroundColor,
      legend: { position: "none" },

      // Hide the sentiment data
      series: {
        1: { 
          visibleInLegend: false,
          lineWidth: 0,
          //no tooltip
          enableInteractivity: false,
        },
      },
    })
  }, [chartTitle])

  const eventListeners = [{
      eventName: "select",
      callback({ chartWrapper }) {
        const selection = chartWrapper.getChart().getSelection()
        if (selection.length === 0)
          setSelectedData(null)
        else {
          const num = selection[0].row;
          setSelectedData({
            date: chartData[num + 1][0],
            mentions: chartData[num + 1][1], 
            sentiment: chartData[num + 1][2]
          });
        }
        
      },
    }]

  const [selectedData, setSelectedData] = useState(null);

  // Reset the selection when the chart changes
  useEffect(() => setSelectedData(null), [chartTitle])

  const dateToString = (date) => {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[date.getUTCMonth()] + " " + date.getUTCFullYear()
  }

  const sentimentToString = (sentiment) => {
    // Color from red to green
    const color = "hsl(" + (sentiment * 120) + ", 100%, 35%)"
    const sentimentString = Math.floor(sentiment * 10 +1) + "/10"
    return <span style={{color: color}}>{sentimentString}</span>
  }


  return (
    <div style={{ width: "100%", height: "400px", display: "flex", justifyContent: "center", backgroundColor: "#f8f9fa"}}>
      {chartData === null ? <div style = {{flexGrow: 1}}>Loading...</div> :
        <div style ={{flexGrow: 1}}>
          <ChartMemoized
            chartType="LineChart"
            width="100%"
            height="100%"
            data={chartData}
            options={options}
            chartEvents={eventListeners}
          />
        </div>
      }

      <div style={{width:"200px", fontSize:"1.1rem", padding:"50px 30px 50px 0"}}>
        <div style = {{fontWeight: 600, width: "100%", borderBottom: "1px solid #1e90ff", marginBottom: 10}}>Selection</div> 
        
        {selectedData === null ? <span>No selection</span> :
          <div>
            <span>{dateToString(selectedData.date)}</span>
            <div style = {{margin: "10px 0"}}>Sentiment: {sentimentToString(selectedData.sentiment)}</div>
            <Button variant="primary" onClick={()=> alert("Not yet implemented")}>Generate Tweets</Button>
          </div>
        }
        
      </div>
    </div>
  );
};

// Only rerender the chart when the title has changed
// This also means that the selection wont always be immediately cleared
const ChartMemoized = React.memo(Chart, (old, current) => current.options.title === old.options.title);

export default TweetTrends;
