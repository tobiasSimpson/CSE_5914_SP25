import React from "react";
import Card from "react-bootstrap/Card";
import "bootstrap-icons/font/bootstrap-icons.css";

const TweetList = ({tweets, setTweets}) => {
  
  return (
    <div>
      <div className="tweets-container" id="tweets-container" style={{ marginTop: '15px' }}>
        {tweets.map((tweet, index) => (
          <Card key={index} style={{ margin: '8px 0', padding: '10px', borderRadius: '8px'}}>
            <Card.Text><i class="bi bi-twitter" style={{color: "#1DA1F2", marginRight: '10px'}}></i> {tweet}</Card.Text>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default TweetList;
