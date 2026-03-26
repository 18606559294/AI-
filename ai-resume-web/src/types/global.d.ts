/**
 * 全局类型声明
 */

declare module 'web-vitals' {
  export interface Metric {
    name: string;
    value: number;
  }

  export function onCLS(callback: (metric: Metric) => void): void;
  export function onFID(callback: (metric: Metric) => void): void;
  export function onLCP(callback: (metric: Metric) => void): void;
  export function onFCP(callback: (metric: Metric) => void): void;
  export function onTTFB(callback: (metric: Metric) => void): void;
}

declare module 'clsx' {
  function clsx(...inputs: any[]): string;
  export default clsx;
}

declare module 'tailwind-merge' {
  export function twMerge(...inputs: any[]): string;
}
