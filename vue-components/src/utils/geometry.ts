import type { Point, EightSymmetryPoints, Interval, Box } from './types'

export function polar(cx: number, cy: number, r: number, angle: number): Point {
  const rad: number = ((angle - 90) * Math.PI) / 180 // angle 0 is up
  return [cx + r * Math.cos(rad), cy + r * Math.sin(rad)]
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
      `M ${o1[0]} ${o1[1]}`,
      `A ${r1} ${r1} 0 1 1 ${o2[0]} ${o2[1]}`,
      `A ${r1} ${r1} 0 1 1 ${o1[0]} ${o1[1]}`,
      `Z`,
      `M ${i1[0]} ${i1[1]}`,
      `A ${r2} ${r2} 0 1 0 ${i2[0]} ${i2[1]}`,
      `A ${r2} ${r2} 0 1 0 ${i1[0]} ${i1[1]}`,
      `Z`,
    ].join(' ')
  }

  const outerStart = polar(cx, cy, r1, start)
  const outerEnd = polar(cx, cy, r1, end)
  const innerStart = polar(cx, cy, r2, start)
  const innerEnd = polar(cx, cy, r2, end)
  const large = end - start > 180 ? 1 : 0

  return [
    `M ${outerStart[0]} ${outerStart[1]}`,
    `A ${r1} ${r1} 0 ${large} 1 ${outerEnd[0]} ${outerEnd[1]}`,
    `L ${innerEnd[0]} ${innerEnd[1]}`,
    `A ${r2} ${r2} 0 ${large} 0 ${innerStart[0]} ${innerStart[1]}`,
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
    'right-bottom': [w * (1 + a), w * (1 + b)],
    'bottom-right': [w * (1 + b), w * (1 + a)],
    'bottom-left': [w * (1 - b), w * (1 + a)],
    'left-bottom': [w * (1 - a), w * (1 + b)],
    'left-top': [w * (1 - a), w * (1 - b)],
    'top-left': [w * (1 - b), w * (1 - a)],
    'top-right': [w * (1 + b), w * (1 - a)],
    'right-top': [w * (1 + a), w * (1 - b)],
  }
}

// Style to anchor a DOM element's top left corner to a point
export function pointToStyle(point: Point): { left: string; top: string } {
  const [x, y] = point
  return {
    left: `${x}px`,
    top: `${y}px`,
  }
}

// style to anchor a dom element's bottom right corner to a point
export function pointToStyleBottomLeft(point: Point): { left: string; bottom: string } {
  const [x, y] = point
  return {
    left: `${x}px`,
    bottom: `${y}px`,
  }
}

// style to anchor a dom element's bottom right corner to a point
export function pointToStyleTopRight(point: Point): { right: string; top: string } {
  const [x, y] = point
  return {
    right: `${x}px`,
    top: `${y}px`,
  }
}

export function boxToStyle(box: Box): { width: string; height: string } {
  const [w, h] = box
  return {
    width: `${w}px`,
    height: `${h}px`,
  }
}
