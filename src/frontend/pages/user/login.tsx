import styled from "styled-components";
import { useForm } from "react-hook-form";
import {useRouter} from 'next/router'
import { useRecoilState } from "recoil";
import { jwtToken } from "../../atoms";
import swal from 'sweetalert';


export default function Login(){
    const router = useRouter();

    const [token, SetToken] = useRecoilState(jwtToken);

    // const regExp = new RegExp(/^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/);

    interface LoginI {
        username: string,
        password: string,
    }

    const onValid = (data: LoginI) => {
        fetch('http://3.38.225.207/accounts/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: data.username,
            password: data.password,
            }),
        })
        .then(response => response.json())
        .then(response => { 
                response.non_field_errors ?  swal("실패!", "정보를 다시 확인해주세요.", "error") : (
                    swal("성공!", "로그인 되었어요.", "success"),
                    SetToken(response.token),
                    router.push("write")
                );
            }
        )
    };

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginI>({
        defaultValues: {
            // email: "@naver.com",
        },
    });

    return (
        <Container>
            <Contents>
                {/* 사업자 등록 번호 */}
                <Form
                    onSubmit={handleSubmit(onValid)}
                >
                    <Input
                    {...register("username", {
                        required: "아이디를 입력해주세요",
                        // pattern: {
                        //     value: regExp,
                        //     message: "유효한 이메일 형식으로 작성해주세요.",
                        // },
                    })}
                    placeholder="아이디"
                    />
                    <Message>{errors?.username?.message}</Message>
                    <Password
                    {...register("password", { required: "비밀번호를 입력해주세요.", minLength: 5})}
                    placeholder="비밀번호"
                    />
                    <Message>{errors?.password?.message}</Message>
                    <Btn>로그인</Btn>
                </Form>
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

const Form = styled.form`
    width: 400px;
    display: flex;
    flex-direction: column;
`;

const Input = styled.input`
    padding: 20px;
    font-size: 20px;
    margin-bottom: 10px;
    border: none;
    border-radius: 10px;
    background-color: ${(props) => props.theme.colors.GRAY};
`;

const Password = styled(Input).attrs({ type: 'password' })`
`;


const Btn = styled.button`
    font-size: 20px;
    position: relative;
    background-color: ${(props) => props.theme.colors.BLUE};
    color: ${(props) => props.theme.colors.GRAY};
    border: none;
    letter-spacing: 1px;
    width: 400px;
    font-weight: 500;
    text-align: center;
    border-radius: 10px;
    text-decoration: none;
    padding: 10px;
    cursor: pointer;
    margin-right: 20px;
`;

const Message = styled.span`
    padding: 10px;
    font-size: 15px;
    color: ${(props) => props.theme.colors.BLUE};
`;