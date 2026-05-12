export function applyToValues(dict, f) {
  const applied_dict = {}
  for (const key in dict) {
    applied_dict[key] = f(dict[key])
  }
  return applied_dict
}
