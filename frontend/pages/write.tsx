import styled from "styled-components";
import { useForm } from "react-hook-form";
import { Idata } from "../atoms";


export default function Write(){

    const onSubmit = (data) => {
        console.log(data);
    };

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<Idata>();

return (
    <Container>
        <Contents>
            <Form
                onSubmit={handleSubmit(onSubmit)}
            >
                <Input
                {...register("business_hours", {
                    required: "근무시간을 입력해주세요",
                })}
                placeholder="근무시간"
                />
                <span>{errors?.business_hours?.message}</span>

                <Input
                {...register("job_specifications", { required: "특이사항을 입력해주세요.", minLength: 5 })}
                placeholder="특이사항"
                />
                <span>{errors?.job_specifications?.message}</span>

                <Input
                {...register("qualification_license", { required: "자격사항을 입력해주세요.", minLength: 5 })}
                placeholder="자격사항"
                />
                <span>{errors?.qualification_license?.message}</span>


                <Input
                {...register("workplace", { required: "근무지를 입력해주세요.", minLength: 5 })}
                placeholder="근무지"
                />
                <span>{errors?.workplace?.message}</span>


                <Input
                {...register("title", { required: "공고 제목을 입력해주세요.", minLength: 5 })}
                placeholder="공고 제목"
                />
                <span>{errors?.title?.message}</span>

                <Input
                {...register("recruitment_staff", { required: "모집인원을 입력해주세요.", minLength: 5 })}
                placeholder="모집인원"
                />
                <span>{errors?.recruitment_staff?.message}</span>


                <Input
                {...register("wages", { required: "임금을 입력해주세요.", minLength: 5 })}
                placeholder="임금"
                />
                <span>{errors?.wages?.message}</span>

                <Input
                {...register("recruitment_field", { required: "분야을 입력해주세요.", minLength: 5 })}
                placeholder="분야"
                />
                <span>{errors?.recruitment_field?.message}</span>

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

const Btn = styled.button``;