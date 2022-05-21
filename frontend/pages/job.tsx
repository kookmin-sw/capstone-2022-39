import styled, {keyframes} from "styled-components";
import { useRecoilState } from "recoil";
import { jobAtom } from "../atoms";
import Link from "next/link";
export default function Job(){
    const [job, setJob] = useRecoilState(jobAtom);
    const onClick = (e : React.MouseEvent<HTMLButtonElement>) => {
        setJob(e.target.name);
    }


    let category : string[] =  [
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

    return (
        <Container>
            <Contents>
                <Question>원하시는 직종이 있으신가요?</Question>
                    <Box>{category.map((job, index) => <Link href={"/nodes/searching"}><Choice key = {index} onClick={onClick} name={job}>{job}</Choice></Link>)}</Box>
            </Contents>
        </Container>
    );
}
//recoil로 받음

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

const Box = styled.div`
    display: flex;
    width: 50%;
    flex-wrap: wrap;
`;
const Animation = keyframes`
    from { transform: translateY(40px); opacity: 0;}
    to { transform: translateY(0); opacity: 1;}
 `;

const Question = styled.span`
    letter-spacing: -3px;
    font-size: 40px;
    font-weight: bold;
    animation-name: ${Animation};
    animation-duration: 1s;
    margin-bottom: 5vh;
`;

const Choice = styled.button`
    animation-name: ${Animation};
    animation-duration: 2s;
    width: 50%;
    display: block;
    border-radius: 4px;
    background-color: white;
    border: none;
    color: ${(props)=> props.theme.colors.BLACK};
    text-align: center;
    font-size: 28px;
    padding: 20px;
    font-weight: bold;
    list-style: none;
    cursor: pointer;

    &:hover{
        background-color: ${(props)=> props.theme.colors.BLUE};
        color: ${(props)=> props.theme.colors.GRAY};
    }
    &:focus {
        background-color: ${(props)=> props.theme.colors.BLUE};
        color: ${(props)=> props.theme.colors.GRAY};
    }
`;