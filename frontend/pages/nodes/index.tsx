import styled from "styled-components";
import { useEffect, useState, } from "react";
import Link from "next/link";
// import Loading from "../components/Loading";
import { dataAtom, keyWordAtom, keyWordFilter } from "../../atoms";
import { useForm } from "react-hook-form";
import { useRecoilState, useRecoilValue } from "recoil";

export default function Searching(){


    //데이터, 전역변수 가져오기
    const [data, setData] = useRecoilState(dataAtom);

    const getData = async() => {
        const json = await(await fetch('https://s3.us-west-2.amazonaws.com/secure.notion-static.com/bcedc431-821d-4734-b59e-9875ccd72a89/announcement_list.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220521%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220521T082521Z&X-Amz-Expires=86400&X-Amz-Signature=bc922e25dd08e2bff78e4bf48b69ad5905410cac9f3f0ea19d3f132cd009cf03&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22announcement_list.json%22&x-id=GetObject')).json();
        setData(json);
      };

    useEffect(()=>{getData()},[]);

    const [keyword, setKeyword] = useRecoilState(keyWordAtom);
    const keywordfilter = useRecoilValue(keyWordFilter);
    const selector = keyword === "default" ? data : keywordfilter;

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

    const btnHandle = (e : React.MouseEvent<HTMLButtonElement>) => {
        setPage(parseInt(e.target.name));
        setInitBtn(false);
    }

    for (let i=1; i<nbtn; i++) btnlist.push(i);
    
    const onSubmit = (data) => {
        setKeyword(data.keyword);
    }

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm({
    });

    return(
        <Container>
            <Contents>
                <Form onSubmit={handleSubmit(onSubmit)}>
                    <Input
                    {...register("keyword", {
                        required: "검색어를 입력해주세요"
                    })}
                    placeholder="키워드를 입력해보세요."
                    />
                    {/* <Image src={img} alt="img"/> */}
                </Form>
                    <div>
                        <Block>
                            <Box>
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
                                }}>
                                    <Tr key={index}>
                                        <State>모집중</State> 
                                        <Title>{{data}.data.title}</Title>
                                        {/* <Th>{{data}.data.workplace}</Th> */}
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
    @media screen and (max-width: 500px) {
        width: 100%;
        margin: 0 0;
        font-size: 15px;
    }
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
    @media screen and (max-width: 500px) {
        display: none;
    }
`;

const Title = styled(Th)`
    font-size: 22px;
    width: 400px;
    border-radius: 10px;
    font-weight: 400;
    @media screen and (max-width: 500px) {
        width: 200px;
        font-size: 20px;
    }
`;

const Tr = styled.tr`

    border-bottom-style: solid;
    border-bottom-color: ${(props)=> props.theme.colors.GRAY};  
`;

const Form = styled.form`
    width: 500px;
    display: flex;
    flex-direction: column;
    margin: 5vh 0;
`;

const Input = styled.input`
    padding: 20px;
    font-size: 20px;
    margin-bottom: 10px;
    border: none;
    border-radius: 10px;
    background-color: ${(props) => props.theme.colors.GRAY};
    width: 500px;
`;