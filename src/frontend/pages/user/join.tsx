import styled from "styled-components";
import { useForm } from "react-hook-form";
import {useRouter} from 'next/router'
import swal from 'sweetalert';

export default function Join(){
    const router = useRouter();

    interface JoinI {
        username: string,
        password: string,
        password1: string,
        email: string,
        phone_number: string,
        company_id: string,
        company_name: string,
      };

    const regExp = new RegExp(/^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/);

    const onSubmit = (data: JoinI) => {
        fetch('http://3.38.225.207/accounts/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: data.username,
            password: data.password,
            email: data.email,
            phone_number: data.phone_number,
            company_id: data.company_id,
            company_name: data.company_name,
        }),
        })
        .then(response => response.json())
        .then(response => {
                response.pk? (
                    swal("성공!", "회원가입 되었어요.", "success"),
                    router.push('/user/login')
                ) :  swal("실패!", "정보를 다시 확인해주세요.", "error");
            }
        );
    };

    const {
        register,
        handleSubmit,
        watch,
        formState: { errors },
    } = useForm<JoinI>({
    });

    const password = watch("password", "");

    return (
        <Container>
            <Contents>
                {/* 사업자 등록 번호 */}
                <Form
                    onSubmit={handleSubmit(onSubmit)}
                >

                    <Input
                    {...register("company_name", { required: "회사명을 입력해주세요." })}
                    placeholder="회사명"
                    />
                    <Message>{errors?.company_name?.message}</Message>


                    <Input
                    {...register("company_id", { required: "사업자 등록 번호를 입력해주세요." })}
                    placeholder="사업자 등록 번호"
                    />
                    <Message>{errors?.company_id?.message}</Message>

                    <Input
                    {...register("username", { required: "아이디를 입력해주세요." })}
                    placeholder="아이디"
                    />
                    <Message>{errors?.username?.message}</Message>

                    <Password
                    {...register("password", { 
                        required: "비밀번호를 입력해주세요.", 
                        minLength: {
                        value: 5,
                        message: "비밀번호가 너무 짧아요.",
                        }
                    })}

                    placeholder="비밀번호"
                    />
                    <Message>{errors?.password?.message}</Message>
                    <Password
                    {...register("password1", {
                        required: "비밀번호확인을 입력해주세요.",
                        validate: 
                            value => value === password || "비밀번호가 일치하지 않습니다."
                    })}
                    placeholder="비밀번호 재입력"
                    />
                    <Message>{errors?.password1?.message}</Message>

                    <Input
                    {...register("email", {
                        required: "이메일을 입력해주세요",
                        pattern: {
                            value: regExp,
                            message: "유효한 이메일 형식으로 작성해주세요.",
                        },
                    })}
                    placeholder="이메일"
                    />
                    <Message>{errors?.email?.message}</Message>

                    <Input
                    {...register("phone_number", { required: "휴대폰 번호 입력해주세요." })}
                    placeholder="휴대폰 번호"
                    />
                    <Message>{errors?.phone_number?.message}</Message>
                    <Btn>가입하기</Btn>
                </Form>
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

