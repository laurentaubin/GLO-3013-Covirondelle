import {Paper} from '@material-ui/core';
import {createStyles, WithStyles, withStyles} from '@material-ui/core/styles';
import React, {Component, ReactNode} from 'react';
import Typography from '@material-ui/core/Typography';

const styles = () => createStyles({
    root: {
        margin: 'auto',
        maxWidth: 345,
        color: '#000000'
    },
    media: {
        height: 70,
    },
    data: {
        flex: 1,
        margin: 'auto',
        paddingTop: 12,
        paddingBottom: 12,
        padding: 20
    }
});

type Props = {
    title: string
    value?: number
    unit: string
    children?: ReactNode
};

type AllProps = Props & WithStyles<typeof styles>;

class DataCard extends Component<AllProps> {

    public render() {
        const {title, value, unit, classes, children} = this.props;

        return (
            <div className={classes.root} data-testid={"data-card"}>
                <Typography gutterBottom variant="subtitle1" component="h2">
                    {title}
                </Typography>
                <div className={classes.data}>
                    <Typography variant="body2" component="p">
                        {value ?? 'N/A'}
                    </Typography>
                    <Typography variant="body2" component="p">
                        {unit}
                    </Typography>
                    {children}
                </div>
            </div>
        );
    }
}

const componentWithStyles = withStyles(styles)(DataCard);

export default componentWithStyles;
