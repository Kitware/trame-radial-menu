export function polar(cx, cy, r, angle) {
  const rad = ((angle - 90) * Math.PI) / 180 // angle 0 is up
  return {
    x: cx + r * Math.cos(rad),
    y: cy + r * Math.sin(rad),
  }
}

export function donutSlicePath(cx, cy, r1, r2, start, end, totalSize) {
  // Offset so the middle of the slice of the first item is at angle start
  const offset = (end - start) / (2 * totalSize)
  start = start - offset
  end = end - offset

  const full = end - start >= 360

  if (full) {
    // split into two semicircles.
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

// When thisBeginSize and thisEndSize are between 0 and totalSize, returns
// thisBeginAngle and thisEndAngle between beginAngle and endAngle, shifted so
// the thisMidAngle is at beginAngle when thisBeginSize=0
export function thisBeginAndEndAnglesFromSizes(
  beginAngle,
  endAngle,
  totalSize,
  thisBeginSize,
  thisEndSize,
) {
  const totalAngle = endAngle - beginAngle
  const offset = beginAngle - totalAngle / (2 * totalSize) // shifted so thisMidAngle is at beginAngle when thisBeginSize=0
  const thisBeginAngle = offset + (totalAngle / totalSize) * thisBeginSize
  const thisEndAngle = offset + (totalAngle / totalSize) * thisEndSize
  return [thisBeginAngle, thisEndAngle]
}

// Given a point of coordinates (a, b) in a [-1, 1] coordinate interval, returns
// the 8 symmetry points by vertical, horizontal, and diagonal axis in a [0, 2*w]
// coordinate interval
export function getEightSymmetryPoints(a, b, w) {
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

export function pointToStyle(point) {
  const [x, y] = point
  return {
    left: `${x}px`,
    top: `${y}px`,
  }
}

export function boxToStyle(w, h) {
  return {
    width: `${w}px`,
    height: `${h}px`,
  }
}
