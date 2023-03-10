import CheckComponent from "../CheckComponent/CheckComponent";
import styles from "./ChecksList.module.css"
import { useState, useEffect } from "react";

const ChecksList = () => {
    const [checks, setChecks] = useState({"checks": []});

    useEffect(() => {
        fetch(`http://localhost:8000/api/data`)
            .then(res => res.json())
            .then(result => {
                setChecks(result);
            });
    }, []);

    return (
        <section className={styles.ListItem}>
            {checks['checks'].map(c => ( 
                <CheckComponent 
                key={c.id} 
                pingId={c['state'].ping_id} 
                name={c.name} 
                host={c.host} 
                type={c.type} 
                status={c['state'].status} 
                lastShut={c['state'].lastDownStart}
                lastRecovery={c['state'].lastDownEnd}
                />))}
            
        </section>
    );

}

export default ChecksList;