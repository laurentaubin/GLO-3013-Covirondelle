import React, {Component} from 'react';
import {createStyles, Theme, withStyles, WithStyles} from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Typography from '@material-ui/core/Typography';
import {Paper} from "@material-ui/core";
import {PuckColor, ZoneCorner} from "../context/context";
import {ResistanceColors} from "../domain/ResistanceColors";

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
        border: '#000000',
        height: 50,
        width: 50,
        borderRadius: 50,
        margin: 'auto'
    }
})

type Props = {
    pucks: PuckColor[]
    activePuckIndex: number | null
    corners: ZoneCorner[]
};

type AllProps = Props & WithStyles<typeof styles>;

class RobotStepper extends Component<AllProps> {
    render() {
        const {activePuckIndex, classes, pucks, corners} = this.props;
        let i = 0
        return (
            <div className={classes.root} data-testid={"pucks-stepper"}>
                <Typography variant="h5" component="h5">Rondelles</Typography>
                {pucks.length === 0 && <Typography variant="subtitle1">En attente</Typography>}
                {pucks.length > 0 && <Stepper activeStep={activePuckIndex ? activePuckIndex : 0} alternativeLabel>
                    {pucks.map((puck) => (
                        <Step key={puck}>
                            <StepLabel>{puck + ' : ' + (i < corners.length) ? corners[i] : ''}</StepLabel>
                            {i= i+1}
                            <div className={classes.circle} style={{backgroundColor: ResistanceColors[puck],}}/>
                            <Typography style={{backgroundColor: ResistanceColors[puck]}}/>
                        </Step>
                        )
                    )}
                </Stepper>
                }
                {activePuckIndex === pucks.length && (
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
