import { useRouter } from "next/router";

export default function nodeTitle(){
    const router = useRouter();
    console.log(router);
    return(
        <div>
            <p>{router.query.title}</p>
            <p>{router.query.url}</p>
            <p>{router.query.workplace}</p>
            <p>{router.query.recruitment_staff}</p>
            <p>{router.query.recruitment_field}</p>
            <p>{router.query.qualification_license}</p>
            <p>{router.query.job_specifications}</p>
            <p>{router.query.employment}</p>
            <p>{router.query.wages}</p>
            <p>{router.query.business_hours}</p>
            <p>{router.query.recruiter}</p>
            <p>{router.query.contact_address}</p>
        </div>
    ) 
}