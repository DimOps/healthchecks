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
                        <button className={styles.Btn}>hours</button>
                        <form className={styles.OutageForm}>
                            <input type="datetime-local" />
                            <Link>
                                <div className={styles.Btn}>
                                    Update Outage
                                </div>
                            </Link>
                        </form>
                </section>
            </div>
        </div>);

}

            export default CheckComponent;