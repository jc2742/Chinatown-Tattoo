import React, {Component} from "react";
import InfoPage from "./InfoPage";
import LoginPage from "./LoginPage";
import{BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";


export default class HomePage extends Component{
    constructor(props){
        super(props);
    }
    render(){
        return (<h4>Chinatown</h4>);
    }
}