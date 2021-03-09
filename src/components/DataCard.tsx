import {Paper, Theme} from '@material-ui/core';
import {createStyles, WithStyles, withStyles} from '@material-ui/core/styles';
import React, {Component} from 'react';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const styles = (theme: Theme) => createStyles({
    root: {
        margin: 20,
        maxWidth: 345,
        color: '#000000'
    },
    media: {
        height: 140,
    },
    data: {
        flex:1,
        margin: 20,
        paddingTop: 12,
        paddingBottom: 12,
        padding: 40
    }
});

type Props = {
    title: string
    value: number
    unit: string
};

type AllProps = Props & WithStyles<typeof styles>;

class DataCard extends Component<AllProps> {

    public render() {
        const {classes} = this.props;
        const {title, value, unit} = this.props;
        return (
            <div className={classes.root}>
                        <Typography gutterBottom variant="h5" component="h2">
                            {title}
                        </Typography>
                    <Paper className={classes.data}>
                        <Typography  variant="body2" component="p">
                            {value}
                        </Typography>
                        <Typography  variant="body2" component="p">
                            {unit}
                        </Typography>
                    </Paper>
            </div>
        );
    }
}

const componentWithStyles = withStyles(styles)(DataCard);

export default componentWithStyles;
