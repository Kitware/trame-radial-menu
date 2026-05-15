import { inject, type InjectionKey } from 'vue'

export function safeInject<T>(key: InjectionKey<T> | string, errorMessage: string): T {
  const value = inject<T>(key)
  if (!value) throw new Error(errorMessage)
  return value
}
