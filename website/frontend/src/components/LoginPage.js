import React, {Component} from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import {Link} from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";

export default class LoginPage extends Component{
    constructor(props){
        super(props);
        this.state = {
            
        }
    }
    render(){
         return (<Grid continer spacing = {1}>
            <Grid item xs = {12} align = "center">
                <Typography component = 'h4' variant = 'h4'>
                    Chinatown Tattoo
                </Typography>
            </Grid>

            <Grid item xs = {12} align = "center">
                <FormControl component = "feildset">

                    <FormHelperText>
                        <div align = 'center'>
                            Artist Login
                        </div>
                    </FormHelperText>

                    <TextField 
                    required = {true} 
                    type="text"
                    defaultValue = ""/>
                    <FormHelperText>
                        <div align ="center">
                            Username
                        </div>
                    </FormHelperText>

                    <TextField 
                    required = {true} 
                    type="password"
                    defaultValue = ""/>
                    <FormHelperText>
                        <div align ="center">
                            Password
                        </div>
                    </FormHelperText>


                    <RadioGroup row defaultValue ='false'>
                        <FormControlLabel
                        value = "No"
                        control = {<Radio color = "primary"/>} 
                        label = "Remember Password" 
                        labelPlacement = "left"/>
                    </RadioGroup>

                </FormControl>
            </Grid>

            <Grid item xs = {12} align = "center">
                    <Button color ="secondary" variant = "contained">
                        Login
                    </Button>
                    <Button color ="secondary" variant = "contained" to="/" component={Link}>
                        Back
                    </Button>
            </Grid>

        </Grid>);
    }
}