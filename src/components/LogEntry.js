import React from 'react';
import '../css/LogEntry.css';

function LogEntry(props) {
    return (
        <div className="LogEntry">
            <h3>{props.country}</h3>
            <h3>{props.city}</h3>
            <h3>{props.defficiency}</h3>
        </div>
    );
}

export default LogEntry;
