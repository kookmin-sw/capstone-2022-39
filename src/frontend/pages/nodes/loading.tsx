import { useRecoilState } from "recoil";
import styled, {keyframes} from "styled-components";
import { cityAtom, city1Atom, city2Atom} from "../../atoms";
import { useRouter } from "next/router";


export default function Loading(){

    const router = useRouter();

    setTimeout(function() {
        router.push('/nodes/searching');
      }, 1500);
    
    const [city, setCity] = useRecoilState(cityAtom);
    const [city1, setCity1] = useRecoilState(city1Atom);
    const [city2, setCity2] = useRecoilState(city2Atom);

    return (
        <Container>
            <Contents>
            <Question><strong>{city}, {city1}, {city2}</strong>에서 일자리를 찾고 있어요 .</Question>
            <Spinner></Spinner>
        </Contents>
        </Container>
    )
}

const Question = styled.span`
    font-size: 40px;
    font-weight: bold;
    strong{
        color: ${(props)=> props.theme.colors.BLUE};
        font-size: 50px;
    }
`;

const rotation = keyframes`
    from{
        transform: rotate(0deg);
    }

    to{
        transform: rotate(360deg);
    }

`;

const Spinner = styled.div`
	height: 80px;
	width: 80px;
	border: 4px solid ${(props)=> props.theme.colors.BLUE};
	border-radius: 50%;
	border-top: none;
	border-right: none;
	margin: 80px auto;
	animation: ${rotation} 1s linear infinite;
`;


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
export { Spinner };