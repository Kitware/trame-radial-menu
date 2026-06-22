import type { CSSProperties } from 'vue'

export interface Point {
  x: number
  y: number
}

export type Interval = [number, number]

export type Box = [number, number]

export interface EightSymmetryPoints {
  'right-bottom': Point
  'bottom-right': Point
  'bottom-left': Point
  'left-bottom': Point
  'left-top': Point
  'top-left': Point
  'top-right': Point
  'right-top': Point
}

export interface BBox {
  top: number
  left: number
  bottom: number
  right: number
}

export interface TopLeftAnchor extends CSSProperties {
  left: string
  top: string
}

export interface BottomLeftAnchor extends CSSProperties {
  left: string
  bottom: string
}

export interface TopRightAnchor extends CSSProperties {
  right: string
  top: string
}

export interface BoxSize extends CSSProperties {
  width: string
  height: string
}
