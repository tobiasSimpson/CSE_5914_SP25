import Button from "react-bootstrap/Button";
import React, { useEffect, useState } from "react";
import { Chart } from "react-google-charts";

const TweetTrends = ({chartData, chartTitle, setTweets}) => {

  const [options, setOptions] = useState(null);

  const [generateTweetsDisabled, setGenerateTweetsDisabled] = useState(false);

  // Sample function to generate tweets
  const generateTweets = async () => {
    if (generateTweetsDisabled) return;
    setGenerateTweetsDisabled(true);
    const tweetTemplates = [
      "AI is taking over the world! 🌍🚀",
      "Just read an amazing article on #MachineLearning!",
      "Data Science is the future of tech! 🔥",
      "Is AI going too far? 🤔",
      "Tech trends are evolving faster than ever!",
      "Big data is reshaping everything we do. #Analytics",
      "Another breakthrough in #ArtificialIntelligence!",
      "The future of work is AI-driven. 🚀",
      "Are we ready for AGI? #ArtificialGeneralIntelligence",
      "Sentiment analysis is fascinating! 📊",
    ];

    // Shuffle and select 5 random tweets
    const randomTweets = tweetTemplates.sort(() => 0.5 - Math.random()).slice(0, 5);
    await new Promise(r => setTimeout(r, 500));
    setTweets(randomTweets);
    setGenerateTweetsDisabled(false);
  };

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
      backgroundColor: "transparent",
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

  const eventListeners = [
    {
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
        
      }
    }
  ]

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
    <div style={{ width: "100%", height: "400px", display: "flex", justifyContent: "center", backgroundColor: "#f8f9fa", borderRadius: "5px", boxShadow: "0px 1px 3px #999"}}>
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
        <div style = {{fontWeight: 600, width: "100%", borderBottom: "1px solid #1e90ff", marginBottom: 10, fontSize: "1.1em", color: "#444"}}>Selection</div> 
        
        {selectedData === null ? <span>Select a date using the graph</span> :
          <div>
            <span>{dateToString(selectedData.date)}</span>
            <div style = {{margin: "10px 0"}}>Sentiment: {sentimentToString(selectedData.sentiment)}</div>
            <Button variant="primary" onClick={generateTweets} disabled={generateTweetsDisabled}>Generate Tweets</Button>
          </div>
        }
      </div>
    </div>
  );
};

// Only rerender the chart when the title has changed
// This also means that the selection wont always be immediately cleared
const ChartMemoized = React.memo(Chart, (old, current) => old.options == null || current.options.title === old.options.title);

export default TweetTrends;
