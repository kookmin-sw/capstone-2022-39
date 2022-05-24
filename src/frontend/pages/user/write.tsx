import styled from "styled-components";
import { useForm } from "react-hook-form";
import {useRouter} from 'next/router'
import { useRecoilState } from "recoil";
import { jwtToken } from "../../atoms";
import * as AWS from 'aws-sdk';
import swal from 'sweetalert';

export default function Write(){
    let today = new Date();   

    // let year = today.getFullYear(); // 년도
    let year = today.getFullYear() % 1000;
    let month = String(today.getMonth() + 1).padStart(2,"0");  // 월
    let date = String(today.getDate()).padStart(2,"0");  // 날짜
    let dateString = year + '/' + month + '/' + date;

    const router = useRouter();
    const [token, SetToken] = useRecoilState(jwtToken);

    const docClient = new AWS.DynamoDB.DocumentClient();

    const putData = (tableName: string, data) => {
        var params = {
            TableName: tableName,
            Item: data
        }
        
        docClient.put(params, function(err, data) {
            if (err) {
                console.log('Error', err)
            } else {
                console.log('Success', data)
            }
        })
    }

    interface Iwrite{
        title: string,
        url: string,
        pay: string,
        location: string,
        gather_count: string,
        category: string,
        recruiter: string,
        call_number: string,
        content: string,
        employment: string,
        work_time: string,
        qualification_license: string,
    }

    const onSubmit = (data: Iwrite) => {
        fetch('http://3.38.225.207/api/recruitment/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${token}`,
        },
        
        body: JSON.stringify({
            title: data.title,
            url: data.url,
            pay: data.pay,
            location: data.location,
            gather_count: data.gather_count,
            category: data.category,
            recruiter: data.recruiter,
            call_number: data.call_number,
            content: data.content,
            employment: data.employment,
            work_time: data.work_time,
            qualification_license: data.qualification_license,
        }),
        })
        .then(response => response.json())
        .then(response => {
            response.author? (
                swal("성공!", "공고 글이 올라갔어요.", "success"),
                router.push("/"),
                putData(`${process.env.NEXT_PUBLIC_TABLE_NAME}`,
                    {   
                        "primary_key": `ILL#${data.title}#${data.recruiter}#${data.location}`,
                        "title": data.title,
                        "url": data.url,
                        "wages": data.pay,
                        "workplace": data.location,
                        "recruitment_staff": data.gather_count,
                        "recruitment_field": data.category,
                        "recruiter": data.recruiter,
                        "contact_address": data.call_number,
                        "job_specifications": data.content,
                        "employment": data.employment,
                        "business_hours": data.work_time,
                        "qualification_license": data.qualification_license,
                        "registration_date": dateString,
                    }
                )
                ):  swal("실패!", "내용을 다시 확인해주세요.", "error");
            });
        };
    

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<Iwrite>();

return (
    <Container>
        <Contents>
            <Form   
                onSubmit={handleSubmit(onSubmit)}
            >
                <Input
                {...register("title", { required: "공고 제목을 입력해주세요.", })}
                placeholder="공고 제목"
                />
                <span>{errors?.title?.message}</span>

                <Input
                {...register("url", { required: "URL을 입력해주세요.",})}
                placeholder="URL"
                />
                <span>{errors?.url?.message}</span>

                <Input
                {...register("pay", { required: "임금을 입력해주세요.", })}
                placeholder="임금"
                />
                <span>{errors?.pay?.message}</span>

                <Input
                {...register("location", { required: "근무지를 입력해주세요.", })}
                placeholder="근무지"
                />
                <span>{errors?.location?.message}</span>


                <Input
                {...register("gather_count", { required: "모집인원을 입력해주세요.", })}
                placeholder="모집인원"
                />
                <span>{errors?.gather_count?.message}</span>


                <Input
                {...register("category", { required: "분야을 입력해주세요.", })}
                placeholder="분야"
                />
                <span>{errors?.category?.message}</span>

                <Input
                {...register("recruiter", { required: "담당자명을 입력해주세요.", })}
                placeholder="담당자"
                />
                <span>{errors?.recruiter?.message}</span>

                <Input
                {...register("call_number", { required: "연락처를 입력해주세요.", })}
                placeholder="연락처"
                />
                <span>{errors?.call_number?.message}</span>

                <Input
                {...register("content", { required: "특이사항을 입력해주세요.", })}
                placeholder="특이사항"
                />
                <span>{errors?.content?.message}</span>

                <Input
                {...register("employment", {
                    required: "고용형태를 입력해주세요",
                })}
                placeholder="고용형태"
                />
                <span>{errors?.employment?.message}</span>

                <Input
                {...register("work_time", {
                    required: "근무시간을 입력해주세요",
                })}
                placeholder="근무시간"
                />
                <span>{errors?.work_time?.message}</span>


                <Input
                {...register("qualification_license", { required: "자격사항을 입력해주세요.", })}
                placeholder="자격사항"
                />
                <span>{errors?.qualification_license?.message}</span>
                <Btn>글쓰기</Btn>
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
    display; grid;
    grid-template-columns: 500px 500px;
    width: 1000px;
    flex-direction: column;
`;

const Input = styled.input`
    display: inline;
    width: 300px;
    padding: 20px;
    margin: 10px;
    font-size: 20px;
    margin-bottom: 10px;
    border: none;
    border-radius: 10px;
    background-color: ${(props) => props.theme.colors.GRAY};
`;

const Btn = styled.button`
    margin-top: 30px;
    font-size: 20px;
    position: relative;
    background-color: ${(props) => props.theme.colors.BLUE};
    color: ${(props) => props.theme.colors.GRAY};
    border: none;
    letter-spacing: 1px;
    width: 700px;
    font-weight: 500;
    text-align: center;
    border-radius: 10px;
    text-decoration: none;
    padding: 10px;
    cursor: pointer;
`;