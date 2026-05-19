<template>
  <svg :width="maxRadius * 2" :height="maxRadius * 2">
    <path :d="donutPath" :fill="props.color" />
  </svg>
  <slot />
</template>

<script setup lang="ts">
import { provide, inject, ref, computed, onUnmounted, type Ref, type ComputedRef } from 'vue'

import type { Interval } from '@/utils/types'
import { donutSlicePath, itemBeginAndEndAnglesFromSizes } from '../utils/geometry'

// Setup

const props = withDefaults(
  defineProps<{
    innerRadius: number
    outerRadius: number
    beginAngle: number
    endAngle: number
    color: string
  }>(),
  {
    innerRadius: -1,
    outerRadius: -1,
    beginAngle: 0,
    endAngle: 360,
    color: '#7777',
  },
)

// Handle inner and outer radii

const parentInnerAndOuterRadii = inject<[Ref<number>, Ref<number>] | null>(
  'innerAndOuterRadii',
  null,
)

const innerRadius = computed<number>(() => {
  if (props.innerRadius >= 0) return props.innerRadius
  if (parentInnerAndOuterRadii !== null) {
    // inner radius is parent wheel's outer radius when parent wheel exists
    return parentInnerAndOuterRadii[1].value
  }
  return 40
})

const outerRadius = computed<number>(() => {
  if (props.outerRadius >= 0) return props.outerRadius
  return innerRadius.value + 60
})

provide('innerAndOuterRadii', [innerRadius, outerRadius])

// Registers

const maxRadius = inject<Ref<number>>('maxRadius')
const registerRadius = inject<(radius: Ref<number>) => void>('registerRadius')
const unregisterRadius = inject<(radius: Ref<number>) => void>('unregisterRadius')
if (!maxRadius || !registerRadius || !unregisterRadius) {
  throw new Error('RadWheel must be under a RadMenu')
}

registerRadius(innerRadius)
registerRadius(outerRadius)
onUnmounted(() => {
  unregisterRadius(innerRadius)
  unregisterRadius(outerRadius)
})

// Handle angles and sizes of items

// sizes of RadItem children
const sizes = ref<Ref<number>[]>([])

// Reactive cumulated sum of sizes
const cumulSizes = computed<number[]>(() => {
  const cumulated: number[] = [0]
  sizes.value.forEach((element) => {
    cumulated.push(cumulated[cumulated.length - 1]! + element.value)
  })
  return cumulated
})

// Reactive sum of all sizes
const totalSize = computed<number>(() => cumulSizes.value[cumulSizes.value.length - 1] || 0)

// When a child registers its size, it gets a ref of its computed begin and end angles
provide('registerSize', (size: Ref<number>): ComputedRef<Interval> => {
  sizes.value.push(size)

  const childId = computed(() => sizes.value.findIndex((elem) => elem === size))
  const cumulSizeBegin = computed(() => cumulSizes.value[childId.value]!)
  const cumulSizeEnd = computed(() => cumulSizes.value[childId.value + 1]!)

  return computed(() =>
    itemBeginAndEndAnglesFromSizes(
      props.beginAngle,
      props.endAngle,
      totalSize.value,
      cumulSizeBegin.value,
      cumulSizeEnd.value,
    ),
  )
})

provide('unregisterSize', (size: Ref<number>) => {
  sizes.value = sizes.value.filter((item) => item !== size)
})

// Draw the donut slice
const donutPath = computed<string>(() => {
  if (!maxRadius) return ''

  return donutSlicePath(
    maxRadius.value,
    maxRadius.value,
    innerRadius.value,
    outerRadius.value,
    props.beginAngle,
    props.endAngle,
    totalSize.value,
  )
})
</script>

<style scoped>
svg {
  pointer-events: none;
  position: absolute;
  transform: 'translate(-50%, -50%)';
}
</style>
