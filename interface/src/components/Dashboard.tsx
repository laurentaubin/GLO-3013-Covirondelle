import { Grid, Paper, Theme, Typography } from "@material-ui/core";
import { createStyles, withStyles } from "@material-ui/core/styles";
import React, { useContext, useEffect } from "react";
import RobotStepper from "./RobotStepper";
import StateCard from "./StateCard";
import DataCard from "./DataCard";
import PucksStepper from "./PucksStepper";
import { AppContext, PuckColor, Stage } from "../context/context";
import { io } from "socket.io-client";
import { SERVER_ENDPOINT, UPDATE_EVENT } from "../config/config";
import { ActionType } from "../context/reducer";
import TableDisplay from "./TableDisplay";
import StopWatch from "../components/StopWatch";

const styles = (theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
      margin: 20,
      color: theme.palette.text.secondary,
    },
    smallPaper: {
      padding: theme.spacing(2),
      textAlign: "center",
      color: theme.palette.text.secondary,
      height: 200,
    },
    paper: {
      padding: theme.spacing(2),
      textAlign: "center",
      color: theme.palette.text.secondary,
    },
  });

export const Dashboard = (props: any) => {
  const { classes } = props;
  const { state, dispatch } = useContext(AppContext);

  useEffect(() => {
    const socket = io(SERVER_ENDPOINT);
    socket.on(UPDATE_EVENT, (received_data) => {
      dispatch({ type: ActionType.UPDATE_STATE, payload: received_data });
    });
  }, [state.IsGameStarted]);

  const send_start_signal = async () => {
    const socket = io(SERVER_ENDPOINT);
    socket.emit("start_game");
    dispatch({ type: ActionType.START_GAME });
  };

  return (
    <>
      <TableDisplay />
      <div className={classes.root}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <Paper className={classes.smallPaper}>
              <DataCard title={"Charge électrique de la batterie"} value={state.BatteryElectricCharge} unit={"%"} />
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Paper className={classes.smallPaper}>
              <DataCard title={"Consommation électrique du robot"} value={state.RobotConsumption} unit={"Watt"} />
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Paper className={classes.smallPaper}>
              <DataCard title={"Temps restant à la batterie"} value={state.BatteryTime} unit={"secondes"} />
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Paper className={classes.smallPaper}>
              <DataCard title={"Résistance mesurée"} value={state.Resistance} unit={"Ω"}>
                <div>
                  {state.PuckColors.map((puck) => (
                    <Typography key="puck" variant="body2">
                      {puck}
                    </Typography>
                  ))}
                </div>
              </DataCard>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={3}>
            <Paper className={classes.smallPaper}>
              <StopWatch isStarted={state.IsGameStarted} isEnded={state.CurrentStage === Stage.cycle_completed} />
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
                title={"État du préhenseur"}
                active={"OCCUPÉ"}
                neutral={"VIDE"}
                isActive={state.IsGripperHolding}
                isWaiting={!state.IsRobotBooted}
              />
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Paper className={classes.smallPaper}>
              <StateCard
                title={"État du robot"}
                active={"ACTIF"}
                neutral={"EN ATTENTE"}
                isActive={state.IsGameStarted}
                isWaiting={!state.IsRobotBooted}
                onClick={send_start_signal}
              />
            </Paper>
          </Grid>
        </Grid>
        <RobotStepper activeStage={state.CurrentStage} />
      </div>
    </>
  );
};

function findActivePuckIndex(pucks: PuckColor[], activePuck?: PuckColor) {
  if (!activePuck) return null;
  return pucks.indexOf(activePuck);
}

const componentWithStyles = withStyles(styles)(Dashboard);

export default componentWithStyles;
