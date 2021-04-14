import React, {useEffect, useState} from 'react';
import Typography from "@material-ui/core/Typography";
import {Grid, Paper, Theme} from "@material-ui/core";
import {createStyles, withStyles} from "@material-ui/core/styles";

const styles = () => createStyles({
    root: {
        margin: 20,
        color: "#000000"
    },
    data: {
        flex:1,
        margin: 2,
        paddingTop: 12,
        paddingBottom: 12,
        padding: 4
    }
});

var   interval: any = 0;

const StopWatch = (props: any) =>  {
    const {isStarted, isEnded, classes} = props
    const [millisecond, setMillisecond] = useState(0)
    const [second, setSecond] = useState(0)
    const [minute, setMinute] = useState(0)
    useEffect(()=>{
        if(isStarted && !isEnded){
            interval = setInterval(()=>{

                setMillisecond(millisecond => millisecond +1)
                if(millisecond === 100){
                    setSecond(second => second + 1)
                    setMillisecond(0)
                }
                if(second === 60){
                    setMinute(minute => minute +1)
                    setSecond(0)
                }

            },10);

        }
        else {
            clearInterval(interval);
        }

        return () => clearInterval(interval);
     }, [second, millisecond, isStarted, isEnded]);


    return(
        <div className={classes.root}>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Typography gutterBottom variant="h5" component="h2">
                        Temps écoulé
                    </Typography>
                </Grid>
                <Grid item xs={12} sm={4}>
                    <Paper className={classes.data}>
                        <Typography  variant="body2" component="p">
                            {minute}
                        </Typography>
                        <Typography  variant="body2" component="p">
                            m
                        </Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} sm={4}>
                    <Paper className={classes.data}>
                        <Typography  variant="body2" component="p">
                            {second}
                        </Typography>
                        <Typography  variant="body2" component="p">
                            s
                        </Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} sm={4}>
                    <Paper className={classes.data}>
                        <Typography  variant="body2" component="p">
                            {millisecond}
                        </Typography>
                        <Typography  variant="body2" component="p">
                            ms
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>
        </div>
    );
}

const componentWithStyles = withStyles(styles)(StopWatch);
export default componentWithStyles;