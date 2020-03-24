import React from 'react';
import '../css/Log.css';
import LogEntry from "./LogEntry";

function Log() {
    return (
        <div className="Log">
            <LogEntry  city={"Xyz"} country={"Abc"} defficiency={"Zinc"}/>
            <LogEntry  city={"Xyz1"} country={"Abc11"} defficiency={"Zinc"}/>
            <LogEntry  city={"Xyz2123"} country={"Abc212"} defficiency={"Vitamin A"}/>
            <LogEntry  city={"Xyz3"} country={"Abc3213"} defficiency={"Zinc"}/>
            <LogEntry  city={"Xyz32"} country={"Abc3"} defficiency={"Zinc"}/>
            <LogEntry  city={"Xyz334"} country={"Abc31"} defficiency={"Vitamin A"}/>
            <LogEntry  city={"Xyz34"} country={"Abc412"} defficiency={"Vitamin A"}/>
            <LogEntry  city={"Xyz3123"} country={"Abc323"} defficiency={"Zinc"}/>
            <LogEntry  city={"Xyz3"} country={"Abc3"} defficiency={"Zinc"}/>
        </div>
    );
}

export default Log;
