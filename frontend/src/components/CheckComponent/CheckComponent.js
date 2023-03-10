import { Link } from "react-router-dom";

import styles from "./CheckComponent.module.css"
const CheckComponent = (props) => {

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
                        <label>Last N hours:</label>
                        <form className={styles.OutageForm}>
                            <input type="number" />
                            <Link>
                                <div className={styles.Btn}>
                                    Outage
                                </div>
                            </Link>
                        </form>
                        <span><label>33%</label></span>
                        <span><label>33%</label></span>
                        <span><label>33%</label></span>
                </section>
            </div>
        </div>);

}

            export default CheckComponent;