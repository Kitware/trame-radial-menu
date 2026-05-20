import type { Point, BBox } from './types'

export function translateBBox(rect: BBox, vec: Point) {
  return {
    left: rect.left + vec.x,
    top: rect.top + vec.y,
    right: rect.right + vec.x,
    bottom: rect.bottom + vec.y,
  }
}

export function BBoxWidth(rect: BBox) {
  return rect.right - rect.left
}

export function BBoxHeight(rect: BBox) {
  return rect.bottom - rect.top
}

export function hasNonZeroArea(box: BBox): boolean {
  return box.top != box.bottom && box.left != box.right
}

export function domRectToBBox(rect: DOMRect) {
  return { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom }
}

export function bBoxUnion(a: BBox, b: BBox): BBox {
  if (!a) return b
  if (!b) return a
  const minX = Math.min(a.left, b.left)
  const minY = Math.min(a.top, b.top)
  const maxX = Math.max(a.right, b.right)
  const maxY = Math.max(a.bottom, b.bottom)
  return { left: minX, top: minY, right: maxX, bottom: maxY }
}
