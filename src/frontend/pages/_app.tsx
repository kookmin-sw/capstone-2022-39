import type {AppProps} from 'next/app';
import { RecoilRoot } from 'recoil';
import styled from 'styled-components';
import {ThemeProvider} from 'styled-components';
import {GlobalStyle} from '../styles/global-styles';
import {theme} from '../styles/theme';
import Link from "next/link";
import logo from "../public/logo.png";
import Image from 'next/image'


// STARTS HERE
import * as AWS from 'aws-sdk'
import { ConfigurationOptions } from 'aws-sdk'

const configuration: ConfigurationOptions = {
    region: process.env.NEXT_PUBLIC_REGION,
    secretAccessKey: process.env.NEXT_PUBLIC_SECRET_ACCESS_KEY,
    accessKeyId: process.env.NEXT_PUBLIC_ACCESS_KEY_ID,
}

AWS.config.update(configuration)
// ENDS HERE

export default function App({Component, pageProps}: AppProps) {
  return (
      <RecoilRoot>
        <ThemeProvider theme={theme}>
            <GlobalStyle/>
            <Helmet>
              <head>
                {`
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=East+Sea+Dokdo&family=Noto+Sans+KR:wght@100;300;400;500;700;900&display=swap" rel="stylesheet">
                `}
            </head>
            </Helmet>
            <Container>
              <Wrap>
                  <Link href = "/"><Logo><Image src={logo} width={100} height={45} alt="logo"></Image></Logo></Link>
              </Wrap>
            </Container>
            <Component {...pageProps} />  
        </ThemeProvider>
      </RecoilRoot>
  );
}

const Container = styled.div`
  max-width: 1600px;
`;

const Wrap = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 44px;
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: right; 
  /* background-color: #f4f4f7; */
`;

const Logo = styled.span`
    opacity: 95%;
    margin-right: 50px;
    cursor: pointer;
  /* @media (max-width: ${(props) => props.theme.breakPoint}) {
    width: 100%;
  } */
`;

