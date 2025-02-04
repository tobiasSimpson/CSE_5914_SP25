import React from "react";
import { useNavigate } from "react-router-dom"; 
import Button from "react-bootstrap/Button";
import "./FrontPage.css";
import logo from "./logo.png"; 

function FrontPage () {
  const navigate = useNavigate(); 

  return (
    <div className="front-page">
      <div className="overlay">
        <img src={logo} alt="EchoX Logo" className="logo" />
        <h1 className="title">Welcome to EchoX</h1>
        <p className="tagline">
          Discover Twitter trends and analysis over time.
        </p>
        <Button variant="primary" className="start-btn" onClick={() => navigate("/home")}>
          Get Started
        </Button>
      </div>
    </div>
  );
};

export default FrontPage;
