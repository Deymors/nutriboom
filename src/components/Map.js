import React from 'react';
import '../css/Map.css';

import rd3 from 'react-d3-library';
const RD3Component = rd3.Component;

class Map extends React.Component {

    constructor(props) {
        super(props);
        this.state = {d3: ''}
    }

    render() {
        return (
            <div className="Map">
            </div>
        )
    }
}

export default Map;