import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme {
    breakPoint: string;

    bg: string;

    colors: {
      BLACK: string;
      red: string;
      yellow: string;
      orange: string;
      GRAY: string;
      BLUE: string;
      POINT_BLUE: string;
    };
  }
}