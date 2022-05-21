import styled, {keyframes} from "styled-components"
import Link from "next/link";
import Image from "next/image";
import Emo from "../public/emo.png"
export default function Home(){
    return (
    <Container>
        <Contents>
            <Question><strong>안녕하세요 .</strong></Question>
            <br/>
            <Question1>어르신에게 꼭 맞는 일자리를 찾아 드릴게요 .</Question1>
            <Link href={"/city"}>
                <Btn>좋아요.</Btn>
            </Link>
            <Link href={"/nodes"}><Btn2>모든 공고 보러가기 ></Btn2></Link>
            <Wrap>
                <Image src={Emo} width={25} height={20} alt="emo"/>
                <Link href={"/join_check"}><span>공고 글을 올리고 싶나요?</span></Link>
            </Wrap>
        </Contents>
    </Container>
    )
}

const Container = styled.div`

    text-align: center;
    display: grid;
    place-items: center;
`;

const Contents = styled.div`
    max-width: 1000px;
    display: flex;
    justify-content: center;
    align-items:center;
    min-height: 100vh; 
    flex-direction: column;
`;
// const Animation = keyframes`
//  0% { height: 100px; width: 100px; }
//  30% { height: 400px; width: 400px; opacity: 1 }
//  40% { height: 405px; width: 405px; opacity: 0.3; }
//  100% { height: 100px; width: 100px; opacity: 0.6; }
//  `;

// const Question = styled.span`
//     font-size: 50px;
//     font-weight: bold;
//     animation-name: ${Animation};
//     animation-duration: 1s;
//     animation-iteration-count: infinite;
// `;

const Animation = keyframes`
    from { transform: translateY(40px); opacity: 0;}
    to { transform: translateY(0); opacity: 1;}
 `;

const Question = styled.span`
     letter-spacing: -3px;
     font-size: 40px;
     font-weight: bold;
     strong{
        font-size: 50px;
    }
    animation-name: ${Animation};
    animation-duration: 1s;
`;

const Question1 = styled.span`
     letter-spacing: -3px;
     font-size: 40px;
     font-weight: bold;
     strong{
        font-size: 50px;
    }
    animation-name: ${Animation};
    animation-duration: 2s;

`;

const Btn = styled.button`
    font-size: 32px;
    position: relative;
    background-color: #1070FF;
    border: none;
    letter-spacing: 1px;
    font-weight: 800px;
    color: #FFFFFF;
    padding: 25px;
    width: 200px;
    text-align: center;
    border-radius: 10px;
    text-decoration: none;
    cursor: pointer;
    margin-top: 30px;

    &:hover{
        background-color: ${(props)=> props.theme.colors.POINT_BLUE};
    }
`
const Btn2 = styled.button`
    margin-top: 10px;
    text-decoration: none;
    border: none;
    background-color: white;
    color: #1070FF;
    font-size: 20px;
    cursor: pointer;
`
const Wrap = styled.div`
    margin-top: 50px;
    display: flex;
    flex-direction: row;
    font-size: 20px;
    font-weight: 300;
    color: #B1B1B1;
    cursor: pointer;
`

//애니매이션 라이브러리 사용, 안녕하세요 나타나고, 어르신 ~ 나타나기
