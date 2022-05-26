import styled from "styled-components";
import { useEffect, useState, } from "react";
import Link from "next/link";
import { jobSelector, dataAtom, jobAtom, cityFilter } from "../../atoms";
import { useRecoilState, useRecoilValue, useSetRecoilState} from "recoil";
import * as AWS from 'aws-sdk';

export default function Searching(){

    const [data, setData] = useRecoilState(dataAtom);
    const docClient = new AWS.DynamoDB.DocumentClient();

    const fetchData = (tableName: string) => {
        var params = {
            TableName: tableName
        }

        docClient.scan(params, function (err, json) {
            if (!err) {
                setData(json.Items);
            }
        })
    }

    const fetchDataFormDynamoDb = () => {
        fetchData(`${process.env.NEXT_PUBLIC_TABLE_NAME}`);
    }

    //데이터, 전역변수 가져오기
    const [job, setJob] = useRecoilState(jobAtom);
    const cityselector = useRecoilValue(cityFilter);
    const jobselector = useRecoilValue(jobSelector);
    const selector = job === "전체" ? cityselector : jobselector;
    const category : string[] =  [
        "전체",
        "경영·사무",
        "연구·공학기술",
        "사회복지",
        "보건·의료",
        "예술·엔터테인먼트",
        "서비스직",
        "영업·판매·운송",
        "건설·채굴",
        "기계·금속",
        "전자·정보통신",
        "화학·섬유·식품가공",
        "제조업",
        "농립·어업",
    ];

    useEffect(()=>{fetchDataFormDynamoDb()},[]);

    //페이지 버튼 만들기
    const [init,setInit] = useState<boolean>(true);
    const [initBtn,setInitBtn] = useState<boolean>(true);
    const [page, setPage] = useState<number>(1);
    let nbtn = Math.ceil(selector?.length/20);
    if (nbtn == 1) nbtn = 2;
    const btnlist = []
    const start : number = (page == 1) ? 0 : (page * 20);
    const end : number = (page == nbtn) ? selector?.length : (start + 20); // (0,20) (20,40)
    const test = selector?.slice(start, end); 
    for (let i=1; i<nbtn; i++) btnlist.push(i);

    const handleScroll = () => {
        window.scrollTo({
            top: 0,
        });
    }

    const btnHandle = (e : React.MouseEvent<HTMLButtonElement>) => {
        setPage(parseInt(e.target.name));
        setInitBtn(false);
        handleScroll();
    }

    //handler
    const onClick = (e : React.MouseEvent<HTMLButtonElement>) => {
        setJob(e.target.name);
        setInit(false);
        setInitBtn(true);
    }
    
    return(
        <Container>
            <Contents>
                <CategoryBox>
                    <Category>{category.map((job, index) => <Link href={"/nodes/searching"}><Choice init={init} key = {index} onClick={onClick} name={job}>{job}</Choice></Link>)}</Category>
                </CategoryBox>
                { test ? 
                    <div>
                        <Block>
                            <Box>
                                <NodeBox>
                                    {test?.map((data, index) =><Link href={{
                                    key: {index},
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
                                }}>
                                    <Tr key={index}>
                                        <State>모집중</State> 
                                        <Title>{{data}.data.title}</Title>
                                        <Th>{{data}.data.business_hours}</Th>
                                        <Th><strong>{{data}.data.wages}</strong></Th>
                                    </Tr>
                                </Link>)}
                                </NodeBox>
                            </Box>
                        </Block>
                        <Block>
                            {btnlist.map((n, index) =><Btn initBtn={initBtn} key={index} onClick={btnHandle} name={n}>{n}</Btn>)}
                        </Block> 
                    </div>
                : null}
            </Contents>
        </Container>
    );
}


const Container = styled.div`
    text-align: center;
    display: grid;
    place-items: center;
    overflow-x: none;
`;

const Contents = styled.div`
    margin-top: 100px;
    display: flex;
    justify-content: flex-start;
    align-items:center;
    min-height: 100vh; 
    flex-direction: column;
`;

const Block = styled.div`
    margin: 0 auto;

`;
const Box = styled.span`
    display: flex;
    justify-content: center;
    align-items:center;
    margin-bottom : 10vh;
    flex-direction: column;
`;

const Btn = styled.button<{initBtn : boolean}>`
    margin-bottom: 10vh;
    color: ${(props)=> props.theme.colors.POINT_GRAY};
    display: inline;
    border: none;
    text-align: center;
    text-decoration: none;
    font-size: 20px;
    background-color: white;
    font-weight: 500;
    cursor: pointer;  

    :first-child{
        color: ${(props) => props.initBtn? props.theme.colors.BLUE : props.theme.colors.POINT_GRAY};
    }
    &:focus{
        color: ${(props)=> props.theme.colors.BLUE};
    }
`;

const NodeBox = styled.table`
    border-collapse: collapse;
`;

const Th = styled.th`
    display: inline-block;
    width: 250px;
    font-size: 20px;
    padding: 15px;
    margin: 20px 0;   
    cursor: pointer; 
    font-weight: 300;
    /* strong{
        color: ${(props)=> props.theme.colors.BLUE};
    } */
`;

const State = styled(Th)`
    color: ${(props)=> props.theme.colors.GRAY};
    background : ${(props)=> props.theme.colors.BLUE};  
    width: 70px;
    border-radius: 10px;
    padding: 10px;
    margin-left: 9vh;
    margin-right: 3vh;
    font-weight: 500;
    font-size: 15px;
`;

const Title = styled(Th)`
    font-size: 22px;
    width: 400px;
    border-radius: 10px;
    font-weight: 400;
`;

const Tr = styled.tr`
   border-bottom-style: solid;
    border-bottom-color: ${(props)=> props.theme.colors.GRAY};  
`;

const CategoryBox = styled.div`
    display: flex;
    flex-wrap: wrap;
    width: 1200px;
    padding: 20px;
    white-space: nowrap;
    justify-content: center;
    margin: 0 auto;
    margin-bottom: 20px;
`;

const Category = styled.span`
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
`;

const Choice = styled.button<{init : boolean}>`
    width: 150px;
    border-radius: 30px;
    background-color: ${(props) => props.theme.colors.GRAY};
    border: none;
    color: ${(props)=> props.theme.colors.BLACK};
    text-align: center;
    font-size: 14px;
    padding: 15px;
    font-weight: bold;
    list-style: none;
    cursor: pointer;
    margin-top: 10px;
    margin-left: 10px;

    :first-child{
        background-color: ${(props) => props.init? props.theme.colors.BLUE : props.theme.colors.GRAY};
        color: ${(props) => props.init? props.theme.colors.GRAY : props.theme.colors.BLACK};
    }

    &:hover{
        background-color: ${(props)=> props.theme.colors.BLUE};
        color: ${(props)=> props.theme.colors.GRAY};
    }
    &:focus {
        background-color: ${(props)=> props.theme.colors.BLUE};
        color: ${(props)=> props.theme.colors.GRAY};
    }
`;
