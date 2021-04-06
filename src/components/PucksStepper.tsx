import React, {Component} from 'react';
import {createStyles, Theme, withStyles, WithStyles} from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Typography from '@material-ui/core/Typography';
import {Paper} from "@material-ui/core";
import {PuckColor} from "../context/context";

const styles = (theme: Theme) => createStyles({
    root: {
        margin: 20,
        width: '100%',
        color: '#000000'
    },
    button: {
        marginTop: theme.spacing(1),
        marginRight: theme.spacing(1),
    },
    actionsContainer: {
        marginBottom: theme.spacing(2),
    },
    resetContainer: {
        padding: theme.spacing(3),
    },
    circle: {
        height: 50,
        width: 50,
        borderRadius: 50,
        margin: 'auto'
    }
})

function getStepColor(label: string) {
    // TODO: add correct colors
    switch (label) {
        case 'rouge':
            return '#DC143C';
        case 'magenta':
            return '#8B008B';
        case 'orange':
            return '#FF8C00';
        case 'vert':
            return '#33CC33'
        default:
            return '#ffffff';
    }
}

type Props = {
    pucks: PuckColor[]
    activePuck: number
};

type AllProps = Props & WithStyles<typeof styles>;

class RobotStepper extends Component<AllProps> {
    render() {
        const {activePuck, classes, pucks} = this.props;
        return (
            <div className={classes.root}>
                <Typography variant="h5" component="h5">Rondelles</Typography>
                {pucks.length === 0 && <Typography variant="subtitle1">En attente</Typography>}
                {pucks.length > 0 && <Stepper activeStep={activePuck + 1} alternativeLabel>
                    {pucks.map((puck) => (
                        <Step key={puck}>
                            <StepLabel>{puck}</StepLabel>
                            <div className={classes.circle} style={{backgroundColor: getStepColor(puck)}}/>
                            <Typography style={{backgroundColor: getStepColor(puck)}}/>
                        </Step>
                    ))}
                </Stepper>
                }
                {activePuck === pucks.length && (
                    <Paper square elevation={0} className={classes.resetContainer}>
                        <Typography>Terminé!</Typography>
                    </Paper>
                )}
            </div>
        );
    }
}

const componentWithStyles = withStyles(styles)(RobotStepper);

export default componentWithStyles;
