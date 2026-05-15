<template>
  <div class="centerAbs" :style="positionStyle">
    <slot />
  </div>
</template>
<script setup lang="ts">
import { inject, computed, onUnmounted, type ComputedRef } from 'vue'

import type { Point, Interval } from '@/utils/types'
import { polar, pointToStyle } from '../utils/geometry'

interface Props {
  size: number
}

const props = withDefaults(defineProps<Props>(), {
  size: 1,
})

// Registers

const registerSize = inject<(sizeRef: ComputedRef<number>) => ComputedRef<Interval>>('registerSize')
const unregisterSize = inject<(sizeRef: ComputedRef<number>) => void>('unregisterSize')
const innerAndOuterRadii = inject<[ComputedRef<number>, ComputedRef<number>]>('innerAndOuterRadii')
const maxRadius = inject<ComputedRef<number>>('maxRadius')
if (!registerSize || !unregisterSize || !innerAndOuterRadii || !maxRadius) {
  throw new Error('RadItem must be under a RadWheel')
}
const sizeRef = computed(() => props.size)
const beginAndEndAngle = registerSize(sizeRef)

onUnmounted(() => {
  unregisterSize(sizeRef)
})

// Compute position

const [innerRadius, outerRadius] = innerAndOuterRadii
const midAngle = computed(() => {
  const [start, end] = beginAndEndAngle.value
  return (start + end) / 2
})
const midRadius = computed(() => (innerRadius.value + outerRadius.value) / 2)
const center_point = computed<Point>(() =>
  polar(maxRadius.value, maxRadius.value, midRadius.value, midAngle.value),
)

const positionStyle = computed(() => pointToStyle(center_point.value))
</script>
<style scoped>
.centerAbs {
  position: absolute;
  transform: translate(-50%, -50%);
}
</style>
