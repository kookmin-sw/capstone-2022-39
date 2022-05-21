
   
import styled from "styled-components";
import { useEffect, useState, } from "react";
import Link from "next/link";
import Loading from "../components/Loading";
import { Idata, dataAtom } from "../../atoms";
import { useRecoilState } from "recoil";


export default function Node(){

    const [data, setData] = useRecoilState(dataAtom);

    const getData = async() => {
        const json = await(await fetch('https://s3.us-west-2.amazonaws.com/secure.notion-static.com/bcedc431-821d-4734-b59e-9875ccd72a89/announcement_list.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220517%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220517T052938Z&X-Amz-Expires=86400&X-Amz-Signature=c46ee448f9156e09239a62aa0749479c6ccde08894db8f7a884191d1f4878621&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22announcement_list.json%22&x-id=GetObject')).json();
        setData(json);
      };


    useEffect(()=>{getData()},[]);
    const [page, setPage] = useState<number>(1);
    const nbtn = Math.ceil(data?.length/20);
    const btnlist = []
    const start : number = (page == 1) ? 0 : (page * 20);
    const end : number = (page == nbtn) ? data?.length : (start + 20); // (0,20) (20,40)
    const test = ({data}.data)?.slice(start, end); 
    const btnHandle = (e : React.MouseEvent<HTMLButtonElement>) => {
        setPage(parseInt(e.target.name));
    }

    for (let i=1; i<nbtn; i++){
        btnlist.push(i);
    }
    
    return(
        <Container>
            <Contents>
                {test ? 
                <div>
                <Block>
                    <Box>
                        {test?.map((data, index) =><Link href={{
                            pathname: `/nodes/${{data}.data.title}`, 
                            query:{ 
                                title: {data}.data.title ,
                                url: {data}.data.url,
                                workplace: {data}.data.workplace,
                                recruitment_staff: {data}.data.recruitment_staff,
                                recruitment_field: {data}.data.recruitment_field,
                                qualification_license: {data}.data.qualification_license,
                                job_specifications: {data}.data.job_specifications,
                                employment: {data}.data.employment,
                                wages: {data}.data.wages,
                                business_hours: {data}.data.business_hours,
                                recruiter: {data}.data.recruiter,
                                contact_address: {data}.data.contact_address,
                            },
                        }}><p>{index} <span key={index}>{{data}.data.title}</span></p></Link>)}
                    </Box>
                </Block>
                <Block>
                    {btnlist.map((n, index) =><Btn key={index} onClick={btnHandle} name={n}>{n}</Btn>)}
                </Block> 
                </div>
                :<Loading/>}

            </Contents>
        </Container>
    );
}
const Container = styled.div`
    text-align: center;
    display: grid;
    place-items: center;
`;

const Contents = styled.div`
    display: flex;
    justify-content: center;
    align-items:center;
    min-height: 100vh; 
    flex-direction: column;
`;
const Block = styled.div`
`;
const Box = styled.span`
    display: flex;
    justify-content: center;
    align-items:center;
    margin-bottom : 10vh;
    flex-direction: column;
`;

const Btn = styled.button`
    display: inline;
    p{
        cursor: pointer;
    }
`;