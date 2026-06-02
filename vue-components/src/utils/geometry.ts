import type {
  Point,
  EightSymmetryPoints,
  Interval,
  Box,
  TopLeftAnchor,
  BottomLeftAnchor,
  TopRightAnchor,
  BoxSize
} from './types'

export function polar(cx: number, cy: number, r: number, angle: number): Point {
  const rad: number = ((angle - 90) * Math.PI) / 180 // angle 0 is up
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) }
}

export function donutSlicePath(
  cx: number,
  cy: number,
  r1: number,
  r2: number,
  start: number,
  end: number,
  totalSize: number,
): string {
  // Offset so the middle of the slice of the first item is at angle start
  const offset = (end - start) / (2 * totalSize)
  start = start - offset
  end = end - offset

  const full = end - start >= 360

  // A full donut can't be drawn with a single donut slice
  if (full) {
    // It needs to be split into two semicircles.
    const o1 = polar(cx, cy, r1, start)
    const o2 = polar(cx, cy, r1, start + 180)
    const i1 = polar(cx, cy, r2, start)
    const i2 = polar(cx, cy, r2, start + 180)
    return [
      `M ${o1.x} ${o1.y}`,
      `A ${r1} ${r1} 0 1 1 ${o2.x} ${o2.y}`,
      `A ${r1} ${r1} 0 1 1 ${o1.x} ${o1.y}`,
      `Z`,
      `M ${i1.x} ${i1.y}`,
      `A ${r2} ${r2} 0 1 0 ${i2.x} ${i2.y}`,
      `A ${r2} ${r2} 0 1 0 ${i1.x} ${i1.y}`,
      `Z`,
    ].join(' ')
  }

  const outerStart = polar(cx, cy, r1, start)
  const outerEnd = polar(cx, cy, r1, end)
  const innerStart = polar(cx, cy, r2, start)
  const innerEnd = polar(cx, cy, r2, end)
  const large = end - start > 180 ? 1 : 0

  return [
    `M ${outerStart.x} ${outerStart.y}`,
    `A ${r1} ${r1} 0 ${large} 1 ${outerEnd.x} ${outerEnd.y}`,
    `L ${innerEnd.x} ${innerEnd.y}`,
    `A ${r2} ${r2} 0 ${large} 0 ${innerStart.x} ${innerStart.y}`,
    `Z`,
  ].join(' ')
}

// There is an affine relation between itemBeginAngle and itemBeginSize and between itemEndAngle and
// itemEndSize
// itemBeginSize, itemEndSize in [0, totalSize] =>
//   itemBeginAngle, itemEndAngle in [beginAngle, endAngle]
// We slightly shift so that itemBeginSize = 0 => itemMidAngle = beginAngle
export function itemBeginAndEndAnglesFromSizes(
  beginAngle: number,
  endAngle: number,
  totalSize: number,
  itemBeginSize: number,
  itemEndSize: number,
): Interval {
  const totalAngle: number = endAngle - beginAngle
  // shifted so that itemBeginSize = 0 => itemMidAngle = beginAngle
  const offset: number = -totalAngle / (2 * totalSize)
  const itemBeginAngle: number = beginAngle + offset + (totalAngle / totalSize) * itemBeginSize
  const itemEndAngle: number = beginAngle + offset + (totalAngle / totalSize) * itemEndSize
  return [itemBeginAngle, itemEndAngle]
}

// Given a point of coordinates (a, b) in a [-1, 1] coordinate interval, returns the 8 symmetry
// points by vertical, horizontal, and diagonal axis in a [0, 2*w] coordinate interval
export function getEightSymmetryPoints(a: number, b: number, w: number): EightSymmetryPoints {
  return {
    'right-bottom': { x: w * (1 + a), y: w * (1 + b) },
    'bottom-right': { x: w * (1 + b), y: w * (1 + a) },
    'bottom-left': { x: w * (1 - b), y: w * (1 + a) },
    'left-bottom': { x: w * (1 - a), y: w * (1 + b) },
    'left-top': { x: w * (1 - a), y: w * (1 - b) },
    'top-left': { x: w * (1 - b), y: w * (1 - a) },
    'top-right': { x: w * (1 + b), y: w * (1 - a) },
    'right-top': { x: w * (1 + a), y: w * (1 - b) },
  }
}

// Style to anchor a DOM element's top left corner to a point
export function pointToStyle(point: Point): TopLeftAnchor {
  return {
    left: `${point.x}px`,
    top: `${point.y}px`,
  }
}

// style to anchor a dom element's bottom right corner to a point
export function pointToStyleBottomLeft(point: Point): BottomLeftAnchor {
  return {
    left: `${point.x}px`,
    bottom: `${point.y}px`,
  }
}

// style to anchor a dom element's bottom right corner to a point
export function pointToStyleTopRight(point: Point): TopRightAnchor {
  return {
    right: `${point.x}px`,
    top: `${point.y}px`,
  }
}

export function boxToStyle(box: Box): BoxSize {
  const [w, h] = box
  return {
    width: `${w}px`,
    height: `${h}px`,
  }
}
