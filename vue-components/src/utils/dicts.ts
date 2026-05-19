import type { EightSymmetryPoints, Point } from './types'

export function applyToValues<U>(
  dict: EightSymmetryPoints,
  f: (value: Point) => U,
): { [key: string]: U } {
  const applied_dict: { [key: string]: U } = {}
  for (const [key, value] of Object.entries(dict)) {
    applied_dict[key] = f(value)
  }
  return applied_dict
}
