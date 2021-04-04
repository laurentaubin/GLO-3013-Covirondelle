import {Grid, Paper, Theme} from '@material-ui/core';
import {createStyles, WithStyles, withStyles} from '@material-ui/core/styles';
import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const styles = (theme: Theme) => createStyles({
    root: {
        flex: 1,
        margin: 20,
        minWidth: 300,
        maxWidth: 800,
        color: '#000000'
    },
    active: {
        flex: 1,
        color: '#ffffff',
        paddingTop: 8,
        paddingBottom: 8,
        padding: 20,
        backgroundColor: theme.palette.primary.light,
        margin: 10
    },
    disabled: {
        flex: 1,
        color: '#F0F0F0',
        paddingTop: 8,
        paddingBottom: 8,
        padding: 20,
        backgroundColor: '#D3D3D3',
        margin: 10
    },
    actionButton: {
        flex: 1,
        padding: 20,
        margin: 5,
        backgroundColor: theme.palette.success.main,
        color: '#ffffff',
        borderRadius: 100,
    },
    disabledButton: {
        opacity: 0.7
    }
});

type Props = {
    title: string
    active: string
    neutral: string
    isActive: boolean
    onClick?: () => void
    label?: string
};

type AllProps = Props & WithStyles<typeof styles>;

class StateCard extends Component<AllProps> {

    public render() {
        const {classes} = this.props;
        const {title, active, neutral, isActive, onClick, label} = this.props;

        return (
            <div className={classes.root}>
                <Typography gutterBottom variant="h5" component="h2">
                    {title}
                </Typography>
                <Grid container spacing={0}>
                    <Grid item xs={6}>
                        <Paper className={isActive ? classes.active : classes.disabled}>
                            <Typography variant="body2" component="p">
                                {active}
                            </Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={isActive ? classes.disabled : classes.active}>
                            <Typography variant="body2" component="p">
                                {neutral}
                            </Typography>
                        </Paper>
                    </Grid>
                </Grid>
                {(onClick) &&
                <Button
                    className={classes.actionButton}
                    onClick={onClick}
                    disabled={isActive}
                    classes={{disabled: classes.disabledButton}}
                >
                    {label ?? 'DÉMARRER'}
                </Button>}
            </div>
        );
    }
}

const componentWithStyles = withStyles(styles)(StateCard);

export default componentWithStyles;
