import {Grid, Paper, Theme, Typography} from '@material-ui/core';
import {createStyles, withStyles} from '@material-ui/core/styles';
import React, {useContext, useEffect} from 'react';
import RobotStepper from "./RobotStepper";
import StateCard from "./StateCard";
import DataCard from "./DataCard";
import PucksStepper from "./PucksStepper";
import {AppContext, PuckColor} from "../context/context";
import {io} from "socket.io-client";
import {SERVER_ENDPOINT, UPDATE_EVENT} from "../config/config"
import {ActionType} from "../context/reducer";


const styles = (theme: Theme) => createStyles({
    root: {
        flexGrow: 1,
        margin: 20,
        color: theme.palette.text.secondary
    },
    smallPaper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        height: 200
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary
    },
});

// TODO: make sure everything is there
// Etape du cycle de jeu en cours DONE
// Liste des étapes du jeu complétées DONE

// Etat du prehenseur DONE
// Statut actuel du robot DONE

// Charge electrique courante de la batterie DONE
// Consommation electrique du robot DONE
// Temps restant à la batterie DONE

// Couleur de la rondelle en train d'etre déplacé DONE
// Couleur des rondelles déplacées avec succès DONE

// Afficher la valeur de la résistance mesurée DONE
// Code de couleur de la résistance mesurée DONE

// Les coins du carré vert où les rondelles seront déposées DONE

// Afficher la position du robot en temps réel EN COURS

// Stopwatch : À la réception de la commande de départ, le
// chronographe, mesurant le temps qui s’écoule pendant l’exécution de la tâche, est mis
// en marche EN COURS

export const Dashboard = (props: any) => {
    const {classes} = props
    const {state, dispatch} = useContext(AppContext);

    useEffect(() => {
        const socket = io(SERVER_ENDPOINT);
        socket.on(UPDATE_EVENT, received_data => {
            dispatch({"type": ActionType.UPDATE_STATE, "payload": received_data})
        });
    }, [state.IsGameStarted]);

    const send_start_signal = async () => {
        const socket = io(SERVER_ENDPOINT)
        socket.emit("start_game")
        dispatch({"type": ActionType.START_GAME})
    }

    return (
        <>
            {state.TableImage ? <img src={`data:image/jpeg;base64,${state.TableImage}`} alt={""}/> : ""}
            <div className={classes.root} data-testid={"dashboard"}>
                <Grid container spacing={3}>
                    <Grid item xs={12} sm={6}>
                        <Paper className={classes.smallPaper}>
                            <DataCard
                                title={'Charge électrique de la batterie'}
                                // TODO: add charge
                                value={state.BatteryElectricCharge}
                                unit={'Watt'}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Paper className={classes.smallPaper}>
                            <DataCard
                                title={'Consommation électrique du robot'}
                                // TODO: check if its the right value
                                value={state.RobotConsumption}
                                unit={'Watt'}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Paper className={classes.smallPaper}>
                            <DataCard
                                title={'Temps restant à la batterie'}
                                // TODO: add battery time
                                value={state.BatteryTime}
                                unit={'secondes'}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Paper className={classes.smallPaper}>
                            <DataCard
                                title={'Résistance mesurée'}
                                // TODO: add resistance
                                value={state.Resistance}
                                unit={'Ω'}
                            >
                                <div>
                                    {state.PuckColors.map((puck) => (
                                        <Typography key="puck" variant="body2">{puck}</Typography>
                                    ))}
                                </div>
                            </DataCard>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <Paper className={classes.smallPaper}>
                            <PucksStepper
                                pucks={state.PuckColors}
                                corners={state.ZoneCornersOrder}
                                activePuckIndex={findActivePuckIndex(state.PuckColors, state.CurrentPuck)}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Paper className={classes.smallPaper}>
                            <StateCard
                                title={'État du préhenseur'}
                                active={'RONDELLE'}
                                neutral={'VIDE'}
                                isActive={state.IsGripperHolding}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Paper className={classes.smallPaper}>
                            <StateCard
                                title={'État du robot'}
                                active={'ACTIF'}
                                neutral={'EN ATTENTE'}
                                isActive={state.IsGameStarted}
                                onClick={send_start_signal}
                            />
                        </Paper>
                    </Grid>
                </Grid>
                <RobotStepper
                    activeStage={state.CurrentStage}
                />
            </div>
        </>
    )
}

function findActivePuckIndex(pucks: PuckColor[], activePuck?: PuckColor) {
    if (!activePuck) return null
    return pucks.indexOf(activePuck)
}

const componentWithStyles = withStyles(styles)(Dashboard);

export default componentWithStyles;
