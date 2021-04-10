import React, {Component} from 'react';
import {createStyles, Theme, withStyles, WithStyles} from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import {Stage} from "../context/context";
import {RobotStages} from "../domain/RobotStages";

const styles = (theme: Theme) => createStyles({
    root: {
        margin: 20,
        width: '100%',
        color: '#000000'
    },
    startButton: {
        marginRight: theme.spacing(1),
    },
    actionsContainer: {
        marginBottom: theme.spacing(2),
    },
    resetContainer: {
        padding: theme.spacing(3),
    },
})

function getStepLabel(step: Stage) {
    return RobotStages[step].description
}

type Props = {
    activeStage: Stage
};

type AllProps = Props & WithStyles<typeof styles>;

class RobotStepper extends Component<AllProps> {
    render() {
        const {activeStage, classes} = this.props;
        const steps = Object.keys(RobotStages);
        const currentStage = RobotStages[activeStage]
        return (
            <div className={classes.root} data-testid={"robot-stepper"}>
                <Typography variant="h5" component="h5">Étapes du robot</Typography>
                <Stepper activeStep={currentStage.order} orientation="vertical">
                    {steps.map((step) => (
                        <Step key={step}>
                            <StepLabel>{getStepLabel(step as Stage)}</StepLabel>
                        </Step>
                    ))}
                </Stepper>
                {currentStage.order === steps.length && (
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
