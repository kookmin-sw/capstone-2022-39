import { atom, selector } from "recoil";
export interface Idata {
    title: string;
    url: string;
    workplace: string;
    recruitment_staff: string;
    recruitment_field: string;
    qualification_license: string;
    job_specifications: string;
    employment: string;
    wages: string;
    business_hours: string;
    recruiter: string;
    contact_address: string;
}
export const cityAtom = atom({
    key: "city",
    default: "",
});

export const city1Atom = atom({
    key: "city1",
    default: "",
});

export const city2Atom = atom({
    key: "city2",
    default: "",
});

export const jobAtom = atom({
    key: "job",
    default: "",
});

export const citydataAtom = atom({
    key: "cityDataAtom",
    default: [],
})

export const dataAtom = atom<Idata[]>({
    key: "data",
    default: [],
});

export const jobSelector = selector({
    key: "jobfilter",
    get: ({ get }) => {
        const data = get(dataAtom);
    let job = get(jobAtom);
    return {data}.data.filter(data => ({data}.data.recruitment_field) == job);
    }
});

export const cityFilter = selector({
  key: "cityfilter",
  get: ({ get }) => {
    const data = get(jobSelector);

    let city = get(cityAtom);
    city = city.replace("특별시", "");
    city = city.replace("광역시", "");
    city = city.replace("특별자치시", "");
    city = city.replace("특별자치도", "");
    console.log("city:", city);

    //서구 같은 경우는 서구라고 적으니까.. 
    // 서구 -> 강서구,, 뜨는...
    let city1 = get(city1Atom);
    if (city1.length > 2){
        city1 = city1.slice(0, -1); //맨 끝 글자만 자르기
    }
    console.log("city1:" , city1);

    let city2 = get(city2Atom);
    if (city2.length > 2){
        city2 = city2.slice(0, -1);
    }
    console.log("city2:" , city2);

    return {data}.data.filter(data => ({data}.data.workplace.includes(city) || {data}.data.workplace.includes(city1) || {data}.data.workplace.includes(city2)));
    }
});

