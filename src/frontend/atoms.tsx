import { atom, selector } from "recoil";

export interface Idata {
    title: string,
    primary_key: string,
    url: string,
    workplace: string;
    recruitment_staff: string,
    recruitment_field: string,
    qualification_license: string,
    job_specifications: string,
    employment: string,
    wages: string,
    business_hours: string,
    recruiter: string,
    contact_address: string,
    registration_date: string,
}

export const loginAtom = atom({
    key: "loginAtom",
    default: false,
});

export const jwtToken = atom({
    key: "jwtToken",
    default: "",
});

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
    default: "전체",
});

export const citydataAtom = atom({
    key: "cityDataAtom",
    default: [],
})

export const dataAtom = atom<Idata[]>({
    key: "data",
    default: [],
});


export const keyWordAtom = atom({
    key:"keyWordAtom",
    default: "default",
})

export const keyWordFilter = selector({
    key: "keyWordFilter",
    get: ({ get }) => {
    let data = get(dataAtom);
    let keyword = get(keyWordAtom);
    return {data}.data.filter(data => ({data}.data.workplace.includes(keyword) || {data}.data.title.includes(keyword) || {data}.data.qualification_license.includes(keyword)));
    //{data}.data.recruitment_field.includes(keyword)
    }
});


export const cityFilter = selector({
  key: "cityfilter",
  get: ({ get }) => {
    let data = get(dataAtom);
    let city = get(cityAtom);
    city = city.replace("특별시", "");
    city = city.replace("광역시", "");
    city = city.replace("특별자치시", "");
    city = city.replace("특별자치도", "");
    // console.log("city:", city);

    let city1 = get(city1Atom);
    if (city1.length > 2){
        city1 = city1.slice(0, -1); //맨 끝 글자만 자르기
    }
    // console.log("city1:" , city1);

    let city2 = get(city2Atom);
    if (city2.length > 2){
        city2 = city2.slice(0, -1);
    }
    // console.log("city2:" , city2);

    return {data}.data.filter(data => ({data}.data.workplace.includes(city) || {data}.data.workplace.includes(city1) || {data}.data.workplace.includes(city2)));
    }
});

export const jobSelector = selector({
    key: "jobfilter",
    get: ({ get }) => {
        const data = get(cityFilter);
    let job = get(jobAtom);
    return {data}.data.filter(data => ({data}.data.recruitment_field) == job);
    }
});