import React, {useEffect, useState} from "react";
import Axios from "axios";
const apiUrl = "http://localhost:8000/api/recruitment/";

function RecruitmentList(){
const [recruitList, setRecruitList] = useState([]);
    useEffect(() => {
        Axios.get(apiUrl)
            .then(response => {
                const { data } = response;
                console.log("loaded response: ", response);
                setRecruitList(data);
            })
            .catch(error => {
                // error.response;
            });
        console.log("mounted");
    }, []);
    return (
        <div>
            <h1>RecruitmentList</h1>
            {recruitList.map(recruitment => {
                const { id } = recruitment;
                    return(
                        <div key={id}>
                            {JSON.stringify(recruitment)}
                        </div>
                    )
            }
            )}
        </div>
    );
}

export default RecruitmentList;