import styled, {keyframes} from "styled-components";
import Image from 'next/image'
import join from '../../public/join.png';
import login from '../../public/login.png';


import Link from "next/link";
export default function check_join(){
    return (
        <Container>
            <Contents>
                <Question>회원만 공고를 올릴 수 있어요 .</Question>
                <Btns>
                    <Link href="/user/join"><Btn><Wrap><Image src={join} width={32} height={30} alt="logo"/> 회원가입</Wrap></Btn></Link>
                    <Link href="/user/login"><Btn2><Wrap><Image src={login} width={32} height={30} alt="logo"/> 로그인</Wrap> </Btn2></Link>
                </Btns>
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
    from { transform: translateY(15px); opacity: 0.5;}
    to { transform: translateY(0); opacity: 1;}
 `;

const Question = styled.div`
    letter-spacing: -3px;
    font-size: 50px;
    font-weight: bold;
    animation-name: ${Animation};
    animation-duration: 1s;
`;

const Btns = styled.div`
    display: flex;
`;

const Wrap = styled.div`
    /* display: flex; */
    justify-content: center;
    align-items:center;
`;

const Btn = styled.button`
    font-size: 35px;
    position: relative;
    background-color: ${(props) => props.theme.colors.BLUE};
    color: ${(props) => props.theme.colors.GRAY};
    border: none;
    letter-spacing: 1px;
    padding: 40px;
    width: 250px;
    font-weight: 500;
    text-align: center;
    border-radius: 10px;
    text-decoration: none;
    cursor: pointer;
    margin-top: 30px;
    margin-right: 20px;
`;

const Btn2 = styled.button`
    font-size: 35px;
    position: relative;
    background-color: ${(props) => props.theme.colors.GRAY};
    color: ${(props) => props.theme.colors.BLUE};
    border: none;
    letter-spacing: 1px;
    font-weight: 500;
    padding: 40px;
    width: 250px;
    font-weight: medium;
    text-align: center;
    border-radius: 10px;
    text-decoration: none;
    cursor: pointer;
    margin-top: 30px;
    margin-right: 20px;
`;