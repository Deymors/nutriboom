import React from 'react';
import './css/App.css';
import Header from "./components/Header";
import MapContainer from "./components/MapContainer";
import Log from "./components/Log";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="App">
      <Header/>
      <div className="body-container">
        <Log/>
        <MapContainer/>
      </div>
      <Footer/>
    </div>
  );
}

export default App;
