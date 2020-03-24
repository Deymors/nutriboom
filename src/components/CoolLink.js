import React from 'react';
import '../css/CoolLink.css';


function CoolLink(props) {
    return (
        <div className="CoolLink">
            <a href={props.linkAddress}>{props.linkName}</a>
        </div>
    );
}

export default CoolLink;
