import { faCircleHalfStroke, faMoon, faSun  } from "@fortawesome/free-solid-svg-icons";
import { Theme } from "./interfaces/theme";


export const Themes: Theme[] = [
  {
    id: 'light',
    displayName: 'ライト',
    icon: faSun,
  },
  {
    id: 'dark',
    displayName: 'ダーク',
    icon: faMoon,
  },
  {
    id: 'auto',
    displayName: '自動',
    icon: faCircleHalfStroke,
  },
];
