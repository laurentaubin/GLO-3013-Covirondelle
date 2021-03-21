import React, {Component} from 'react';
import {makeStyles, Theme, createStyles, withStyles, WithStyles} from '@material-ui/core/styles';
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

function getSteps() {
    return [
        'Attente du signal de départ',
        'En route vers la station de lecture des résistances',
        'Mesure de la valeur de résistance en cours',
        'En route vers le panneau de commande',
        'Lecture du panneau de commande en cours',
        'En route vers la première rondelle',
        'Maniement du préhenseur',
        'En route vers la destination de la première rondelle',
        'En route vers la première rondelle',
        'Maniement du préhenseur',
        'En route vers la destination de la première rondelle',
        'Confirmation de la position de la rondelle',
        'En route vers la deuxième rondelle',
        'Maniement du préhenseur',
        'En route vers la destination de la deuxième rondelle',
        'Confirmation de la position de la rondelle',
        'En route vers la troisième rondelle',
        'Maniement du préhenseur',
        'En route vers la destination de la troisième rondelle',
        'Confirmation de la position de la rondelle',
        'En route vers la quatrième rondelle',
        'Maniement du préhenseur',
        'En route vers la destination de la quatrième rondelle',
        'Confirmation de la position de la rondelle',
        'Transporter la rondelle', 'Stop'
    ];
}

function getStepContent(step: number) {
    // TODO: add correct description or remove this part of the stepper
    switch (step) {
        case 0:
            return `For each ad campaign that you create, you can control how much
              you're willing to spend on clicks and conversions, which networks
              and geographical locations you want your ads to show on, and more.`;
        case 1:
            return 'An ad group contains one or more ads which target a shared set of keywords.';
        case 2:
            return `Try out different ad text to see what brings in the most customers,
              and learn how to enhance your ads using features like ad extensions.
              If you run into any problems with your ads, find out how to tell if
              they're running and how to resolve approval issues.`;
        default:
            return 'Unknown step';
    }
}

type Props = {
    activeStep: number
};

type AllProps = Props & WithStyles<typeof styles>;

class RobotStepper extends Component<AllProps> {
    render () {
        const {activeStep, classes} = this.props;
        const steps = getSteps();
        return (
            <div className={classes.root}>
                <Typography variant="h5" component="h5">Étapes du robot</Typography>
                <Stepper activeStep={activeStep} orientation="vertical">
                    {steps.map((label, index) => (
                        <Step key={label}>
                            <StepLabel>{label}</StepLabel>
                            <StepContent>
                                <Typography>{getStepContent(index)}</Typography>
                            </StepContent>
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
