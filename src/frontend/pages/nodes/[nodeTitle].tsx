import { useRouter } from "next/router";
import styled from "styled-components";
import Link from "next/link";

export default function nodeTitle(){
    const router = useRouter();
    const URL : any = router?.query.url;
    
    return(
        <Container>
            <Box>
                <Block>
                    <Title>{router.query.title}</Title>
                    <Btns>
                        <Btn1><span>{router.query.wages}</span></Btn1>
                        {URL? <Link href={URL}><Btn>본문보기</Btn></Link> : null }
                    </Btns>
                </Block>
                <Block2>
                    <CategoryBox>
                        <Category>모집사항</Category>
                        <Li><strong>근무지역:</strong>{router.query.workplace}</Li>
                        <Li><strong>모집인원:</strong>{router.query.recruitment_staff}</Li>
                        <Li><strong>분야:</strong>{router.query.recruitment_field}</Li>
                    </CategoryBox>

                    <CategoryBox>
                        <Category>채용 담당자 정보</Category>
                        <Li><strong>담당자명:</strong>{router.query.recruiter}</Li>
                        <Li><strong>연락처:</strong>{router.query.contact_address}</Li>
                    </CategoryBox>
                </Block2>
                <Block2>
                    <CategoryBox1>
                            <Category>근무사항</Category>
                            <Li><strong>특이사항:</strong>{router.query.job_specifications}</Li>
                            <Li><strong>고용형태:</strong>{router.query.employment}</Li>
                            <Li><strong>근무시간:</strong>{router.query.business_hours}</Li>
                            <Li><strong>자격사항:</strong>{router.query.qualification_license}</Li>
                    </CategoryBox1>
                </Block2>

            </Box>
        </Container>
    ) 
}
const Container = styled.div`
    display: flex;
    justify-content: center;
    align-items:center;
    min-height: 100vh; 
    flex-direction: column;
`;

const Box = styled.div`
    width: 1000px;
    margin: auto;
    /* border: solid blue; */
    /* text-align: center; */
`;

const Block = styled.div`
    display: flex;
    width: 100%;
    margin-bottom: 80px;
    /* border-bottom: solid ${(props)=> props.theme.colors.POINT_GRAY};
    border-width: 0.1px; */
`;

const Btns = styled.div`
    display: inline-block;
    margin-left: auto;
`;


const Title = styled.div`
    display: inline-block;
    font-size: 38px;
    font-weight: 700;
`;

const Btn = styled.button`
    font-size: 20px;
    background-color: #1070FF;
    border: none;
    letter-spacing: 1px;
    font-weight: 800px;
    color: #FFFFFF;
    padding: 15px;
    width: 180px;
    text-align: center;
    border-width: 0.1px;
    text-decoration: none;
    cursor: pointer;

    &:hover{
        background-color: ${(props)=> props.theme.colors.POINT_BLUE};
    }
`
const Block2 = styled.div`
    display: flex;
    justify-content: space-between;
    margin-top: 50px;
`;
const Btn1 = styled(Btn)`
    color: ${(props)=> props.theme.colors.BLUE};
    background-color: ${(props)=> props.theme.colors.GRAY};
    cursor: default;
    &:hover{
        background-color: ${(props)=> props.theme.colors.GRAY};
    }
`
// const Line = styled.div`
//     width: 5px;
//     color: red;
//     height: 100%;
// `;
const CategoryBox = styled.div`
    display: inline-block;
    width: 500px;
`;

const CategoryBox1 = styled.div`
    display: inline-block;
    width: 1000px;
`;

const Category = styled.div`
    font-size: 25px;
    font-weight: 350;
    margin-bottom: 10px;
    color: ${(props)=> props.theme.colors.BLUE};
`;

const Li = styled.li`
    font-size: 20px;
    list-style: none;
    margin-bottom: 10px;
    strong{
        font-weight: 400;
        color: ${(props)=> props.theme.colors.POINT_GRAY};
        margin-right: 10px;
    }
`;