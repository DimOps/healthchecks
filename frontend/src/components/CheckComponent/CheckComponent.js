import { useState } from "react";
import styles from "./CheckComponent.module.css"
const CheckComponent = (props) => {
    const [hours, setHours] = useState(0)

    const submitHandler = (e) => {
        e.preventDefault();
        const kwargs = {'from': 0, 'to': 0}
        const hoursBack = hours
        kwargs.to = Date.now()
        kwargs.from = Date.now() - Number(hoursBack)*60000
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
                        <span>Last shut: estimateStart</span>
                        <span>Last recovery: recoveryEstimation</span>
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

                                <input className={styles.Btn} type="submit" value="Outage"/>

                        </form>
                        <span><label>33%</label></span>
                        <span><label>33%</label></span>
                        <span><label>33%</label></span>
                </section>
            </div>
        </div>);

}

            export default CheckComponent;