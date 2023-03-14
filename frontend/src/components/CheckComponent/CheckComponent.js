import { useState } from "react";
import styles from "./CheckComponent.module.css"

import moment from "moment";


const CheckComponent = (props) => {
    const [hours, setHours] = useState(0)
    const [outage, setOutage] = useState({'unknown': 100, 'up': 0, 'down': 0})
    const kwargs = { 'timefrom': 0, 'timeto': 0 }

    const FetchReport = (pingId, kwargs) => {       
        const body = {
            'checkId': pingId,
            'kwargs': kwargs
        }
        const url = `http://localhost:8000/api/summary`

        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': "application/json",
            },
            body: JSON.stringify(body),
        })
            .then(res => res.json())
            .then(result => setOutage(result))   
    };

    const submitHandler = (e) => {
        e.preventDefault();
        const hoursBack = hours
        kwargs.timeto = Math.floor(Date.now() / 1000)
        kwargs.timefrom = Math.floor((Date.now() - Number(hoursBack) * 3600000) / 1000)
        FetchReport(props.pingId, kwargs)
    };

    const outageHandler = (e) => {
        setHours(e.target.value);
    };

    return (
        <div className={styles.Env}>
            <div className={styles.Check}>
                <section>
                    <header className={styles.CheckHeader}>
                        <span>Name: {props.name}</span>
                        <span>Last shut: {props.lastShut ? moment(props.lastShut).format("MMMM Do YYYY, hh:mm") : 'unknown'}</span>
                        <span>Last recovery: {props.lastRecovery ? moment(props.lastRecovery).format("MMMM Do YYYY, hh:mm") : 'unknown'}</span>
                    </header>
                    <hr />
                    <p className={styles.CheckDetails}>
                        <span>Host: {props.host}</span>
                        <span>Type: {props.type}</span>
                        <span>Status: {props.status}</span>
                    </p>

                </section>
                <section className={styles.OutageInfo}>
                    <label>*Last N hours:</label>
                    <form className={styles.OutageForm} onSubmit={submitHandler}>
                        <input
                            id="interval"
                            type="number"
                            name="interval"
                            placeholder="168 hours default"
                            onChange={outageHandler}
                            value={hours} />
                        <input className={styles.Btn} type="submit" value="Outage" />
                    </form>
                    <span className={styles.Outage}>Unknown<label>{outage.unknown}%</label></span>
                    <span className={styles.Outage}>Up<label>{outage.up}%</label></span>
                    <span className={styles.Outage}>Down<label>{outage.down}%</label></span>
                </section>
            </div>
        </div>);

}

export default CheckComponent;