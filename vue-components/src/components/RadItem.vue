<template>
  <div class="centerAbs" :style="positionStyle">
    <slot />
  </div>
</template>
<script setup>
import { inject, computed, onUnmounted } from 'vue'
import { polar } from '@/utils/geometry.js'
import { pointToStyle } from '../utils/geometry'

// Setup

const props = defineProps({
  size: { type: Number, default: 1 },
})

// Throw an error if not under a RadWheel
inject('parentRadWheel', () => {
  throw new Error('RadItem must be under a RadWheel')
})()

// Registers

const sizeRef = computed(() => props.size)
const beginAndEndAngle = inject('registerSize')(sizeRef)
const [innerRadius, outerRadius] = inject('innerAndOuterRadii')
const menu_cx = inject('maxRadius')
const menu_cy = menu_cx

// Calculates angles, radii and positions

const midAngle = computed(() => (beginAndEndAngle.value[0] + beginAndEndAngle.value[1]) / 2)
const center_point = computed(() =>
  polar(menu_cx.value, menu_cy.value, (innerRadius.value + outerRadius.value) / 2, midAngle.value)
)

const positionStyle = computed(() => pointToStyle([center_point.value.x, center_point.value.y]))

onUnmounted(() => {
  inject('unregisterSize')(sizeRef)
})
</script>

<style scoped>
.centerAbs {
  position: absolute;
  transform: translate(-50%, -50%);
}
</style>
