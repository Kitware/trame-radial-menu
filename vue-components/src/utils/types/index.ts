export type Point = [number, number]

export type Interval = [number, number]

export type Box = [number, number]

export type EightSymmetryPoints = {
  'right-bottom': Point
  'bottom-right': Point
  'bottom-left': Point
  'left-bottom': Point
  'left-top': Point
  'top-left': Point
  'top-right': Point
  'right-top': Point
}

export type BBox = {
  top: number
  left: number
  bottom: number
  right: number
}
