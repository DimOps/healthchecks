import styles from './Header.module.css'
import { useState, useEffect } from 'react';
import moment from 'moment';

const Header = () => {

    const [timeNow, setTimeNow] = useState([]);

    useEffect(() => {
        setInterval(() => {
            setTimeNow(moment().format('MMMM Do YYYY, h:mm:ss a'))
        }, 1000);
    }, []);

    const header = (
        <div className={styles.header}>
                <label>Now is: </label>
                <span>{timeNow}</span>
        </div>
    );

    return header;
};

export default Header;