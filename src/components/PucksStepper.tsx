import React, {Component} from 'react';
import {makeStyles, Theme, createStyles, withStyles, WithStyles, decomposeColor} from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import StepContent from '@material-ui/core/StepContent';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

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
    steps: string[]
    activeStep: number
};

type AllProps = Props & WithStyles<typeof styles>;

class RobotStepper extends Component<AllProps> {
    render () {
        const {activeStep, classes, steps} = this.props;
        return (
            <div className={classes.root}>
                <Typography variant="h5" component="h5">Rondelles</Typography>
                <Stepper activeStep={activeStep} alternativeLabel>
                    {steps.map((puck) => (
                        <Step key={puck}>
                            <StepLabel>{puck}</StepLabel>
                            <div className={classes.circle} style={{backgroundColor: getStepColor(puck)}} />
                            <Typography style={{backgroundColor: getStepColor(puck)}} />
                        </Step>
                    ))}
                </Stepper>
                {activeStep === steps.length && (
                    <Paper square elevation={0} className={classes.resetContainer}>
                        <Typography>Game cycle completed!</Typography>
                    </Paper>
                )}
            </div>
        );
    }
}

const componentWithStyles = withStyles(styles)(RobotStepper);

export default componentWithStyles;
