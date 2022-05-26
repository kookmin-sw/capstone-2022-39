import {createGlobalStyle} from 'styled-components';
import {normalize} from 'styled-normalize';

export const GlobalStyle = createGlobalStyle`


@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;900&display=swap');

  ${normalize}

  html {
    box-sizing: border-box;
    font-size: 62.5%;
    min-width: 320px;
} 
  * {
    font-family: 'Noto Sans KR', sans-serif;
  }

  button {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
  }

  a { cursor: pointer; text-decoration: none; }
`;

