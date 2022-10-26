import React, {Component} from "react";
import {render} from "react-dom";
import HomePage from "./HomePage";
import InfoPage from "./InfoPage";
import LoginPage from "./LoginPage";
import{BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";


export default class App extends Component{
    constructor(props){
        super(props);
    }
    render(){
        return <Router>
            <Routes>
                <Route exact path ='/' element = {<HomePage/>}/>
                 <Route exact path ='/info' element={<InfoPage/>} />
                 <Route exact path ='/login' element={<LoginPage/>}/>
            </Routes>
        </Router>;
    }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);