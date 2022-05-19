import styled, {keyframes} from "styled-components";
import { useRecoilState } from "recoil";
import { jobsAtom } from "../atoms";
import Link from "next/link";
export default function Job(){
    const test = ["보험","경호원","환경미화원","청소","파일정리","테스트","테스트입니다"]

    const [jobs, setJobs] = useRecoilState(jobsAtom);
    const onClick = (e : React.MouseEvent<HTMLButtonElement>) => {
        setJobs(e.target.name);
    }

    return (
        <Container>
            <Contents>
                <Question>원하시는 직종이 있으신가요?</Question>
                {test.map((test, index) => <Link href={"/nodes/searching"}><Choice key = {index} onClick={onClick} name={test}>{test}</Choice></Link>)}
            {/* //     <br></br>
            //  <Link href={"/searching"}>확인</Link> */}

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
    width: 100%;
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