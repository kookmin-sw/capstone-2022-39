import styled from "styled-components";
import { useEffect, useState, } from "react";
import Link from "next/link";
import Loading from "../components/Loading";
import { cityFilter, dataAtom, jobAtom } from "../../atoms";
import { useRecoilState, useRecoilValue} from "recoil";


export default function Searching(){

    const [data, setData] = useRecoilState(dataAtom);
    const [job, setJob] = useRecoilState(jobAtom);
    const selector = useRecoilValue(cityFilter);

    const getData = async() => {
        const json = await(await fetch('https://s3.us-west-2.amazonaws.com/secure.notion-static.com/bcedc431-821d-4734-b59e-9875ccd72a89/announcement_list.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220521%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220521T082521Z&X-Amz-Expires=86400&X-Amz-Signature=bc922e25dd08e2bff78e4bf48b69ad5905410cac9f3f0ea19d3f132cd009cf03&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22announcement_list.json%22&x-id=GetObject')).json();
        setData(json);
      };

    useEffect(()=>{getData()},[]);

    console.log(selector);
    console.log(job);
    const [page, setPage] = useState<number>(1);
    let nbtn = Math.ceil(selector?.length/20);
    
    if (nbtn == 1){
        nbtn = 2;
    }

    const btnlist = []
    const start : number = (page == 1) ? 0 : (page * 20);
    const end : number = (page == nbtn) ? selector?.length : (start + 20); // (0,20) (20,40)
    // const test = ({data}.data)?.slice(start, end); 
    const test = selector?.slice(start, end); 

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
                        {/* {test?.map((data, index) =><Link href={{ */}
                        <NodeBox>
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
                        // }}><p>{index} <span key={index}>{{data}.data.title}</span></p></Link>)}
                        }}>
                            <Tr key={index}>
                                <State>모집 중</State> 
                                <Title>{{data}.data.title}</Title>
                                <Th>{{data}.data.workplace}</Th>
                                <Th>{{data}.data.business_hours}</Th>
                                <Th>{{data}.data.wages}</Th>
                            </Tr>
                        </Link>)}
                        </NodeBox>
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
    margin-top: 15vh;
    margin-top: 15vh;

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
    color: ${(props)=> props.theme.colors.BLACK};
    display: inline;
    border: none;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    background-color: white;
    &:focus{
            color: ${(props)=> props.theme.colors.BLUE};
        }
    p{
        cursor: pointer;
       
    }
`;

const NodeBox = styled.table`
    border-collapse: collapse;`;

const Th = styled.th`
    display: inline-block;
    width: 250px;
    font-size: 20px;
    padding: 15px;
    cursor: pointer; 
    font-weight: 300;
`;

const State = styled(Th)`
    color: ${(props)=> props.theme.colors.GRAY};
    background : ${(props)=> props.theme.colors.BLUE};  
    width: 80px;
    border-radius: 10px;
    padding: 10px;
    margin-left: 9vh;
    margin-right: 3vh;

`;

const Title = styled(Th)`
    font-size: 22px;
    width: 300px;
    border-radius: 10px;
    padding: 10px;
    font-weight: 400;
`;


const Tr = styled.tr`
    border-bottom-style: solid;
    border-bottom-color: ${(props)=> props.theme.colors.BLUE};  
    border-radius: 50px;
`;