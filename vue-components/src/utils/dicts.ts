export function applyToValues<T, U>(
  dict: { [key: string]: T },
  f: (value: T) => U,
): { [key: string]: U } {
  const applied_dict: { [key: string]: U } = {}
  for (const [key, value] of Object.entries(dict)) {
    applied_dict[key] = f(value)
  }
  return applied_dict
}
